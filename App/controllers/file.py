from App.models import File
from App.database import db

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

def deleteFile(fileId):
    file = File.query.get(fileId)
    db.session.delete(file)
    db.session.commit()
    return file