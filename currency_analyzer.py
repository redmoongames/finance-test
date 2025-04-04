from currency_service import CurrencyService
from currency_models import CurrencyStatistics
def main():
    """
    Основная функция программы
    """
    service = CurrencyService(parallel_requests=15)
    stats: CurrencyStatistics = service.get_statistics(days=90)
    print(stats)


if __name__ == "__main__":
    main() 