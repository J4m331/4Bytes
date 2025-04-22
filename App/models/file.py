from App.database import db
import io
import csv


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    year = db.Column(db.Integer)
    campus = db.Column(db.String(1024))
    fileData = db.Column(db.LargeBinary)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, data, userId):
        self.name = name
        self.fileData = data
        self.userId = userId

    @property
    def first_header(self):
        try:
            stream = io.StringIO(self.fileData.decode('utf-8'))
            reader = csv.reader(stream)
            headers = next(reader, [])
            return headers[0] if headers else None
        except Exception:
            return None
