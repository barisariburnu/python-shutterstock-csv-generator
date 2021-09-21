import os
import sys
import config
import requests
from bs4 import BeautifulSoup
from model import ShutterStock


def get_photo_details(filename):
    url = f"https://publicdomainvectors.org/en/free-clipart/details/{filename}.html"
    response = requests.get(url)

    if response.status_code != 200:
        return

    return response.text


class CsvGenerator:
    def __init__(self, source_path, category, tag):
        self.source_path = source_path
        self.category = category
        self.tag = tag

    def __parse_photo_details(self, html):
        soup = BeautifulSoup(html, "html.parser")

        vector_details = soup.find_all("div", {"class": "vector-details"})
        title = str(vector_details[0].find_all('p')[0].get_text()).strip().replace('"', ' ').title()
        tags = soup.find_all("div", {"class": "single-vector-tags"})[0]

        cleared_title = []
        for item in title.lower().split('.'):
            if item.find('upload') > -1 or item.find('http') > -1 \
                    or item.find('openclipart') > -1 or item.find('domain') > -1 \
                    or item.find('public domain') or item.strip() == '':
                continue
            cleared_title.append(item)

        eps_title = '.'.join(cleared_title).title()
        jpg_title = eps_title.lower().replace('vector', '').replace('  ', ' ').title()

        keywords = []
        for tag in tags:
            if str(tag).strip() != '':
                item = str(tag.find('a').get_text().strip().lower())
                if item not in ['openclipart', 'svg', 'ai', 'eps']:
                    keywords.append(item)

        if self.tag == 'flag':
            keywords.extend(config.FLAG_TAGS)
        elif self.tag == 'symbol':
            keywords.extend(config.SIGNS_SYMBOLS_TAGS)
        elif self.tag == 'map':
            keywords.extend(config.MAP_TAGS)

        keywords = ','.join(keywords[:50])

        return {
            'eps_title': eps_title,
            'jpg_title': jpg_title,
            'keywords': keywords
        }

    def export_to_csv(self, data, filename, header):
        with open(os.path.join(self.source_path, filename), "w") as f:
            f.write(f'{",".join(header)}\n')
            f.writelines('\n'.join(data))

    def generate(self):
        only_files = [f for f in os.listdir(self.source_path) if os.path.isfile(os.path.join(self.source_path, f))]

        shutter_stock_data = []
        for f in only_files:
            filename = os.path.splitext(os.path.basename(f))[0]
            extension = os.path.splitext(os.path.basename(f))[1]

            if extension not in ['.eps', '.jpg']:
                continue

            html = get_photo_details(filename=filename)
            data = self.__parse_photo_details(html=html)
            data['filename'] = filename
            data['category'] = self.category

            shutter_stock = ShutterStock(data)
            shutter_stock_data.extend(shutter_stock.to_array())

            print(f'Add file: {f}')

        self.export_to_csv(shutter_stock_data, config.SHUTTER_FILENAME, config.SHUTTER_HEADER)


if __name__ == '__main__':
    path = sys.argv[1]
    category = sys.argv[2]
    tag = sys.argv[3]

    if not os.path.exists(path):
        print(f'[ERROR] No such path: "{path}"')
        exit(0)

    generator = CsvGenerator(path, category, tag)

