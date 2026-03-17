
# Intelligent Document Management
<!-- Quick intro -->
This project allows the user to quickly gain insights into their data, such as the author, language, or creation date. Additionally, the user can categorize their data by using one of three implemented classifiers to label their files (more information on the classifiers below). All metadata and generated labels get saved in a persistent **PostreSQL** relation database. 

<!-- Describe API endpoint + interactions -->
The app runs through **FastAPI**, and contains two API endpoints:
- `folder/insights`: This endpoint allows the user to retrieve metadata, such as author, language, word count, file size from all files within the provided directory (details in [section on PostreSQL](#postresql-database)). It supports the following document types: .docx, .pdf and .txt. All gathered metadata is saved in the database.
- `folder/classify`: This endpoint allows the user to classify all .docx, .pdf and .txt file in a provided directory, using one of three implemented classifiers (more details in [section on classifiers](#classifiers--tradeoffs)). The generated labels get saved in the database.

<!-- Describe docker setup -->
The project is containerized with **Docker**, allowing for quick and easy deployment on other machines, as well as scalability (for example by deploying on larger machines). The project is divided into three different docker containers:
- The **app container** holds the main code for running the endpoints. It communicates with the **database container** and is orchestrated by `docker-compose.yaml`.
- The **database container** contains the PostreSQL database. Only the app container can communicate with this container, adding a layer of security for outside access. Moreover, there are no exposed ports outside of the ones used by the app container. This container is orchestrated by `docker-compose.yaml`.
- The tests live in their own **test container**, which allows for easy and quick testing testing through `docker-compose-tests.yaml`. 

## Classifiers & Tradeoffs
The user can choose between three different classifiers to label documents: 
- **multilingual-MiniLMv2-L6-mnli-xnli**: a small multilingual model capable of Natural Language Inference (NLI) and zero-shot classification. The model is a distillation from the larger XLM-RoBERTa-large.
- **Phi-4-mini-instruct**: a somewhat larger LLM by Microsoft, capable of mulitlingual text generation. This model is part of the Phi-4 family. 
- **gemini-3.1-flash-lite-preview**: A very capable LLM from Gemini, capable of high-volume agentic tasks, translation and processing. This model has a generous free tier. 

Different models may suit different users, as each classifier comes with its own (dis)-advantages. The table below illustrates strengths and weaknesses of each classifier:

| Classifier | Pros | Cons |
|---|---|---|
| **multilingual-MiniLMv2-L6-mnli-xnli** | - Fast inference<br>- Requires no large download | - Requires predetermined set of labels<br>- Lower quality labels |
| **Phi-4-mini-instruct** | - No predetermined set of labels<br>- Generally accurate labels | - Requires downloading model checkpoints on first run (+-5GB)<br>- Slower inference |
| **gemini-3.1-flash-lite-preview** | - High quality labels<br>- Requires no download<br>- Fast inference<br>- Has free tier<br>- No predetermined set of labels | - There is a quota on the free tier |

The default classifier is zero-shot, as this is fast and requires not API key. However, for best performance, the gemini classifier is recommended. Details on how to use each classifier are in the [Setup section](#setup-instructions).

## PostreSQL Database

All of the metadata gets saved in a persistant **PostreSQL** relational database. This database system is capable of handling large databases, thus allowing scalability. Moreover, it supports a number of security features, such as multi-factor authorization.

The database resides in its own docker container, which helps with keeping it secure from the outside and allowing scalability. The only communication comes through the app container, and the contents of the database get saved across different runs and container rebuilds. 

Depending on the file type, the following metadata can get saved in the database:

| What?  | Note | Supported Filetype |
|---|---|---|
| `author` | Name of author | .docx and .pdf |
| `filename` | Name of file | .txt, .docx and .pdf |
| `title` | Title of document | .pdf |
| `subject` | Topic of document | .pdf |
| `keywords` | Keywords of document | .pdf |
| `language` | Language of text in document | .txt, .docx and .pdf |
| `created` | Time of creation | .txt, .docx and .pdf |
| `modified` | Time of last edit | .txt, .docx and .pdf |
| `file_type` | File type | .txt, .docx and .pdf |
| `file_size` | Size in bytes | .txt, .docx and .pdf |
| `paragraph_count` | Number of paragraphs in text | .docx |
| `table_count` | Number of tables in text | .docx |
| `section_count` | Number of sections in text | .docx |
| `word_count` | Number of words in text | .txt, .docx and .pdf |
| `created_with` | Tool used to create document | .pdf |
| `label` | Label generated by classifier | .txt, .docx and .pdf |

## Repository Structure

To create a clear overview, a description of the top-level directories are shown here:
- `data/`
Contains sample documents for testing the API endpoints. The files are of .docx, .txt and .pdf types.
- `docker/`
Contains the Dockerfile, which is used by both `docker-compose.yaml` and `docker-compose-tests.yaml`. This Dockerfile sets up dependencies and runs the FastAPI app. 
- `src/`
Contains the main code for running the app and setting up the database. Additionally, it contains: 
    - `services`
    Contains the code for ingesting documents and extracting their metadata, as well as classifying and saving to the database.
- `tests/`
Contains code for testing the endpoints and individual methods. This is split into: 
    - `unit/`
    Contains the unit tests for validating individual methods.
    - `integration/`
    Contains the code for testing the endpoint outputs.

# Setup Instructions
To run the app, please follow the instructions below.

## Prerequisites
This project requires a working Docker installation. Version 29.2.1 is recommended. 

## Setting `.env `
Before running the project, the user needs to set some variables in their `.env`. First copy the `.env.example`:
```bash
cp .env.examples .env
```
All of the variables that need to be set can be edited through an editor such as nano. Alternatively, you can use the one-liners below to edit the values. 

You can choose different classifiers by setting them in your `.env` file. By default, the code runs with the zero-shot classifier. Alternatively, for Phi-4-mini-instruct set `ClASSIFIER` to `phi4`. This requires downloading the model checkpoints the first time (-+6GB), so loading the app can take longer. 
```bash
sed -i 's/CLASSIFIER=.*/CLASSIFIER=phi4/' .env
```
Or, to use the Gemini API (free tier) as a classifier set it to `gemini`. This option requires a valid gemini API key.
```bash
sed -i 's/CLASSIFIER=.*/CLASSIFIER=gemini/' .env
sed -i 's/GEMINI_API_KEY=.*/GEMINI_API_KEY=<your-api-key>/' .env
```
For security purposes, the database requires a user and password to be set in `.env`. Remember to replace <user> and <password> with a username and password of your choice. 
```bash
# Replace <user> with your username
sed -i 's/POSTGRES_USER=.*/POSTGRES_USER=<user>/' .env
# Replace <password> with your password
sed -i 's/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=<password>/' .env
```
By default, the code runs on GPU if it's available. To force GPU or CPU, set `TORCH_DEVICE` in `.env` to cuda or cpu, respectively: 
```bash
# For GPU
sed -i 's/TORCH_DEVICE=.*/TORCH_DEVICE=cuda/' .env
# For CPU
sed -i 's/TORCH_DEVICE=.*/TORCH_DEVICE=cpu/' .env
```
## Running the app
The app runs with: 
```bash
docker compose up
```
You can interact with the API endpoints at [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/).  
You can provide a path to your folder for both endpoints (for example, "data/Company_A").

To stop the container, run:
```bash
docker compose down
```

# Testing
For automated and quick testing, the project uses unittests for verifying smaller functions and integration tests for testing the endpoints. The tests are set up in their Docker container, and can be run with:
```bash
docker compose -f docker-compose-tests.yaml up
```
To stop the container, run: 
```bash
docker compose -f docker-compose-tests.yaml down -v
```