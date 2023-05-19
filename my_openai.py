from dotenv import load_dotenv
import os
import asyncio
from config import Config
import openai
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY


def genarate_prompt_to_slide(slide_text, topic):
    return Config.TEMPLATE_PREFIX_TO_OPENAI_SLIDE_EXPLANATION.format(topic, slide_text)


async def async_get_explanation_to_presentation(list_of_slides, topic):
    tasks_slide_explains = [get_explanation_to_slide(slide_text, topic) for slide_text in list_of_slides]
    explanations_list = await asyncio.gather(*tasks_slide_explains)
    print(explanations_list)


async def async_ask_openai(prompt):
    try:
        completion = await openai.ChatCompletion.acreate(max_tokens=Config.MAX_TOKENS, model=Config.MODEL,
                                                         messages=[{"role": "user", "content": prompt}], timeout=2)
    except openai.error.RateLimitError as e:
        return f'api kei get to the limit msg:{e}'

    return completion.choices[0].message.content


async def get_explanation_to_slide(slide_text, topic):
    if not slide_text:
        return ""

    prompt = genarate_prompt_to_slide(slide_text, topic)
    slide_explanation = await async_ask_openai(prompt)

    return slide_explanation


if __name__ == '__main__':
    l = ['End of course exercise',
         'Generative AI and software development What are the possible uses of generative ai, and natural language processing in software development?',
         'Generative AI and software products What are the possible uses of generative ai, and natural language processing in software products?']
    # asyncio.run(async_get_explanation_to_presentation(l, topic="end of course exercise"))
    # l = ['End of course exercise']
    l=['data structures and manipulation in Python', 'Customizing classes - dunder functions\nDunder methods are also known as magic methods or special methods in Python.\nThey are pre-defined methods that allow you to define the behavior of your objects when certain operations are performed on them.\nDunder methods are surrounded by double underscores, hence the name "dunder".\nExamples of dunder methods include __init__, __str__, and __eq__.\n__init__ is used to initialize an object\'s attributes.\n__str__ is used to define how the object should be represented as a string.\n__eq__ is used to define the equality comparison between two objects.']

    asyncio.run(async_get_explanation_to_presentation(l, topic="end of course exercise"))


