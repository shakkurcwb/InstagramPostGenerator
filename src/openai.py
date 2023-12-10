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

    def get_chat_completion(self, messages, model, max_tokens=1000, nb_choices=1, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None, stream=None, function_call=None, functions=None):
        response = self.openai.ChatCompletion.create(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            n=nb_choices,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            stream=stream,
            # function_call=function_call,
            # functions=functions,
        )

        return response

    def get_legacy_completion(self, prompt, model, max_tokens=5, nb_choices=1, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None, stream=None):
        response = self.openai.Completion.create(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            n=nb_choices,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            stream=stream,
        )

        return response

    def get_image(self, prompt, nb_images=1, size="512x512", response_format="url"):
        response = self.openai.Image.create(
            prompt=prompt,
            n=nb_images,
            size=size,
            response_format=response_format,
        )

        return response
