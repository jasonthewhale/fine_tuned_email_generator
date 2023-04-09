import random

def read_file(filepath, mode='content'):
    with open(filepath, 'r', encoding='utf-8') as infile:
        if mode == 'content':
            return infile.read()
        elif mode == 'lines':
            return [line.strip() for line in infile.readlines()]

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def test_replace():
    prompt_model = read_file("general_prompt.txt")
    types = read_file("types.txt", mode='lines')
    years = read_file("years.txt", mode='lines')
    countries = read_file("countries.txt", mode='lines')

    for type in random.sample(types, 8):
        for year in random.sample(years, 5):
            for country in random.sample(countries, 10):
                filled_prompt = prompt_model.replace("<<TYPE>>", type).replace("<<YEAR>>", year).replace("<<COUNTRY>>", country)
                file_name = f"{type}_{country}_{year}"
                file_path = f"./test_synthesize_files/{file_name}.txt"
                print(filled_prompt)
                save_file(file_path, filled_prompt)

test_replace()