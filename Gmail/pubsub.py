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
from oauth2client.client import SignedJwtAssertionCredentials
import json
import httplib2
from apiclient import discovery

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

PUBSUB_SCOPES = 'https://www.googleapis.com/auth/pubsub'
email ='122534795334-ce500nnmr1jt7o8tt9scssuoecok6bd6@developer.gserviceaccount.com'


def create_pubsub_client():
	client_email = '123456789000-abc123def456@developer.gserviceaccount.com'
	with open("MyProject.p12") as f:
  		private_key = f.read()

	credentials = SignedJwtAssertionCredentials(email, private_key, PUBSUB_SCOPES)

    	if credentials.create_scoped_required():
        	credentials = credentials.create_scoped(PUBSUB_SCOPES)
        http = httplib2.Http()
    	credentials.authorize(http)
	return discovery.build('pubsub', 'v1beta2', http=http)

def main():
	client = create_pubsub_client()
	topic = client.projects().topics().create(name='projects/api-project-122534795334/topics/mirrortopic', body={}).execute()
	print 'Created: %s' % topic.get('name')


if __name__ == '__main__':
    main()
