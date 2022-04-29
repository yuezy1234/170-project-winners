# from urllib.request import urlopen
# from bs4 import BeautifulSoup

# size = ['small', 'medium', 'large']

# url = "https://leaderboard.cs170.dev/#/leaderboard/small/001"
# html = urlopen(url).read()
# soup = BeautifulSoup(html, features="html.parser")

# # kill all script and style elements
# for script in soup(["script", "style"]):
#     script.extract()    # rip it out

# # get text
# text = soup.get_text()

# print(text)

# # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)

# print(text)

from urllib.request import Request, urlopen

req = Request('https://leaderboard.cs170.dev/#/leaderboard/small/001', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

print(webpage)