### Application
Simple Python app based on built-in **HTTPServer**.
Class inherited from **BaseHTTPRequestHandler** has simple routing for 3 URLs:   
- **/** - index page
- **/metrics** - prometheus metrics exporter
- default handler for 404 requests. 
  
Metrics included in the app are simple counters for 200 and 404 responses.

### Dockerfile
Based on minimal image, including necessary Pyhton interpreter and additional modules. Healthcheck is present.

### Run the app
Application is launching among with Prometheus and Grafana to collect metrics and draw images.   

    mkdir trl && cd trl
    git clone https://github.com/wdowny/trltest.git .
    docker-compose build && docker-compose up -d

This runs the application and binds it to 80 port of the host. Prometheus and Grafana should respond on their standard ports (9090 and 3000, respectively). Credentials are default.

### Kubernetes
`kubespec.yaml` includes *all* necessary settings to run application (app itself was built and placed to DockerHub). In the same directory which remained from previous chapter, run

    kubectl apply -f kubespec.yaml
    
Application itself should respond on port 30080, Prom on 30090 and Grafana on port 30030, binded to address of any node of your cluster.
