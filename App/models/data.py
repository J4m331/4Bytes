from App.database import db

class dataField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Enrollment = db.Column(db.String(1024))
    student_demographics = db.Column(db.String(1024))
    gradute = db.Column(db.String(1024))
    timeSeriesEnrollment = db.Column(db.String(1024))
    year = db.Column(db.Integer)
    
    def __init__(self, Enrollment, student_demographics, gradute, timeSeriesEnrollment):
        self.Enrollment = Enrollment
        self.student_demographics = student_demographics
        self.gradute = gradute
        self.timeSeriesEnrollment = timeSeriesEnrollment
    def __repr__(self):
        return f"dataField('{self.Enrollment}', '{self.student_demographics}', '{self.gradute}', '{self.timeSeriesEnrollment}')"
    def __str__(self):
        return f"dataField('{self.Enrollment}', '{self.student_demographics}', '{self.gradute}', '{self.timeSeriesEnrollment}')"