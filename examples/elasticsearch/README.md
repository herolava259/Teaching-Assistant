# Elastic search Tutorial

## Comparing Elastic search with traditional relational database 

- Elastic search ~ PostgreSql
- Index ~ Database 
- Type ~ Table
- Document ~ Row 
- Fields ~ Column

## Interacting with Elastic Search on Kibana

```bash
# Create index
PUT course_v001 

# read all indexes in elastic search
GET _cat/indices

# read index 
GET course_v001

# delete index 
DELETE course_v001

 
```
## Create document with Postman 
- HTTP method: POST
- url: http://localhost:9200/course_v001/course
- type(table): course
- body
```json
{
    "title": "Caculus I",
    "type": "Math",
    "category": "natural science",
    "weight": 3
}
```

- Unless one provide id, elatic search automatically create a id randomly

- If you assign a specified id for the document you create, you can do the following way:
    - HTTP method: PUT
    - url: http://localhost:9200/course_v001/course/10001
    - type(table)
    - body: similar to the above 
## Read a specificed a document in elastic search
- HTTP method: GET 
- template url: http(s)://{your_domain}:9200/{your_index}/{your_type}/{specified_id}

- search all document in type: 
    - url: http(s)://{your_domain}:9200/{your_index}/{your_type}/_search

## CRUD on Postman

1. Delete:
- template url: http(s)://{hostname}:9200/{your_index}/{yourtype}/{specified_id}

## Partial update a specified document in elasticsearch
- template url: http(s)://{hostname}:9200/{your_index}/{your_type}/{specified_id}/_update
- body:
```json
{
    "doc":{
        "title" : "Physical I"

    }
}
```

## Delete by query 
- template url: http(s)://{hostname}:9200/{your_index}/{your_type}/_delete_by_query
- http method: POST
- body (json):
```json
{
    "query": {
        "match":{
            "title" : "Physic I"
        }
    }
}
```
## Advanced query
1. Search all by condition with pagination
- template url: http(s)://{hostname}:9200/{your_index}/{your_type}/_search
- http method: GET
- body(json):
```json
{
    "query":{
        "match_all":{

        },
        "sort":{
            "title":{
                "order": "asc"
            }
        }
        "from": 0,
        "size": 1,
        "_source": ["title"]
    }
}
```

2. Query with multiple condition
- template url: http(s)://{hostname}:9200/{your_index}/{your_type}/_search
- http method: GET
- body(json):

- and between all condition item
```json
{
    "query":{
        "bool":{
            "must":[
                {
                    "match":{
                        "title":"Physic I"
                    }
                },
                {
                    "match":{
                        "weight": 3
                    }
                }
            ]
        }
    }
}
```

- or between all condition item
```json
{
    "query":{
        "bool":{
            "should":[
                {
                    "match":{
                        "title":"Physic I"
                    }
                },
                {
                    "match":{
                        "title":"Caculus I"
                    }
                }
            ]
        }
    }
}
```

- query range: 
- ex: weight of course must be greater than 2

```json
{
    "query":{
        "bool":{
            "must":[
                {
                    "match":{
                        "title":"Physic I"
                    }
                }
            ],
            "filter":
            {
                "range":{
                    "weight":{
                        "gt": 1
                    }
                }
            }
        }
    }
}
```

- search extractly follow by specified field:
```json
{
    "query":{
        "match_pharse":{
            "title":"Physic I"
        }
    }
}
```

- hightlight specified text field:
```json
{
    "query":{
        "match_pharse":{
            "title":"Physic I"
        }
    },
    "hightlight":{
        "fields":{
            "title":{}
        }
    }
}
```

- group attributes:
```json
{
    "aggs": {
        "weight_group":{
            "terms":{
                "field": "weight"
            }
        }
    },
    "size": 0
}
```

- average a number specified field
```json
{
    "aggs":{
        "weight_avg":{
            "avg":{
                "field": "weight"
            }
        }
    }
}
```
* Note:
- with "must" field es will retrieve with all "match" item between and condition
- if one search with multiple criteria but at least 1 condition that match, one use "should" field instead of "must"
## Inverted Index
1. Create index
- url template: http(s)://{host_name}:9200/{my_index}/{my_type}/_mapping
- http method: PUT
* examples:
- my_type: user
- schema:
    - username: str
    - mobile: str
- body(json)

```json
{
    "propeties":{
        "username":{

            "type": "text",
            "index": true,
        },
        "mobile":{
            "type": "keyword",
            "index": false
        }
    }
}
```

* Note:
- What diffference between "keyword" type and "text" type
    - keyword: es consider the string only a string
    - text: ES considers the string as a text with many words

2. Read all index in specified type:
- url template: http(s)://{hostname}:9200/{my_index}/_mapping
- http method: GET

## Source for Elastic Search
- [ElasticSearch, Architecting for search](https://medium.com/better-programming/system-design-series-elasticsearch-architecting-for-search-5d5e61360463)
- [Basic CRUD in elasticsearch](https://www.youtube.com/watch?v=QaHvavpqxMU&t=789s)
- [Dev tool console](https://www.elastic.co/blog/dev-tools-console-kibana)
- [python-log-with-es](https://medium.com/devops-dudes/python-logs-a-jsons-journey-to-elasticsearch-ffbabfd44b83)
- [logging-master-es](https://www.youtube.com/watch?v=_hhO56anumg)
- [deepdive-es-distributed-architechture](https://viblo.asia/p/elasticsearch-distributed-search-ZnbRlr6lG2Xo)
- [es-how-to-work](https://viblo.asia/p/elasticsearch-zero-to-hero-2-co-che-hoat-dong-cua-elasticsearch-38X4ENMXJN2)
- [inverted-index-indexing-document-engineering](https://viblo.asia/p/tim-hieu-ve-inverted-index-trong-elasticsearch-3Q75wGpJ5Wb)
- [Elastic-Search-API](https://www.youtube.com/watch?v=L5q2xNIQQrc&t=96s)


