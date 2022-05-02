import json
import os
from pathlib import Path
import shutil
import requests
from bs4 import BeautifulSoup


def removesuffix(s: str, suffix: str):
    if not s.endswith(suffix):
        return s

    return s[:-len(suffix)]

sizes = ['small', 'medium', 'large']

url = 'https://project.cs170.dev/scoreboard/'
iroot = 'inputs'
oroot = 'best13'

for size in sizes:
    ranks = {}

    for outf in os.listdir(os.path.join(iroot, size)):
        # if not outf.endswith(".out"):
        #     continue

        outf = os.path.join(oroot, size, f"{removesuffix(Path(outf).name, '.in')}.out")
        # print(outf)
        try:
            with open(outf, 'r') as f:
                top_line = f.readline()
                if '#' in top_line:
                    pen = round(float(top_line.split()[-1]), 4)
                    num = int(Path(outf).stem)
                    if num > 241: continue
                else:
                    print("empty")
        except:
            print(outf, "not here")
            continue

        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(url + size + '/' + Path(outf).stem).text

        j = json.loads(html_content)['Entries']
        scores = []
        for entry in j:
            scores.append(round(entry['TeamScore'], 4))
        scores = sorted(scores)
        rank = 0
        for i in range(len(scores)):
            if pen <= scores[i]:
                break
            # if i != 0 and scores[i] == scores[i-1]: continue
            rank += 1
        
        ranks[Path(outf).stem] = rank

    f = open(f'{size}_ranks.txt', 'w')
    for k,v in ranks.items(): 
        if v != 0:
            print(k, ":", v, file=f)
    f.close()




#     c += 1
#     outf = os.path.join(oroot, size, f"{removesuffix(Path(outf).name, '.in')}.out")

#     try:
#         with open(outf, 'r') as f:
#             top_line = f.readline()
#             if '#' in top_line:
#                 pen = round(float(top_line.split()[-1]), 4)
#                 num = int(Path(outf).stem)
#                 if num > 241: continue
#                 if top_scores[size][num] == None: 
#                     bads.append(num)
#                     bad_paths.append(outf)
#                 if pen <= top_scores[size][num]:
#                     hit += 1
#                     goods.append(num)
#                     # print(f"Case {num}: {top_scores[size][num]} {pen}")
#                 else:
#                     bads.append(num)
#                     bad_paths.append(outf)
#                     print(f"Case {num}: {top_scores[size][num]} {pen}")
#             else:
#                 bads.append(num)
#                 bad_paths.append(outf)
#     except:
#         print(outf, "not here")
#         bad_paths.append(outf)

# loc = os.path.join('need_work', size)

# for outf in bad_paths:
#     dest = os.path.join(loc, f"{removesuffix(Path(outf).name, '.out')}.in")
#     src = os.path.join('inputs', size, f"{removesuffix(Path(outf).name, '.out')}.in")
#     print(src, '->', dest)
#     shutil.copyfile(src, dest)

# print(len(bad_paths))
            
# print(c)