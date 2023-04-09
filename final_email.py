import re
import os
import json
import openai
from time import time,sleep
from uuid import uuid4

API_KEY=""
openai.api_key = API_KEY


def append_json(filepath, content):
    with open(filepath, 'a') as f:
        f.write(json.dumps(content) + '\n')


def read_file(filepath, mode='content'):
    with open(filepath, 'r', encoding='utf-8') as infile:
        if mode == 'content':
            return infile.read()
        elif mode == 'lines':
            return [line.strip() for line in infile.readlines()]


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def gpt35_completion(messages, model='gpt-3.5-turbo'):
    # token limitation of turbo is 4096
    max_retry = 5
    retry = 0
    while True:
        try:
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
            return completion
        except Exception as overload:
            retry += 1
            if retry >= max_retry:
                return "turbo error: %s" %overload
            print('Error communicating with OpenAI:', overload)
            sleep(2)


def main():
    stories_prompt_foler_path = "./conversations"
    pre_prompt_template = read_file("final_conversation_prompt_template.txt")

    for file in os.listdir(stories_prompt_foler_path):
        scenario = read_file(stories_prompt_foler_path + "/" + file)
        prompt = pre_prompt_template.replace("<<SCENARIO>>", scenario)
        messages = [{"role": "user", "content": prompt}]
        completiion = gpt35_completion(messages)
        data = {"prompt": scenario + '\nPERFECT EMAIL:', "completion": completiion}
        append_json("perfect_emails.jsonl", data)
        print("\n\n-----------------------------\n" + str(data))
        sleep(2)

main()


"""
stories_prompt_foler_path = "./conversations"
pre_prompt_template = read_file("final_conversation_prompt_template.txt")

for file in os.listdir(stories_prompt_foler_path):
    scenario = read_file(stories_prompt_foler_path + "/" + file)
    prompt = pre_prompt_template.replace("<<SCENARIO>>", scenario)
    messages = [{"role": "user", "content": prompt}]
    completiion = gpt35_completion(messages)
    data = {"prompt": scenario + '\nPERFECT EMAIL:', "completion": completiion}
    append_json("perfect_emails.jsonl", data)
    print("\n\n-----------------------------\n" + str(data))
    sleep(2)
"""
