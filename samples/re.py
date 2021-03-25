import re

LINK_FINDER = ['w{0,3}[.]?[w]{0,2}[a-zA-Z0-9_]+[.][a-z]+']


res = re.findall(LINK_FINDER[0], 'https://www.kommersant.ru/doc/4307921')
print(list((map(lambda item: item[4:] if item.startswith('www.') else item, res))))
print(res)
