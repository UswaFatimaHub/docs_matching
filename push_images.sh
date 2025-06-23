#!/bin/bash

# Docker Hub credentials
DOCKERHUB_USER="uswafatima0"
REPO_NAME="embeddings_matcher"

# Full image names
WEB_IMAGE="$DOCKERHUB_USER/$REPO_NAME:web"
SCHEDULER_IMAGE="$DOCKERHUB_USER/$REPO_NAME:scheduler"

# Tag images
echo " Tagging images..."
docker tag embedding_project-web $WEB_IMAGE
docker tag embedding_project-scheduler $SCHEDULER_IMAGE

# Push images
echo " Pushing web image to Docker Hub..."
docker push $WEB_IMAGE

echo " Pushing scheduler image to Docker Hub..."
docker push $SCHEDULER_IMAGE

echo "✅ All images pushed successfully!"
