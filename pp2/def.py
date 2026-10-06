import re

text=input()

text1=re.findall(r'pq{2,3}',text)

print(text1)