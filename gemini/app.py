import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from utils import get_api_key

application = Flask(__name__)

load_dotenv()

GOOGLE_API_KEY = get_api_key('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


@application.route("/")
def home():
    return 'Welcome'


@application.route("/prompt", methods=['POST'])
def prompt():
    prompt_text = request.get_json()['prompt']
    # genai.configure(api_key=GOOGLE_API_KEY)
    # for m in genai.list_models():
    #     if 'generateContent' in m.supported_generation_methods:
    #         print(m.name)

    model = genai.GenerativeModel('gemini-pro')

    # response = model.generate_content("What is the meaning of life?", stream=True)
    #
    # for chunk in response:
    #     print(chunk.text)
    #     print("_" * 80)

    response = model.generate_content(prompt_text)
    return jsonify({'status': 'success', 'response': str(response.text)})


# TODO: needs an chat ID implementation for each chat conversation to map to corresponding history
# @application.route("/chat", methods=['POST'])
# def chat():
#     message = request.get_json()['message'] # string
#     chat_history = request.get_json()['chat_history'] # array
#
#     model = genai.GenerativeModel('gemini-pro')
#     chat = model.start_chat(history=chat_history)
#
#     # response = chat.send_message(message)
#
#     # for message in chat.history:
#     #     print(f'**{message.role}**: {message.parts[0].text}'))
#
#     return jsonify({'status': 'success', 'response': chat.history})


@application.route("/gen_embeddings", methods=['POST'])
def gen_embeddings():
    content = request.get_json()['content']
    # Note: The retrieval_document task type is the only task that accepts a title.
    title = request.get_json()['title']

    model = "models/embedding-001"
    result = genai.embed_content(
        model=model,
        content=content,
        task_type="retrieval_document",
        title=title)

    # 1 input > 1 vector output
    return jsonify({'status': 'success', 'embeddings': result['embedding'][:100]})


# TODO: needs an action button to upload image from UI
# @application.route("/img2txt")
# def img2txt():
#     pass


if __name__ == '__main__':
    application.run(debug=True)
