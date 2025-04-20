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
    reader = csv.reader(csv_file_like)
    for row in reader:
        data = Data(file_id=file_id, gradute=row[0], fauculty=row[1], programme=row[2], age=row[3])
        db.session.add(data)
        db.session.commit()
        print(f"Data created: {data}")

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