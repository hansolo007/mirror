import sys
sys.path.insert(1, '/Library/Python/2.7/site-packages')
from datetime import datetime
import os
import base64
from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import client
from oauth2client import tools
import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    service = build('gmail', 'v1', http=credentials.authorize(Http()))

    results = service.users().labels().get(userId='me', id='Label_11').execute()
    #print results
    mails = service.users().messages().list(userId='me', labelIds='Label_11', q=None, pageToken=None, maxResults=None, includeSpamTrash=None).execute()    
    messages = mails.get('messages', [])
    if not messages:
	print 'no messages found.'
    else:
	threadSet =set()
	smsSet = list()
	for m in messages:
		#print m
		if m['threadId'] not in threadSet :
			threadSet.add(m['threadId'])
			threads = service.users().threads().get(userId='me', id=m['threadId'], format=None, metadataHeaders=None).execute()
			threadMessages = threads['messages']
			for mm in threadMessages:
				payload = mm['payload']
				text =None
				if 'data'in payload['body']:
					text = base64.b64decode( payload['body']['data'])
					sms ={}
					for header in  payload['headers']:
						if header['name'] == 'From':
							sms['id'] = m['threadId']
							sms['text'] = header['value'][1:header['value'].index(' ')] + ' says : ' + text
						if header['name'] == 'Date':
							sms['date'] = header['value']
						if 'date' in sms and 'id' in sms:
							smsSet.append(sms)
							break
											
							#print (header['value'][0:header['value'].index(' ')] + ' says : ' + text)
	smsSet= sorted(smsSet, key = threadMsgSort )
	for sms in smsSet:
		print sms['text']
								
	
def threadMsgSort(threadMsg):
	date = threadMsg['date']
	date = date[ date.index(', ') + 2 : date.index('+')-1]
	time = datetime.strptime(date, '%d %b %Y %H:%M:%S')
	return time					   

if __name__ == '__main__':
    main()
