import requests
import re


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
