# Simple chatbot using Elasticsearch
This repo demonstrates how we can create a simple chatbot that responds to user inputs using the Elasticsearch engine.  We use Elasticsearch as it is fast and efficient and has built-in methods for searching texts.  

## How to use
### Step 1
Before we can run the code, we have to install and run the Elasticsearch server. For simplicity, I recommend using the official docker of Elasticsearch. 
Execute the following to pull the Elasticseach docker image:
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.5.4
```
Then run the following to start the server:
```bash
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.5.4
```
Please refer to [this](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) reference for more info about the Elasticsearch docker. 
### Step 2
Now that we have the Elasticsearch engine running, we can run our python script. But before that, please make sure that you have the required packages installed by running the following command:
```bash
pip install -r requirements.txt
```
Ok, now run the following to start the program:
```bash
python main.py
```
Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and start chatting with the bot :)

![sample image](imgs/sample.gif)

## Control commands
You can add a new input-output pair to the knowledge base by sending the `/learn` command to the bot and following the on-screen instructions. To stop the learning mode, send `/stop` command. 

## Dataset
The dataset that I used here is the [Chatterbot's English corpus](https://github.com/gunthercox/chatterbot-corpus) which is translated from English to Persian by:
[Saeed Torabzadeh](https://github.com/zhn1010), [Alireza Davoudi](https://github.com/adavoudi) and [Ebrahim Soroush](https://github.com/e3oroush)
