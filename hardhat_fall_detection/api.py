import requests
from datetime import datetime, timedelta
endpoint = "HTTPS ENDPOINT"
api_key = "API KEY" 
headers = {
    "X-API-Key": f"{api_key}",
}


def get_photos( numberofphotos = 10, cutofftime = datetime.now()):
    get = "FileData?cutoffId=" + str(cutofftime) + "&hasAlert=false&ResolvedAlert=false&pageSize=" + str(numberofphotos)
    response = requests.get(endpoint+get, headers=headers)
    response = response.json()
    photos_data = []
    for data in response['data']:
        photos_data.append([data['filename'], data['sasUrl'], data['fileId']]) 
    return photos_data


def set_alert(fileId, alert_label):
    data = {
    "fileId": str(fileId),
    "alert": str(alert_label)
    }   
    response = requests.post(endpoint+"alert", headers=headers, json=data)
