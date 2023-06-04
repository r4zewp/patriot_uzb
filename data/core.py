language_global = 'ru'

def set_language(language):
    global language_global
    language_global = language

sex_dict = {'m': {
                'ru': 'Мужские',
                'uz': 'Erkaklar'
            },
            'w': {
                'ru': 'Женские',
                'uz': 'Ayollar',
            },
        }

def price_to_string(price: int):
    return "{:,}".format(price).replace(",", ".")