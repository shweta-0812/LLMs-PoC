from flask import Flask, request, jsonify
from openai_func_call import function_calling
from langchain import simple_message_chain, simple_retrieval_chain, simple_conversation_retrival_chain
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

application = Flask(__name__)


@application.route("/")
def home():
    return 'Welcome'


# @application.route("/function_call", methods=['POST'])
@application.route("/function_call")
def function_call():
    # function_name = request.get_json()['func_name']
    # prompt_message = request.get_json()['prompt_message']
    # prompt_message = "What's the weather like in Boston?"

    # call open ai function call methods
    resp = function_calling(func_name="get_current_weather", prompt_message="What's the weather like in Boston?")
    return jsonify({'status': 'success'})


@application.route("/simple_message_chain", methods=['POST'])
def simple_message_chain():
    # template = "tell me a short joke about {topic}"
    # topic = "software engineer"
    template = request.get_json()['template']
    topic = request.get_json()['topic']
    response = simple_message_chain(template=template, topic=topic)
    return jsonify({'status': 'success', 'response': response})


@application.route("/simple_retrieval_chain", methods=['POST'])
def simple_retrieval_chain():
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    template_options = {
        'context': "",
        'question': ""
    }
    # template = request.get_json()['template']
    # template_options = request.get_json()['template_options']
    response = simple_retrieval_chain(template=template, template_options=template_options)
    return jsonify({'status': 'success', 'response': response})


@application.route("/simple_conversation_retrival_chain", methods=['POST'])
def simple_conversation_retrival_chain():
    # template = """Answer the question based only on the following context:
    # {context}
    #
    # Question: {question}
    # """
    # template_options = {
    #     'context': "",
    #     'question': ""
    # }
    template = request.get_json()['template']
    template_options = request.get_json()['template_options']
    response = simple_conversation_retrival_chain(template=template, template_options=template_options)
    return jsonify({'status': 'success', 'response': response})


if __name__ == '__main__':
    application.run(debug=True)
