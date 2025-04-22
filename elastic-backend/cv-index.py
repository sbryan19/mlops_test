import pandas as pd
from elasticsearch import Elasticsearch, helpers

def generate_data(dataframe: pd.DataFrame, index_name: str):

    for i, row in dataframe.iterrows():
        yield {
            "_index": index_name,
            "_id": i,
            "_source": row.to_dict()
        }

if __name__ == "__main__":

    INDEX_NAME = "cv-transcriptions"
    DATASOURCE = "../asr/cv-valid-dev.csv"

    print("Loading dataset...")

    # Load dataset and keep only searchable columns
    cv_dev_df = pd.read_csv(DATASOURCE)
    cv_dev_df = cv_dev_df[['generated_text', 'duration', 'age', 'gender', 'accent']]

    cv_dev_df = cv_dev_df.fillna("NA")

    print("Initializing ElasticSearch client")

    # Initialize ElasticSearch client
    es_client = Elasticsearch("http://3.25.54.197:9200")
    
    # Delete old index if it exists
    if es_client.indices.exists(index=INDEX_NAME):
        print(f"Deleting existing index with name: {INDEX_NAME}")
        es_client.indices.delete(index=INDEX_NAME)

    # Create new index
    es_client.indices.create(index=INDEX_NAME)

    # Bulk upload data to index
    print("Uploading data to index")
    success, _ = helpers.bulk(es_client, generate_data(cv_dev_df, INDEX_NAME))

    print(f"Successfully uploaded {success} documents to index {INDEX_NAME}")
    
    