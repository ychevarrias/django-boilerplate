import random
from decimal import Decimal
from datetime import date
from django import template
register = template.Library()


def rand_price(start, end):
    entero = random.randint(start, end)
    decimal = random.randint(0, 99)
    return Decimal(f"{entero}.{'%02d' % decimal}")


def rand_name():
    year = date.today().year
    dataset = [
        ["Polo",       "Negro",        "Apple"],
        ["Polera",     "Rojo",         "Adidas"],
        ["Poleron",    "Dorado",       "Dolce & Gabana"],
        ["Cartera",    "Grey Space",   "Element"],
        ["Chompa",     "Golden Pink",  "Sony"],
        ["Billetera",  "Azulado",      "Renzo Costa"],
        ["Audífono",   "de lana",      "Anker"],
        ["Blazer",     f"{year}",      "Maui & sons"],
        ["Pantalon",   "fitness",      ""],
    ]
    tipo = random.choice([dato[0] for dato in dataset])
    adjetivo = random.choice([dato[1] for dato in dataset])
    marca = random.choice([dato[2] for dato in dataset])
    return f"{tipo} {adjetivo} {marca}"


@register.filter
def get_range(value):
    """
        Permite crear un loop con una variable inexistente
    """
    return range(value)


@register.filter
def get_rand_prices(value, rango):
    """
        retorna un loop con numeros aleatorios
    """
    def get_looper(length):
        for loop in range(length):
            _rango = [int(d) for d in rango.split(",")]
            yield rand_price(*_rango)
    return get_looper(value)


@register.filter
def get_products_dummy(length):
    """
        retorna un loop con numeros aleatorios
    """
    products = list()
    for loop in range(length):
        img_w = random.randint(480, 960)
        img_h = random.randint(480, 960)
        products.append({
            "nombre": rand_name(),
            "precio": rand_price(100, 10000),
            "stars": random.randint(0, 5),
            "imagen": f"https://picsum.photos/id/{loop}/{img_w}/{img_h}"
        })
    return products
