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
5. Once the docker container is up, run the flask backend service
``$python3 app.py --debug``
6. To shut down the server. Simply do Crtl+C


Connect to Weaviate DB and run Queries:
1. To test Weaviate DB connection:
``GET http://127.0.0.1:5000/check_client``
2. To 