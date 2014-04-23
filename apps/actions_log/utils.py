from django.conf import settings
import datetime
from pymongo import MongoClient

def saveErrorLog(errordata):
    try:
        logfile = open("error.log", "a")
        try:
            logfile.write('%s %s \n' % (datetime.datetime.now(), errordata))
        finally:
            logfile.close()
    except IOError:
        pass

def connect_to_actarium_db():
    MONGODB = settings.MONGODB
    
    uri = "mongodb://%s:%s@localhost/actarium"%(MONGODB['USER'],MONGODB['PASSWORD'])
    try:
        connection = MongoClient(uri,port=MONGODB['PORT'])
        print "----conected to localhost, user %s "%(MONGODB['USER'])
        actarium_db = connection.actarium
        return actarium_db
    except:
        error = "Error connecting to MongoDB: ",uri, " port: ", MONGODB['PORT']
        print error
        saveErrorLog(error)
        return False
    

    