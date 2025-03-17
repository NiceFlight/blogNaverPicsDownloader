import os
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup

HEADERS = {
            User-Agent": "Mozilla/5.0 (Windows NT 10.0; "
                            "Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) "
                            "Chrome/126.0.0.0 Safari/537.36"
            }

url = input('Enter the url you want to download: ')
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)


# find the counts of photos
def Countsofphotos(url):
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    imgs = soup.find_all("a", class_="se-module-image-link __se_image_link __se_link")
    imgs_length = len(imgs)
    return imgs_length

def Downloadphotos(imgs_length):
    if not os.path.exists('images'):
        os.makedirs('images')
    for img in range(imgs_length):
        # the photoview url
        photo_url = f'{url}&photoView={img}'
        driver.get(photo_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_url = soup.find('img', class_='cpv__img cpv__fade').get('data-src')
        file_extension = img_url.split('?')[0].split('.')[-1]

        download_photo = requests.get(img_url, headers=HEADERS, stream=True)

        if download_photo.status_code == 200:
            with open(f"images/{img}.{file_extension}", 'wb') as file:
                file.write(download_photo.content)
            print(f"{img} downloading{"." * 20}\n")
        else:
            print(f'download {img}.{file_extension} failed!')
    print('finished')
    driver.quit()

if __name__ == '__main__':
    Downloadphotos(Countsofphotos(url))
