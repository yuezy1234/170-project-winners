from bs4 import BeautifulSoup
from operator import itemgetter
from selenium import webdriver
import pandas as pd
import time

size = ['small', 'medium', 'large']
cases = 241
top_score = []
url = "https://leaderboard.cs170.dev/#/leaderboard/small/"
browser = webdriver.Chrome()

for case in ["{0:03}".format(i) for i in range(cases+1)]:
    print(case)
    browser.get(url + case)
    time.sleep(0.5) # wait for page to fully load
    soup = BeautifulSoup(browser.page_source, 'lxml')
    data_table = soup.find_all('table')

    if(len(data_table) == 0):
        top_score.append(None)
        continue

    df = pd.read_html(str(data_table))
    r = round(df[0]['Penalty'][0], 4)
    top_score.append(r)

browser.close()
print(top_score)
print(len(top_score))

scores = [None] * 242 
with open('run_penalty.txt', 'r') as f:
    lines = f.readlines()

    for line in lines:
        if 'solution' in line and 'small' in line:
            sp = line.split()
            num = int(sp[0].split('/')[-1][:3])
            pen = round(float(sp[-1]), 4)
            scores[num] = pen
            print(pen)
            print(line)
print(scores)
print(len(scores))

bads = []

print("SCORES:")
hits = 0
for i in range(len(top_score)):
    print(top_score[i], scores[i])
    if top_score[i] == None or scores[i] == None: continue
    if top_score[i] >= scores[i]:
        hits += 1
    else:
        bads.append(i)

print(f"Hits: {hits} / 240")

for b in bads:
    print(f"Case {b}:", top_score[b], scores[b])