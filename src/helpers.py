import requests
import re

from src.openai import OpenAI


def download_image(url, file_path):
    """
    Download an image from a URL and save it locally.

    :param url: str, The URL of the image to download.
    :param file_path: str, The local file path where the image will be saved.
    """
    # Send a HTTP request to the URL of the image.
    response = requests.get(url, stream=True)

    # Check if the request was successful.
    if response.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        response.raw.decode_content = True

        # Open a local file with wb (write binary) permission and write the content.
        with open(file_path, 'wb') as file:
            file.write(response.content)

            print(f"Image successfully downloaded: {file_path}")
    else:
        print(f"Error downloading image: {response.status_code}")

    return response.content


def generate_image(prompt, nb_images=1, size="512x512", response_format="url"):
    """
    Generate an image using Dall-E.

    :param prompt: str, The prompt to generate an image from. Can be any text.
    :param nb_images: int, The number of images to generate. Can be either 1, 2, 3, or 4.
    :param size: str, The size of the image to generate. Can be either '256x256', '512x512', or '1024x1024'.
    :param response_format: str, The format of the response. Can be either 'url' or 'b64_json'.
    """
    response = OpenAI().get_image(prompt, nb_images, size, response_format)

    return response


def generate_text(prompt, max_tokens=100, nb_choices=1, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None, stream=None):
    """
    Generate text using GPT-3.5.

    :param prompt: str, The prompt to generate text from. Can be any text.
    :param max_tokens: int, The maximum number of tokens to generate. Can be between 1 and 2048.
    :param nb_choices: int, The number of choices to generate. Can be between 1 and 8.
    :param temperature: float, The temperature to use for generation. Can be between 0 and 1.
    :param top_p: float, The top p value to use for generation. Can be between 0 and 1.
    :param frequency_penalty: float, The frequency penalty to use for generation. Can be between 0 and 1.
    :param presence_penalty: float, The presence penalty to use for generation. Can be between 0 and 1.
    :param stop: str, The stop sequence to use for generation. Can be any text.
    :param stream: bool, Whether to stream the response or not. Can be either true or false.
    """
    response = OpenAI().get_legacy_completion(prompt, OpenAI.MODEL_BABBAGE, max_tokens, nb_choices, temperature, top_p, frequency_penalty, presence_penalty, stop, stream)

    return response


def generate_chat(messages: list, model: str = OpenAI.MODEL_GPT_35_TURBO, max_tokens=1000, nb_choices=1, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None, stream=None, function_call=None, functions=None):
    """
    Generate a chat using the chat API.

    :param messages: list, The messages to use for chat. Can be any text.
    :param model: str, The model to use for chat. Can be any model from OpenAI.MODEL_*.
    :param max_tokens: int, The maximum number of tokens to generate. Can be between 1 and 2048.
    :param nb_choices: int, The number of choices to generate. Can be between 1 and 8.
    :param temperature: float, The temperature to use for generation. Can be between 0 and 1.
    :param top_p: float, The top p value to use for generation. Can be between 0 and 1.
    :param frequency_penalty: float, The frequency penalty to use for generation. Can be between 0 and 1.
    :param presence_penalty: float, The presence penalty to use for generation. Can be between 0 and 1.
    :param stop: str, The stop sequence to use for generation. Can be any text.
    :param stream: bool, Whether to stream the response or not. Can be either true or false.
    :param function_call: str, The function call to use for generation. Can be either 'auto' or 'none'.
    :param functions: list, The functions to use for generation. Can be any function from OpenAI.FUNCTION_*.
    """
    response = OpenAI().get_chat_completion(messages, model, max_tokens, nb_choices, temperature, top_p, frequency_penalty, presence_penalty, stop, stream, function_call, functions)

    return response


def slugfy(text):
    """
    Slugify a text.

    :param text: str, The text to slugify.
    """
    # Convert the text to lowercase.
    text = text.lower()

    # Replace all non-alphanumeric characters with a hyphen.
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text)

    # Remove any leading or trailing hyphens.
    text = text.strip("-")

    return text


def remove_html_tags(input_string):
    clean_text = re.sub(r'<.*?>', '', input_string)
    return clean_text
