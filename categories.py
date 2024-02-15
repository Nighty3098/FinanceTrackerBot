from config import *

categories = {
    "Drive": ["такси", "поездка", "автобус", "метро", "машина", "поезд"],
    "Food": ["еда", "ресторан", "похавать", "кофе"],
    "Devices": ["днс", "девайсы", "пк"],
    "Subscription": [
        "подписка",
        "теле2",
        "музыка",
        "yt",
        "spotify",
        "netflix",
        "yandex",
    ],
    "Books": ["книги"],
    "Other": ["другое", " "],
    "Work": ["фриланс", "работа", "программирование", "разработка"],
}


async def change_category(text):
    for category, words in categories.items():
        if any(word in text for word in words):
            return category
