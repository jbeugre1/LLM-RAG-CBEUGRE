from elasticsearch import Elasticsearch
import json
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from index import mymapping

es = Elasticsearch("https://127.0.0.1:9200/",basic_auth=("elastic","elastic"),verify_certs=False)

listdir = os.listdir("./Corpus")
print(listdir)



try:
    es.indices.create(index="corpus",mappings=mymapping)
except Exception:
    print("Index already exist")



for x in listdir:
    path = "./Corpus/"+x
    if os.path.isfile(path):
        print(path)
    

        with open(listdir, 'r') as file:
            data = json.load(file)
            df = pd.DataFrame(data)
            
        metadata_df = pd.json_normalize(df['metadata'])
        newdf = pd.concat([df.drop(['metadata'], axis=1),metadata_df],axis=1)
        newdf.fillna("",inplace=True)
        model = SentenceTransformer("all-MiniLM-L12-v2")
        newdf["Title_Context"] = newdf["Titre"] + " ; " + newdf["context"]
        newdf["context_vector"] = newdf["Title_Context"].apply(lambda x: model.encode(x))
        
        
        record_list = newdf.to_dict("records")


        for x in record_list:
            es.index(index="corpus_v2test",document=x)





