from bs4 import BeautifulSoup
from operator import itemgetter
from selenium import webdriver
import pandas as pd
import time
import json

size = ['small', 'medium', 'large']
cases = 241
top_score_dict = {
    'small': [],
    'medium': [],
    'large': []
}
url = "https://leaderboard.cs170.dev/#/leaderboard/"
browser = webdriver.Chrome()

for s in size:
    url_size = url + s + '/'
    for case in ["{0:03}".format(i) for i in range(cases+1)]:
        print(s, case)
        browser.get(url_size + case)
        time.sleep(0.5) # wait for page to fully load
        soup = BeautifulSoup(browser.page_source, 'lxml')
        data_table = soup.find_all('table')

        if(len(data_table) == 0):
            top_score_dict[s].append(None)
            continue

        df = pd.read_html(str(data_table))
        print(df[0]['Penalty'][0])
        r = round(float(df[0]['Penalty'][0]), 4)
        top_score_dict[s].append(r)

browser.close()
print(top_score_dict)

# scores = [None] * 242 
# with open('run_penalty.txt', 'r') as f:
#     lines = f.readlines()

#     for line in lines:
#         if 'solution' in line and 'medium' in line:
#             sp = line.split()
#             num = int(sp[0].split('/')[-1][:3])
#             pen = round(float(sp[-1]), 4)
#             scores[num] = pen
#             print(pen)
#             print(line)
# print(scores)
# print(len(scores))

# bads = []

# print("SCORES:")
# hits = 0
# for i in range(len(top_score)):
#     print(top_score[i], scores[i])
#     if top_score[i] == None or scores[i] == None: continue
#     if top_score[i] >= scores[i]:
#         hits += 1
#     else:
#         bads.append(i)

# print(f"Hits: {hits} / 240")

# for b in bads:
#     print(f"Case {b}:", top_score[b], scores[b])

j = json.dumps(top_score_dict)

with open('top_score.json', 'w') as f:
    json.dump(j, f)
