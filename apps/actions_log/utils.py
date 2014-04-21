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
    
    uri = "localhost:27017/actarium"
    try:
        connection = MongoClient('mongodb://admin:123456@localhost/admin')
        print "----conected to localhost"
    except:
        error = "Error connecting to MongoDB"
        print error
        saveErrorLog(mongodb_error)
    
    actarium_db = connection.actarium

    return actarium_db