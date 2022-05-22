from cgitb import html
from requests_html import HTMLSession
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://codeforces.com/problemset/problem/1678/B2')
time.sleep(5)
htmlSource = driver.page_source

soup = BeautifulSoup(htmlSource, "html.parser")
results = soup.find(class_="title")
print(results)