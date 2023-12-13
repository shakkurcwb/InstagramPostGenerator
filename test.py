from src.instagram_post_generator import (
    ImageBuilder, Box, TextBox, ImageBox, ROBOTO_32,
)


def run():
    image = ImageBuilder(1080, 1080, template='6.png')

    box = Box(108, 108, 216, 216, border_color='red', border_width=1, fill_color='green', transparency=128)

    text = TextBox(200, 200, 400, 400, border_color='purple', border_width=1, fill_color='brown', transparency=128, text='Hello World', font=ROBOTO_32, text_color='pink')

    image_ = ImageBox(500, 500, 700, 700, border_color='orange', border_width=1, fill_color='blue', transparency=128, image_path='output/test.png')

    box.draw(image)
    text.draw(image)
    image_.draw(image)

    image.save('output/instagram/tests/test.png')


if __name__ == "__main__":
    run()
