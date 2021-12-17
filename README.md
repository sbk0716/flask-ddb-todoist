# flask-on-docker

## create table
```sh
admin@gw-mac flask-on-docker % docker ps 
CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS          PORTS                                       NAMES
db9ca4b52ab8   flask-on-docker_api            "python app.py"          55 seconds ago   Up 54 seconds   0.0.0.0:5001->5001/tcp, :::5001->5001/tcp   api
dfbb39a2d9bd   flask-on-docker_web            "python app.py"          55 seconds ago   Up 54 seconds   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   web
421dfeba1d52   amazon/dynamodb-local:latest   "java -jar DynamoDBL…"   55 seconds ago   Up 54 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   dynamodb-local
admin@gw-mac flask-on-docker % 
admin@gw-mac flask-on-docker % aws dynamodb list-tables --endpoint-url http://localhost:8000
{
    "TableNames": []
}
admin@gw-mac flask-on-docker % 
admin@gw-mac flask-on-docker % aws dynamodb create-table \
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
admin@gw-mac flask-on-docker % 
admin@gw-mac flask-on-docker % aws dynamodb list-tables --endpoint-url http://localhost:8000                    
{
    "TableNames": [
        "dev-tasks"
    ]
}
admin@gw-mac flask-on-docker % 
admin@gw-mac flask-on-docker % docker-compose exec api /bin/ash
/src # apk add bind-tools
OK: 21 MiB in 47 packages
/src # nslookup dynamodb-local
Server:         127.0.0.11
Address:        127.0.0.11#53

Non-authoritative answer:
Name:   dynamodb-local
Address: 192.168.0.3

/src # dig dynamodb-local

; <<>> DiG 9.16.22 <<>> dynamodb-local
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40665
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;dynamodb-local.                        IN      A

;; ANSWER SECTION:
dynamodb-local.         600     IN      A       192.168.0.3

;; Query time: 2 msec
;; SERVER: 127.0.0.11#53(127.0.0.11)
;; WHEN: Fri Dec 17 21:29:58 UTC 2021
;; MSG SIZE  rcvd: 62

/src # exit
admin@gw-mac flask-on-docker % 
```