from dataclasses import dataclass

@dataclass
class Currency:
    """Модель для представления валюты и её курса"""
    code: str
    name: str
    rate: float
    date: str
    
    def __str__(self) -> str:
        return f"{self.name} ({self.code}): {self.rate:.4f} RUB от {self.date}"

@dataclass
class CurrencyStatistics:
    """Модель для представления статистики по валютам"""
    max_currency: Currency
    min_currency: Currency
    average_rate: float
    currencies_count: int
    
    def __str__(self) -> str:
        return (
            f"\n===== РЕЗУЛЬТАТЫ =====\n"
            f"Максимальный курс: {self.max_currency.rate:.4f} RUB\n"
            f"Валюта: {self.max_currency.name} ({self.max_currency.code})\n"
            f"Дата: {self.max_currency.date}\n"
            f"\nМинимальный курс: {self.min_currency.rate:.4f} RUB\n"
            f"Валюта: {self.min_currency.name} ({self.min_currency.code})\n"
            f"Дата: {self.min_currency.date}\n"
            f"\nСредний курс по всем валютам: {self.average_rate:.4f} RUB\n"
            f"Всего проанализировано валют: {self.currencies_count}"
        ) 