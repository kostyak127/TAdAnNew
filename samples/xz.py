import re

link = re.findall('[a-zA-z0-9_]+[.][a-z]+', 'http://youtube.com')[0]
print(link)