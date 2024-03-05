import sqlite3
from datetime import datetime, timedelta, date


from config import *


monthes = [
    "December",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
]
month_name = date.today().strftime("%B")
now_year = str(datetime.now().strftime("%Y"))




async def create_connection(user_id):
    connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
    cursor = connection.cursor()
    connection.close()


async def create_table(user_id):
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


async def add_consumption(user_id, value, note):
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


async def add_income(user_id, value, note):
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


async def get_summary(user_id):
    connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
    cursor = connection.cursor()

    cursor.execute("SELECT SUM(value) FROM income")
    sum_income = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(value) FROM consumption")
    sum_consumption = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    summarize = str(sum_income) + " " + str(sum_consumption)

    return summarize

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

        summarize = str(sum_income) + " " + str(sum_consumption)

        return summarize
    except sqlite3.OperationalError as err:
        logger.error(err)


async def today(user_id):
    try:
        today = datetime.now()
        current_date = str(today.strftime("%d.%m.%Y"))

        connection = sqlite3.connect(f"data/finances_{user_id}_{month_name}_{now_year}.db")
        cursor = connection.cursor()

        cursor.execute("SELECT SUM(value) FROM income WHERE date = ?", (current_date))
        income = cursor.fetchall()

        cursor.execute("SELECT SUM(value) FROM consumption WHERE date = ?", (current_date))
        consumption = cursor.fetchall()

        cursor.close()
        connection.close()

        result = " + " + str(income) + " руб\n" + " - " + str(consumption) + "руб"

        return result

    except sqlite3.OperationalError as err:
        logger.error(err)
    except sqlite3.ProgrammingError as err: 
        logger.error(err)
    except sqlite3.AttributeError as err:
        logger.error(err)

        return "Отсутствуют данные"


async def get_year_summary(user_id):
    message = " "

    for i in range(1, 13):
        try:
            connection = sqlite3.connect(
                f"data/finances_{user_id}_{monthes[i]}_{now_year}.db"
            )
            cursor = connection.cursor()

            cursor.execute("SELECT SUM(value) FROM income")
            total_income = cursor.fetchall()

            cursor.execute("SELECT SUM(value) FROM consumption")
            total_consumption = cursor.fetchall()

            message += f"{monthes[i]}: +{total_income} руб\n -{total_consumption} руб\n"
            
            cursor.close()
            connection.close()

        except sqlite3.OperationalError as err:
            logger.error(err)
        except sqlite3.ProgrammingError as err:
            logger.error(err)
        except sqlite3.AttributeError as err:
            logger.error(err)
            message += f"{monthes[i]: Отсутствуют данные}\n"

    return message
