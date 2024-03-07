
async def rus_category(category):
    if category == "Drive":
        ru_category = "Поездки"
    elif category == "Food":
        ru_category = "Еда"
    elif category == "Subscriptions":
        ru_category = "Подписки"
    elif category == "Books":
        ru_category = "Книги"
    elif category == "Other":
        ru_category = "Другое"
    elif category == "Courses":
        ru_category = "Обучение"
    elif category == "Work":
        ru_category = "Работа"
    else:
        ru_category = " "

    return ru_category

async def rus_month(month):
    if month == "December":
        ru_month = "Декабрь"
    elif month == "January":
        ru_month = "Январь"
    elif month == "February":
        ru_month = "Февраль"
    elif month == "March":
        ru_month = "Март"
    elif month == "April":
        ru_month = "Апрель"
    elif month == "May":
        ru_month = "Май"
    elif month == "June":
        ru_month = "Июнь"
    elif month == "July":
        ru_month = "Июль"
    elif month == "August":
        ru_month = "Август"
    elif month == "September":
        ru_month = "Сентябрь"
    elif month == "October":
        ru_month = "Октябрь"
    elif month == "November":
        ru_month = "Ноябрь"
    else:
        ru_month = " "

    return ru_month


