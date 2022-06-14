import logging
from datetime import datetime

from elasticsearch import Elasticsearch

from sem_search import search_similar_movies


def get_vecs(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    word_vec = {}
    for i in data:
        i = i.strip().split(' ')
        word = i[0]
        vecs = i[1:]
        vecs = [float(i) for i in vecs]
        word_vec[word] = vecs
    return word_vec


def connect_elastic():
    client = Elasticsearch("http://localhost:9200")
    if client.ping():
        print("yay.. connected ")

    else:
        print("Cannot connect.")
    return client


def make_index(es_client, index_name, mappings):
    es_client.indices.create(index=index_name, ignore=400, body=mappings)
    return es_client


def put_record(es_client, index_name, doc, id):
    resp = es_client.index(index=index_name, id=id, document=doc)
    return resp


if __name__ == '__main__':
    # connect_elasticsearch()
    word_vec = get_vecs('example.txt')

    # doc = {
    #     'author': 'Ajay',
    #     'text': 'Interensting content ajay ...',
    #     'timestamp': datetime.now(),
    # }

    # resp = create_an_index(es_client=es_client,index_name="company",doc=doc,id=2)
    # print(resp)
    # resp = es_client.get(index="words", id='the')
    # print(resp)

    # print("*"*100)
    # resp = es_client.search(index="words", query={"match_all": {}})
    # print(resp)
    # logging.basicConfig(level=logging.ERROR)

    mappings = {
        "mappings": {
            "properties": {
                "vector": {
                    "type": "dense_vector",
                    "dims": 50
                },
                "my_text": {
                    "type": "text"
                }
            }
        }
    }
    es_client = connect_elastic()
    # es= make_index(es_client,'words',mappings)

    # ##### created word embeddings in elastic search

    # # word_vec= get_vecs('example.txt')
    # # print(word_vec['in'])
    # for word in word_vec:
    #     doc={
    #         "word": word,
    #         "vector":word_vec[word]
    #     }
    #     resp = put_record(es_client=es,index_name="words",doc=doc,id=word)
    #     print(resp)
    #     print('\n*'*10)

    ## cosine similiarity

    search_query = {
        "size": 3,

        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.queryVector, 'vector') + 1.0",
                    "params": {
                        # "queryVector": vector.tolist()
                        "queryVector": word_vec['.']
                    }
                }
            }
        }
    }

    responses = es_client.search(index='words', body=search_query)
    for resp in responses['hits']['hits']:
        print(
            "Word: {} - Score: {} ".format(resp['_source']['word'], resp['_score']))
        # print(resp)
