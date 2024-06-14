import os
import sys

import loguru
import pretty_errors
from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.types import *
from aiogram.utils.markdown import *
from loguru import *

from db import *

TOKEN = os.getenv("FTB_TOKEN")
log_file = "~/logs/FTB.log"

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

whitelist = ["1660218648"]

monthes = [
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
    "December"
]

logger = loguru.logger

logger.level("DEBUG", color="<green>")
logger.level("INFO", color="<cyan>")
logger.level("WARNING", color="<yellow>")
logger.level("CRITICAL", color="<red>")

logger.add(
    log_file,
    level="DEBUG",
    rotation="1000 MB",
    retention="31 days",
    backtrace=True,
    diagnose=True,
)

