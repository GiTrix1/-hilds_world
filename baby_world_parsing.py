import csv
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


logger = logging.getLogger("baby_world")


def collect_data(geo_city='RU-MOW'):  # RU-SPE | Питер
    page = 1
    current_time = datetime.datetime.now().strftime('%d.%m.%Y_%H:%M')
    user_agent = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'User-Agent': user_agent.random
    }
    cookies = {
        'geoCityDMIso': f'{geo_city}'
    }
    if geo_city == 'RU-MOW' or geo_city == '':
        geo_city = 'г. Москва'
    else:
        geo_city = 'г. Санкт-Петербург'
    logger.info(f"Данные собираются по {geo_city}")
    print(f"Данные собираются по {geo_city}")
    with open(f'{geo_city}_{current_time}.csv', 'w', encoding='utf-8') as file_result:
        writer = csv.writer(file_result)
        writer.writerow(
            (
                'id',
                'title',
                'price',
                'promo_price',
                'url'
            )
        )
    logger.info("Записываю заголовки в файл")
    print("Записываю заголовки в файл")
    while page != 0:
        if page == 1:
            response = requests.get(url=f'https://www.detmir.ru/catalog/index/name/lego/', headers=headers,
                                    cookies=cookies)
            logger.info("Начал собирать данные с 1 страницы")
            print("Начал собирать данные с 1 страницы")
        else:
            response = requests.get(url=f'https://www.detmir.ru/catalog/index/name/lego/page/{page}/', headers=headers,
                                    cookies=cookies)
            logger.info(f"Начал собирать данные с {page} страницы")
            print(f"Начал собирать данные с {page} страницы")
        soup = BeautifulSoup(response.text, 'lxml')
        cards = soup.find_all('a', class_='Rl RN')
        if not cards:
            page = 0
            logger.info("Актуальных конструкторов LEGO больше нет.")
            continue
        for card in cards:
            card_id_goods_and_title = card.find('p', class_='Rp').text.split()
            card_price = card.find('p', class_='RA').text
            card_link = card.get('href')
            try:
                card_old_price = card.find('span', class_='RC').text
                with open(f'{geo_city}_{current_time}.csv', 'a', encoding='utf-8') as file_result:
                    writer = csv.writer(file_result)
                    writer.writerow(
                        (
                            card_id_goods_and_title[-1].strip('()'),
                            ' '.join(card_id_goods_and_title[:-1]),
                            card_old_price,
                            card_price,
                            card_link
                        )
                    )
            except AttributeError:
                with open(f'{geo_city}_{current_time}.csv', 'a', encoding='utf-8') as file_result:
                    writer = csv.writer(file_result)
                    writer.writerow(
                        (
                            card_id_goods_and_title[-1].strip('()'),
                            ' '.join(card_id_goods_and_title[:-1]),
                            card_price,
                            'Скидки нет',
                            card_link
                        )
                    )
        logger.info(f"Собрал данные с {page} страницы")
        print(f"Собрал данные с {page} страницы")
        page += 1
    print(f'{geo_city}_{current_time}.csv успешно создан!')


def main():
    city = input('Укажите ваш город в формате RU-MOW.\n'
                 'Москва - RU-MOW, Санкт-Петербург - RU-SPE. '
                 'Если вы ничего не укажите, то будет по умолчанию Москва\n'
                 'По умолчанию выбрана Москва: ')
    collect_data(geo_city=city)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="logs_baby_world.txt",
    )
    main()
