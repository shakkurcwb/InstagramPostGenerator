from src.instagram_post_generator import (
    ImageBuilder, TextBox, ImageBox, LAYOUTS,
    INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT,
)


class TestInstagramPostGeneratorTemplates:
    def test_head_body_footer_template(self):
        header = TextBox(**LAYOUTS['head_body_footer']['head'])
        body = TextBox(**LAYOUTS['head_body_footer']['body'])
        footer = TextBox(**LAYOUTS['head_body_footer']['footer'])

        builder = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        header.draw(builder)
        body.draw(builder)
        footer.draw(builder)

        builder.save('output/instagram/tests/test_head_body_footer_template.png')

    def test_head_body_template(self):
        header = TextBox(**LAYOUTS['head_body']['head'])
        body = TextBox(**LAYOUTS['head_body']['body'])

        builder = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        header.draw(builder)
        body.draw(builder)

        builder.save('output/instagram/tests/test_head_body_template.png')

    def test_title_text_image_template(self):
        title = TextBox(**LAYOUTS['title_text_image']['title'])
        text = TextBox(**LAYOUTS['title_text_image']['text'])
        image = ImageBox(**LAYOUTS['title_text_image']['image'])

        builder = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        title.draw(builder)
        text.draw(builder)
        image.draw(builder, builder.image)

        builder.save('output/instagram/tests/test_title_text_image_template.png')

    def test_title_text1_text2_template(self):
        title = TextBox(**LAYOUTS['title_text1_text2']['title'])
        text1 = TextBox(**LAYOUTS['title_text1_text2']['text1'])
        text2 = TextBox(**LAYOUTS['title_text1_text2']['text2'])

        builder = ImageBuilder(INSTAGRAM_POST_WIDTH, INSTAGRAM_POST_HEIGHT, "white")

        title.draw(builder)
        text1.draw(builder)
        text2.draw(builder)

        builder.save('output/instagram/tests/test_title_text1_text2_template.png')
