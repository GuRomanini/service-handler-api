#!/usr/bin/env bash
# Send docker image to GCP imgs repository

if [ "$1" != "" ]; then
version=$(git rev-parse HEAD)

tag=`echo "$1" | tr '[:upper:]' '[:lower:]'`
repo_name='service-handler-api'

docker build -t $repo_name --build-arg COMMIT=$version --target=prod -f infrastructure/Dockerfile .

gcloud config set project uav-as-a-service

GCP_PROJECT=`gcloud config get-value project 2> /dev/null`
echo "$GCP_PROJECT"

docker tag $repo_name:latest gcr.io/$GCP_PROJECT/$repo_name:$version
docker push gcr.io/$GCP_PROJECT/$repo_name:$version

docker tag $repo_name:latest gcr.io/$GCP_PROJECT/$repo_name
docker push gcr.io/$GCP_PROJECT/$repo_name

for CLUSTERZONES in $(gcloud beta container clusters list --project=$GCP_PROJECT --format="csv[no-heading](name,zone)")
do
  # Parse (name,zone) --> $CLUSTER, $LOCATION
  IFS="," read CLUSTER LOCATION <<<"${CLUSTERZONES}"
  echo -e "Cluster:       ${CLUSTER}"
  echo -e "Location:      ${LOCATION}"
done

gcloud container clusters get-credentials ${CLUSTER} --zone ${LOCATION} --project $GCP_PROJECT
kubectl apply -f infrastructure/deploy/deployment.yml
kubectl set image deployment $repo_name-deployment $repo_name-container=gcr.io/$GCP_PROJECT/$repo_name:$version

