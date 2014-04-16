from django.conf import settings
import datetime

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
	try:
		connection = MongoClient('localhost', MONGODB['PORT'])
	except:
		mongodb_error =  'problem connecting to mongo client on port: %s'%(MONGODB['PORT'])
		saveErrorLog(mongodb_error)
		print mongodb_error
		return False

	try:
		response = connection.actarium(MONGODB['USER'], MONGODB['PASSWORD'])
	except:
		mongodb_error =  'Error authenticating mongodb user %s, %s '%(MONGODB['USER'], MONGODB['PASSWORD'])
		saveErrorLog(mongodb_error)
		print mongodb_error
		return False

	actarium_db = connection.actarium

	return actarium_db