from src.instagram_post_generator import (
    InstagramPostGenerator, 
)


class HealthCareEducatorInstagramPostGenerator(InstagramPostGenerator):
    BUSINESS_MODEL = "health care educator instagram page"


def run():
    seed = "How home-care based agencies impact society and the economy?"

    # debug_file = "output/instagram/ideas/2023-12-09-20-32-00-cannabis-tolerance-is-a-real-thing"

    generator = HealthCareEducatorInstagramPostGenerator(seed, output=None)

    summary = generator.generate()

    print(summary)


if __name__ == "__main__":
    run()
