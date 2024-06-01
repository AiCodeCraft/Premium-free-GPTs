import requests
import re
import os
from github import Github

# Function to check if a URL is reachable
def check_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Function to update the README file with status indicators
def update_readme(readme_content):
    url_pattern = re.compile(r'\[(.*?)\]\((https?://.*?)\)')
    updated_content = readme_content

    for match in url_pattern.finditer(readme_content):
        name, url = match.groups()
        status = check_url(url)
        status_indicator = '🟢' if status else '🔴'
        updated_content = updated_content.replace(f'[{name}]({url})', f'[{name}]({url}) {status_indicator}')

    return updated_content

# Path to the README file
readme_path = 'README.md'

# Read the content of the README file
with open(readme_path, 'r') as file:
    readme_content = file.read()

# Update the README content with status indicators
updated_content = update_readme(readme_content)

# Write the updated content back to the README file
with open(readme_path, 'w') as file:
    file.write(updated_content)

# Commit and push the changes using the GitHub API
g = Github(os.getenv('GITHUB_TOKEN'))
repo = g.get_repo('AiCodeCraft/Awesome-free-GPTs')
contents = repo.get_contents(readme_path)

repo.update_file(contents.path, "Update URL status", updated_content, contents.sha)
