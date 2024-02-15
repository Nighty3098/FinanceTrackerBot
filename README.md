<h1 align="center">Телеграм бот для отслеживания финансов</h1>
<h2 align="center">Команды</h2>

 - ```/month``` -  вывести все расходы и доходы за определённый месяц ( месяц выбирается через InlineKeyboardMarkup )
 - ```/year``` - вывести все расходы и доходы за год
 - ```/consumption``` - Добавить расход
 - ```/income``` - Добавить доход
 - ```/summary``` - Вывести итоговые данные за месяц


<h1 align="center">Installing</h1>

```
git clone https://github.com/Nighty3098/FinanceTrackerBot 
cd FinanceTrackerBot

python3 -m venv FTB
source FTB/bin/activate

pip3 install -r requirements.txt

FTB_TOKEN=%токен_вашего_бота% python3 main.py
```

