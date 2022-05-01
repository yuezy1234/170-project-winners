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

oroot = 'best7'

bads = []

bad_paths = []

hit = 0

size='large'

for outf in os.listdir(os.path.join(oroot, size)):
    if not outf.endswith(".out"):
        continue
    outf = os.path.join(oroot, size, outf)
    with open(outf, 'r') as f:
        top_line = f.readline()
        if '#' in top_line:
            pen = round(float(top_line.split()[-1]), 4)
            num = int(Path(outf).stem)
            if num > 241 or top_scores[size][num] == None: continue
            if pen <= top_scores[size][num]:
                hit += 1
            else:
                bads.append(num)
                bad_paths.append(outf)
                print(f"Case {num}: {top_scores[size][num]} {pen}")

loc = os.path.join('a_work', size)

for outf in bad_paths:
    dest = os.path.join(loc, f"{removesuffix(Path(outf).name, '.out')}.in")
    src = os.path.join('inputs', size, f"{removesuffix(Path(outf).name, '.out')}.in")
    print(src, '->', dest)
    shutil.copyfile(src, dest)

print(len(bads))
            
