import requests 
import logging
from http import HTTPStatus

logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    filename='logs.log', 
    level=logging.INFO)

url = "https://api.opensea.io/api/v1/collection/"

def get_price(collection):
    """Fetch Price for specific collection."""
    url_collection = url + collection
    response = requests.get(url_collection)
    if response.status_code == HTTPStatus.OK:
        response_json = response.json()
        floor_price = response_json['collection']['stats']['floor_price']
        logging.info('Price of {} is {}'.format(collection, floor_price))
        return floor_price
    else:
        logging.error('Failed to access OS API with status code {}'.format(response.status_code))


def check_collection(collection):
    """Check if collection exists."""
    url_collection = url + collection
    response = requests.get(url_collection)
    if response.status_code != HTTPStatus.OK:
        logging.info('Collection {}, does not exist.'.format(collection))
        return False
    else:
        logging.info('Collection {}, exists'.format(collection))
        return True
    
