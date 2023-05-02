import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xlsxwriter

class channel:
    name = ""
    followers = ""
    mentions = ""
    def __init__(self,name, fol, ment):
        self.name = name
        self.followers = fol
        self.mentions = ment

    def __hash__(self):
        return hash((self.name, self.mentions, self.followers))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.name == other.name and self.followers == other.followers and self.mentions == other.mentions
def parse():
    URL = "https://tgstat.ru/quotes/@MID_Russia/channels"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    driver.maximize_window()
    driver.implicitly_wait(10)
    button = driver.find_element(By.XPATH, "//*[@id='channels-list-form']/div/div[2]/button")
    button.click()
    while True:
        try:
            button.click()
        except:
            break
    page_content = driver.page_source
    time.sleep(100)
    with open("page.html", 'w', encoding='utf-8') as file:
        file.write(page_content)

def write_to_excel():
    s = set()
    workbook = xlsxwriter.Workbook('tg_channels.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Название")
    worksheet.write(0, 1, "Подписчиков")
    worksheet.write(0, 2, "Упоминания")
    row = 1
    f = open("page.html", 'r', encoding='utf-8')
    html_code = f.read()
    soup = BeautifulSoup(html_code, "html.parser")
    channels = soup.find("ul", class_="list-group list-group-flush mx-n3 mx-sm-0 posts-list lm-list-container rounded")
    tables = channels.find_all("div", class_="row")
    for table in tables:
        media_div = table.find("div", class_="media-body")
        a = media_div.find("a")
        b = media_div.find("b")
        mentions_table = table.find("div", class_="col col-5 align-items-center text-right")
        mention_a = mentions_table.find("a")

        ch = channel(a.text, b.text, mention_a.text)
        s.add(ch)
    for ch in s:
        worksheet.write(row, 0, ch.name)
        worksheet.write(row, 1, ch.followers)
        worksheet.write(row, 2, ch.mentions)
        row += 1
    workbook.close()
if __name__ == '__main__':
    #parse() # фукнция которая нажимает на кнопку до конца и закидывает полученный html код в файл (можно запустить 1 раз)
    write_to_excel()
