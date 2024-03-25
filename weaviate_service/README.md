How to run Weaviate Vector DB.

Pre-requisite: Make sure you have docker-desktop installed.

1. go to the weaviate_service dir
``$cd weaviate_service``
2. [Optional] since weaviate_service is written in flask, if you want to run it inside a python virtualenv then you can do the following:
``$pip3 install virtualenv``
``$virtualenv weaviate_venv``
``$source weaviate_venv/bin/activate``
and remember to run
``$deactivate`` after you have shutdown the flask backend server. 
3. run pip install for requirements.
``$pip3 install -r requirements.txt``
4. Now run ``$docker-compose -p my-weaviate-db up -d`` to run weaviate DB in background inside a docker container. 
5. create a `.env` file inside the current dir and add the following env vars
   - WEAVIATE_DB_HOST=0.0.0.0
   - WEAVIATE_DB_PORT=8080
   - WEAVIATE_DB_HTTP_SECURE=False
   - WEAVIATE_DB_GRPC_HOST=localhost
   - WEAVIATE_DB_GRPC_PORT=50051
   - WEAVIATE_DB_GRPC_SECURE=False
   - WEAVIATE_API_KEY=shweta-secret-key
   - OPENAI_API_BASE=<your-val>
   - OPENAI_API_KEY=<your-val>
   - COHERE_API_KEY=<your-val>
   - COHERE_API_BASE=<your-val>
6. Once the docker container is up, run the flask backend service
``$python3 app.py --debug``
7. To shut down the server. Simply do Crtl+C


Connect to Weaviate DB and run Queries:
1. To test Weaviate DB connection:
``GET http://127.0.0.1:5000/check_client``
2. To run different methods, you can initiate the corresponding REST API endpoints for the same.