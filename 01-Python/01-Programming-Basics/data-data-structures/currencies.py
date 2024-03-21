# pylint: disable=missing-docstring

RATES = {
    "USDEUR": 0.85,
    "GBPEUR": 1.13,
    "CHFEUR": 0.86
}

def convert(amount, currency):
    """returns the converted amount in the given currency
    amount is a tuple like (100, "EUR")
    currency is a string
    """
    from_currency = amount[1]
    original_sum = amount[0]


    if rate := RATES.get(currency + from_currency):
        converted_amount = original_sum * (1/rate)
        return round(converted_amount)

    if rate := RATES.get(from_currency + currency):
        converted_amount = original_sum * rate
        return round(converted_amount)

    return None
