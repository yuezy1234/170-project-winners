import json
import os
from pathlib import Path
import shutil


def removesuffix(s: str, suffix: str):
    if not s.endswith(suffix):
        return s

    return s[:-len(suffix)]


with open('top_score.json', 'r') as f:
    top_scores = json.loads(json.load(f))

iroot = 'inputs'

oroot = 'best9'

bads = []

bad_paths = []

goods = []

hit = 0

size='small'

for outf in os.listdir(os.path.join(iroot, size)):
    # if not outf.endswith(".out"):
    #     continue
    outf = os.path.join(oroot, size, f"{removesuffix(Path(outf).name, '.in')}.out")

    try:
        with open(outf, 'r') as f:
            top_line = f.readline()
            if '#' in top_line:
                pen = round(float(top_line.split()[-1]), 4)
                num = int(Path(outf).stem)
                if num > 241: continue
                if top_scores[size][num] == None: 
                    bads.append(num)
                    bad_paths.append(outf)
                if pen <= top_scores[size][num]:
                    hit += 1
                    goods.append(num)
                    # print(f"Case {num}: {top_scores[size][num]} {pen}")
                else:
                    bads.append(num)
                    bad_paths.append(outf)
                    print(f"Case {num}: {top_scores[size][num]} {pen}")
            else:
                bads.append(num)
                bad_paths.append(outf)
    except:
        bad_paths.append(outf)

loc = os.path.join('needs_work', size)

for outf in bad_paths:
    dest = os.path.join(loc, f"{removesuffix(Path(outf).name, '.out')}.in")
    src = os.path.join('inputs', size, f"{removesuffix(Path(outf).name, '.out')}.in")
    print(src, '->', dest)
    shutil.copyfile(src, dest)

print(len(bad_paths))
            
