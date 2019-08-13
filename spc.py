from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.request import urlopen


def get_most_recent_md_url():
    doc = urlopen("https://www.spc.noaa.gov/products/md/")
    soup = BeautifulSoup(doc, "html.parser")

    for tag in soup.find_all("a"):
        if "/md/md" in tag.get("href"):
            return "https://www.spc.noaa.gov" + tag.get("href")


def get_md_from_url(url):
    doc = urlopen(url)
    soup = BeautifulSoup(doc, "html.parser")
    raw_md = soup.find_all("pre")[0].text
    raw_md_lines = raw_md.split("\n")
    first = None
    last = None
    for i, line in enumerate(raw_md_lines):
        if "SUMMARY..." in line:
            first = i
        elif len(line.split("..")) == 3 and len(line.split("/")) >= 3:
            last = i
    return "\n".join(raw_md_lines[first:last])


def get_md_by_number(num):
    return get_md_from_url("https://www.spc.noaa.gov/products/md/md{:0>4}.html".format(num))


def get_mds(numbers, f):
    for number in numbers:
        f.write(get_md_by_number(number))
