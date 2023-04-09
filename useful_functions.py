import os

def concatenate_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                content = file.read().replace('\n', ' ')
            with open(os.path.join(folder_path, filename), 'w') as file:
                file.write(content)


def test(file_path):
    with open(file_path, 'r') as file:
        content = file.read().replace('\n', ' ')
    with open(file_path, 'w') as file:
        file.write(content)

def combine(foler_path, file_path):
    with open(file_path, 'w') as output_file:
        for filename in os.listdir(foler_path):
            if filename.endswith('.txt'):
                with open(os.path.join(foler_path, filename), 'r') as input_file:
                    content = input_file.read()
                    output_file.write(content + '\n')

combine("./stories", "./combined_stories.txt")