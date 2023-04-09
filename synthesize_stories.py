import re
import os
import openai
from time import time,sleep
from uuid import uuid4

API_KEY="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"
openai.api_key = API_KEY


def read_file(filepath, mode='content'):
    with open(filepath, 'r', encoding='utf-8') as infile:
        if mode == 'content':
            return infile.read()
        elif mode == 'lines':
            return [line.strip() for line in infile.readlines()]


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def correct_filename(text):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, '')
    return text


def fill_story_template():
    story_template = read_file("story_prompt_template.txt")
    intents = read_file("email_intents.txt", "lines")

    for intent in intents:
        filled_prompt = story_template.replace("<<UUID>>", str(uuid4())).replace("<<INTENT>>", intent)
        file_name = correct_filename(intent)
        file_path = "./prompt_stories/%s.txt" %file_name
        save_file(file_path, filled_prompt)
        print("\n\n" + filled_prompt)


def fill_story_email_template():
    story_email_template = read_file("conversation_prompt.txt")
    scenarios = read_file("combined_stories.txt", "lines")

    for scenario in scenarios:
        filled_email_prompt = story_email_template.replace("<<UUID>>", str(uuid4())).replace("<<SCENARIO>>", scenario)
        file_name = str(time()) + '_messy_prompt'
        file_path = "./prompt_conversation/%s.txt" %file_name
        save_file(file_path, filled_email_prompt)
        print("\n\n" + filled_email_prompt)


def gpt35_completion(messages, folder_path, model='gpt-3.5-turbo'):
    # token limitation of turbo is 4096
    response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=1024)
    """
        Fine-tuned parameters for turbo:
            temperature=0.9,
            max_tokens=500,
            top_p=0.1,
            frequency_penalty=0.2,
            presence_penalty=0.0
    """
    completion = response['choices'][0]['message']['content'].strip()
    completion = re.sub('\s+', ' ', completion)
    file_name = str(time()) + '.txt'

    pre_chat = "ASSISTANT: Hi there! How can I help you today?\nUSER: I need you to draft an email for me.\nASSISTANT: What do you need the email to say?\nUSER:"


    save_file(f'{folder_path}/{file_name}', pre_chat + completion)
    return completion


def generate_story():
    stories_prompt_foler_path = "./prompt_conversation"
    # stories_prompt_foler_path = "./prompt_bullit_point"

    for file in os.listdir(stories_prompt_foler_path):
        content = read_file(stories_prompt_foler_path + "/" + file)
        # content = read_file(stories_prompt_foler_path + "/" + file)
        messages = [{"role": "user", "content": content}]
        completion = gpt35_completion(messages, "./conversations")
        print('\n\n=================================\n' + completion)
        exit()
        sleep(1)

generate_story()