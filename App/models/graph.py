from App.database import db

class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    graphData = db.Column(db.LargeBinary)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fileId = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)

    def __init__(self, name, data, userId):
        self.name = name
        self.fileData = data
        self.userId = userId

