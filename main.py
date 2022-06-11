#!/home/dmytro/PycharmProjects/Currency_exchange_rate/venv/bin/python3


import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os.path import exists
import csv
from datetime import date


url_reiff = 'https://raiffeisen.ua/currency'
destination_file = '/home/dmytro/Desktop/currencies.csv'


def get_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url=url)
        driver.implicitly_wait(20)
        html_page = driver.page_source
        driver.close()
    except Exception as ex:
        print(ex)
        return None

    # with open('index.html', 'w') as file:
    #     file.write(html_page)
    return html_page


def get_currency_rate(html_file):
    # with open(html_file) as file:
    #     html = file.read()

    soup = BeautifulSoup(html_file, 'lxml')

    currency_list = []

    today = date.today()
    # dd.mm.YYYY
    check_date = today.strftime("%d.%m.%Y")
    currency_list.append(check_date)

    nbu_list = soup.find('div', class_='exchange-rate-wide-body__main').find_all('div', class_='value-rate-block__data')
    euro_nbu = nbu_list[0].text.strip()
    usd_nbu = nbu_list[1].text.strip()
    currency_list.append(euro_nbu)          # dd.mm.YYYY, euro_nbu
    currency_list.append(usd_nbu)           # dd.mm.YYYY, euro_nbu, usd_nbu

    currency_block_list = soup.find('div', class_='bank-rate-body__body-main-block')\
        .find_all('div', class_='value-rate-block__data')

    for each in currency_block_list:
        currency_list.append(each.text.strip())
    # dd.mm.YYYY, euro_nbu, usd_nbu, euro_buy, euro_cell, usd_buy, uds_cell, pln_buy, pln_cell

    del currency_list[-2:]
    # dd.mm.YYYY, euro_nbu, usd_nbu, euro_buy, euro_cell, usd_buy, uds_cell

    cross_exchange_rate_block_list = soup.find_all('div', class_='col-md-6 exchange-rate-kros-info__col')

    cross_exchange_rate_list = []
    for each in cross_exchange_rate_block_list:
        cross_exchange_rate_list.append(each.text.strip())

    usd_eur = cross_exchange_rate_list[0].split('\n')[1].strip()[:-1]       # USD/EUR
    eur_usd = cross_exchange_rate_list[1].split('\n')[1].strip()[:-1]       # EUR/USD

    currency_list.append(usd_eur)   # euro_nbu, usd_nbu, euro_buy, euro_cell, usd_buy, uds_cell, USD/EUR
    currency_list.append(eur_usd)   # euro_nbu, usd_nbu, euro_buy, euro_cell, usd_buy, uds_cell, USD/EUR, EUR/USD
    return currency_list


def write_data(csv_file, currency_list):

    if not exists(csv_file):
        with open(csv_file, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    'Дата',
                    'EUR НБУ',
                    'USD НБУ',
                    'EUR Покупка в касі',
                    'EUR Продаж в касі',
                    'EUR Покупка online',
                    'EUR Продаж online',
                    'USD Покупка в касі',
                    'USD Продаж в касі',
                    'USD Покупка online',
                    'USD Продаж online',
                    'USD/EUR',
                    'EUR/USD'
                )
            )

    with open(csv_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(
            currency_list
        )

    print('Job is done!')


def send_message():
    title = 'Курс валют'
    message = 'Перевірку виконано'
    os.system(f'notify-send "{title}" "{message}"')


def main():
    page = get_page(url_reiff)
    currencies = get_currency_rate(page)
    write_data(destination_file, currencies)
    send_message()


if __name__ == '__main__':
    main()
