from flask import Flask, jsonify

from db.weaviate_client import create_weaviate_client, create_db_collection, reset_db_collection, load_sample_data
from search.weaviate_search import search

application = Flask(__name__)


@application.route("/")
def home():
    return 'Welcome'


@application.route("/check_client")
def check_client():
    meta_data = create_weaviate_client()
    return jsonify({'status': 'success', 'meta_data': meta_data})


@application.route("/create_db_schema")
def create_db_schema():
    response = create_db_collection(schema_name='questions')
    return jsonify({'status': 'success', 'response': response})


@application.route("/reset_db_schema")
def reset_db_schema():
    response = reset_db_collection(schema_name='questions')
    return jsonify({'status': 'success', 'response': response})


@application.route("/load_sample_data")
def load_sample_data():
    count = load_sample_data(schema_name='questions')
    return jsonify({'status': 'success', 'data_count': count})


@application.route("/search", methods=['POST'])
def search():
    schema_name = "questions"
    properties = ["question", "answer"]
    # query = "animal"
    query = {"concepts": ["animal"]}
    search_type = 'dense'
    limit = 1
    # schema_name = request.get_json()['schema_name']
    # properties = request.get_json()['properties']
    # query = request.get_json()['query']
    # alpha = request.get_json()['alpha']
    # search_type = request.get_json()['search_type']
    # limit = request.get_json()['limit']

    response = search(schema_name=schema_name, properties=properties, query=query, search_type=search_type, limit=limit)
    return jsonify({'status': 'success', 'response': response})


if __name__ == '__main__':
    application.run(debug=True)
