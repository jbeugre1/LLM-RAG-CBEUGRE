LLM RAG (Language Model Retrieval-Augmented Generation) is an advanced AI technique that combines the strengths of large language models (LLMs) with retrieval-based mechanisms to enhance information accuracy and relevance.

In a typical RAG setup, the language model generates responses by not only relying on its pre-trained knowledge but also by dynamically retrieving and integrating information from a vast external database or a curated set of documents. This dual approach allows the system to provide more precise, up-to-date, and contextually appropriate answers, especially in scenarios where the pre-trained model alone might lack specific or recent information.

The key components of LLM RAG include:

1.	Language Model (LLM): A pre-trained model capable of understanding and generating human-like text based on the input it receives.
2.	Retrieval Mechanism: A system that searches and fetches relevant documents or data from an external source based on the input query.
3.	Integration Module: A component that seamlessly integrates the retrieved information with the language model’s generated text to produce coherent and accurate responses.




### Download elastic ###

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.14.2-windows-x86_64.zip <br>
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.14.3-darwin-x86_64.tar.gz <br>
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.14.2-linux-x86_64.tar.gz <br>

### Unzip ###
(Vous maitrisez deja)

### Launch elastic Search ###
elasticsearch-8.14.3\bin\elasticsearch.bat (Windows)
./elasticsearch-8.14.3/bin/elasticsearch (Mac/Linux)

IMPORTANT: Ensure the password remains confidential and update the authentication in the main.py and injest.py code.

### Install Ollama ###

curl -fsSL https://ollama.com/install.sh | sh

### Install LLM Model ###

ollama pull llama3
ollama pull gemma2

### Other Requirement ###

Python version:python 3.10.8

install git
install pip (ubuntu) : sudo apt install python3-pip -y
install virtual : sudo apt install python3-virtualenv


### Launch Bot###

clone repositry : https://github.com/jbeugre1/MLOPS_LLM

create virtual env
activate the environment
install requirement.txt for python module

launch the shell: ./run_serie

### Run_Serie ###

Run_serie run two python code Injest.py and Main.py

Injest check if there is json file in the folder "Corpus" and insert them in our elasticsearch index and after that move it in the folder "Traité"
Main.py run telegram bot and our model LLM


### Json format ###


{
"context": "",
        "metadata": {
            "Titre": "",
            "version": "",
            "Lien": "",
            "date-vectorisation": ""
        }
}
