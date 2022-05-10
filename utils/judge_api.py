import aiohttp
import time
from bs4 import BeautifulSoup

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

async def fetch(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }

    driver = webdriver.Chrome(ChromeDriverManager().install())
    time.sleep(5)
    driver.get(url)
    content = driver.page_source

    return content


async def codeforces_fetch(id):
    if not id[-1].isdigit():
        content = await fetch(f"https://codeforces.com/contest/{id[:-1]}/problem/{id[-1]}")
    else:
        content = await fetch(f"https://codeforces.com/contest/{id[:-2]}/problem/{id[-2:]}")

    soup = BeautifulSoup(content, "html.parser")
    results = soup.find(class_="title")

    return results.text.split(". ")[1]


async def atcoder_fetch(id):
    url = f"https://atcoder.jp/contests/{id.split('_')[0]}/tasks/{id}"

    content = await fetch(url)

    soup = BeautifulSoup(content, "html.parser")
    results = soup.find(class_="h2")

    return results.text.split("- ")[1].split('\n')[0]


async def vnoj_fetch(id):
    url = f"https://oj.vnoi.info/problem/{id}"

    content = await fetch(url)

    soup = BeautifulSoup(content, "html.parser")
    results = soup.find("h2")

    return results.text


async def fetch_problem_name(judge, id):
    for c in id:
        if not (c.isdigit() or c.isalpha() or c == '_'):
            return None

    try:
        name = await globals()[f"{judge}_fetch"](id)
        return name
    except:
        return None
