import urllib.request
import re

url = 'http://127.0.0.1:3440/main.js'
content = urllib.request.urlopen(url).read().decode('utf-8')

strings = re.findall(r'\"([A-Z][^\"]{3,100})\"', content)
strings += re.findall(r'\'([A-Z][^\']{3,100})\'', content)

ui_strings = set()
for s in strings:
    if ' ' in s and not re.search(r'[A-Z][a-z]+[A-Z]', s) and not '_' in s and not '{' in s and not '%' in s:
        if re.match(r'^[A-Z][a-z]+( [a-zA-Z0-9,\.\'!-?()]+)+$', s):
            ui_strings.add(s)

with open('candidates.txt', 'w', encoding='utf-8') as f:
    for s in sorted(list(ui_strings)):
        f.write(s + '\n')

print(f'Extracted {len(ui_strings)} from main.js.')
