import io
import csv
from App.models import Data,File
import pandas as pd
from App.database import db

def getData(file_id):
    data = Data.query.filter_by(file_id=file_id).all()
    return data

def createData(file_id):
    file = File.query.filter_by(id=file_id).first()
    csv_file_like = io.StringIO(file.fileData.decode('utf-8'))
    df = pd.read_csv(csv_file_like)
    
    for _, row in df.iterrows():
        data_dict = row.to_dict()
        data = Data(file_id=file_id, data_dict=data_dict)
        db.session.add(data)

    db.session.commit()
    
    return list(df.columns)

def getHeaders(file_id):
    file = File.query.filter_by(id=file_id).first()
    csv_file_like = io.StringIO(file.fileData.decode('utf-8'))
    headers = pd.read_csv(csv_file_like, nrows=0).columns.tolist()
    return headers

def getDF(file_id):
    data = getData(file_id)
    data_dicts = [d.get_data() for d in data]
    return pd.DataFrame(data_dicts)

def createGraphData(file_id, field):
    df = getDF(file_id)
    chart_data = [
        {
            'id': str(field),
            'label': str(field),
            'value': int(count),
            'color': f'hsl({abs(hash(str(field))) % 360}, 70%, 50%)'
        }
        for field, count in df[field].value_counts().items()
    ]
    return chart_data