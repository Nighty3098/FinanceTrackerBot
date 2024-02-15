import sqlite3
from datetime import datetime, timedelta, date


from config import *

month_name = date.today().strftime("%B")

async def create_connection(user_id):
    connection = sqlite3.connect(f"finances_{user_id}_{month_name}.db")
    cursor = connection.cursor()
    connection.close()


async def create_table(user_id):
    connection = sqlite3.connect(f"finances_{user_id}_{month_name}.db")
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
    now = datetime.now()
    connection = sqlite3.connect(f"finances_{user_id}_{month_name}.db")
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
    now = datetime.now()
    connection = sqlite3.connect(f"finances_{user_id}_{month_name}.db")
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
    connection = sqlite3.connect(f"finances_{user_id}_{month_name}.db")
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
        connection = sqlite3.connect(f"finances_{user_id}_{month}.db")
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


