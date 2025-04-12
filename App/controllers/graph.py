from App.models import Graph
from App.database import db

def createGraph(name, data, userId):
    newfile = Graph(name, data, userId)
    db.session.add(newfile)
    db.session.commit()
    return newfile

def getGraph(graphId):
    file = Graph.query.get(graphId)
    return file

def getAllGraphs():
    return Graph.query.all()

def deleteGraph(graphId):
    graph = Graph.query.get(graphId)
    db.session.delete(graph)
    db.session.commit()
    return graph