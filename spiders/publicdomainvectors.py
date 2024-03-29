import os
import config
import requests
from bs4 import BeautifulSoup
from model import ShutterStock, AdobeStock, Freepik, Vecteezy


def get_photo_details(filename):
    url = f"https://publicdomainvectors.org/en/free-clipart/details/{filename}.html"
    response = requests.get(url)

    if response.status_code != 200:
        return

    return response.text


def parse_photo_details(html):
    soup = BeautifulSoup(html, "html.parser")

    title = str(soup.find_all('h1')[0].get_text()).strip()
    tags = soup.find_all("div", {"class": "single-vector-tags"})[0]

    keywords = []
    for tag in tags:
        if str(tag).strip() != '':
            item = str(tag.find('a').get_text().strip().lower())
            if item not in ['openclipart', 'svg', 'ai', 'eps', 'clipart', 'clip art', 'vector']:
                keywords.append(item)

    keywords.extend(config.TAGS)
    keywords = ','.join(keywords[:50])

    return {
        'title': f'{title}, isolated background.'.title(),
        'keywords': keywords
    }


class CsvGenerator:
    def __init__(self, source_path, category, category_id=0):
        self.source_path = source_path
        self.category = category
        self.category_id = category_id

    def export_to_csv(self, data, filename, header):
        with open(os.path.join(self.source_path, filename), "w") as f:
            f.write(f'{header}\n')
            f.writelines('\n'.join(data))

    def generate(self):
        print(f'Executing path: {self.source_path}')
        only_files = [f for f in os.listdir(self.source_path) if os.path.isfile(os.path.join(self.source_path, f))]

        shutter_stock_data = []
        adobe_stock_data = []
        freepik_data = []
        vecteezy_data = []
        for f in only_files:
            filename = os.path.splitext(os.path.basename(f))[0]
            extension = os.path.splitext(os.path.basename(f))[1]

            if extension != '.eps':
                continue

            try:
                html = get_photo_details(filename=filename)
                data = parse_photo_details(html=html)
                data['filename'] = filename
                data['category'] = self.category
                data['category_id'] = self.category_id

                shutter_stock = ShutterStock(data)
                shutter_stock_data.extend(shutter_stock.to_array())
                adobe_stock = AdobeStock(data)
                adobe_stock_data.extend(adobe_stock.to_array())
                freepik = Freepik(data)
                freepik_data.extend(freepik.to_array())
                vecteezy = Vecteezy(data)
                vecteezy_data.extend(vecteezy.to_array())

                print(f'Add file: {f}')
            except Exception as ex:
                print(f'Error file: {filename}{extension} - {ex}')

        self.export_to_csv(shutter_stock_data, config.SHUTTER_FILENAME, ",".join(config.SHUTTER_HEADER))
        self.export_to_csv(adobe_stock_data, config.ADOBE_FILENAME, ",".join(config.ADOBE_HEADER))
        self.export_to_csv(freepik_data, config.FREEPIK_FILENAME, ";".join(config.FREEPIK_HEADER))
        self.export_to_csv(vecteezy_data, config.VECTEEZY_FILENAME, ",".join(config.VECTEEZY_HEADER))
