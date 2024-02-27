from pathlib import Path
from bs4 import BeautifulSoup
import time
import requests
import os
from selenium import webdriver
os.environ['PATH']+=r"C:/Users/dell/Documents/WebScraping"
driver = webdriver.Chrome()
#Chrome Version 104.0.5112.102 (Official Build) (32-bit) 

# Fetch the HTML content from the URL
url = 'https://www.eazydiner.com/dubai/restaurants/cuisines'
html_text = requests.get(url).text

soup = BeautifulSoup(html_text, 'lxml')

def sanitize_folder_name(name):
    invalid_chars = '<>:"\\|?*'
    for ch in invalid_chars:
        name = name.replace(ch, '_')
    return name

# Fetches links for cuisines from the main page
links0=[]
blocks=soup.find_all('h3',class_='h3 bold ellipsis')
for link in blocks:
    links0.append(link.a['href'])

# Iterates over cuisine
for i in range(21,len(links0)):
    url=links0[i]
    cusine=url
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    # Fetches links for restaurants for each cuisisne
    links1=[]
    blocks=soup.find_all('div',class_='flex margin-t-10')
    for block in blocks:
        a_tag = block.find('a')
        if a_tag:
            links1.append(a_tag['href'])

    # Iterates over every restaurant
    for i in range(len(links1)):
        url='https://www.eazydiner.com'+links1[i]
        html_text = requests.get(url).text

        def download_image(url, folder_path, img_name):
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(folder_path, img_name), 'wb') as file:
                    file.write(response.content)

        # Opens web page dynamically to download images
        try:
            driver.get(url)
            time.sleep(1)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'lxml')

            title=soup.find('h1',class_='font-20 bold grey').text
            title=title.replace('\t','')
            jaga=sanitize_folder_name("/English_"+title+"_Dubai")
            print(jaga)
            folder=r"C:/Users/dell/Documents/WebScraping/images"+cusine[43::]+jaga
            Path(folder).mkdir(parents=True, exist_ok=True)

            container = soup.find('div', class_='menus_container')
            images = container.find_all('img')
            img_urls = [img['src'] for img in images if 'src' in img.attrs]

            for i, img_url in enumerate(img_urls):
                img_name = f'image_{i}.jpg'
                download_image(img_url, folder, img_name)

        finally:
            driver.quit()