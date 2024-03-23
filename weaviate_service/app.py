from flask import Flask, jsonify

from db.weaviate_client import create_weaviate_client, create_db_collection, reset_db_collection, load_sample_data

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


@application.route("/sample_data")
def sample_data():
    count = load_sample_data(schema_name='questions')
    return jsonify({'status': 'success', 'data_count': count})


if __name__ == '__main__':
    application.run(debug=True)
