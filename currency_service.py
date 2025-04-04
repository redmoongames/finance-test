import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import statistics
import concurrent.futures
from typing import List, Optional

from currency_models import Currency, CurrencyStatistics

class CurrencyService:
    
    def __init__(self, parallel_requests: int = 10):
        self.parallel_requests = parallel_requests
        self.base_url = "http://www.cbr.ru/scripts/XML_daily_eng.asp"
    
    def get_exchange_rates(self, date_str: str) -> List[Currency]:
        url = f"{self.base_url}?date_req={date_str}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Не удалось получить данные за {date_str}: {response.status_code}")
            return []
        
        return self._parse_xml_response(response.content, date_str)
    
    def get_rates_for_period(self, days: int = 90) -> List[Currency]:
        all_currencies = []
        date_strings = self._get_date_strings(days)
        
        print(f"Получение курсов валют за последние {days} дней...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.parallel_requests) as executor:
            future_to_date = {executor.submit(self.get_exchange_rates, date_str): date_str 
                             for date_str in date_strings}
            
            for future in concurrent.futures.as_completed(future_to_date):
                date_str = future_to_date[future]
                try:
                    currencies = future.result()
                    if currencies:
                        all_currencies.extend(currencies)
                        print(f"Получены данные за {date_str} - {len(currencies)} валют")
                    else:
                        print(f"Нет данных за {date_str}")
                except Exception as e:
                    print(f"Ошибка при получении данных за {date_str}: {e}")
        
        return all_currencies
    
    def get_statistics(self, days: int = 90) -> Optional[CurrencyStatistics]:
        all_currencies = self.get_rates_for_period(days)
        
        if not all_currencies:
            print("Данные не получены. Завершение работы.")
            return None
        
        max_currency = max(all_currencies, key=lambda x: x.rate)
        
        min_currency = min(all_currencies, key=lambda x: x.rate)
        
        average_rate = statistics.mean([currency.rate for currency in all_currencies])
        
        return CurrencyStatistics(
            max_currency=max_currency,
            min_currency=min_currency,
            average_rate=average_rate,
            currencies_count=len(all_currencies)
        )
    
    def _parse_xml_response(self, xml_content: bytes, date_str: str) -> List[Currency]:
        try:
            root = ET.fromstring(xml_content)
            currencies = []
            
            for valute in root.findall('Valute'):
                name = valute.find('Name').text
                value_str = valute.find('Value').text.replace(',', '.')
                value = float(value_str)
                nominal_str = valute.find('Nominal').text
                nominal = int(nominal_str)
                
                rate = value / nominal
                
                currencies.append(Currency(
                    code=valute.find('CharCode').text,
                    name=name,
                    rate=rate,
                    date=date_str
                ))
            
            return currencies
        except Exception as e:
            print(f"Ошибка при парсинге XML за {date_str}: {e}")
            return []
        
    def _get_date_strings(self, days: int) -> List[str]:
        today = datetime.now()
        date_strings = []
        for i in range(days):
            date = today - timedelta(days=i)
            date_strings.append(date.strftime("%d/%m/%Y"))
            
        return date_strings
