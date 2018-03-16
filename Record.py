import requests
import json
import base64
from dotenv import load_dotenv, find_dotenv
load_dotenv( find_dotenv() )
import os

API_KEY = os.getenv('API_KEY')
USER_KEY = os.getenv('USER_KEY')
BASIC_TOKEN = base64.b64encode(b'{}:{}'.format(API_KEY, USER_KEY))
HEADERS = {'Authorization': 'Basic {}'.format(BASIC_TOKEN), 'Content-type': 'application/json'}
ROOT = 'https://sandbox-api-ca.metrc.com'

PARAMETERS_DICT = {
    'retail': ''
    , 'lab': ''
    , 'packaging': {'licenseNumber': os.getenv('PACKAGING_LICENSE_NUMBER') }
}

URL_DICT = {
    'rooms-create': '/rooms/v1/create'
    , 'rooms-update': '/rooms/v1/update'
    , 'rooms-read': '/rooms/v1/active'
    , 'strains-create': '/strains/v1/create'
    , 'strains-update': '/strains/v1/update'
    , 'strains-read': '/strains/v1/active'
    , 'plantbatches-create': '/plantbatches/v1/createplantings'
    , 'plantbatches-changegrowth': '/plantbatches/v1/changegrowthphase'
    , 'plantbatches-delete': '/plantbatches/v1/destroy'
    , 'plantbatches-read': '/plantbatches/v1/active'
    , 'plants-read': '/plants/v1/flowering'
    , 'plants-move': '/plants/v1/moveplants'
    , 'plants-destroy': '/plants/v1/destroyplants'
    , 'plants-manicure': '/plants/v1/manicureplants'
    , 'plants-harvest': '/plants/v1/harvestplants'
    , 'harvests-read': '/harvests/v1/active'
    , 'harvests-createpackages': '/harvests/v1/createpackages'
    , 'harvests-removewaste': '/harvests/v1/removewaste'
    , 'harvests-finish': '/harvests/v1/finish'
    , 'harvests-unfinish': '/harvests/v1/unfinish'
    , 'packages-read': '/packages/v1/active'
    , 'items-create': '/items/v1/create'
    , 'items-read': '/items/v1/active'
    , 'items-update': '/items/v1/update'
    , 'items-categories': '/items/v1/categories'
    , 'packages-types': '/packages/v1/types'
    , 'packages-read': '/packages/v1/active'
    , 'packages-create': '/packages/v1/create'
    , 'packages-changeitem': '/packages/v1/change/item'
}

class Sender():
    def __init__(self, license_number):
        # data we send
        self.data = []

        # data we get back with the id
        self.filtered_data = []
        self.headers = HEADERS
        self.license_number = PARAMETERS_DICT.get(license_number)

    def PopulateData(self, list_map_fields, limit):
        if limit is None:
            self.data += list_map_fields
        else:
            self.data += list_map_fields[0:limit]

    def UpdateData(self, list_map_fields):
        for map_fields, filtered_record in zip(list_map_fields, self.data):
            for key,value in map_fields.items():
                filtered_record[key] = value
        print self.data

    def UpdateFilteredData(self, list_map_fields):
        for map_fields, filtered_record in zip(list_map_fields, self.filtered_data):
            for key,value in map_fields.items():
                filtered_record[key] = value
        print self.filtered_data

    def GetFromApi(self, endpoint):
        response = requests.get(ROOT + URL_DICT.get(endpoint), headers=self.headers, params=self.license_number)
        if response.status_code != 200:
            error_message = 'Error with endpoint {}. Status code {}. Error message: {}'.format(URL_DICT.get(endpoint), response.status_code, response.content)
            raise Exception(error_message)
        else:
            # self.data = json.loads(response.text)
            return json.loads(response.text)

    def FilterReceivedData(self, endpoint, limit, search_list, needed_fields):
        received_data = self.GetFromApi(endpoint)
        for record in received_data:
            filtered_record = {}
            for search_map in search_list:
                for key,value in search_map.items():
                    if record[key] == value:
                        for field in needed_fields:
                            filtered_record[field] = record[field]
                        self.filtered_data.append(filtered_record)
                        print self.filtered_data
        # print '200 in call to {}. Data you will need to give to Metrc: {}'.format(self.endpoint, self.filtered_data)
        # print self.filtered_data


    def SendToApi(self, endpoint, data, needed_fields):
        # self.PopulateData(list_map_fields)
        response = requests.post(ROOT + URL_DICT.get(endpoint), data=json.dumps(data), headers=self.headers, params=self.license_number )
        if response.status_code != 200:
            error_message = 'Error with endpoint {}. Status code {}. Error message: {}'.format(URL_DICT.get(endpoint), response.status_code, response.content)
            raise Exception(error_message)
        else:
            save_list = []
            for elem in data:
                record = {}
                for field in needed_fields:
                    record[field] = elem[field]
                save_list.append(record)
            print '{} in call to {}. Data you will need to give to Metrc: {}'.format(response.status_code, URL_DICT.get(endpoint), save_list)
            return save_list
