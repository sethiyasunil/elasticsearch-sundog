##########ch-01
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


#######  ch-02
http://files.grouplens.org/datasets/movielens/ml-latest-small.zip



curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/_bulk?pretty' --data-binary @movies.json

