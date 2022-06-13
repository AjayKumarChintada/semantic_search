from datetime import datetime
from elasticsearch import Elasticsearch
from sem_search import search_similar_movies
import logging
# def connect_elasticsearch():
#     _es = None
#     _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#     if _es.ping():
#         print('Yay Connect')
#     else:
#         print('Awww it could not connect!')
#     return _es


def connect_elastic():
    client = Elasticsearch("http://localhost:9200")
    if client.ping():
        print("yay.. connected ")

    else:
        print("Cannot connect.")
    return client


def create_an_index(es_client, index_name,doc,id):
    
    resp = es_client.index(index=index_name, id=id, document=doc)
    return resp 

    


if __name__ == '__main__':
    # connect_elasticsearch()
    es_client= connect_elastic()
    doc = {
        'author': 'Ajay',
        'text': 'Interensting content...',
        'timestamp': datetime.now(),
    }

    resp = create_an_index(es_client=es_client,index_name="company",doc=doc,id=1)
    print(resp)
    # logging.basicConfig(level=logging.ERROR)
