# Usage

## 1. docker-compose up
```sh
admin@gw-mac flask-ddb-todoist % docker-compose up -d --build  
Creating network "flask-ddb-todoist_default" with the default driver
Building api
[+] Building 19.8s (10/10) FINISHED                                                                                                                        
 => [internal] load build definition from Dockerfile                                                                                                  0.0s
 => => transferring dockerfile: 561B                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9-alpine                                                                                  2.2s
 => [1/5] FROM docker.io/library/python:3.9-alpine@sha256:091e589aa641a59b10cc764bfc959a91b70003643f2aac91fd4fc0353f09dddf                            0.0s
 => [internal] load build context                                                                                                                     0.0s
 => => transferring context: 7.43kB                                                                                                                   0.0s
 => CACHED [2/5] WORKDIR /src                                                                                                                         0.0s
 => [3/5] COPY ./api ./                                                                                                                               0.0s
 => [4/5] RUN ls -la && sleep 10                                                                                                                     10.2s
 => [5/5] RUN pip install -r requirements.txt                                                                                                         7.1s 
 => exporting to image                                                                                                                                0.2s 
 => => exporting layers                                                                                                                               0.2s 
 => => writing image sha256:936546cfb58b1076c5e790235af721d345ee75ee8fed817e3908efd1d6b6eed8                                                          0.0s 
 => => naming to docker.io/library/flask-ddb-todoist_api                                                                                              0.0s 
                                                                                                                                                           
Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them                                                       
Building web
[+] Building 14.1s (10/10) FINISHED                                                                                                                        
 => [internal] load build definition from Dockerfile                                                                                                  0.0s
 => => transferring dockerfile: 561B                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                     0.0s
 => => transferring context: 2B                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9-alpine                                                                                  0.9s
 => [1/5] FROM docker.io/library/python:3.9-alpine@sha256:091e589aa641a59b10cc764bfc959a91b70003643f2aac91fd4fc0353f09dddf                            0.0s
 => [internal] load build context                                                                                                                     0.0s
 => => transferring context: 7.65kB                                                                                                                   0.0s
 => CACHED [2/5] WORKDIR /src                                                                                                                         0.0s
 => [3/5] COPY ./web ./                                                                                                                               0.0s
 => [4/5] RUN ls -la && sleep 10                                                                                                                     10.2s
 => [5/5] RUN pip install -r requirements.txt                                                                                                         2.9s
 => exporting to image                                                                                                                                0.1s 
 => => exporting layers                                                                                                                               0.1s 
 => => writing image sha256:21a8f527b360333cd1c87fd6e1041dd9108dae9d5fdc8a12787541ae38986a1c                                                          0.0s 
 => => naming to docker.io/library/flask-ddb-todoist_web                                                                                              0.0s 
                                                                                                                                                           
Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them                                                       
Creating dynamodb-local ... done
Creating web            ... done
Creating api            ... done
admin@gw-mac flask-ddb-todoist % 
admin@gw-mac flask-ddb-todoist % docker ps  
CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS          PORTS                                       NAMES
e59b4620e470   flask-ddb-todoist_api          "python app.py"          19 seconds ago   Up 17 seconds   0.0.0.0:5001->5001/tcp, :::5001->5001/tcp   api
fff5156c92fe   amazon/dynamodb-local:latest   "java -jar DynamoDBL…"   19 seconds ago   Up 18 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   dynamodb-local
421896f955f7   flask-ddb-todoist_web          "python app.py"          19 seconds ago   Up 18 seconds   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   web
admin@gw-mac flask-ddb-todoist % 
```


## 2. create dynamodb table
```sh
admin@gw-mac flask-ddb-todoist % curl -I http://localhost:8000
HTTP/1.1 400 Bad Request
Date: Fri, 17 Dec 2021 22:32:21 GMT
Content-Type: application/x-amz-json-1.0
x-amzn-RequestId: 6492649d-b3f2-4e79-9835-2088d1b17fae
Content-Length: 173
Server: Jetty(9.4.18.v20190429)

admin@gw-mac flask-ddb-todoist % 
admin@gw-mac flask-ddb-todoist % aws dynamodb list-tables --endpoint-url http://localhost:8000
{
    "TableNames": []
}
admin@gw-mac flask-ddb-todoist % 
admin@gw-mac flask-ddb-todoist % aws dynamodb create-table \
--table-name dev-tasks \
--attribute-definitions AttributeName=task_id,AttributeType=S \
--key-schema AttributeName=task_id,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
--endpoint-url http://localhost:8000
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "task_id",
                "AttributeType": "S"
            }
        ],
        "TableName": "dev-tasks",
        "KeySchema": [
            {
                "AttributeName": "task_id",
                "KeyType": "HASH"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": "2021-12-18T06:26:08.119000+09:00",
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": "1970-01-01T09:00:00+09:00",
            "LastDecreaseDateTime": "1970-01-01T09:00:00+09:00",
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:ddblocal:000000000000:table/dev-tasks"
    }
}
admin@gw-mac flask-ddb-todoist % 
admin@gw-mac flask-ddb-todoist % aws dynamodb list-tables --endpoint-url http://localhost:8000
{
    "TableNames": [
        "dev-tasks"
    ]
}
admin@gw-mac flask-ddb-todoist % 
```


## 3. docker-compose exec
```sh
admin@gw-mac flask-ddb-todoist % docker-compose exec api /bin/ash
/src # 
/src # apk add bind-tools curl
OK: 21 MiB in 47 packages
/src # 
/src # nslookup dynamodb-local
Server:         127.0.0.11
Address:        127.0.0.11#53

Non-authoritative answer:
Name:   dynamodb-local
Address: 192.168.0.3

/src # curl -I http://dynamodb-local:8000
HTTP/1.1 400 Bad Request
Date: Fri, 17 Dec 2021 22:35:27 GMT
Content-Type: application/x-amz-json-1.0
x-amzn-RequestId: 186e9f5b-4906-490d-b4a3-549328926ed8
Content-Length: 173
Server: Jetty(9.4.18.v20190429)

/src # 
admin@gw-mac flask-ddb-todoist % 
admin@gw-mac flask-ddb-todoist % docker-compose exec web /bin/ash
/src # 
/src # apk add bind-tools curl
OK: 21 MiB in 47 packages
/src # 
/src # nslookup api
Server:         127.0.0.11
Address:        127.0.0.11#53

Non-authoritative answer:
Name:   api
Address: 192.168.112.4

/src # 
/src # curl http://api:5001/tasks
[
  {
    "detail": "afdsafa", 
    "status": "WIP", 
    "task": "fdsaf", 
    "task_id": "0596559e-5920-40b2-9631-6c76e6c5b37c"
  }, 
  {
    "detail": "fsadfasfsadfasfs", 
    "status": "DONE", 
    "task": "fsdaf", 
    "task_id": "137f42f9-842a-401b-809c-c9456fd8405a"
  }, 
  {
    "detail": "aaa", 
    "status": "TODO", 
    "task": "testtask1", 
    "task_id": "04770f36-0b4d-4561-b6eb-554a26195903"
  }
]
/src # exit
admin@gw-mac flask-ddb-todoist % 
```