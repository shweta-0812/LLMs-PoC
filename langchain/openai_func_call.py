from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv
from utils import get_api_key

_ = load_dotenv(find_dotenv())  # read local .env file

OPENAI_API_KEY = get_api_key('OPENAI_API_KEY')

MODEL = "gpt-3.5-turbo-0613"

client = OpenAI(api_key=OPENAI_API_KEY)


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def get_function_details_from_function_name(func_name):
    match func_name:
        case "get_current_weather":
            func_details = [
                {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                }
            ]
            return func_details
        case 1:
            return "one"
        case _:  # default
            return "nothing"


def get_message_template():
    message_template = [
        {
            "role": "user"
        }
    ]
    return message_template


def call_openai_chat_complete(messages, functions=None, function_call=None):
    if functions is None and function_call is None:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
    elif functions and function_call is None:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            functions=functions,
        )
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            functions=functions,
            function_call=function_call,
        )
    return response


def function_calling(func_name, prompt_message):
    functions = get_function_details_from_function_name(func_name=func_name)

    # 1.
    messages = get_message_template()
    messages[0]["content"] = prompt_message

    response = call_openai_chat_complete(messages=messages, functions=functions)
    print(response)

    # response =>
    # {
    #     "id": "chatcmpl-94oSK9u0CxeXKwGIwLiolrMWKNDV6",
    #     "object": "chat.completion",
    #     "created": 1710934292,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": null,
    #                 "function_call": {
    #                     "name": "get_current_weather",
    #                     "arguments": "{\n\"location\": \"Boston, MA\"\n}"
    #                 }
    #             },
    #             "logprobs": null,
    #             "finish_reason": "function_call"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 82,
    #         "completion_tokens": 17,
    #         "total_tokens": 99
    #     },
    #     "system_fingerprint": null
    # }

    response_message = response["choices"][0]["message"]
    print(response_message)

    # response_message =>
    # < OpenAIObject at 0x7f1c045a9c70 > JSON: {
    #     "role": "assistant",
    #     "content": null,
    #     "function_call": {
    #         "name": "get_current_weather",
    #         "arguments": "{\n\"location\": \"Boston, MA\"\n}"
    #     }
    # }

    print(response_message["content"])
    # response_message["content"] =>
    # null

    print(response_message["function_call"])
    # response_message["function_call"] =>
    # < OpenAIObject at 0x7f1c045b1c70 > JSON: {
    #     "name": "get_current_weather",
    #     "arguments": "{\n\"location\": \"Boston, MA\"\n}"
    # }

    args = json.loads(response_message["function_call"]["arguments"])
    print(args)

    # args =>
    # {'location': 'Boston, MA'}

    resp = get_current_weather(args)
    print(resp)

    # resp =>
    # '{"location": {"location": "Boston, MA"}, "temperature": "72", "unit": "fahrenheit", "forecast": ["sunny", "windy"]}'

    # 2.
    messages = get_message_template()
    messages[0]["content"] = "hi!"

    response = call_openai_chat_complete(messages=messages, functions=functions)
    print(response)

    # response =>
    # {
    #     "id": "chatcmpl-94oSK9mFEhxvQhf2HRMVxVBlusxRh",
    #     "object": "chat.completion",
    #     "created": 1710934292,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": "Hello! How can I assist you today?"
    #             },
    #             "logprobs": null,
    #             "finish_reason": "stop"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 76,
    #         "completion_tokens": 10,
    #         "total_tokens": 86
    #     },
    #     "system_fingerprint": null
    # }


    # 3.
    messages = get_message_template()
    messages[0]["content"] = "hi!"

    response = call_openai_chat_complete(messages=messages, functions=functions, function_call="auto")
    print(response)

    # response =>
    # {
    #     "id": "chatcmpl-94oSLTAoYigtUetmGbgTnuBpG0v7l",
    #     "object": "chat.completion",
    #     "created": 1710934293,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": "Hello! How can I assist you today?"
    #             },
    #             "logprobs": null,
    #             "finish_reason": "stop"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 76,
    #         "completion_tokens": 10,
    #         "total_tokens": 86
    #     },
    #     "system_fingerprint": null
    # }

    # 4.
    messages = get_message_template()
    messages[0]["content"] = "hi!"

    response = call_openai_chat_complete(messages=messages, functions=functions, function_call="none")
    print(response)
    # response =>
    # {
    #     "id": "chatcmpl-94oSMhFAZwvp29zdxOZWe9Uef8tAU",
    #     "object": "chat.completion",
    #     "created": 1710934294,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": "Hello! How can I assist you today?"
    #             },
    #             "logprobs": null,
    #             "finish_reason": "stop"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 77,
    #         "completion_tokens": 9,
    #         "total_tokens": 86
    #     },
    #     "system_fingerprint": null
    # }

    # 5.
    messages = get_message_template()
    messages[0]["content"] = "What's the weather in Boston?"

    response = call_openai_chat_complete(messages=messages, functions=functions, function_call="none")
    print(response)
    # response =>
    # {
    #     "id": "chatcmpl-94oSM0Afo89FJY99OymE3DAbOTr2c",
    #     "object": "chat.completion",
    #     "created": 1710934294,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": "Let me check the current weather in Boston for you."
    #             },
    #             "logprobs": null,
    #             "finish_reason": "stop"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 82,
    #         "completion_tokens": 11,
    #         "total_tokens": 93
    #     },
    #     "system_fingerprint": null
    # }

    # 6.
    messages = get_message_template()
    messages[0]["content"] = "hi!"

    response = call_openai_chat_complete(messages=messages, functions=functions,
                                         function_call={"name": "get_current_weather"})
    print(response)
    # response =>
    # {
    #     "id": "chatcmpl-94oSN8OS83byTfxf6zF3grAQhWldd",
    #     "object": "chat.completion",
    #     "created": 1710934295,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": null,
    #                 "function_call": {
    #                     "name": "get_current_weather",
    #                     "arguments": "{\n  \"location\": \"San Francisco, CA\"\n}"
    #                 }
    #             },
    #             "logprobs": null,
    #             "finish_reason": "stop"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 83,
    #         "completion_tokens": 12,
    #         "total_tokens": 95
    #     },
    #     "system_fingerprint": null
    # }

    # 7.
    messages = get_message_template()
    messages[0]["content"] = "What's the weather like in Boston!"

    response = call_openai_chat_complete(messages=messages, functions=functions,
                                         function_call={"name": "get_current_weather"})
    print(response)
    # response =>
    # {
    #     "id": "chatcmpl-94oSOFBVICgdEbDE3DgEqOtoOqQIR",
    #     "object": "chat.completion",
    #     "created": 1710934296,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": null,
    #                 "function_call": {
    #                     "name": "get_current_weather",
    #                     "arguments": "{\n\"location\": \"Boston, MA\"\n}"
    #                 }
    #             },
    #             "logprobs": null,
    #             "finish_reason": "stop"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 89,
    #         "completion_tokens": 10,
    #         "total_tokens": 99
    #     },
    #     "system_fingerprint": null
    # }

    messages.append(response["choices"][0]["message"])
    args = json.loads(response["choices"][0]["message"]['function_call']['arguments'])

    observation = get_current_weather(args)

    messages.append(
        {
            "role": "function",
            "name": "get_current_weather",
            "content": observation,
        }
    )
    response = call_openai_chat_complete(messages=messages)
    print(response)

    # response =>
    # {
    #     "id": "chatcmpl-94oSOxdIvC3loqHW4ryGGZeGhCV5j",
    #     "object": "chat.completion",
    #     "created": 1710934296,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": "The current temperature in Boston, MA is 72 degrees Fahrenheit. It is sunny and windy."
    #             },
    #             "logprobs": null,
    #             "finish_reason": "stop"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 76,
    #         "completion_tokens": 19,
    #         "total_tokens": 95
    #     },
    #     "system_fingerprint": null
    # }

    return {'status': 'success'}
