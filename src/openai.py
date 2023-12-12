import openai

# inject api key globally
openai.api_key = "OPEN_AI_API_KEY_HERE"


class OpenAI:
    openai = None

    MODEL_ADA = "ada"
    MODEL_BABBAGE = "babbage"
    MODEL_CURIE = "curie"
    MODEL_DAVINCI = "davinci"
    MODEL_GPT_4 = "gpt-4"
    MODEL_GPT_4_32K = "gpt-4-32k"
    MODEL_GPT_35_TURBO = "gpt-3.5-turbo"
    MODEL_GPT_35_TURBO_16K = "gpt-3.5-turbo-16k"
    MODEL_BABBAGE_002 = "babbage-002"
    MODEL_DAVINCI_002 = "davinci-002"

    MODELS = [
        MODEL_ADA,
        MODEL_BABBAGE,
        MODEL_CURIE,
        MODEL_DAVINCI,
        MODEL_GPT_4,
        MODEL_GPT_4_32K,
        MODEL_GPT_35_TURBO,
        MODEL_GPT_35_TURBO_16K,
        MODEL_BABBAGE_002,
        MODEL_DAVINCI_002,
    ]

    def __init__(self, api_key = None):
        self.openai = openai

        if api_key:
            self.openai.api_key = api_key

        if not self.openai.api_key:
            raise Exception("OpenAI API key not found.")

    def get_chat_completion(self, messages, model, max_tokens=1000, nb_choices=1, temperature=0.5, **kwargs):
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
        :return: dict, The response from the API.
        """
        return self.openai.ChatCompletion.create(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            n=nb_choices,
            temperature=temperature,
            **kwargs,
        )

    def get_text_completion(self, prompt, model, max_tokens=5, nb_choices=1, temperature=0.5, **kwargs):
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
        :return: dict, The response from the API.
        """
        return self.openai.Completion.create(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            n=nb_choices,
            temperature=temperature,
            **kwargs,
        )

    def get_image(self, prompt, nb_images=1, size="512x512", response_format="url"):
        """
        Generate an image using Dall-E.
        :param prompt: str, The prompt to generate an image from. Can be any text.
        :param nb_images: int, The number of images to generate. Can be either 1, 2, 3, or 4.
        :param size: str, The size of the image to generate. Can be either '256x256', '512x512', or '1024x1024'.
        :param response_format: str, The format of the response. Can be either 'url' or 'b64_json'.
        :return: dict, The response from the API.
        """
        return self.openai.Image.create(
            prompt=prompt,
            n=nb_images,
            size=size,
            response_format=response_format,
        )
