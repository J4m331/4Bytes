from App.database import db
import json

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    data_json = db.Column(db.Text, nullable=False)
    
    def __init__(self, file_id, data_dict):
        self.file_id = file_id
        self.data_json = json.dumps(data_dict)
    
    def get_data(self):
        return json.loads(self.data_json)
    
    def __repr__(self):
        return f"Data(id={self.id}, file_id={self.file_id})"
    
    def __str__(self):
        return f"Data(id={self.id}, file_id={self.file_id})"