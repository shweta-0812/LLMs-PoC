How to use Langchain wrapper to execute queries to OpenAI.


1. go to the langchain dir
``$cd langchain``
2. [Optional] since langchain is written in flask, if you want to run it inside a python virtualenv then you can do the following:
``$pip3 install virtualenv``
``$virtualenv langchain_venv``
``$source langchain_venv/bin/activate``
and remember to run
``$deactivate`` after you have shutdown the flask backend server. 
3. run pip install for requirements.
``$pip3 install -r requirements.txt``
4. create a `.env` file inside the current dir and add the following env vars
  - OPENAI_API_BASE=<your-val>
  - OPENAI_API_KEY=<your-val>
  - TAVILY_SEARCH_API_KEY=<your-val>

5.Once the docker container is up, run the flask backend service
``$python3 app.py --debug``
6.To shut down the server. Simply do Crtl+C


Finally:
1. Check connection:
``GET http://127.0.0.1:5000/``
2. To run different methods, you can initiate the corresponding REST API endpoints for the same.