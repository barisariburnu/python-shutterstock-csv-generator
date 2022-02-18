# -*- coding: utf-8 -*-

import os
import config
import requests
from bs4 import BeautifulSoup
from model import ShutterStock
from model import AdobeStock


BASE_URI = 'http://www.countryflags.com'


def get_country_list():
    response = requests.get(BASE_URI)

    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, "html.parser")
    tiles = soup.find_all("div", {"class": "thumb"})
    urls = []

    for tile in tiles:
        url = tile.find('a')['href'].split('/')[-2:-1][0]
        title = tile.find('a').getText()
        urls.append({
            url: title
        })

    return urls


def get_photo_details(filename):
    query = filename.split('-flag')[0]
    flag_types = filename.split('-flag')[1] if filename.split('-flag')[1] else None

    if query == 'vanuatu':
        url = f"{BASE_URI}/vanuatu-flag"
    elif query == 'north-korea':
        url = f"{BASE_URI}/flag-of-korea-north"
    elif query == 'south-korea':
        url = f"{BASE_URI}/flag-of-korea-south"
    else:
        url = f"{BASE_URI}/flag-of-{query}"
    response = requests.get(url, verify=False)

    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, "html.parser")

    description = soup.find(class_="content").getText()
    country = soup.find_all(class_="col-7")[0].getText().strip().lower()
    continent = soup.find_all(class_="col-7")[1].getText().strip().lower()
    tags = [continent, country]

    if len(soup.find_all(class_="col-7")) >= 3:
        capital = soup.find_all(class_="col-7")[3].getText().strip().lower().split("(")[0]
        tags.append(capital)

    tags.append('flag')
    tags.extend(flag_types.split('-')[1:])
    tags.extend([tag.getText().strip().lower() for tag in soup.find_all(class_="btn-secondary")])
    tags.extend([tag.getText().strip().lower() for tag in soup.find_all(class_="flag-color")])

    eps_title = f'Vector Flag of {country.title()}, {continent.title()}, Isolated on White Background.'
    jpg_title = f'Flag of {country.title()}, {continent.title()}, Isolated on White Background.'

    tags.extend(config.TAGS)
    tags = ','.join(tags[:50])

    return {
        'eps_title': eps_title,
        'jpg_title': jpg_title,
        'description': description,
        'keywords': tags
    }


def export_to_csv(path, data, filename, header):
    with open(os.path.join(path, filename), "w") as f:
        f.write(f'{",".join(header)}\n')
        f.writelines('\n'.join(data))


class CsvGenerator:
    def __init__(self, source_path, category="Signs/Symbols", category_id=8):
        self.source_path = source_path
        self.category = category
        self.category_id = category_id

    def export_to_csv(self, data, filename, header):
        with open(os.path.join(self.source_path, filename), "w", encoding="utf-8") as f:
            f.write(f'{",".join(header)}\n')
            f.writelines('\n'.join(data))

    def generate(self):
        print(f'Executing path: {self.source_path}')
        continents = [f for f in os.listdir(self.source_path) if not os.path.isfile(os.path.join(self.source_path, f))]

        for continent in continents:
            continent_path = os.path.join(self.source_path, continent)
            countries = [f for f in os.listdir(continent_path) if not os.path.isfile(os.path.join(continent_path, f))]

            for country in countries:
                country_path = os.path.join(self.source_path, continent, country)
                files = [f for f in os.listdir(country_path) if os.path.isfile(os.path.join(country_path, f))]

                shutter_stock_data = []
                adobe_stock_data = []
                data = {}
                for f in files:
                    filename = os.path.splitext(os.path.basename(f))[0]
                    extension = os.path.splitext(os.path.basename(f))[1]

                    if extension not in ['.eps']:
                        continue

                    if not data:
                        data = get_photo_details(filename=filename)

                    try:
                        data['filename'] = filename
                        data['category'] = self.category
                        data['category_id'] = self.category_id

                        shutter_stock = ShutterStock(data)
                        shutter_stock_data.extend(shutter_stock.to_array())

                        adobe_stock = AdobeStock(data)
                        adobe_stock_data.extend(adobe_stock.to_array())

                        print(f'[Add file]: {f}')
                    except Exception as e:
                        print(f'[Error]: {e}')

                self.export_to_csv(
                    shutter_stock_data,
                    os.path.join(continent, country, config.SHUTTER_FILENAME),
                    config.SHUTTER_HEADER
                )
                self.export_to_csv(
                    adobe_stock_data,
                    os.path.join(continent, country, config.ADOBE_FILENAME),
                    config.ADOBE_HEADER
                )
