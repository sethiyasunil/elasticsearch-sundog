##########ch-01

```
Reference https://sundog-education.com/elasticsearch/
 
 
PUT /shakespeare
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 0
  }
}

 curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/shakespeare/_mapping' --data-binary @shakes-mapping.json
 
 curl -H 'Content-Type: application/json' -XPOST  'http://127.0.0.1:9200/shakespeare/_bulk?pretty' --data-binary @shakespeare_7.0.json
 
 
 curl -H 'Content-Type: application/json' -XGET 'http://127.0.0.1:9200/shakespeare/_search?pretty' -d '{"query" : {"match_phrase" : {"text_entry" : "to be or not to be"}}}'
```

#######  ch-02
```
http://files.grouplens.org/datasets/movielens/ml-latest-small.zip


DELETE /movies
GET /movies/_mapping

PUT /movies?include_type_name=true
{
  "mappings": {
    "_doc": {
      "properties": {
        "type": { "type": "keyword" },
        "year" : {"type": "date"},
        "genre": {"type": "text"}
      }
    }
  }
}

GET /movies/_mapping

curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/_bulk?pretty' --data-binary @movies.json

GET /movies2/_search
{
  "query":{
    "match_all":{}
  }
}



POST /movies/_doc/109487
{ "title" : "Interstellar", "year":2014 , "genre":["Sci-Fi", "IMAX"] , "type":"movie"}



POST /movies/_update/109487
{
  "doc":{
   "title" : "Interstellar"
  }
}
  

POST /movies/_update/109487?version=5
{
  "doc":{
   "title" : "Interstellar"
  }
}


GET  /movies/_search
{
  "query":{
    "match":{
    "genre": "Sci-Fi"
    }

  }
}
```

```

DELETE /series
PUT /series?include_type_name=true
{
  "mappings": {
    "_doc":{
      "properties": {
        "type": { "type": "keyword" },
        "year" : {"type": "date"},
        "genre": {"type": "text"},
        "film_to_franchise":{"type":"join", "relations":{"franchise":"film"}}
     }      
    }
  }
}
GET  /series/_search
{
  "query":{
    "match_all":{ }

  }
}


curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/_bulk?pretty' --data-binary @series.json
GET  /series/_search
{
  "query":{
    "parent_id":{ 
      "type":"film",
      "id":1
    }
  }
}

```



