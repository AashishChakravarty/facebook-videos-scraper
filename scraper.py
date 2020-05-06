## -*- coding: utf-8 -*-
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json

def scroll_to_bottom(driver):

    old_position = 0
    new_position = None

    while new_position != old_position:
        time.sleep(.5)

        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))


def remove_extra_characters(title):
    title = title.translate({ord('\"'): None})
    title = title.translate({ord('?'):  ' '})
    title = title.translate({ord('\n'): ' '})
    title = title.translate({ord('|'): None})
    title = title.replace('  ', ' ')

    return title


def find_data(video_elems):
    data = []
    i=0
    for video_elem in video_elems:
        if video_elem.find('span', attrs={'class':'_3vwb _400z _2-40'}):
            if i%2==0:
                link = video_elem.find('span', attrs={'class':'_3vwb _400z _2-40'})['href']

                title = video_elem.find('div', attrs={'class':'l9j0dhe7 stjgntxs ni8dbmo4'}).text
                
                title = remove_extra_characters(title)

                img = video_elem.find('img', attrs={'class':'_28_- img'})['src']

                data.append({"link":link, "title": title, "img": img })
            i+=1

    return data
    
url = input("Enter a Facebook Page Videos Page URL: ")

link_array = url.split('/')
file_name = link_array[link_array.index("videos")-1]

driver = webdriver.Chrome("./driver/chromedriver.exe")

driver.get(url)

time.sleep(1)

scroll_to_bottom(driver)

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')

results = soup.find(class_='gl4o1x5y')
video_elems = results.find_all('div',attrs={'class': 'kfpcsd3p'})

data = find_data(video_elems)

with open('data/' + file_name + ".json", "w", encoding='utf8') as write_file:
    json.dump(data, write_file, ensure_ascii=False)

print("Successfully Fetched")
driver.close()