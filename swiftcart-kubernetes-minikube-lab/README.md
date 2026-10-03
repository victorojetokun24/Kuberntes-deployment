# SwiftCart Logistics — Kubernetes + Minikube Lab

Continuation of the Docker and Docker Compose labs.

## Resources covered
- Pod
- Deployment
- Service
- ConfigMap
- Secret
- PersistentVolumeClaim / Volume
- Ingress

## Quick start

```bash
minikube start --driver=docker
minikube addons enable ingress
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-configmap.yaml
kubectl apply -f k8s/02-secret.yaml
kubectl apply -f k8s/03-postgres-pvc.yaml
kubectl apply -f k8s/04-postgres-deployment.yaml
kubectl apply -f k8s/05-postgres-service.yaml
eval $(minikube docker-env)
docker build -t swiftcart-api:3.0.0 ./app
kubectl apply -f k8s/06-app-deployment.yaml
kubectl apply -f k8s/07-app-service.yaml
kubectl apply -f k8s/08-ingress.yaml
kubectl get all -n swiftcart
```

See the full student guide for verification, Ingress access, persistence, scaling, rolling updates and troubleshooting.
