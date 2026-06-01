import urllib.request
import re
import json

url = 'http://127.0.0.1:3440/'
try:
    req = urllib.request.urlopen(url)
    html = req.read().decode('utf-8')
except Exception as e:
    print("Failed to connect to language server:", e)
    exit(1)

js_files = re.findall(r'<script.*?src=[\'\"]([^\'\"]+\.js)[\'\"]', html)
print(f'Found JS files: {js_files}')

ui_strings = set()

for js in js_files:
    js_url = url + js.lstrip('/')
    try:
        content = urllib.request.urlopen(js_url).read().decode('utf-8')
        # Extract all string literals (simple regex for double and single quotes)
        strings = re.findall(r'\"([A-Z][^\"]{3,150})\"', content)
        strings += re.findall(r'\'([A-Z][^\']{3,150})\'', content)
        
        for s in strings:
            # Filter: must contain space, no camelCase, no snake_case, mostly English letters
            if ' ' in s and not re.search(r'[A-Z][a-z]+[A-Z]', s) and not '_' in s:
                if re.match(r'^[A-Z][A-Za-z0-9 ,.\'!?()-:]+$', s):
                    ui_strings.add(s)
    except Exception as e:
        print(f'Failed {js_url}: {e}')

with open('candidates.txt', 'w', encoding='utf-8') as f:
    for s in sorted(list(ui_strings)):
        f.write(s + '\n')

print(f'Extracted {len(ui_strings)} candidate strings.')
