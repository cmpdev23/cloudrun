#!/bin/bash
# 🐳 Script de déploiement pour Google Cloud Run

# chmod +x deploy.sh

# ./deploy.sh

# 🧾 Variables à ajuster
PROJECT_ID="noble-history-405615"
REGION="northamerica-northeast1"
REPO="app-utile"
IMAGE_NAME="create-deal-optimized"
TAG="latest"
SERVICE_NAME="create-deal-optimized"

# 🔐 Authentifier Docker à Google Artifact Registry
gcloud auth configure-docker $REGION-docker.pkg.dev

# 🏗️ Construire l'image localement
docker build -t $IMAGE_NAME .

# 🏷️ Taguer l'image pour le push vers Artifact Registry
docker tag $IMAGE_NAME $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE_NAME:$TAG

# 📤 Pousser l'image
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE_NAME:$TAG

# 🚀 Déployer sur Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE_NAME:$TAG \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated
