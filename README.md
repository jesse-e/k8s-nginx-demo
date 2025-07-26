# k8s-nginx-demo
K8's Starter

kubectl get pods
kubectl get services
kubectl get namespace
kubectl get deployments

kubectl get service flask-service

kubectl apply -f flask-app/flask-deployment.yaml

kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring
kubectl port-forward svc/loki 3100:3100 -n monitoring
kubectl port-forward svc/tempo-query-frontend 3200:3200 -n monitoring
kubectl port-forward svc/flask-service 8888:80

helm repo add fluent https://fluent.github.io/helm-charts
helm repo update
helm install fluent-bit fluent/fluent-bit \
  --namespace monitoring --create-namespace \
  --set backend.type=loki \
  --set backend.loki.host=loki.monitoring.svc \
  --set backend.loki.port=3100 \
  --set backend.loki.tls="off"

docker images
docker rmi <imagehash>
docker build -t tactilevisages/flask-app-traced:latest .
docker push tactilevisages/flask-app-traced:latest
kubectl rollout restart deployment flask-app

minikube ip

kubectl delete deployment flask-app
kubectl delete service flask-service