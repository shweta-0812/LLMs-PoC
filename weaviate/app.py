from flask import Flask, jsonify

from weaviate_app import create_weaviate_client

application = Flask(__name__)


@application.route("/")
def home():
    client_meta_data = create_weaviate_client()
    return jsonify({'status': 'success', 'weaviate': client_meta_data})


if __name__ == '__main__':
    application.run(debug=True)
