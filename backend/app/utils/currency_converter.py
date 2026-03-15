"""
Currency Converter - Converts between currencies and determines destination currency.
"""
from typing import Dict, Tuple, Optional


class CurrencyConverter:
    """Handles currency conversion and destination currency detection."""
    
    # Approximate exchange rates (USD base)
    # In production, use real-time API like exchangerate-api.com
    EXCHANGE_RATES = {
        'USD': 1.0,
        'EUR': 0.92,
        'GBP': 0.79,
        'JPY': 149.50,
        'INR': 83.12,
        'AUD': 1.53,
        'CAD': 1.36,
        'CHF': 0.88,
        'CNY': 7.24,
        'SGD': 1.34,
        'HKD': 7.83,
        'NZD': 1.67,
        'SEK': 10.89,
        'KRW': 1337.50,
        'NOK': 10.87,
        'MXN': 17.08,
        'BRL': 4.97,
        'ZAR': 18.65,
        'RUB': 92.50,
        'TRY': 32.15,
        'AED': 3.67,
        'SAR': 3.75,
        'THB': 35.82,
        'IDR': 15678.0,
        'MYR': 4.72,
        'PHP': 56.35,
        'PLN': 4.03,
        'DKK': 6.86,
        'CZK': 23.15,
        'HUF': 361.50,
        'ILS': 3.66,
        'CLP': 973.50,
        'ARS': 1012.50,
        'COP': 3925.0,
        'EGP': 48.75,
        'PKR': 278.50,
        'BDT': 109.75,
        'VND': 24515.0,
        'NGN': 1555.0,
        'UAH': 41.25,
        'RON': 4.57,
        'BGN': 1.80,
        'HRK': 6.93,
        'ISK': 138.50,
        'QAR': 3.64,
        'KWD': 0.31,
        'OMR': 0.38,
        'BHD': 0.38,
        'JOD': 0.71
    }
    
    # City to currency mapping
    CITY_CURRENCIES = {
        # Europe
        'paris': 'EUR', 'france': 'EUR', 'lyon': 'EUR', 'nice': 'EUR', 'marseille': 'EUR',
        'london': 'GBP', 'uk': 'GBP', 'edinburgh': 'GBP', 'manchester': 'GBP',
        'amsterdam': 'EUR', 'rotterdam': 'EUR', 'netherlands': 'EUR',
        'berlin': 'EUR', 'munich': 'EUR', 'hamburg': 'EUR', 'germany': 'EUR',
        'rome': 'EUR', 'milan': 'EUR', 'venice': 'EUR', 'florence': 'EUR', 'italy': 'EUR',
        'barcelona': 'EUR', 'madrid': 'EUR', 'seville': 'EUR', 'spain': 'EUR',
        'lisbon': 'EUR', 'porto': 'EUR', 'portugal': 'EUR',
        'vienna': 'EUR', 'austria': 'EUR', 'salzburg': 'EUR',
        'prague': 'CZK', 'czech': 'CZK',
        'budapest': 'HUF', 'hungary': 'HUF',
        'warsaw': 'PLN', 'krakow': 'PLN', 'poland': 'PLN',
        'athens': 'EUR', 'greece': 'EUR', 'santorini': 'EUR',
        'copenhagen': 'DKK', 'denmark': 'DKK',
        'stockholm': 'SEK', 'sweden': 'SEK',
        'oslo': 'NOK', 'norway': 'NOK',
        'zurich': 'CHF', 'geneva': 'CHF', 'switzerland': 'CHF',
        'brussels': 'EUR', 'belgium': 'EUR',
        'dublin': 'EUR', 'ireland': 'EUR',
        
        # Asia
        'tokyo': 'JPY', 'osaka': 'JPY', 'kyoto': 'JPY', 'japan': 'JPY',
        'bangkok': 'THB', 'phuket': 'THB', 'chiang mai': 'THB', 'thailand': 'THB',
        'singapore': 'SGD',
        'hong kong': 'HKD',
        'seoul': 'KRW', 'busan': 'KRW', 'korea': 'KRW',
        'taipei': 'TWD', 'taiwan': 'TWD',
        'shanghai': 'CNY', 'beijing': 'CNY', 'china': 'CNY',
        'bali': 'IDR', 'jakarta': 'IDR', 'indonesia': 'IDR',
        'kuala lumpur': 'MYR', 'penang': 'MYR', 'malaysia': 'MYR',
        'manila': 'PHP', 'philippines': 'PHP',
        'hanoi': 'VND', 'ho chi minh': 'VND', 'vietnam': 'VND',
        'mumbai': 'INR', 'delhi': 'INR', 'bangalore': 'INR', 'india': 'INR',
        'dubai': 'AED', 'abu dhabi': 'AED', 'uae': 'AED',
        'istanbul': 'TRY', 'turkey': 'TRY',
        
        # Americas
        'new york': 'USD', 'los angeles': 'USD', 'chicago': 'USD', 'miami': 'USD',
        'san francisco': 'USD', 'usa': 'USD', 'us': 'USD', 'america': 'USD',
        'toronto': 'CAD', 'vancouver': 'CAD', 'montreal': 'CAD', 'canada': 'CAD',
        'mexico city': 'MXN', 'cancun': 'MXN', 'mexico': 'MXN',
        'buenos aires': 'ARS', 'argentina': 'ARS',
        'rio': 'BRL', 'sao paulo': 'BRL', 'brazil': 'BRL',
        'lima': 'PEN', 'peru': 'PEN',
        'bogota': 'COP', 'colombia': 'COP',
        
        # Oceania
        'sydney': 'AUD', 'melbourne': 'AUD', 'australia': 'AUD',
        'auckland': 'NZD', 'new zealand': 'NZD',
        
        # Africa & Middle East
        'cairo': 'EGP', 'egypt': 'EGP',
        'johannesburg': 'ZAR', 'south africa': 'ZAR',
        'marrakech': 'MAD', 'morocco': 'MAD',
    }
    
    def __init__(self):
        """Initialize currency converter."""
        pass
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount from one currency to another."""
        if from_currency == to_currency:
            return amount
        
        from_rate = self.EXCHANGE_RATES.get(from_currency, 1.0)
        to_rate = self.EXCHANGE_RATES.get(to_currency, 1.0)
        
        # Convert to USD first, then to target currency
        usd_amount = amount / from_rate
        converted = usd_amount * to_rate
        
        return round(converted, 2)
    
    def get_destination_currency(self, destination: str) -> str:
        """Determine the currency used in destination."""
        dest_lower = destination.lower().strip()
        
        # Check direct matches
        for city, currency in self.CITY_CURRENCIES.items():
            if city in dest_lower or dest_lower in city:
                return currency
        
        # Default to USD
        return 'USD'
    
    def format_currency(self, amount: float, currency: str) -> str:
        """Format amount with currency symbol."""
        symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'INR': '₹',
            'AUD': 'A$', 'CAD': 'C$', 'CHF': 'CHF', 'CNY': '¥', 'SGD': 'S$',
            'HKD': 'HK$', 'NZD': 'NZ$', 'SEK': 'kr', 'KRW': '₩', 'NOK': 'kr',
            'MXN': 'MX$', 'BRL': 'R$', 'ZAR': 'R', 'RUB': '₽', 'TRY': '₺',
            'AED': 'AED', 'SAR': 'SAR', 'THB': '฿', 'IDR': 'Rp', 'MYR': 'RM',
            'PHP': '₱', 'PLN': 'zł', 'DKK': 'kr', 'CZK': 'Kč', 'HUF': 'Ft',
            'ILS': '₪', 'CLP': 'CLP$', 'ARS': 'ARS$', 'COP': 'COP$',
            'EGP': 'E£', 'PKR': 'Rs', 'BDT': '৳', 'VND': '₫', 'NGN': '₦',
            'TWD': 'NT$', 'PEN': 'S/', 'MAD': 'MAD'
        }
        
        symbol = symbols.get(currency, currency + ' ')
        
        # Format large numbers with commas
        if amount >= 1000:
            formatted = f"{amount:,.2f}"
        else:
            formatted = f"{amount:.2f}"
        
        return f"{symbol}{formatted}"


# Singleton instance
currency_converter = CurrencyConverter()
