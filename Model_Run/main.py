from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
#from qdrant_client import QdrantClient
#from langchain.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings  # Optionnel pour les embeddings
from langchain.schema.runnable import RunnablePassthrough 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import LLMChain
#from prompt import chain_type_kwargs
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer



import asyncio 
import logging 
import sys 

from aiogram import Bot, Dispatcher, Router, types 
from aiogram.enums import ParseMode 
from aiogram.filters import CommandStart 
from aiogram.types import Message 
from aiogram.utils.markdown import hbold 

# Bot token can be obtained via https://t.me/BotFather  ,nom = @Camer_bot
TOKEN = "7163174561:AAFOGNdvoaVXQuizTWKMi0Dt8ip3KdkDLBw"
es = Elasticsearch("https://127.0.0.1:9200/",basic_auth=("elastic","elastic"),verify_certs=False)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML) 

# Load https://huggingface.co/sentence-transformers/all-mpnet-base-v2
model = SentenceTransformer("all-MiniLM-L12-v2")


# All handlers should be attached to the Router (or Dispatcher) 
dp = Dispatcher() 
class Chat:
    
    @dp.message(CommandStart()) 
    async def command_start_handler(message: Message) -> None: 
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!") 

    @dp.message() 
    async def echo_handler(message: types.Message) -> None: 

        # Envoyer une action "traitement en cours"
        message_wait= await bot.send_message(chat_id=message.chat.id, text="Traitement en cours...")

        #Variable pour le prompt 
        message_prompt= message.text
        response = chat.ask(message_prompt)

        # effacer traitement en cours
        await bot.delete_message(chat_id=message.chat.id, message_id=message_wait.message_id)


        #afficher dans telegram
        #print(response)
        await message.answer(response) 

   
         


    def __init__(self):
        self.model = Ollama(model="gemma2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)

        self.engine = None  # Initialiser engine à None par défaut (gestion des erreurs)
        self.collection=None
        self.client=None


    def ask(self, query: str):
        
        vec_querry = model.encode(query)
        count_index = es.count(index="corpus")["count"]
        query_search = {"field":"context_vector", "query_vector":vec_querry,"k":3,"num_candidates":count_index}
        
        result = es.knn_search(index="corpus",knn=query_search,source=["context","Titre","Lien"])
        context = ""
        for x in result["hits"]["hits"]:
            
            context = context + x["_source"]["context"]
            context = context + "\n" +"Titre: "+x["_source"]["Titre"]
            context = context + "\n" +"Lien: "+x["_source"]["Lien"] + "\n\n"
                
        
        #print(search_result_concat)
        
        #print(search_result_concat)
        prompts=f""" 
Vous êtes Genora un assistant intelligent de la company Orange Côte d’Ivoire conçu pour répondre à des questions en utilisant uniquement des informations provenant de diverses sources d’Orange Côte d’Ivoire.Votre objectif est de fournir des réponses précises et détaillées mais courte en utilisant les données récupérées.
Ne reponds pas avec tes connaissances. Reponds uniquement avec le context ci-dessous.
Reponds Uniquement en Francais
______________________
        
Question:
{query}

Context/Reponse:
{context}

_____________________

Si le contexts/Reponses ne repond pas du tout à la question, excuse toi et dit que l'informateur n'est pas dans ta base de connaissance.
Si le contexts/Reponses n'a pas assez d'element demande à l'utilisateur d'etre plus explisite.
Si le contexts est coherent pour repondre a la question, reponds en moin de 400 characteres
Si un lien suit le contexte le plus pertinent, veuillez le placer à la fin de la réponse.
S'il ny a pas de titre ou de lien juste après le contexte qui reponds a la question ne met rien a la fin de la réponse.
Considère aussi le titre du document.
_____________________
Exemple de Reponse
_____________________

Il y a exactement 9 directions chez Orange Côte d'Ivoire.

Pour plus d'informations, vous pouvez consulter le lien suivant :[Lien]
_____________________

Propose un lien uniquement s'il le contexte propose un lien
"""
                
                
        #self.chain = ({"context": search_result, "question": query} | chain_type_kwargs | self.model ) 
        # chain = LLMChain(llm=self.model,prompt=chain_type_kwargs)
        
        print(prompts)
        

        return self.model.invoke(prompts)
    def clear(self):
        if self.client:
            del self.client
            self.client = None
            del self.collection
            self.collection = None
            
chat = Chat()

# chat.ingest(corpus=docs, collection_name= "corpus")  # Charger le corpus


async def main() -> None: 
    # Initialize Bot instance with a default parse mode which will be passed to all API calls 
    # And the run events dispatching 
    await dp.start_polling(bot) 
 
 
 

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout) 
    asyncio.run(main())

