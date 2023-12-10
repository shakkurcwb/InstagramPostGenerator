from src.instagram_post_generator import (
    InstagramPostGenerator, 
)


class QaLocalizerEducatorInstagramPostGenerator(InstagramPostGenerator):
    BUSINESS_MODEL = "QA localization manager on a gaming company owning a side-project as an educator on instagram"


def run():
    seed = "How game companies can use localization as a tool to expand on the market?"

    # debug_file = "output/instagram/ideas/2023-12-09-21-57-22-how-quality-assurance-localization-affect-gamers-around-the-world"

    generator = QaLocalizerEducatorInstagramPostGenerator(seed, output=None)

    summary = generator.generate()

    print(summary)


if __name__ == "__main__":
    run()
