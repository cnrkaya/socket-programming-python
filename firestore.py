#requirements
#pip install firebase-admin
#pip install google-cloud-firestore

from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
import os,sys

working_directory = os.path.dirname(sys.argv[0])
os.chdir(working_directory)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=working_directory+"\green-house_admin.json"

# initialize sdk
cred = credentials.Certificate("green-house_admin.json")
firebase_admin.initialize_app(cred)

# initialize firestore instance
db = firestore.Client()


data = {
    u'name': u'Sera1',
    u'target_temp': u'15',
    u'current_temp': u'15'
}
#set data
#db.collection(u'GreenHouses').document(u'sera3').set(data)

#read data
sera_id = 1
sera_dict = db.collection(u'GreenHouses').document(u'sera{}'.format(sera_id)).get().to_dict()
if sera_dict['current_temp'] != sera_dict['target_temp']:
    print("turn on the heater")

# read all datas
snapshots = list(db.collection(u'GreenHouses').get())
for snapshot in snapshots:
    print(snapshot.to_dict())
    if snapshot.to_dict()['name'] == "Sera1":
        print("Sera1")
