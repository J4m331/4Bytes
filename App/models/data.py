from App.database import db

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    gradute = db.Column(db.String(1024))
    fauculty = db.Column(db.String(1024))
    programme = db.Column(db.String(1024))
    age = db.Column(db.Integer)
    
    def __init__(self, file_id, gradute, fauculty, programme, age):
        self.file_id = file_id
        self.gradute = gradute
        self.fauculty = fauculty
        self.programme = programme
        self.age = age

    def __repr__(self):
        return f"data('{self.id}','{self.file_id}', '{self.gradute}', '{self.fauculty}', '{self.programme}', '{self.age}')"
    def __str__(self):
        return f"data('{self.id}','{self.file_id}', '{self.gradute}', '{self.fauculty}', '{self.programme}', '{self.age}')"