# serverless-flights-price-checker

it needs a .env file or some env variables

API_KEY=<API_KEY>
API_HOST=sky-scanner3.p.rapidapi.com
TELEGRAM_TOKEN=<TELEGRAM_TOKEN>


TDB

## DEPLOY in GCP Function
```
export API_KEY=<API_KEY>
export TELEGRAM_TOKEN=<TELEGRAM_TOKEN>
gcloud beta functions deploy webhook --set-env-vars "API_KEY=$API_KEY>,API_HOST=sky-scanner3.p.rapidapi.com,TELEGRAM_TOKEN=$TELEGRAM_TOKEN" --runtime python39 --trigger-http
```
