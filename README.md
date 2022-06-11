# Currency_exchange_rate
This script goes to https://raiffeisen.ua/currency and checks USD and EUR currency rate relating to UAH.

### To run this script you need to:
  - Install python interpreter version 3.10+ from:
    * https://www.python.org/;
  - Create virtual environment with **cli command**:
    * **python3 -m venv venv**;
  - Activate the virtual environment with:
    * **source venv/bin/activate**;
  - Install all dependencies from 'requirements.txt' with command:
    * **pip install -r requirements.txt**;

Received data will be written in .csv file (global variable '**destination_file**').

### It puts there:
  - current date,
  - official **EUR** and **USD** rate according to **National Bank of Ukraine**,
  - current exchange rate **EUR** to UAH according to **Raiffeisen Bank in Ukraine** both buy and cell,
  - current exchange rate **USD** to UAH according to **Raiffeisen Bank in Ukraine** both buy and cell,
  - current rate **USD/EUR** and **EUR/USD**
