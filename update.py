import os
import re

def fix_md_format(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    content_str = ''.join(content)

    if not (content_str.startswith('---') and 'layout: post' in content_str and content_str.count('---') >= 2):
        title_line = next((line for line in content if line.startswith('title:')), None)
        header_image_line = next((line for line in content if line.startswith('header-image:')), None)
        categories_line = next((line for line in content if line.startswith('categories:')), None)

        if title_line and header_image_line and categories_line:
            new_front_matter = [
                '---\n',
                title_line,
                header_image_line,
                categories_line,
                'layout: post\n',
                '---\n'
            ]

            # Add the remaining content after the found lines
            remaining_content = content[max(content.index(title_line), content.index(header_image_line), content.index(categories_line)) + 1:]
            content = new_front_matter + remaining_content

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

def update_readme(md_files, readme_path):
    new_entries = []

    for file_path in md_files:
        file_name = os.path.basename(file_path)
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', file_name)

        if date_match:
            date_part = date_match.group(0)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()

            title_line = next((line for line in content if line.startswith('title:')), None)
            if title_line:
                title = title_line.split('title: ')[1].strip()
                new_entry = f'* [{date_part} {title}](https://github.com/NLGithubWP/tech-notebook/blob/master/_posts/paper-notebook/{file_name})\n'
                new_entries.append(new_entry)

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as file:
            readme_content = file.readlines()
    else:
        readme_content = []

    new_readme_content = readme_content + new_entries

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.writelines(new_readme_content)

def main():
    directory = './_posts/paper-notebook/'  # Set this to the directory containing the .md files
    md_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.md')]
    readme_path = './README.md'  # Updated path for README.md

    for md_file in md_files:
        print(f'Processing file: {md_file}')
        fix_md_format(md_file)

    print('Updating README.md...')
    update_readme(md_files, readme_path)
    print('README.md updated successfully.')

if __name__ == "__main__":
    main()
