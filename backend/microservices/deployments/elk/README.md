

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