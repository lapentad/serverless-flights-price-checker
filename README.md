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

To deploy this Python application on Google Cloud Run, you'll need to create a Docker container for your application and then deploy it to Cloud Run. I'll guide you through the steps:

### Enable Google Cloud APIs

Ensure the following Google Cloud services are enabled:

1. **Cloud Run API**: For running your containerized applications.
2. **Cloud Build API**: For building your container images.
3. **Artifact Registry (optional)**: If you want to use Google’s Artifact Registry to store your Docker images.

You can enable these via the Google Cloud Console or using the `gcloud` CLI:

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Build and Push the Docker Image

Before deploying your app, you need to build the Docker image and push it to Google Container Registry (GCR) or Artifact Registry.

1. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   ```

2. **Set the project ID** (replace `your-project-id` with your actual project ID):
   ```bash
   gcloud config set project your-project-id
   ```

3. **Build the Docker image**:
   From the root of your project directory (where the `Dockerfile` is located), run the following command:
   ```bash
   gcloud builds submit --tag gcr.io/your-project-id/your-image-name .
   ```

   This will build your Docker image and push it to Google Container Registry (`gcr.io`).

### Deploy to Cloud Run

Once your image is in Container Registry, you can deploy it to Cloud Run.

1. **Deploy the image** to Cloud Run:
   ```bash
   gcloud run deploy your-service-name \
     --image gcr.io/your-project-id/your-image-name \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars API_KEY=your_api_key,API_HOST=your_api_host,TELEGRAM_TOKEN=your_telegram_token
   ```

   - Replace `your-service-name` with the name you want to give your Cloud Run service.
   - Replace `your-image-name` with the name of your Docker image in GCR.
   - You can change the region (`us-central1`) to the one that is closest to you.

2. After the deployment, Cloud Run will provide you with a URL where your application is hosted.


### Test the Deployment

Once deployed, you should be able to access your app using the URL provided by Cloud Run. You can test it by interacting with your Telegram bot. Send commands like `/start` and `/get CDG JFK` to see if it returns the expected flight details.
