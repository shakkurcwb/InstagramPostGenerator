from src.instagram_post_generator import (
    InstagramPostGenerator, 
)


class CannabisEducatorInstagramPostGenerator(InstagramPostGenerator):
    BUSINESS_MODEL = "cannabis educator instagram page"


def run():
    seed = "How cannabis impact your learning and memory?"

    debug_file = "output/instagram/ideas/2023-12-09-21-30-52-cannabis-impact-on-economy"

    generator = CannabisEducatorInstagramPostGenerator(seed, template="6.png", reuse_ideas_filepath=debug_file)

    summary = generator.generate()

    print(summary)


if __name__ == "__main__":
    run()
