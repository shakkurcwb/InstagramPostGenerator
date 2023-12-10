from src.instagram_post_generator import (
    InstagramPostGenerator, 
)


class CannabisEducatorInstagramPostGenerator(InstagramPostGenerator):
    BUSINESS_MODEL = "cannabis educator instagram page"


def run():
    seed = "How cannabis impact your learning and memory?"

    # debug_file = "output/instagram/ideas/2023-12-09-20-32-00-cannabis-tolerance-is-a-real-thing"

    generator = CannabisEducatorInstagramPostGenerator(seed, output=None)

    summary = generator.generate()

    print(summary)


if __name__ == "__main__":
    run()
