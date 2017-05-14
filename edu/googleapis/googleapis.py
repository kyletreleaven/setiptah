
from collections import namedtuple

def enumify(enum_name, values):
	_Class = namedtuple(enum_name, values)
	id_map = { i : i for i in values }
	return _Class(**id_map)

from oauth2client.client import GoogleCredentials	
# the ones you set up with gcloud

# build a client for some api
from googleapiclient import discovery

if __name__ == '__main__':

	API = 'deploymentmanager'
	VERSION = 'v2'

	credentials = GoogleCredentials.get_application_default()
	client = discovery.build(API, VERSION, credentials)

	PROJECT = 'plasma-myth-140513'

	#request = client.method(project=PROJECT)
	request.execute()
