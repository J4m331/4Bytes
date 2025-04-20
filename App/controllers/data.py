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
    print(f"Data created for file_id: {file_id}, rows: {len(df)}")
    
    return list(df.columns)

def getHeaders(file_id):
    file = File.query.filter_by(id=file_id).first()
    csv_file_like = io.StringIO(file.fileData.decode('utf-8'))
    headers = pd.read_csv(csv_file_like, nrows=0).columns.tolist()
    print(headers)
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

def dataByProgramme(file_id):
    data = getData(file_id)
    data_dicts = []
    for d in data:
        data_dicts.append({
            'programme': d.programme,
            'age': d.age,
            'gradute': d.gradute,
            'fauculty': d.fauculty
        })
        df = pd.DataFrame(data_dicts)
        chart_data = [
            {
                'id': str(programme),
                'label': str(programme),
                'value': int(count),
                'color': f'hsl({abs(hash(str(programme))) % 360}, 70%, 50%)'
            }
            for programme, count in df['programme'].value_counts().items()
        ]
    return chart_data
def dataByAge(file_id):
    data = getData(file_id)
    data_dicts = []
    for d in data:
        data_dicts.append({
            'programme': d.programme,
            'age': d.age,
            'gradute': d.gradute,
            'fauculty': d.fauculty
        })
        df = pd.DataFrame(data_dicts)
        chart_data = [
            {
                'id': str(age),
                'label': str(age),
                'value': int(count),
                'color': f'hsl({abs(hash(str(age))) % 360}, 70%, 50%)'
            }
            for age, count in df['age'].value_counts().items()
        ]
    return chart_data
def dataByFaculty(file_id):
    data = getData(file_id)
    data_dicts = []
    for d in data:
        data_dicts.append({
            'programme': d.programme,
            'age': d.age,
            'gradute': d.gradute,
            'fauculty': d.fauculty
        })
        df = pd.DataFrame(data_dicts)
        chart_data = [
            {
                'id': str(fauculty),
                'label': str(fauculty),
                'value': int(count),
                'color': f'hsl({abs(hash(str(fauculty))) % 360}, 70%, 50%)'
            }
            for fauculty, count in df['fauculty'].value_counts().items()
        ]
    return chart_data
def dataByGraduate(file_id):
    data = getData(file_id)
    data_dicts = []
    for d in data:
        data_dicts.append({
            'programme': d.programme,
            'age': d.age,
            'gradute': d.gradute,
            'fauculty': d.fauculty
        })
        df = pd.DataFrame(data_dicts)
        chart_data = [
            {
                'id': str(gradute),
                'label': str(gradute),
                'value': int(count),
                'color': f'hsl({abs(hash(str(gradute))) % 360}, 70%, 50%)'
            }
            for gradute, count in df['gradute'].value_counts().items()
        ]
    return chart_data