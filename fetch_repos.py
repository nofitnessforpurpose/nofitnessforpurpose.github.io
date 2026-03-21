import urllib.request
import json
import os

TOKEN = os.environ.get('GITHUB_TOKEN')
USER = 'nofitnessforpurpose'

# Fetch all pages
repos = []
page = 1
while True:
    req = urllib.request.Request(f'https://api.github.com/users/{USER}/repos?per_page=100&page={page}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    if TOKEN:
        req.add_header('Authorization', f'token {TOKEN}')

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if not data:
                break
            repos.extend(data)
            if len(data) < 100:
                break
            page += 1
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        break

output = []
for r in repos:
    output.append({
        'name': r.get('name', ''),
        'html_url': r.get('html_url', ''),
        'description': r.get('description', ''),
        'topics': r.get('topics', [])
    })

with open('repos.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"Saved {len(output)} repositories to repos.json")
