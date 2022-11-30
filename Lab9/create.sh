docker build -t diasdra/audit:latest ./"Audit"
docker build -t diasdra/processor:latest ./"Processor"
docker build -t diasdra/receiver:latest ./"Reciever"
docker build -t diasdra/storage:latest ./"Storage"

docker push diasdra/audit:latest
docker push diasdra/processor:latest
docker push diasdra/receiver:latest 
docker push diasdra/storage:latest 
