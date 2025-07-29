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

helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring


docker images
docker rmi <imagehash>
docker build -t tactilevisages/flask-app-traced:latest .
docker push tactilevisages/flask-app-traced:latest
kubectl rollout restart deployment flask-app

minikube ip

kubectl delete deployment flask-app
kubectl delete service flask-service

kubectl config get-contexts
to switch
kubectl config use-context minikube


kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo


 eks-cluster-terraform % eksctl create cluster \
  --name eks-monitoring-cluster \
  --region us-west-2 \
  --zones us-west-2a,us-west-2b,us-west-2c \
  --nodegroup-name default-ng \
  --node-type t3.medium \
  --nodes 2 \
  --managed \
  --with-oidc \
  --tags Environment=dev

kubectl get pods -n monitoring -o wide

get pw
kubectl get secret -n monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
