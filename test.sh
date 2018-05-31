#/bin/bash

echo "invoke_person 1"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":11,"method":"invoke_person","params":{"key":"1"}}' http://localhost:9000/api/v1/transactions
echo "invoke_person 2"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":12,"method":"invoke_person","params":{"key":"2"}}' http://localhost:9000/api/v1/transactions
sleep 2

echo "query_person 1"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"13","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
echo "query_person 2"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"14","method":"query_person","params":{"key":"2"}}' http://localhost:9000/api/v1/query
sleep 2


echo "invoke_purchase_token person1 10"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"15","method":"invoke_purchase_token","params":{"key":"1","purchase_token":"10"}}' http://localhost:9000/api/v1/transactions
echo "invoke_purchase_token person2 20"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"16","method":"invoke_purchase_token","params":{"key":"2","purchase_token":"20"}}' http://localhost:9000/api/v1/transactions
sleep 2

echo "query_person 1"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"17","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
echo "query_person 2"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"18","method":"query_person","params":{"key":"2"}}' http://localhost:9000/api/v1/query
sleep 2

echo "invoke_spend_token person1 5"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"19","method":"invoke_spend_token","params":{"key":"1","spending_amount":"5"}}' http://localhost:9000/api/v1/transactions
echo "invoke_spend_token person2 10"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"20","method":"invoke_spend_token","params":{"key":"2","spending_amount":"10"}}' http://localhost:9000/api/v1/transactions
sleep 2

echo "query_person 1"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"21","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
echo "query_person 2"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"22","method":"query_person","params":{"key":"2"}}' http://localhost:9000/api/v1/query
sleep 2

echo "invoke_contract"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"23","method":"invoke_contract","params":{"key":"c1","value":{"farmer":"1","location":"seoul","reward":3,"citizen":"2","when":"18/6/1","uptime":"now","fulfillment":"yet"}}}' http://localhost:9000/api/v1/transactions
sleep 2

echo "query_contract"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"24","method":"query_contract","params":{"key":"c1"}}' http://localhost:9000/api/v1/query
echo "query_person"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"25","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
sleep 2

echo "invoke_cancel"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"26","method":"invoke_cancel","params":{"key":"c1","value":{"who":"1","why":"no reason","uptime":"tomorrow"}}}' http://localhost:9000/api/v1/transactions
sleep 2

echo "query_contract"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"27","method":"query_contract","params":{"key":"c1"}}' http://localhost:9000/api/v1/query
echo "query_person"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"28","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
sleep 2

echo "invoke_contract"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"29","method":"invoke_contract","params":{"key":"c2","value":{"farmer":"1","location":"seoul","reward":3,"citizen":"2","when":"18/6/1","uptime":"now","fulfillment":"yet"}}}' http://localhost:9000/api/v1/transactions
sleep 2


echo "invoke_done"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"30","method":"invoke_done","params":{"key":"c1","value":{"starting_time":"9:00","end_time": "18:00"}}}' http://localhost:9000/api/v1/transactions
sleep 2

echo "query_contract"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"31","method":"query_contract","params":{"key":"c2"}}' http://localhost:9000/api/v1/query
echo "query_person 1"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"32","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
echo "query_person 2"
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"33","method":"query_person","params":{"key":"2"}}' http://localhost:9000/api/v1/query
