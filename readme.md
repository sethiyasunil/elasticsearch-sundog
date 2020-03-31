## installation

```

Refer installation/readme.md
Refer "Course Materials_ Elasticsearch and the Elastic Stack.pdf"
https://medium.com/@pierangelo1982/how-to-install-elasticsearch-6-on-ubuntu-64316dc2de1c


set virtualbox network (openports.png)

open putty and connect to ubantu

sudo apt-get update
sudo apt-get install openjdk-8-jre-headless -y
sudo apt-get install openjdk-8-jdk-headless -y
sudo apt-get install apt-transport-https


Download and install Elastic search package manually
Refer 'Download and install the Debian package manually' https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#install-deb
scp -P 2200 D:\sunil\setups\elasticsearch\ubantu\elasticsearch-7.6.1-amd64.deb e@localhost:/home/e/sunil
sudo dpkg -i elasticsearch-7.6.1-amd64.deb

sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
systemctl start elasticsearch.service
systemctl status elasticsearch.service

Check service is working7
curl -X GET 'localhost:9200/'
```

Install Kibana
```
download https://www.elastic.co/guide/en/kibana/current/deb.html#install-deb
scp -P 2200 D:\sunil\setups\elasticsearch\ubantu\kibana-7.6.1-amd64.deb e@localhost:/home/e/sunil
sudo dpkg -i kibana-7.6.1-amd64.deb

sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
sudo systemctl start kibana.service
sudo systemctl status kibana.service
```

Update ES and Kibana configuration

``` 
ificonfig - take ip
sudo vim /etc/kibana/kibana.yml
	server.host: "10.0.2.15"
http://localhost:5601/app/kibana#
``` 


## Whats new in ES7
``` 
Type is removed (table concept). Type allows different schema in same index.
SQL support
Default shard are 5 instead of 1
Leucene version is upgraded
Java is inbuild
Replication across cluster is now possible
Java Client is now available.
 ``` 

## Shakespeare example

```
Reference https://sundog-education.com/elasticsearch/
 
You cannot change number of shared once setup
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

##  movies example

Insert record
```
http://files.grouplens.org/datasets/movielens/ml-latest-small.zip

DELETE /movies

PUT /movies
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 0
  }
}


PUT /moviess
{
  "mappings": {
      "properties": {
		"id" :{"type":"integer"},
        "year" : {"type": "date"},
        "genre": {"type": "text"}
      }      
  }
}


POST /movies/_doc/109487
{ "title" : "Interstellar", "year":2014 , "genre":["Sci-Fi", "IMAX"] , "type":"movie"}
```


```
Bulk insert
curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/_bulk?pretty' --data-binary @movies.json

GET /movies/_search
{
  "query":{
    "match_all":{}
  }
}
```

```
Update documents

POST /movies/_update/109487
{
  "doc":{
   "title" : "Interstellar"
  }
}


DELETE /movies/_doc/109487
```


```
Concurency

POST /movies/_update/109487?if_seq_no=x&if_primary_term=y
{
  "doc":{
   "title" : "Interstellar"
  }
}
```

##   movies example (De-normalize data)
```
DELETE /series

PUT /series
{
  "mappings": {
      "properties": {
        "year" : {"type": "date"},
        "genre": {"type": "text"},
        "film_to_franchise":{"type":"join", "relations":{"franchise":"film"}}
     }      
    }
}


curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/_bulk?pretty' --data-binary @series.json

GET  /series/_search
{
  "query":{
    "parent_id":{
      "type":"film",
      "id":9999
    }
  }
}

GET  /series/_search
{
  "query":{
    "has_parent":{ 
      "parent_type":"franchise",
      "query": {
        "match": {
          "title" : "Star Wars"
        }
      }
    }
  }
}

```

##   movies example (queries and filters)
```
Filter types - filter.png
terms, term, range, exists, missing, bool

Queries Types - queries.png
match_all, match, multi_match, bool , match_phrase, prefix, wildcard, 

```


##   movies example (ngram analyzer example to get feature - search as you type)
```
DELETE /movies

PUT /movies
{
  "settings": {
    "analysis": {
      "filter": {
        "autocomplete_filter": {
          "type": "edge_ngram",
          "min_gram": 1,
          "max_gram": 20
          }
          },
          "analyzer": {
          "autocomplete": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
          "lowercase",
          "autocomplete_filter"
          ]
        }
      }
    }
  }
}


PUT /movies/_mapping
{
  "properties": {
    "title": {
      "type" : "text",
      "analyzer": "autocomplete"
    }
  }
}

```

##   import data
```
cd import-data
python3 import-movies-script.py >movies.json
python3 import-ratings.py >ratings.json
python3 import-tags.py > tags.json

curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/_bulk?pretty' --data-binary @movies.json
curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/_bulk?pretty' --data-binary @ratings.json
curl -H 'Content-Type: application/json' -XPUT 'http://127.0.0.1:9200/_bulk?pretty' --data-binary @tags.json
```

##  logstach

```
installation steps on page 0141
OR
Download and install manully https://www.elastic.co/downloads/logstash
scp -P 2200 D:\sunil\setups\elasticsearch\ubantu\logstash-7.6.1.deb e@localhost:/home/e/sunil/
sudo dpkg -i logstash-7.6.1.deb


configuration fiel to parse access logs - 0142

scp -P 2200 access_log e@localhost:/home/e/sunil/logstash/
scp -P 2200 logstash.conf e@localhost:/etc/logstash/conf.d/logstash.conf

cd /usr/share/logstash
sudo bin/logstash -f /etc/logstash/conf.d/logstash.conf --path.settings /etc/logstash
```


```
Histogram - page 0177
Time series - page 0181
Nexted Aggregations : -page 0189

```

## filebeat
```
Refer page 213
download https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.6.1-amd64.deb
scp -P 2200 D:\sunil\setups\elasticsearch\ubantu\filebeat-7.6.1-amd64.deb e@localhost:/home/e/sunil
sudo dpkg -i filebeat-7.6.1-amd64.deb

systemctl stop elasticsearch.service
systemctl start elasticsearch.service

cd /etc/filebeat/modules.d
sudo mv apache.yml.disabledapache.yml
Edit apache.yml, add paths:
["/home/student/logs/access*"]["/home/student/logs/error*”]
systemctl start filebeat.service


sudo filebeat setup --dashboards

```


## sql
```
POST /_xpack/sql?format=txt
{
"query": "DESCRIBE movies"
}

```

```
POST /_sql?format=txt
{
"query": "SELECT title from movies where year<1920 order by year"
}

```

```

POST /_sql/translate?pretty
{
"query": "SELECT title from movies where year<1920 order by year"
}

```

```
 cd /usr/share/elasticsearch/
 sudo bin/elasticsearch-sql-cli
```


## running multiple nodes

Edit elasticsearch.yml
cd /etc/elasticsearch
vim elasticsearch.yml
```
cluster.name: cluster-movies
node.name: node-1
http.port: 9200	
cluster.initial_master_nodes: ["node-1", "node-2","node-3"]
node.max.local.storage.nodes=3
```

Copy entire elasticnode  folder. 
```
cd /etc
sudo cp -rp elasticsearch elasticsearch-node2
sudo cp -rp elasticsearch elasticsearch-node3
```


Update /etc/elasticsearch-node2/elasticsearch.yml
```
cluster.name: cluster-movies
node.name: node-2
http.port: 9201	
```

Update /etc/elasticsearch-node3/elasticsearch.yml
```
cluster.name: cluster-movies
node.name: node-3
http.port: 9202
```

Update configuration
```
cd :/usr/lib/systemd/system
cp elasticsearch.service elasticsearch-node2.service
cp elasticsearch.service elasticsearch-node3.service

vim elasticsearch-node2.service
	Environment=ES_PATH_CONF=/etc/elasticsearch-node2
	
vim elasticsearch-node3.service
	Environment=ES_PATH_CONF=/etc/elasticsearch-node3	
```