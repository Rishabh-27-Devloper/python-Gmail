import os
from flask import Flask, redirect,render_template,request,jsonify, url_for
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import quote
import base64,json
import warnings
from email.mime.text import MIMEText

# Suppress the warning about the scope change
warnings.filterwarnings("ignore", category=UserWarning, module="google.auth._cloud_sdk")
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']
token = os.path.join(os.path.abspath("."),'static','token.json')
credn = os.path.join(os.path.abspath("."),'static','credentials.json')
session = {}
Mon = ['-- Select --',
    'Jan', 'Feb', 'Mar', 'Apr',
    'May', 'Jun', 'Jul', 'Aug',
    'Sep', 'Oct', 'Nov', 'Dec'
]

app = Flask(__name__)

def get_credentials():
    global credn
    creds = None
    token = os.path.join(os.path.abspath("."),'static','token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not checklogin():
        flow = InstalledAppFlow.from_client_secrets_file(
            credn, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token, 'w') as token:
            token.write(creds.to_json())
    else:
        creds = Credentials.from_authorized_user_file(token, SCOPES)
    return creds

@app.route('/login')
def get_login_url():
    if not checklogin():
        get_credentials()
    return redirect(url_for('inbox', _external=True))

def serve():
    global token, credn
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    return service
def load_messages(service,messages):
    email_list = []
    try:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_list.append(msg)
        return email_list
    except HttpError:
        return []
def get_all_messages():
    service = serve()
    try:
        messages = []
        nextPageToken = None
        while True:
            inbox = service.users().messages().list(userId='me', labelIds=['INBOX'], pageToken=nextPageToken).execute()
            messages.extend(inbox.get('messages', []))
            nextPageToken = inbox.get('nextPageToken')
            if not nextPageToken:
                break
        return messages
    except HttpError as error:
        return f'An error occurred: {error}'

def get_inbox():
    service = serve()
    try:
        #Labels = service.users().labels().list(userId='me').execute()
        #labels = Lables.get('labels', [])
        #inbox = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        #messages = inbox.get('messages', [])
        messages = get_all_messages()
        print(len(messages))
        return [service,messages]
    except HttpError as error:
        return[f'An error occurred: {error}']
    
def checklogin():
    tkn = os.path.join(os.path.abspath("."),'static','token.json')
    if os.path.exists(tkn):
        creds = Credentials.from_authorized_user_file(tkn, SCOPES)
        if not creds or not creds.valid:
            print("Token File not valid")
            return False
        else:
            return True
    else:
        print("No token File")
        return False
@app.route("/inbox")
def inbox():
    if checklogin() == True:
        global session
        session = {}
        tot = len(get_all_messages())
        return render_template('inbox.html',months=Mon,total=tot)#,le = len(mails),mail = mls)
    else:
        return redirect('/')
def search(keywords,string):
    for keyword in keywords:
        if keyword.lower() in string.lower():
            return True
    return False
@app.route('/fetch')
def fetch():
    try:
        ids = session['ids']
        if ids == []:
            return {'mail':[]}
    except KeyError:
        ids = []
    if checklogin():
        key = {'EDUCATIONAL': ['education','result','results','marks','roll', 'learn', 'educate', 'degree', 'college', 'colleges', 'University', 'institute', 'learning', 'teaching', 'school', 'course', 'study', 'academic', 'knowledge', 'student', 'curriculum'], 'SOCIAL': ['social', 'network', 'friend', 'community', 'connection', 'sharing', 'group', 'event', 'notifications', 'shared', 'messagesconversation', 'interaction'], 'E-COMMERCE': ['e-commerce','ecommerce','cart', 'shopping', 'online', 'purchase', 'product', 'store', 'sale', 'discount', 'shopping cart', 'checkout'], 'PAYMENTS': ['payment','order','orders' ,'invoice', 'transaction', 'billing', 'pay', 'purchase', 'money', 'transfer', 'receipt', 'financial'], 'VERIFICATION CODE': ['verification code', 'code', 'verify', 'authentication', 'security', 'access', 'confirmation', 'PIN', 'token', 'validation'], 'COMMUNITY': ['community', 'group', 'organization', 'society', 'association', 'club', 'network', 'member', 'event', 'support']}
        if ids == []:
            service,ids = get_inbox()
        else:
            service = serve()
        mails = load_messages(service,ids[:10])
        session['ids'] = ids[10:]
        mls = []
        for i in mails:
            temp = {
                "ID":i["id"]
            }
            for j in i['payload']['headers']:
                if j['name'] == "Date":
                    temp['Date'] = j['value']
                elif j['name'] == "From":
                    temp['From'] = j['value']
                elif j['name'] == "To":
                    temp['To'] = j['value']
                elif j['name'] == "Subject":
                    temp['Message'] = j['value']
            try:
                subject = temp['Message']
            except KeyError:
                subject = ''
            if search(key['EDUCATIONAL'],subject):
                temp['Category']=['EDUCATIONAL']
            elif search(key['SOCIAL'],subject):
                temp['Category']=['SOCIAL']
            elif search(key['E-COMMERCE'],subject):
                temp['Category']=['E-COMMERCE']
            elif search(key['PAYMENTS'],subject):
                temp['Category']=['PAYMENTS']
            elif search(key['VERIFICATION CODE'],subject):
                temp['Category']=['VERIFICATION']
            elif search(key['COMMUNITY'],subject):
                temp['Category']=['COMMUNITY']
            else:
                temp['Category']=['PRIMARY']
                pass
            mls.append(temp)
        
        return {'mail':mls}
def create_message(sender, to, subject, message_text):
    message = {
        'raw': base64.urlsafe_b64encode(message_text.as_bytes()).decode(),
        'payload': {
            'headers': [
                {'name': 'From', 'value': sender},
                {'name': 'To', 'value': to},
                {'name': 'Subject', 'value': subject}
            ]
        }
    }
    return message

def send_message(service, user_id, message,to):
    try:
        service.users().messages().send(userId=user_id, body=message).execute()
        return True
    except Exception as e:
        print(e)
        return e
def get_user_email(service):
    profile = service.users().getProfile(userId='me').execute()
    email = profile['emailAddress']
    return email
@app.route('/send_email', methods=['POST'])
def send_email():
    service = serve()
    me = get_user_email(service)
    to = request.form['to']
    subject = request.form['subject']
    message = MIMEText(request.form['message'])
    message['to'] = to
    message['subject'] = subject
    email_message = create_message(me,to, subject, message)
    print(email_message)
    Status = send_message(service, 'me', email_message,to)
    if Status == True:
        return redirect('/inbox')
    else:
        return Status
@app.route('/compose')
def compose():
    return render_template('compose.html')
@app.route('/logout')
def logout():
    if checklogin() == True:
        os.remove(token)
    return str(0)

@app.route('/delete_email/<string:email_id>', methods=['GET','POST'])
def delete_email(email_id):
    email_id = json.loads(str(email_id))
    service = serve()
    try:
        for email in email_id:
            service.users().messages().delete(userId='me', id=email).execute()
        return jsonify({"success": True, "message": f"{len(email_id)} Email(s) deleted successfully."})
    except HttpError as error:
        return jsonify({"success": False, "message": f"An error occurred: {error}"})
@app.route("/")
def login():
    if checklogin() == False:
        print("Not Login")
        return render_template('index.html')
    else:
        return redirect('/inbox')

if __name__ == '__main__':
    app.run(debug=True)