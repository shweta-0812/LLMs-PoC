from flask import Flask, request, jsonify
from openai_func_call import function_calling
from langchain import simple_chain, simple_doc_retriever, complex_chain

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


@application.route("/simple_chain", methods=['POST'])
def simple_chain():
    # template = "tell me a short joke about {topic}"
    # topic = "software engineer"
    template = request.get_json()['template']
    topic = request.get_json()['topic']
    response = simple_chain(template=template, topic=topic)
    return jsonify({'status': 'success', 'response': response})


@application.route("/simple_doc_retriever", methods=['POST'])
def simple_doc_retriever():
    # doc = ["harrison worked at kensho", "bears like to eat honey"]
    # queries = ["where did harrison work?", "what do bears like to eat"]
    doc = request.get_json()['doc']
    queries = request.get_json()['topic']

    relevant_docs = simple_doc_retriever(doc=doc, queries=queries)
    return jsonify({'status': 'success', 'response': relevant_docs})


@application.route("/complex_chain", methods=['POST'])
def complex_chain():
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
    response = complex_chain(template=template, template_options=template_options)
    return jsonify({'status': 'success', 'response': response})


if __name__ == '__main__':
    application.run(debug=True)
