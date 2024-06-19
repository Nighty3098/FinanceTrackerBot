import sqlite3
from datetime import datetime, timedelta, date
from types import resolve_bases

from config import *
from to_rus import *

month_name = date.today().strftime("%B")
now_year = str(datetime.now().strftime("%Y"))

async def create_connection(user_id):
    try:
        connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
        cursor = connection.cursor()
        connection.close()
    except Exception as err:
        logger.error(f"{err}")

async def create_table(user_id):
    try:
        connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS income  (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            value INTEGER NOT NULL,
            note TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS consumption  (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            value INTEGER NOT NULL,
            note TEXT
            )
            """
        )

        connection.commit()
        connection.close()
    except Exception as err:
        logger.error(f"{err}")


async def add_consumption(user_id, value, note):
    try:
        today = datetime.now()
        now = today.strftime("%d.%m.%Y")

        connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
        cursor = connection.cursor()

        logger.debug(
            cursor.execute(
                "INSERT INTO consumption (date, value, note) VALUES (?, ?, ?)",
                (now, value, note)
            )
        )

        connection.commit()
        connection.close()
    except Exception as err:
        logger.error(f"{err}")


async def add_income(user_id, value, note):
    try:
        today = datetime.now()
        now = today.strftime("%d.%m.%Y")
        connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
        cursor = connection.cursor()

        logger.debug(
            cursor.execute(
                "INSERT INTO income (date, value, note) VALUES (?, ?, ?)",
                (now, value, note)
            )
        )

        connection.commit()
        connection.close()
    except Exception as err:
        logger.error(f"{err}")


async def get_summary(user_id):
    try:
        connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
        cursor = connection.cursor()

        cursor.execute("SELECT SUM(value) FROM income")
        sum_income = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(value) FROM consumption")
        sum_consumption = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if sum_consumption is not None and sum_income is not None:
            result = f"Ваша статистика за текущий месяц:\n+{str(sum_income)}\n-{str(sum_consumption)}\n\n{str(int(sum_income) - int(sum_consumption))} руб."
        else:
            result = f"Ваша статистика за текущий месяц:\n+{str(sum_income)}\n-{str(sum_consumption)}"
            result = result.replace('None', '0')
    
        return result

    except Exception as err:
        logger.error(f"{err}")


async def get_summary_by_month(user_id, month):
    try:
        connection = sqlite3.connect(f"data/finances_{user_id}_{month}_{now_year}.db")
        cursor = connection.cursor()

        cursor.execute("SELECT SUM(value) FROM income")
        sum_income = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(value) FROM consumption")
        sum_consumption = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if sum_consumption is not None and sum_income is not None:
            result = f"Данные за {str(await rus_month(month_name))}:\n+{str(sum_income)}\n-{str(sum_consumption)}\n\n{str(int(sum_income) - int(sum_consumption))} руб."
        else:
            result = f"Данные за {str(await rus_month(month_name))}:\n+{str(sum_income)}\n-{str(sum_consumption)}"
            result = result.replace('None', '0')

        return result
    except Exception as err:
        logger.error(f"{err}")


async def today(user_id):
    try:
        today = datetime.now()
        current_date = str(today.strftime("%d.%m.%Y"))

        connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
        cursor = connection.cursor()

        cursor.execute("SELECT SUM(value) FROM income WHERE date = ?", (current_date,))
        income = cursor.fetchall()

        cursor.execute("SELECT SUM(value) FROM consumption WHERE date = ?", (current_date,))
        consumption = cursor.fetchall()

        cursor.close()
        connection.close()

        if consumption[0][0] is not None and income[0][0] is not None:
            result = f"Статистика за {current_date}\n+ {str(income[0][0])} руб.\n- {str(consumption[0][0])} руб.\n\n{str(int(income[0][0]) - int(consumption[0][0]))} руб."
        else:
            result = f"Статистика за {current_date}\n+ {str(income[0][0])} руб.\n- {str(consumption[0][0])} руб."
            result = result.replace('None', '0')

    except Exception as err:
        logger.error(f"{err}")
    except AttributeError as err:
        logger.error(err)
        result = f"{monthes[i]: Отсутствуют данные}\n"
    return result



async def get_year_summary(user_id):
    try:
        message = " "

        year_income = 0
        year_consumption = 0

        for i in range(12):
            try:
                connection = sqlite3.connect(
                    f"data/finances_{user_id}_{monthes[i]}_{now_year}.db"
                )
                cursor = connection.cursor()

                cursor.execute("SELECT SUM(value) FROM income")
                total_income = cursor.fetchall()

                cursor.execute("SELECT SUM(value) FROM consumption")
                total_consumption = cursor.fetchall()

                message += f"\n{str(await rus_month(monthes[i]))}:\n+ {str(total_income[0][0])} руб.\n- {str(total_consumption[0][0])} руб."
                message = message.replace('None', '0')

                cursor.close()
                connection.close()

            except Exception as err:
                logger.error(f"{err}")
            except AttributeError as err:
                logger.error(err)
                message += f"{monthes[i]: Отсутствуют данные}\n"
        return message
    except Exception as err:
        logger.error(f"{err}")


async def get_summary_by_category(user_id, category, month):
    try:
        connection = sqlite3.connect(f"data/finances_{user_id}_{month}_{now_year}.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT SUM(value) FROM income WHERE note = ?", (category,)
        )
        income = cursor.fetchall()

        cursor.execute(
            "SELECT SUM(value) FROM consumption WHERE note = ?", (category,)
        )
        consumption = cursor.fetchall()

        cursor.close()
        connection.close()

        if consumption[0][0] is not None and income[0][0] is not None:
            result = f"{str(await rus_month(month))}\nСтатистика по категории: {str(await rus_category(category))}\n+ {str(income[0][0])} руб.\n- {str(consumption[0][0])} руб.\n\n{str(int(income[0][0]) - int*(consumption[0][0]))} руб."
        else:
            result = f"{str(await rus_month(month))}\nСтатистика по категории: {str(await rus_category(category))}\n+ {str(income[0][0])} руб.\n- {str(consumption[0][0])} руб."
            result = result.replace('None', '0')

        return result
    except Exception as err:
        logger.error(f"{err}")