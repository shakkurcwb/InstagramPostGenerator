# Instagram Post Generator

[Work-in-progress] Simple implementation of an Instagram Post Generator. Generates ideas using GPT and plot on images.

## Requirements

- Python 3.x

## Installation

1. Create a virtual environment (optional):
`python -m venv venv`

2. Activate the virtual environment (optional):
`venv\Scripts\activate`

3. Install dependencies:
`pip install -r requirements.txt`

4. Set OpenAI Api Token on `src\openai.py`.

## Usage

1. Extend `InstagramPostGenerator` class;
2. Define the business model you are representing;
3. Instanciate `CannabisEducatorInstagramPostGenerator(seed)` where `seed` is the post subject;
4. Invoke `generator.generate()` for the process to start.

#### Implementation Examples:
- `cannabis_educator_instagram.py`;
- `health_care_educator_instagram.py`;
- `qa_localizer_educator_instagram.py`;

### Output Samples:

Check folder `output/instagram/ideas` for some of the samples generated previously.

![Example of post about Cannabis Tolerance](output\instagram\ideas\2023-12-09-20-32-00-cannabis-tolerance-is-a-real-thing\idea-0-page-2-post.png)