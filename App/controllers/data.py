from App.models import Data
from App.database import db

def getData():
    data = Data.query.all()
    return data