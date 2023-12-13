import textwrap
import json

from pathlib import Path
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont, ImageColor

from src.helpers import slugfy
from src.openai import OpenAI

NOTO_EMOJI_FONT = "fonts/NotoColorEmoji-Regular.ttf"
NOTO_EMOJI_24 = ImageFont.truetype(NOTO_EMOJI_FONT, 109)
NOTO_EMOJI_32 = ImageFont.truetype(NOTO_EMOJI_FONT, 109)
NOTO_EMOJI_64 = ImageFont.truetype(NOTO_EMOJI_FONT, 109)

SYMBOLA_FONT = "fonts/Symbola.ttf"
SYMBOLA_24 = ImageFont.truetype(SYMBOLA_FONT, 24)
SYMBOLA_32 = ImageFont.truetype(SYMBOLA_FONT, 32)
SYMBOLA_64 = ImageFont.truetype(SYMBOLA_FONT, 64)

ROBOTO_FONT = "fonts/Roboto-Regular.ttf"
ROBOTO_24 = ImageFont.truetype(ROBOTO_FONT, 24)
ROBOTO_32 = ImageFont.truetype(ROBOTO_FONT, 32)
ROBOTO_64 = ImageFont.truetype(ROBOTO_FONT, 64)

TEMPLATES_FOLDER = "output/instagram/templates"

INSTAGRAM_POST_WIDTH = 1080
INSTAGRAM_POST_HEIGHT = 1080

TEXT_SPACING = 30
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
            'border_color': 'black',
            'border_width': 5,
        },
    },
}


class ImageBuilder:
    def __init__(self, width: int, height: int, color: str = None, template: str = None):
        # Create a new image with the given size
        self.image = Image.new("RGBA", (width, height), color)

        if template:
            # Open the template image
            self.template = Image.open(f"{TEMPLATES_FOLDER}/{template}").convert("RGBA")

            # Paste the template image into the new image
            self.paste(self.template, 0, 0, self.template)

    @property
    def draw(self):
        return ImageDraw.Draw(self.image, "RGBA")

    def copy(self):
        return self.image.copy()

    def crop(self, x1: int, y1: int, x2: int, y2: int):
        return self.image.crop((x1, y1, x2, y2))

    def paste(self, image: Image, x: int, y: int, mask: Image = None):
        self.image.paste(image, (x, y), mask)

    def save(self, filename: str):
        self.image.save(filename)


class Box:
    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        border_color: str = None,
        border_width: int = 0,
        fill_color: str = None,
        transparency: int = 0,
    ):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.outline = border_color
        self.width = border_width

        self.fill = fill_color
        self.alpha = transparency  # Transparency value (0-255)

    def draw(self, builder: ImageBuilder):
        image_copy = builder.copy()

        xy = [(self.x1, self.y1), (self.x2, self.y2)]

        args = {
            "outline": self.outline,
            "width": self.width,
        }

        if self.fill:
            fill_color = self._parse_fill_color()
            args["fill"] = fill_color

        # Draw the filled rectangle with transparency on a separate image
        fill_image = Image.new("RGBA", image_copy.size)
        fill_draw = ImageDraw.Draw(fill_image)
        fill_draw.rectangle(xy, **args)

        # Paste the filled rectangle onto our copy of the original image so that it's transparent
        image_copy.paste(fill_image, (0, 0), fill_image)

        # Paste the copy of the original image with the filled rectangle back onto the original image
        builder.paste(image_copy, 0, 0)

    def _parse_fill_color(self):
        red, green, blue = ImageColor.getrgb(self.fill)

        return (red, green, blue, self.alpha)


class TextBox(Box):
    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        text: str,
        text_color: str = "black",
        font: ImageFont = None,
        font_fallback: ImageFont = None,
        border_color: str = "black",
        border_width: int = 1,
        fill_color: str = "white",
        transparency: int = 255,
    ):
        super().__init__(x1, y1, x2, y2, border_color, border_width, fill_color, transparency)

        self.text = text
        self.color = text_color
        self.font = font
        self.font_fallback = font_fallback if font_fallback else font

    def draw(self, builder: ImageBuilder):
        super().draw(builder)

        # Split the text into lines that fit within the specified max_width in pixels
        lines = textwrap.wrap(self.text, width=self._wrap_text(builder.draw))

        current_y = self.y1 + TEXT_SPACING
        for idx, text in enumerate(lines):
            # Reset current_x for each new line
            current_x = self.x1 + TEXT_SPACING

            for char in text:
                # Select font based on ASCII value (support emojis)
                font = self.font if ord(char) < 255 else self.font_fallback

                # Get the width of the character
                char_width = builder.draw.textlength(char, font=font)

                # Draw the character onto the image
                builder.draw.text((current_x, current_y), char, fill=self.color, font=font, embedded_color=True)

                # Increment current_x by the width of the character
                current_x += char_width

            # Increment current_y by the height of the font
            current_y += font.size + 5

    def _wrap_text(self, draw: ImageDraw):
        words = self.text.split()
        wrapped_lines = []
        line = words[0]

        for word in words[1:]:
            test_line = line + ' ' + word
            if draw.textlength(test_line, font=self.font) <= self.x2 - self.x1 - TEXT_SPACING * 2:
                line = test_line
            else:
                wrapped_lines.append(line)
                line = word

        wrapped_lines.append(line)
        return len(max(wrapped_lines, key=len))


class ImageBox(Box):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, image_path: str, border_color: str = "black", border_width: int = 1, fill_color: str = "white", transparency: int = 255):
        super().__init__(x1, y1, x2, y2, border_color, border_width, fill_color, transparency)

        self.image = Image.open(image_path)

        if not self.image:
            raise Exception(f"Image {image_path} could not be found.")

    def draw(self, builder: ImageBuilder):
        super().draw(builder)

        resized_image = self.image.resize((self.x2 - self.x1, self.y2 - self.y1))

        builder.paste(resized_image, self.x1, self.y1)


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

    def __init__(self, seed: str, template: str = None, reuse_ideas_filepath: str = None):
        self.seed = seed
        self.template = template
        self.skip_ideas_generation = False

        if reuse_ideas_filepath:
            self.output = reuse_ideas_filepath

            self.path = Path(self.output)

            if not self.path.exists():
                raise Exception(f"Folder {self.output} could not be found.")

            self.skip_ideas_generation = True

        if not reuse_ideas_filepath:
            self.slug = slugfy(self.seed)

            self.timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

            self.output = f"output/instagram/ideas/{self.timestamp}-{self.slug}"

            self.path = Path(self.output)

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
            ideas.append(json.loads(str(content)))

        return ideas

    def _generate_posts(self, ideas: list) -> list:
        posts = []

        for idx, idea in enumerate(ideas):
            posts.append({
                "first_page": self._generate_first_page(idx, idea),
                "pages": self._generate_pages(idx, idea),
            })

        return posts

    def _generate_first_page(self, idx: int, idea: dict) -> dict:
        head = {
            'x1': SPACING,
            'y1': SPACING,
            'x2': INSTAGRAM_POST_HEIGHT - SPACING,
            'y2': SPACING * 5,
            'text': idea['first_page']['title'],
            'text_color': 'white',
            'font': ROBOTO_64,
            'font_fallback': NOTO_EMOJI_64,
            'border_color': 'black',
            'border_width': 1,
            "fill_color": "blue",
            "transparency": 64,
        }

        image = {
            'x1': SPACING,
            'y1': SPACING * 7,
            'x2': INSTAGRAM_POST_WIDTH - SPACING,
            'y2': INSTAGRAM_POST_HEIGHT - SPACING,
            'image_path': 'output/test.png',
            'border_color': 'black',
            'border_width': 1,
        }

        h = TextBox(**head)
        i = ImageBox(**image)

        builder = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, template=self.template)

        h.draw(builder)
        i.draw(builder)

        filename = self.path / f"idea-{idx}-page-0-post.png"

        builder.save(filename)

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
                'text_color': 'white',
                'font': ROBOTO_64,
                'font_fallback': NOTO_EMOJI_64,
                'border_color': 'white',
                'border_width': 1,
                "fill_color": "blue",
                "transparency": 64,
            }

            text = {
                'x1': SPACING,
                'y1': SPACING * 7,
                'x2': INSTAGRAM_POST_WIDTH - SPACING,
                'y2': INSTAGRAM_POST_HEIGHT - (SPACING * 5),
                'text': page['text'],
                'text_color': 'white',
                'font': ROBOTO_32,
                'font_fallback': NOTO_EMOJI_32,
                'border_color': 'white',
                'border_width': 1,
                "fill_color": "blue",
                "transparency": 64,
            }

            footer = {
                'x1': SPACING,
                'y1': INSTAGRAM_POST_HEIGHT - (SPACING * 4),
                'x2': INSTAGRAM_POST_WIDTH - SPACING,
                'y2': INSTAGRAM_POST_HEIGHT - SPACING,
                'text': page['footer'],
                'text_color': 'white',
                'font': ROBOTO_24,
                'font_fallback': NOTO_EMOJI_24,
                'border_color': 'white',
                'border_width': 1,
                "fill_color": "blue",
                "transparency": 64,
            }

            h = TextBox(**head)
            t = TextBox(**text)
            f = TextBox(**footer)

            builder = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, template=self.template)

            h.draw(builder)
            t.draw(builder)
            f.draw(builder)

            filename = self.path / f"idea-{idx}-page-{page_count + 1}-post.png"

            builder.save(filename)

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

        generator = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        header.draw(generator.draw)
        body.draw(generator.draw)
        footer.draw(generator.draw)

        generator.save('output/instagram/tests/test_head_body_footer_template.png')

    def test_head_body_template(self):
        header = TextBox(**LAYOUTS['head_body']['head'])
        body = TextBox(**LAYOUTS['head_body']['body'])

        generator = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        header.draw(generator.draw)
        body.draw(generator.draw)

        generator.save('output/instagram/tests/test_head_body_template.png')

    def test_title_text_image_template(self):
        title = TextBox(**LAYOUTS['title_text_image']['title'])
        text = TextBox(**LAYOUTS['title_text_image']['text'])
        image = ImageBox(**LAYOUTS['title_text_image']['image'])

        generator = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        title.draw(generator.draw)
        text.draw(generator.draw)
        image.draw(generator.draw, generator.image)

        generator.save('output/instagram/tests/test_title_text_image_template.png')

    def test_title_text1_text2_template(self):
        title = TextBox(**LAYOUTS['title_text1_text2']['title'])
        text1 = TextBox(**LAYOUTS['title_text1_text2']['text1'])
        text2 = TextBox(**LAYOUTS['title_text1_text2']['text2'])

        generator = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        title.draw(generator.draw)
        text1.draw(generator.draw)
        text2.draw(generator.draw)

        generator.save('output/instagram/tests/test_title_text1_text2_template.png')


if __name__ == '__main__':
    TestInstagramPostTemplates().test_head_body_footer_template()
    TestInstagramPostTemplates().test_head_body_template()
    TestInstagramPostTemplates().test_title_text_image_template()
    TestInstagramPostTemplates().test_title_text1_text2_template()
