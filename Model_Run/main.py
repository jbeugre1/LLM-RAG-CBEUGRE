from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from qdrant_client import QdrantClient
#from langchain.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings  # Optionnel pour les embeddings
from langchain.schema.runnable import RunnablePassthrough 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import LLMChain
from prompt import chain_type_kwargs
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
        self.model = Ollama(model="llama3")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)

        self.engine = None  # Initialiser engine à None par défaut (gestion des erreurs)
        self.collection=None
        self.client=None


    def ask(self, query: str):
        
        vec_querry = model.encode(query)
        count_index = es.count(index="corpus_v2test")["count"]
        query_search = {"field":"context_vector", "query_vector":vec_querry,"k":3,"num_candidates":count_index}
        
        result = es.knn_search(index="corpus_v2test",knn=query_search,source=["context","Titre","Lien"])
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
docs =[ "question:  Qu'est-ce qu'Orange Côte d'Ivoire ?   reponse:  Orange Côte d'Ivoire (Orange CI ou OCI) est un opérateur de télécommunications leader en Côte d'Ivoire. Ils proposent une large gamme de services, y compris la téléphonie fixe et mobile, l'internet (3G, 4G, fibre), le Mobile Banking et la télévision.   source:    date :  2024-03-19",
        "question:  Quelle est le nombre d'abonnées sur linkedin d'Orange Côte d'Ivoire ?   reponse:  Orange CI compte 152 K abonnés sur linkedin   source:    date :  2024-03-19",
        "question:  Quand Orange Côte d'Ivoire a-t-elle été créée ?   reponse:  Orange CI a été créée en 1996.   source:    date :  2024-03-19",
        "question:  Quels sont les services offerts par Orange Côte d'Ivoire ?   reponse:  Orange CI offre une gamme complète de services de télécommunications, notamment :Téléphonie fixe et mobile,Internet (3G, 4G, fibre),Mobile Banking,Télévision,Services digitaux   source:    date :  2024-03-19",
        "question:  Qu'est-ce qui distingue Orange Côte d'Ivoire de ses concurrents ?   reponse:  Orange CI se distingue par son engagement envers l'innovation, la qualité et la responsabilité sociétale d'entreprise. Ils ont été certifiés ISO 9001 et Top Employer, et ils ont réalisé plus de 390 projets sociaux à travers la Fondation Orange Côte d'Ivoire.   source:    date :  2024-03-19",
        "question:  Où puis-je trouver plus d'informations sur Orange Côte d'Ivoire ?   reponse:  Vous pouvez trouver plus d'informations sur Orange Côte d'Ivoire sur leur site web : http://www.orangebusiness.ci   source:    date :  2024-03-19",
        "question:  Quelles sont les initiatives RSE d'Orange Côte d'Ivoire ?   reponse:  Orange CI s'engage dans plusieurs initiatives RSE, notamment dans les domaines de la santé, de l'éducation et de la culture. Ils ont réalisé plus de 390 projets sociaux à travers la Fondation Orange Côte d'Ivoire.   source:    date :  2024-03-19",
        "question:  Quelles sont les conditions de travail chez Orange Côte d'Ivoire ?   reponse:  : Orange CI offre des conditions de travail et de santé exceptionnelles à ses employés. Ils ont été certifiés Top Employer quatre années consécutives (2014-2017).   source:    date :  2024-03-19",
        "question:  Quelles sont les perspectives d'avenir pour Orange Côte d'Ivoire ?   reponse:  Orange CI continue d'investir dans l'innovation et le développement de ses réseaux. Ils visent à devenir le leader de la transformation digitale en Côte d'Ivoire.   source:    date :  2024-03-19",
        "question:  Comment puis-je contacter Orange Côte d'Ivoire ?   reponse:  Vous pouvez contacter Orange CI via leur site web, leur page Facebook, ou en appelant leur service client.   source:    date :  2024-03-19",
        "question:  Quelle est la position d'Orange CI sur le marché ivoirien ?   reponse:  Orange CI est le leader de la téléphonie mobile en Côte d'Ivoire avec près de 12 882 895 d'abonnés en Mars 2017 (selon l'ARTCI).   source:    date :  2024-03-19",
        "question:  Quand Orange Côte d'ivoire a fusionné avec Côte d'Ivoire Telecom ?   reponse:  Orange Côte d'ivoire a fusionné le 31 décembre 2016 avec Côte d’Ivoire Telecom   source:    date :  2024-03-19",
        "question:  Quelles sont les filiales d'Orange CI ?   reponse:  Orange CI a racheté Cellcom-Libéria et Airtel-Burkina Faso en 2017, qui sont devenues respectivement Orange Libéria et Orange Burkina Faso.   source:    date :  2024-03-19",
        "question:  Quelles sont les certifications d'Orange CI ?   reponse:  Orange CI est certifiée ISO 9001 par l'AFAQ-AFNOR pour sa démarche Qualité et Top Employer 2014, 2015, 2016 et 2017 pour ses conditions de travail et de santé exceptionnelles.   source:    date :  2024-03-19",
        "question:  Combien d'employés compte Orange CI ?   reponse:  Orange CI compte entre 1 001 et 5 000 employés et 2 115 membres associés.   source:    date :  2024-03-19",
        "question:  Que propose Orange CI en tant qu'entreprise citoyenne ?   reponse:  Orange CI s'engage dans la Responsabilité Sociétale d'Entreprise (RSE) et a réalisé plus de 390 projets sociaux (santé, éducation, culture) à travers la Fondation Orange Côte d'Ivoire.   source:    date :  2024-03-19",
        "question:  Qu'elle est le slogan d'orange   reponse:  Vous rapprocher de l'essentiel   source:    date :  2024-03-19",
        "question:  Quelle est le nombre de followers sur instagram d'Orange Côte d'Ivoire ?   reponse:  Orange CI compte 229 K de followers   source:    date :  2024-03-19",
        "question:  Qui est le Directeur Général du Groupe Orange d'Ivoire ?   reponse:  Mamadou Bamba est le Directeur Général du Groupe Orange d'Ivoire.   source:    date :  2024-03-19",
        "question:  Qui est la Directrice Générale Adjointe du Groupe Orange Côte   reponse:  Nafy Coulibaly Silué est la Directrice Générale Adjointe du Groupe Orange Côte d'Ivoire.   source:    date :  2024-03-19",
        "question:  Qui est le Directeur Général d'Orange Libéria ?   reponse:  Marius Yao est le Directeur Général d'Orange Libéria.   source:    date :  2024-03-19",
        "question:  Qui est le Directeur Général d'Orange Burkina ?   reponse:  Mamadou Coulibaly est le Directeur Général d'Orange Burkina.   source:    date :  2024-03-19",
        "question:  Qui est la Directrice Générale d'Orange Money Côte d'Ivoire ?   reponse:  Mariame Toure est la Directrice Générale d'Orange Money Côte d'Ivoire.   source:    date :  2024-03-19",
        "question:  Qui est le Directeur Général de Côte d'Ivoire Câbles ?   reponse:  Koné Kolo est le Directeur Général de Côte d'Ivoire Câbles.   source:    date :  2024-03-19",
        "question:  Quelle est la mission d'Orange CI en Afrique subsaharienne ?   reponse:  La mission d'Orange CI en Afrique subsaharienne est de connecter les populations et de leur donner accès aux avantages du numérique.   source:  https://groupe.orange.ci/fr/engagement-operateur-engage.html  date :  2024-03-19",
        "question:  Quels sont les engagements d'Orange CI en matière de développement durable ?   reponse:  Orange CI s'engage à rendre le numérique accessible à tous et à contribuer aux Objectifs de Développement Durable (ODD), notamment en matière d'éducation, de santé et d'inclusion sociale.   source:  https://groupe.orange.ci/fr/engagement-operateur-engage.html  date :  2024-03-19",
        "question:  Quels sont les programmes mis en place par Orange CI pour favoriser l'inclusion numérique ?   reponse:  Orange CI a mis en place plusieurs programmes, tels que les Orange Digital Centers, qui visent à former les jeunes aux métiers du numérique, à développer l'entrepreneuriat numérique et à sensibiliser les populations aux usages du numérique.   source:  https://groupe.orange.ci/fr/engagement-operateur-engage.html  date :  2024-03-19",
        "question:  Comment Orange CI accompagne-t-elle la révolution digitale du secteur de la santé ?   reponse:  Orange CI propose des solutions digitales pour améliorer la gestion des patients, la télémédecine et la formation des professionnels de la santé.   source:  https://groupe.orange.ci/fr/engagement-operateur-engage.html  date :  2024-03-19"
    ]
# chat.ingest(corpus=docs, collection_name= "corpus")  # Charger le corpus


async def main() -> None: 
    # Initialize Bot instance with a default parse mode which will be passed to all API calls 
   
    # And the run events dispatching 
    await dp.start_polling(bot) 
 
 
 

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout) 
    asyncio.run(main())

