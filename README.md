# Intelligent Document Management
This project allows the user to quickly gain insights into their data, such as the author, language, or creation date. Additionally, the user can categorize their data by using one of three implemented classifiers to label their files (more information on the classifiers below). 

## Classifiers
The project contains three different classifiers to label documents: a small multilingual zero-shot classifier from HuggingFace, Phi-4-mini-instruct by Microsoft from HuggingFace and gemini-3.1-flash-lite-preview using the Gemini API. Each classifier comes with its own (dis)-advantages, which are listed here:

| Classifier | Pros | Cons |
|---|---|---|
| zero-shot | - Fast inference<br>- Requires no download | - Requires predetermined set of labels<br>- Lower quality labels |
| Phi-4-mini-instruct | - No predetermined set of labels<br>- Generally accurate labels | - Requires downloading model checkpoints on first run (-+6GB)<br>- Slower inference |
| gemini-3.1-flash-lite-preview | - High quality labels<br>- Requires no download<br>- Fast inference<br>- Has free tier<br>- No predetermined set of labels | - There is a quota on the free tier |

## Getting started
To run the app, please follow the instructions below.

### Prerequisites
This project requires a working Docker installation. 

### Running the app
To run the project, frst copy the `.env.example`:
```bash
cp .env.examples .env
```
By default, the code runs with the zero-shot classifier. Alternatively, for Phi-4-mini-instruct set `ClASSIFIER` to `phi4`. This requires downloading the model checkpoints the first time (-+6GB), so loading the app can take longer. 
```bash
sed -i 's/CLASSIFIER=.*/CLASSIFIER=phi4/' .env
```
Or, to use the Gemini API (free tier) as a classifier set it to `gemini`. This option requires a valid gemini API key.
```bash
sed -i 's/CLASSIFIER=.*/CLASSIFIER=gemini/' .env
sed -i 's/GEMINI_API_KEY=.*/GEMINI_API_KEY=<your-api-key>/' .env
```
Then, the app runs with:
```bash
docker compose up
```
You can interact with the API endpoints at [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/). 

You can provide a path to your folder for both endpoints (for example, "data/Company_A").