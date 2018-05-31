#/bin/bash

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":1,"method":"invoke_person","params":{"key":"1"}}' http://localhost:9000/api/v1/transactions
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":2,"method":"invoke_person","params":{"key":"2"}}' http://localhost:9000/api/v1/transactions

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"3","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"4","method":"query_person","params":{"key":"2"}}' http://localhost:9000/api/v1/query

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"5","method":"invoke_purchase_token","params":{"key":"1","purchase_token":"10"}}' http://localhost:9000/api/v1/transactions
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"6","method":"invoke_purchase_token","params":{"key":"2","purchase_token":"20"}}' http://localhost:9000/api/v1/transactions

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"3","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"4","method":"query_person","params":{"key":"2"}}' http://localhost:9000/api/v1/query

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"5","method":"invoke_spend_token","params":{"key":"1","spending_amount":"5"}}' http://localhost:9000/api/v1/transactions
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"6","method":"invoke_spend_token","params":{"key":"2","spending_amount":"10"}}' http://localhost:9000/api/v1/transactions

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"3","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"4","method":"query_person","params":{"key":"2"}}' http://localhost:9000/api/v1/query

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"5","method":"invoke_contract","params":{"key":"c1","value":{"farmer":"1","location":"seoul","reward":3,"citizen":"2","when":"18/6/1","uptime":"now","fulfillment":"yet"}}}' http://localhost:9000/api/v1/transactions

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"1","method":"query_contract","params":{"key":"c1"}}' http://localhost:9000/api/v1/query
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"3","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"5","method":"invoke_cancel","params":{"key":"c1","value":{"who":"1","why":"no reason","uptime":"tomorrow"}}}' http://localhost:9000/api/v1/transactions

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"1","method":"query_contract","params":{"key":"c1"}}' http://localhost:9000/api/v1/query
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"3","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"0","method":"invoke_contract","params":{"key":"c2","value":{"farmer":"1","location":"seoul","reward":3,"citizen":"2","when":"18/6/1","uptime":"now","fulfillment":"yet"}}}' http://localhost:9000/api/v1/transactions


curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"8","method":"invoke_done","params":{"key":"c1","value":{"starting_time":"9:00","end_time": "18:00"}}}' http://localhost:9000/api/v1/transactions

curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"1","method":"query_contract","params":{"key":"c2"}}' http://localhost:9000/api/v1/query
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"2","method":"query_person","params":{"key":"1"}}' http://localhost:9000/api/v1/query
curl -H "Content-Type: application/json" -X POST -d '{"jsonrpc":"2.0","id":"3","method":"query_person","params":{"key":"2"}}' http://localhost:9000/api/v1/query
