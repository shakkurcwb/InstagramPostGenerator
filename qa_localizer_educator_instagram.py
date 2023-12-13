from src.instagram_post_generator import (
    InstagramPostGenerator, 
)


class QaLocalizerEducatorInstagramPostGenerator(InstagramPostGenerator):
    BUSINESS_MODEL = "QA localization manager on a gaming company owning a side-project as an educator on instagram"


def run():
    seed = "How game companies can use localization as a tool to expand on the market?"

    generator = QaLocalizerEducatorInstagramPostGenerator(seed, template="7.png")

    summary = generator.generate()

    print(summary)


if __name__ == "__main__":
    run()
