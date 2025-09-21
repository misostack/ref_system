from pprint import pprint
from elasticsearch import Elasticsearch


def main():
    es = Elasticsearch("http://localhost:9200")
    client_info = es.info()
    if es.ping():
        print("Elasticsearch is up!")
        pprint(client_info.body)
        # remove index
        es.options(ignore_status=[400, 404]).indices.delete(
            index="product_index")
        # create index
        es.indices.create(
            index="product_index",
            settings={
                "number_of_shards": 2,  # how many parts your document will be split into
                "number_of_replicas": 1  # how many copies of your data
            }
        )
        # get all indices
        for index in es.cat.indices(format="json"):
            print(
                f"Index: {index['index']}, Shards: {index['pri']}, Replicas: {index['rep']}")
        # insert document
        document = {
            "name": "Apple iPhone 14 Pro Max",
            "price": 1099,
            "in_stock": True,
            "created_at": "2023-09-01T10:00:00"
        }
        response = es.index(index="product_index", document=document)
        pprint(response)

    else:
        print("Elasticsearch is down!")


if __name__ == "__main__":
    main()
