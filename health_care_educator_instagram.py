from src.instagram_post_generator import (
    InstagramPostGenerator, 
)


class HealthCareEducatorInstagramPostGenerator(InstagramPostGenerator):
    BUSINESS_MODEL = "health care educator instagram page"


def run():
    seed = "How home-care based agencies impact society and the economy?"

    generator = HealthCareEducatorInstagramPostGenerator(seed, template="3.png")

    summary = generator.generate()

    print(summary)


if __name__ == "__main__":
    run()
