# wikipedia-article-summarization
Summarizes Wikipedia articles with transformers T5 model. You can execute it through a Python script, access it through a fast API's REST API or through a streamlit web page.  
You can access a live web page <a href="http://149.56.100.90:8502/">here</a>.

## Installing

1. Install requirements
```shell
pip install -r requirements.txt
```

2 (optional). Install Docker if you wish to run the web application in a Docker container. You can skip step 1 if that is the only application you wish to execute.

## Usage

### 1. Python program  

Run summarize_wikipedia.py [--limit <character_limit>] <english wikipedia page's URL>:
```shell
python summarize_wikipedia.py --limit 1000 https://en.wikipedia.org/wiki/PageRank
```

### 2. REST API  

Generate an API key (e.g. "abc" with salt "1"):
```shell
python ./utils/hash_key.py "abc" "1"
```

Set API key and salt as environment variables (use export instead of set for Linux systems):
```shell
set SUMMARIZE_API_KEYS="abc"
set SUMMARIZE_SALT="1"
```

Run fast API with uvicorn (or other web server of your choice):
```shell
uvicorn api:app --host 0.0.0.0 --port 8000
```

Send a GET request to /summarize/ endpoint with URL and character limit as parameters, with API key as header (/utils/request.ps1 provides a Powershell example):
```shell
./utils/request.ps1
```

### 3. Web app

You can run the web app through streamlit directly or through Docker using the provided Dockerfile.

Run streamlit web app (python):
```shell
streamlit run webpage.py
```

Run streamlit web app (docker):
```shell
docker build -t summarizer_webapp .
```

```shell
docker run -p 8502:8502 summarizer_webapp
```

Access the web page in http://localhost:8501 (ran via streamlit) or http://localhost:8502 (ran via docker).
