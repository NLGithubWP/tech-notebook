import os
import re
import requests
from bs4 import BeautifulSoup


def fix_md_format(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Check if the front matter is missing
    content_str = ''.join(content)
    if not (content_str.startswith('---') and 'layout: post' in content_str and content_str.count('---') >= 2):
        title_line = next((line for line in content if line.startswith('title:')), None)
        if title_line:
            title_index = content.index(title_line)
            content.insert(0, '---\n')
            content.insert(title_index + 2, 'layout: post\n')
            content.insert(title_index + 3, '---\n')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)


def get_paper_info(title):
    search_url = f'https://scholar.google.com/scholar?q={title}'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('div', class_='gs_ri')
    if result:
        title = result.find('h3').text
        publication_info = result.find('div', class_='gs_a').text
        return title, publication_info
    return title, None


def update_readme(md_files, readme_path):
    new_entries = []

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_part = re.search(r'\d{4}-\d{2}-\d{2}', file_name).group(0)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        title_line = next((line for line in content if line.startswith('title:')), None)
        if title_line:
            title = title_line.split('title: ')[1].strip()
            fixed_title, publication_info = get_paper_info(title)
            new_entry = f'* [{date_part} {fixed_title}]({file_path})'
            if publication_info:
                new_entry += f' - {publication_info}'
            new_entries.append(new_entry)

    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.readlines()

    new_readme_content = readme_content + new_entries

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.writelines(new_readme_content)


def main():
    directory = './_posts/paper-notebook/'  # Set this to the directory containing the .md files
    md_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.md')]
    readme_path = os.path.join(directory, 'README.md')

    for md_file in md_files:
        fix_md_format(md_file)

    update_readme(md_files, readme_path)


if __name__ == "__main__":
    main()
