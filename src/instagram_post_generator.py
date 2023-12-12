import textwrap
import json

from pathlib import Path
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from src.helpers import slugfy
from src.openai import OpenAI


ROBOTO_FONT = "fonts/Roboto-Regular.ttf"

ROBOTO_24 = ImageFont.truetype(ROBOTO_FONT, 24)
ROBOTO_32 = ImageFont.truetype(ROBOTO_FONT, 32)
ROBOTO_64 = ImageFont.truetype(ROBOTO_FONT, 64)

INSTAGRAM_POST_WIDTH = 1080
INSTAGRAM_POST_HEIGHT = 1080

SPACING = 50

LAYOUTS = {
    'head_body_footer': {
        'head': {
            'x1': SPACING,
            'y1': SPACING,
            'x2': INSTAGRAM_POST_HEIGHT - SPACING,
            'y2': SPACING * 5,
            'text': 'Head',
            'font': ROBOTO_64,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
        'body': {
            'x1': SPACING,
            'y1': SPACING * 7,
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - (SPACING * 7),
            'text': 'Body',
            'font': ROBOTO_32,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
        'footer': {
            'x1': SPACING,
            'y1': INSTAGRAM_POST_HEIGHT - (SPACING * 5),
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - SPACING,
            'text': 'Footer',
            'font': ROBOTO_32,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
    },
    'head_body': {
        'head': {
            'x1': SPACING,
            'y1': SPACING,
            'x2': INSTAGRAM_POST_HEIGHT - SPACING,
            'y2': SPACING * 5,
            'text': 'Head',
            'font': ROBOTO_64,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
        'body': {
            'x1': SPACING,
            'y1': SPACING * 7,
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - SPACING,
            'text': 'Body',
            'font': ROBOTO_32,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
    },
    'title_text_image': {
        'title': {
            'x1': SPACING,
            'y1': SPACING,
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': SPACING * 5,
            'text': 'Title',
            'font': ROBOTO_64,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
        'text': {
            'x1': SPACING,
            'y1': SPACING * 7,
            'x2': INSTAGRAM_POST_WIDTH // 2 - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - SPACING,
            'text': 'Text',
            'font': ROBOTO_32,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
        'image': {
            'x1': INSTAGRAM_POST_WIDTH // 2 + SPACING,
            'y1': SPACING * 7,
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - SPACING,
            'image_path': 'output/test.png',
            'border_color': 'black',
            'border_width': 5,
        },
    },
    'title_text1_text2': {
        'title': {
            'x1': SPACING,
            'y1': SPACING,
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': SPACING * 5,
            'text': 'Title',
            'font': ROBOTO_64,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
        'text1': {
            'x1': SPACING,
            'y1': SPACING * 7,
            'x2': INSTAGRAM_POST_WIDTH // 2 - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - SPACING,
            'text': 'Text1',
            'font': ROBOTO_32,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
        'text2': {
            'x1': INSTAGRAM_POST_WIDTH // 2 + SPACING,
            'y1': SPACING * 7,
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - SPACING,
            'text': 'Text2',
            'font': ROBOTO_32,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 5,
        },
    },
}


class ImageGenerator:
    def __init__(self, width: int, height: int, color: str = "white"):
        self._image = Image.new("RGB", (width, height), color)
        self._draw = ImageDraw.Draw(self.image)

    @property
    def image(self):
        return self._image

    @property
    def draw(self):
        return self._draw

    def save(self, filename: str):
        self.image.save(filename)


class Box:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, border_color: str = "black", border_width: int = 1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.outline = border_color
        self.width = border_width

    def draw(self, draw: ImageDraw):
        draw.rectangle([(self.x1, self.y1), (self.x2, self.y2)], outline=self.outline, width=self.width)


class TextBox:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, text: str, text_color: str = "black", font: ImageFont = None, wrapped_lines: bool = True, border_color: str = "white", border_width: int = 1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.outline = border_color
        self.width = border_width

        self.text = text
        self.color = text_color
        self.font = font
        self.wrapped_lines = wrapped_lines

    def draw(self, draw: ImageDraw):
        draw.rectangle([(self.x1, self.y1), (self.x2, self.y2)], outline=self.outline, width=self.width)

        if not self.wrapped_lines:
            draw.text((self.x1 + SPACING, self.y1 + SPACING), self.text, fill=self.color, font=self.font)
            return

        # Split the text into lines that fit within the specified max_width in pixels
        lines = textwrap.wrap(self.text, width=self._wrap_text(draw))

        current_y = self.y1 + SPACING
        for line in lines:
            draw.text((self.x1 + SPACING, current_y), line, fill=self.color, font=self.font)
            current_y += SPACING

    def _wrap_text(self, draw: ImageDraw):
        words = self.text.split()
        wrapped_lines = []
        line = words[0]

        for word in words[1:]:
            test_line = line + ' ' + word
            if draw.textlength(test_line, font=self.font) <= self.x2 - self.x1 - SPACING * 2:
                line = test_line
            else:
                wrapped_lines.append(line)
                line = word

        wrapped_lines.append(line)
        return len(max(wrapped_lines, key=len))


class ImageBox:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, image_path: str, border_color: str = "black", border_width: int = 1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.image_path = image_path
        self.image = Image.open(self.image_path)

        self.outline = border_color
        self.width = border_width

    def draw(self, draw: ImageDraw, image: Image):
        draw.rectangle([(self.x1, self.y1), (self.x2, self.y2)], outline=self.outline, width=self.width)

        resized_image = self.image.resize((self.x2 - self.x1, self.y2 - self.y1))

        image.paste(resized_image, (self.x1, self.y1))


class InstagramPostGenerator:
    BUSINESS_MODEL = "cannabis educator instagram page"

    SYSTEM_PROMPT = [
        "You are responsible for the social media marketing of a {}.".format(BUSINESS_MODEL),
        "You are tasked with creating a post that will be shared on the page.",
        "The post should be informative and engaging.",
        "The post should be written in a professional tone.",
        "The post most contain a page with title and image, followed by 6 to 8 pages with title, text, image and a footer.",
        "Make sure to include references whenever necessary - this is educational content based on science or cerfied sources.",
        "Use the following example in order to format the response (JSON):",
        """
        {
            "first_page": {
                "image": "PLACEHOLDER - describe a prompt for Dall-E image here (specify art style, e.g. A vehicle with a flamingo head and a fish tail using pixel art)",
                "image_alt: "PLACEHOLDER - image alternative text here (accessible text for visually impaired people)",
                "title": "PLACEHOLDER - fill the title here (include emojis if appropriate)"
            },
            "pages": [
                {
                    "image": "PLACEHOLDER - describe a prompt for Dall-E image here (specify art style)",
                    "image_alt: "PLACEHOLDER - image alternative text here (accessible text for visually impaired people)",
                    "title": "PLACEHOLDER - fill the page title here (include emojis if appropriate, keep succinct)",
                    "text": "PLACEHOLDER - fill the page content here - be precise and do not use return carriage (\\n) - max 2000 characters",
                    "footer": "PLACEHOLDER - fill the page footer here (references or observations - be precise and do not use return carriage (\\n))"
                },
            ],
            "keywords": [
                "PLACEHOLDER - fill the hashtags (#) for SEO on instagram here (max 20, choose wisely)"
            ],
        }
        """,
    ]

    MAX_TOKENS = 2000
    CHOICES = 1
    TEMPERATURE = 0.5

    def __init__(self, seed, output = None):
        self.seed = seed
        self.skip_ideas_generation = False

        if output:
            self.output = output

            self.path = Path(self.output)

            if not self.path.exists():
                raise Exception(f"Folder {self.output} could not be found.")

            self.skip_ideas_generation = True

        if not output:
            self.slug = slugfy(self.seed)

            self.timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

            self.output = f"output/instagram/ideas/{self.timestamp}-{self.slug}"

            self.path = Path(self.output)

            self._create_folder()

    def _create_folder(self):
        self.path.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            raise Exception(f"Folder {self.output} could not be created.")

    def generate(self):
        prompt = self._prepare_prompt()

        ideas = self._generate_ideas(prompt)

        posts = self._generate_posts(ideas)

        summary = self._generate_summary(ideas, posts)

        return summary

    def _prepare_prompt(self) -> list:
        user_prompt = [
            f"The essence of the post should be about '{self.seed}'.",
        ]

        prompt = [
            {
                "role": "system",
                "content": "\n".join(self.SYSTEM_PROMPT),
            },
            {
                "role": "user",
                "content": "\n".join(user_prompt),
            },
        ]

        return prompt

    def _generate_ideas(self, prompt: list) -> list:
        ideas = []

        if not self.skip_ideas_generation:
            response = OpenAI().get_chat_completion(
                messages=prompt,
                model=OpenAI.MODEL_GPT_4,
                max_tokens=self.MAX_TOKENS,
                nb_choices=self.CHOICES,
                temperature=self.TEMPERATURE,
            )

            if not response:
                raise Exception("GPT response is empty.")

            with open(self.path / "prompts.json", "w", encoding='utf-8') as file:
                file.write(str(response))

        with open(self.path / "prompts.json", "r", encoding='utf-8') as file:
            response = file.read()

        json_response = json.loads(str(response))

        choices = [choice['message']['content'] for choice in json_response['choices']]

        if not choices:
            raise Exception("GPT Response has no choices.")

        for idx, content in enumerate(choices):
            # sanitized_content = content.replace("\\n", "\n")

            ideas.append(json.loads(str(content)))

        return ideas

    def _generate_posts(self, ideas: list) -> list:
        posts = []

        for idx, idea in enumerate(ideas):
            post = self._generate_post(idx, idea)

            posts.append(post)

        return posts

    def _generate_post(self, idx: int, idea: dict) -> dict:
        first_page = self._generate_first_page(idx, idea)

        pages = self._generate_pages(idx, idea)

        return {
            "first_page": first_page,
            "pages": pages,
        }

    def _generate_first_page(self, idx: int, idea: dict) -> dict:
        head = {
            'x1': SPACING,
            'y1': SPACING,
            'x2': INSTAGRAM_POST_HEIGHT - SPACING,
            'y2': SPACING * 5,
            'text': idea['first_page']['title'],
            'font': ROBOTO_64,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 1,
        }

        image = {
            'x1': SPACING,
            'y1': SPACING * 7,
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - SPACING,
            'text': idea['first_page']['image'],
            'font': ROBOTO_32,
            'wrapped_lines': True,
            'border_color': 'black',
            'border_width': 1,
        }

        h = TextBox(**head)
        i = TextBox(**image)

        g = ImageGenerator(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT)

        h.draw(g.draw)
        i.draw(g.draw)

        filename = self.path / f"idea-{idx}-page-0-post.png"

        g.save(filename)

        return str(filename)

    def _generate_pages(self, idx: int, idea: dict) -> list:
        pages = []

        for page_count, page in enumerate(idea['pages']):
            head = {
                'x1': SPACING,
                'y1': SPACING,
                'x2': INSTAGRAM_POST_HEIGHT - SPACING,
                'y2': SPACING * 5,
                'text': page['title'],
                'font': ROBOTO_64,
                'wrapped_lines': True,
                'border_color': 'black',
                'border_width': 1,
            }

            text = {
                'x1': SPACING,
                'y1': SPACING * 7,
                'x2': INSTAGRAM_POST_WIDTH - SPACING,
                'y2': INSTAGRAM_POST_HEIGHT - (SPACING * 5),
                'text': page['text'],
                'font': ROBOTO_32,
                'wrapped_lines': True,
                'border_color': 'black',
                'border_width': 1,
            }

            image = {
                'x1': INSTAGRAM_POST_WIDTH // 2 + SPACING,
                'y1': SPACING * 7,
                'x2': INSTAGRAM_POST_WIDTH - SPACING,
                'y2': INSTAGRAM_POST_HEIGHT - (SPACING * 5),
                'text': page['image'],
                'font': ROBOTO_32,
                'wrapped_lines': True,
                'border_color': 'black',
                'border_width': 1,
            }

            footer = {
                'x1': SPACING,
                'y1': INSTAGRAM_POST_HEIGHT - (SPACING * 4),
                'x2': INSTAGRAM_POST_WIDTH - SPACING,
                'y2': INSTAGRAM_POST_HEIGHT - SPACING,
                'text': page['footer'],
                'font': ROBOTO_24,
                'wrapped_lines': True,
                'border_color': 'black',
                'border_width': 1,
            }

            h = TextBox(**head)
            t = TextBox(**text)
            # i = TextBox(**image)
            f = TextBox(**footer)

            g = ImageGenerator(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT)

            h.draw(g.draw)
            t.draw(g.draw)
            # i.draw(g.draw)
            f.draw(g.draw)

            filename = self.path / f"idea-{idx}-page-{page_count + 1}-post.png"

            g.save(filename)

            pages.append(str(filename))

        return pages

    def _generate_summary(self, ideas: list, posts: list) -> dict:
        summary = {}

        summary['seed'] = self.seed
        summary['output'] = self.output

        summary['ideas'] = ideas
        summary['posts'] = posts
        
        summary['summary'] = [
            self._summarize_idea(idx, idea) for idx, idea in enumerate(ideas)
        ],

        with open(self.path / "summary.json", "w", encoding='utf-8') as file:
            json.dump(summary, file, indent=4)

        return summary

    def _summarize_idea(self, idx: int, idea: dict) -> dict:
        summary = []

        summary.extend([
            idea['first_page']['title'],
            idea['first_page']['image'],
            idea['first_page']['image_alt'],
            "",
        ])

        for page in idea['pages']:
            summary.extend([
                page['title'],
                page['text'],
                page['image'],
                page['image_alt'],
                page['footer'],
                "",
            ])

        if 'keywords' in idea:
            summary.extend([
                "",
                ", ".join(idea['keywords']),
                "",
            ])

        return "\n".join(summary)


class TestInstagramPostTemplates:
    def test_head_body_footer_template(self):
        header = TextBox(**LAYOUTS['head_body_footer']['head'])
        body = TextBox(**LAYOUTS['head_body_footer']['body'])
        footer = TextBox(**LAYOUTS['head_body_footer']['footer'])

        generator = ImageGenerator(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        header.draw(generator.draw)
        body.draw(generator.draw)
        footer.draw(generator.draw)

        generator.save('output/instagram/tests/test_head_body_footer_template.png')

    def test_head_body_template(self):
        header = TextBox(**LAYOUTS['head_body']['head'])
        body = TextBox(**LAYOUTS['head_body']['body'])

        generator = ImageGenerator(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        header.draw(generator.draw)
        body.draw(generator.draw)

        generator.save('output/instagram/tests/test_head_body_template.png')

    def test_title_text_image_template(self):
        title = TextBox(**LAYOUTS['title_text_image']['title'])
        text = TextBox(**LAYOUTS['title_text_image']['text'])
        image = ImageBox(**LAYOUTS['title_text_image']['image'])

        generator = ImageGenerator(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        title.draw(generator.draw)
        text.draw(generator.draw)
        image.draw(generator.draw, generator.image)

        generator.save('output/instagram/tests/test_title_text_image_template.png')

    def test_title_text1_text2_template(self):
        title = TextBox(**LAYOUTS['title_text1_text2']['title'])
        text1 = TextBox(**LAYOUTS['title_text1_text2']['text1'])
        text2 = TextBox(**LAYOUTS['title_text1_text2']['text2'])

        generator = ImageGenerator(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        title.draw(generator.draw)
        text1.draw(generator.draw)
        text2.draw(generator.draw)

        generator.save('output/instagram/tests/test_title_text1_text2_template.png')


if __name__ == '__main__':
    TestInstagramPostTemplates().test_head_body_footer_template()
    TestInstagramPostTemplates().test_head_body_template()
    TestInstagramPostTemplates().test_title_text_image_template()
    TestInstagramPostTemplates().test_title_text1_text2_template()
