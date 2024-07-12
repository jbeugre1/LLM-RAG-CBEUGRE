from elasticsearch import Elasticsearch
import json
import pandas as pd
import os
import shutil
from sentence_transformers import SentenceTransformer
from index import mymapping

es = Elasticsearch("https://127.0.0.1:9200/",basic_auth=("elastic","hgE3g61Bz3LTNaBg2=k="),verify_certs=False)

listdir = os.listdir("./Corpus")
print(listdir)


try:
    es.indices.create(index="corpus",mappings=mymapping)
except Exception:
    print("Index already exist")



for x in listdir:
    path_json = "./Corpus/"+x
    insert_path = "./Corpus/Traité/"+x
    if os.path.isfile(path_json) and ".gitkeep" not in path_json :
        print(path_json)
    

        with open(path_json, 'r') as file:
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
            es.index(index="corpus",document=x)
            
            
        shutil.move(path_json, insert_path)





