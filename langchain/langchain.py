from utils import get_api_key

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

from langchain_core.messages import HumanMessage, AIMessage

from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults

TAVILY_SEARCH_API_KEY = get_api_key('TAVILY_SEARCH_API_KEY')
SEARCH_TOOL = TavilySearchResults()

OPENAI_API_KEY = get_api_key('OPENAI_API_KEY')
MODEL = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

'''Simple language chain'''


def simple_template_chain(template, topic):
    # template = """Answer the question based only on the following context:
    # {context}
    #
    # Question: {question}
    # """
    prompt = ChatPromptTemplate.from_template(template=template)

    # The output of a ChatModel is a message. it's more convenient to work with strings.so add a simple output parser
    # to convert the chat message to a string.
    output_parser = StrOutputParser()

    # create a simple chain using '|'
    chain = prompt | MODEL | output_parser

    # We can now invoke a chain and ask a question to llm
    return chain.invoke({"topic": topic})


def simple_message_chain(messages, topic):
    # messages = [
    #     ("system", "You are world class technical documentation writer."),
    #     ("user", "{input}")
    # ]
    prompt = ChatPromptTemplate.from_messages(messages)
    output_parser = StrOutputParser()

    chain = prompt | MODEL | output_parser
    # call the chain
    return chain.invoke({"input": "how can langsmith help with testing?"})


def load_sample_docs_to_vectorspace(docs=None):
    if docs is None:
        # we use beautifulsoup to crawl a sample webpage to store in our vector dB
        loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
        docs = loader.load()

    # initialise embeddings model to generate text embeddings
    embeddings = OpenAIEmbeddings()

    # use embedding model to ingest document text embeddings into a FAISS vectorstore
    # build index
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

    # load to vector space
    vector = FAISS.from_documents(documents, embeddings)
    return vector


'''Complex chains: llm answer using context via retrieval A Retriever can be backed by anything - a SQL table, 
the internet, etc - but in this instance we will populate a vector store and use that as a retriever.
'''


def simple_retrieval_chain():
    # create a prompt from template
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

    # Method 1:
    document_chain = create_stuff_documents_chain(MODEL, prompt)

    # incase of specified context as part of prompt
    response_1 = document_chain.invoke({
        "input": "how can langsmith help with testing?",
        "context": [Document(page_content="langsmith can let you visualize test results")]
    })
    print(response_1["answer"])

    # Method 2:
    # incase of dynamic selection of relevant docs from the vectordb
    vector = load_sample_docs_to_vectorspace()
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response_2 = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
    print(response_2["answer"])


'''Use case: LLM for chat bots The retrieval method takes the whole history of chat into account when responding to a 
prompt The final LLM chain likewise takes the whole history into account. This chain will take in the most recent 
input (input) and the conversation history (chat_history) and use an LLM to generate a search query. '''


def simple_conversation_retrival_chain():
    vector = load_sample_docs_to_vectorspace()
    retriever = vector.as_retriever()

    # First we need a prompt that we can pass into an LLM to generate this search query

    # case 1
    prompt_1 = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information "
                 "relevant to the conversation")
    ])

    retriever_chain = create_history_aware_retriever(MODEL, retriever, prompt_1)

    # generate synthetic history
    chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]

    # add history to chain for giving context
    response_1 = retriever_chain.invoke({
        "chat_history": chat_history,
        "input": "Tell me how"
    })

    print(response_1)

    # case 2:
    prompt_2 = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])

    document_chain = create_stuff_documents_chain(MODEL, prompt_2)
    retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

    chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
    response_2 = retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": "Tell me how"
    })
    print(response_2)


'''
    An agent - the LLM decides what steps to take based on query
    when building an agent we need to decide what tools it should have access to
    For this simple agent, we will give the agent access to two tools:

    1. A vector db retriever.
    2. A search tool - The search tool that we will use is Tavily.
'''
def simple_llm_agent():
    vector = load_sample_docs_to_vectorspace()
    retriever = vector.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "langsmith_search",
        "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
    )

    tools = [retriever_tool, SEARCH_TOOL]


# Retrieval Augmentation Generation