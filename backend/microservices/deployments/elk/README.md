# Setting up ELK triage

## Install Elastich search - Logtash(later) - Kibana 

## 1. **Install without docker compose**

### * Check private network whether they are available 

```bash
docker network ls 
```

### * Create a private network for elastic-search and kibana (to easily managemenet)

```bash 
docker network create es-net --driver=bridge
```

### * Install and run elastic search service 

```bash 
docker run -d \ 
--name es-container ## name of the container after compose es image \
--net es-net ## name of the private which one've recently built \
-p 9200:9200 ## port private and public \
-e xpack.security.enabled=false ## no requirement for user proceed signin functionality \
-e discovery.type=single-node ## only once node for elastic search \ 
docker.elastic.co/elasticsearch/elasticsearch:7.11.0
```

### * Install kibana

```bash 
docker run -d \ 
--name kb-container \ 
--net es-net \
-p 5601:5601 \
-e ELASTICSEARCH_HOSTS=http://es-container:9200 \
docker.elastic.co/kibana/kibana:7.11.0
```

### * Shutting and prune service 
```bash 
docker container stop kb-container
docker container stop es-container
```

```bash
docker container prune 
```

## 2. **Using Docker compose to build**
- Running the following cmd to compose and run a cluster of container include **elasticsearch + kibana**
- From microservices folder: Redirect your terminal to **./deployments/elk** folder 

```bash
cd deployments/elk

```

and run: 
```bash 
docker compose -f docker-compose-elk.yml up -d
```

and stop the cluster of containers
```bash
docker-compose down
```

## 3. **Additional step: Setup elastic search with tls/ssl certificates (so tired |~_~|, feel painful+stressful)**

- project sturture 

```arduino
elasticsearch-docker/
├── docker-compose-elk.yml
├── config/
│   └── elasticsearch.yml
└── certs/
```
- Step 1: Generate TLS certificates
    * Create directory
    * begin at: ./deployments/elk
```bash
mkdir certs && cd certs 
```
----------
> Run the elasticsearch-certutil in a temporary container:
---------
```bash
docker run --rm -v $PWD:/certs \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.0 \
  bin/elasticsearch-certutil ca --pem -out /certs/elastic-stack-ca.zip

```
------
> **Unzip generated CA:**

```bash
unzip elastic-stack-ca.zip
```
---
>generate certificates for ssl/tls 
``` bash
docker run --rm -v $PWD:/certs \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.0 \
  bin/elasticsearch-certutil cert --name es-node --ca-cert /certs/ca/ca.crt --ca-key /certs/ca/ca.key --pem -out /certs/elastic-certificates.zip
```
---
>Unzip generated certificates
```bash
unzip elastic-certificates.zip
```

- Step 2: Elasticsearch Configuration

> Create **config/elasticsearch.yml**:

```yaml
cluster.name: "docker-secure-cluster"
network.host: 0.0.0.0
xpack.security.enabled: true
xpack.security.http.ssl:
  enabled: true
  key: /usr/share/elasticsearch/config/certs/es-node/es-node.key
  certificate: /usr/share/elasticsearch/config/certs/es-node/es-node.crt
  certificate_authorities: [ "/usr/share/elasticsearch/config/certs/ca/ca.crt" ]
xpack.security.transport.ssl:
  enabled: true
  verification_mode: certificate
  key: /usr/share/elasticsearch/config/certs/es-node/es-node.key
  certificate: /usr/share/elasticsearch/config/certs/es-node/es-node.crt
  certificate_authorities: [ "/usr/share/elasticsearch/config/certs/ca/ca.crt" ]
```

- Step 3: Some modification on docker-compose-elk.yml to docker-compose-elk-secure.tml 

```bash
environments:
    ...
    - cluster.name=secure-cluster
    - xpack.security.http.ssl.enabled=true
    - xpack.security.transport.ssl.enabled=true
    - xpack.security.http.ssl.keystore.path=/usr/share/elasticsearch/config/certs/es-node/es-node.p12
    - xpack.security.transport.ssl.keystore.path=/usr/share/elasticsearch/config/certs/es-node/es-node.p12
    ...
```

```bash
...
healthcheck: test: curl --cacert /usr/share/elasticsearch/config/certs/ca/ca.crt -u elastic:changeme https://localhost:9200 || exit 1
...
```

```bash
volumes
    - ./config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
    - ./certs:/usr/share/elasticsearch/config/certs:ro
```

## How to setup logtash docker 