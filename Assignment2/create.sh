docker build -t diasdra/audit:latest ./Audit
docker build -t diasdra/processor:latest ./Processor 
docker build -t diasdra/receiver:latest ./Receiver 
docker build -t diasdra/storage:latest ./Storage 
docker build -t diasdra/dashboard:latest ./dashboard-ui 
docker build -t diasdra/health:latest ./Health
 
docker push diasdra/audit:latest 
docker push diasdra/processor:latest 
docker push diasdra/receiver:latest 
docker push diasdra/storage:latest 
docker push diasdra/dashboard:latest
docker push diasdra/health:latest