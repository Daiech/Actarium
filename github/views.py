from django.http import HttpResponse
from django.conf import settings

import commands
import os


# hace git pull y copia los archivos estaticos a public_html
def update(solicitud):
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    gitpull = commands.getstatusoutput('git pull origin master')[1]

    return HttpResponse("<pre>"+gitpull+"</pre>")

def runMongo(solicitud):
    
    os.chdir('/home2/anuncio3/bin/mongodb-linux-x86_64-2.4.1/bin')
    mongoresponse = commands.getstatusoutput("./mongod --fork --dbpath 'data/db' --smallfiles --logpath 'data/mongodb.log' --logappend")[1]
    return HttpResponse("<pre>"+mongoresponse+"</pre>")