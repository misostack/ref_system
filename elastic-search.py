from pprint import pprint
from elasticsearch import Elasticsearch
import json

PRODUCT_INDEX = "products"


def main():
    es = Elasticsearch("http://localhost:9200")
    client_info = es.info()
    if es.ping():
        print("Elasticsearch is up!")
        pprint(client_info.body)
        # remove index
        es.options(ignore_status=[400, 404]).indices.delete(
            index="products")
        # create index
        es.indices.create(
            index="products",
            settings={
                "number_of_shards": 2,  # how many parts your document will be split into
                "number_of_replicas": 1  # how many copies of your data
            }
        )
        # by default, ES have its own mapping, you can customize it
        # https://www.elastic.co/docs/manage-data/data-store/mapping/dynamic-field-mapping
        mapping = {
            "properties": {
                "id": {"type": "long"},
                "name": {"type": "text"},
                "price": {"type": "double"},
                "in_stock": {"type": "boolean"},
                "tags": {"type": "keyword"},
                "date_created": {"type": "date"},
                "meta_data": {"type": "object"},
                "attributes": {"type": "nested"},
            }
        }
        es.indices.put_mapping(index=PRODUCT_INDEX, body=mapping)
        # get all indices
        for index in es.cat.indices(format="json"):
            print(
                f"Index: {index['index']}, Shards: {index['pri']}, Replicas: {index['rep']}")
        # insert document
        products = read_products()
        for document in products:
            response = es.index(index=PRODUCT_INDEX, document=document)
            pprint(response)
        pprint(es.count(index=PRODUCT_INDEX).body)
        # index mapping
        mapping = es.indices.get_mapping(index=PRODUCT_INDEX)
        pprint(mapping)

    else:
        print("Elasticsearch is down!")


def read_products():
    data = json.loads(open("data.json").read())
    return data["products"]


if __name__ == "__main__":
    main()
