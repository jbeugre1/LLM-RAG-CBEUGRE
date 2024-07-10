from elasticsearch import Elasticsearch
import json
import pandas as pd
import os
import shutil
from sentence_transformers import SentenceTransformer
from index import mymapping

es = Elasticsearch("https://127.0.0.1:9200/",basic_auth=("elastic","elastic"),verify_certs=False)

# Query to delete all documents
query = {
    "query": {
        "match_all": {}
    }
}

# Perform the deletion
response = es.delete_by_query(index="corpus", body=query)