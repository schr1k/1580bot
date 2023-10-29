import pdf2image
import requests

from bot import config


def parse_menu():
    url1 = 'https://prikaz.1580.ru/sites/prikaz.1580.ru/files/food/13.pdf'
    url2 = 'https://prikaz.1580.ru/sites/prikaz.1580.ru/files/food/14.pdf'
    url3 = 'https://prikaz.1580.ru/sites/prikaz.1580.ru/files/food/15.pdf'

    urls = [url1, url2, url3]
    for building, url in enumerate(urls):
        pdf = requests.get(url=url, stream=True)
        image = pdf2image.convert_from_bytes(pdf.content, poppler_path=config.POPPLER_PATH)
        image[0].save(f'{config.PROJECT_PATH}/src/food/{building + 1}.jpg', 'JPEG')
