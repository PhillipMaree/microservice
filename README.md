#### Author J.P Maree
#### 2022.02.21

#### Directory structure

	data	test data used for testing service
	doc	OpenAPI Spesification endpoint definition and documentation
	docker	All dockerfiles and cloud architecture building blocks
	src	Backend servers and functionality related to services


#### Getting started 

git clone https://github.com/PhillipMaree/microservice.git 

From the root directory of cloned repository  <./microservice>, run: 

    /docker/docker-compose build     // build microservice framework
    /docker/docker-compose up -d     // spins up services
    /docker/docker-compose down      // kills serivces
    
    
#### Microservice queries

[1.] Test health of API microservice by runnnig:

    curl "http://0.0.0.0:5999/health"
    
  
    
[2.] Upload data by running the followinf in the <./microservice/data> path:

    curl -d @data_batch0.json "http://0.0.0.0:5999/upload"
    
[3.] Run a query calculation

    curl "http://0.0.0.0:5999/example?id=1"
    
    or
    
    curl "http://0.0.0.0:5999/example?id=1&t0=XX&t1=YY"          // supply parameters on [XX,YY]
	

