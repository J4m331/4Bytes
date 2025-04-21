from App.models import File
from App.database import db
import csv
from io import StringIO

def createFile(name, data, userId):
    newfile = File(name, data, userId)
    db.session.add(newfile)
    db.session.commit()
    return newfile

def getFile(fileId):
    file = File.query.get(fileId)
    return file

def getAllFiles():
    return File.query.all()

def getFilebyName(name):
    file = File.query.filter_by(name=name).first()
    return file

def getFirstHeader(fileId):
    file = getFile(fileId)
    data = file.fileData.decode('utf-8')

    csv_reader = csv.reader(StringIO(data))
    headers = next(csv_reader, [])
    return headers[0]

def deleteFile(fileId):
    file = File.query.get(fileId)
    db.session.delete(file)
    db.session.commit()
    return file