import requests
endpoint = "ENDPOINT"
api_key = "API KEY" 
headers = {
    "X-API-Key": f"{api_key}",
}

def get_counters():
    response = requests.get(endpoint+"Counter", headers=headers)
    print (response.json())

def send_to_api(new_people_count):
    ulrpostdata = endpoint+"Counter?counterId=unique_counter&count=" + str(new_people_count)
    response = requests.post(ulrpostdata, headers=headers)
    print(response)
    print(f'Liczba osób na budowie się zmieniła! Nowa liczba: {new_people_count}')
