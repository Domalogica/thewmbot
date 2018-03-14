wada = """
ID 121 пр.Акушинского 30 [с ботом]
ID 221 ул.Научный городок 1 [с ботом]
ID 321 пр.Гамидова 81 [с ботом]
ID 421 пр.А.Султана 1 [с ботом]
ID 521 ул.Батырая 136л [с ботом]
ID 621 пр.Акушинского 28 [с ботом]
ID 721 пр.Насрутдинова 107 [с ботом]
ID 821 пр.Петра Первого 49д [с ботом]
ID 921 ул.Ирчи Казака 49к4 [с ботом]
ID 1021 пр.Гамидова 49к7 [с ботом]
ID 1121 пос. Ленинкент (центральная мечеть) [без бота]
ID 1221 ул.Газопроводная 107б [с ботом]
ID 1321 пр.Акушинского 31 [без бота]
ID 1421 пр.Акушинского 11е [с ботом]
ID 1521 Индустриальный пр. 6в [с ботом]


Готовятся к установке

пр. Имама Шамиля 103
пр. Имама Шамиля 99
пр. Имама Шамиля 8
ул. Зоя Космодемьянская 54 а
ул. Зоя Космодемьянская 46 а
ул. Зоя Космодемьянская 52
пр.Петра первого 59
пр.Петра первого 59з
ул. Энгельса 24
"""
opp = "🤦"

f = "\nВ разделы Отзывы вы можете указать желаемое место установки водомата.\nМы делаем все, чтобы вам было удобно!;)"

# token = config["token"]

# pswd = config["pswd"]


text_welcome = "Добро пожаловать!\nПрисоединяйтесь к нам в соцсетях и получайте новые " \
               "идеи!\ninstagram.com/domalogica/\nfb.com/domalogica @proektSV\nУ вас 25 подарочных литров Свежей воды."

text_start = "Добро пожаловать!\nВы получили 25 литров воды бесплатно!\nПрисоединяйтесь к нам в соцсетях и получайте " \
             "новые идеи!\ninstagram.com/domalogica/\nfb.com/domalogica @proektSV"

text_get = "Выберите один из пунктов меню"

text_id = "Введите ID водомата"

text_price = "Введите цену за литр:"

text_vol = "Введите объем"

command_error = "Ошибка ввода!"

balance_empty = "Недостаточно средств для совершения покупки ("

text_water = "\n\n1. Установите тару в водомат\n\n2. Нажмите кноку \"Старт\" на аппарате.\n\n Цена за 1 литр 4₽\n\n" \
             "Чтобы пополнить баланс используйте купюроприемник и монетоприемник.\n\nВаш баланс: "

text_wait = "Подождите, идет подключение к водомату..."

text_c = "Введите ресурс картриджа:"

filters_command = "Выберите ресурсы фильтрова из меню!"

status_water = "Подождите, водомат используется другим пользователем..."

text_error = "Команда не найдена ("

text_personal = "Ваш личный кабинет"

text_review = "Поделитесь вашим впечатлением"

text_review_answer = "Спасибо за ваш отзыв!"

location = "Отправьте локализацию где вы желаете видеть водомат."

back_menu_list = ["Назад"]

stop_menu_list = ["Остановить"]

main_menu_list = [
    "Подключиться к водомату",
    "Личный кабинет",
    "Обратная связь"
]

personal_menu_list = [
    "Баланс",
    # "Ближайшие водоматы",
    # "Промокод",
    # "Статистика",
    "Адреса водоматов"
]

admin_menu_list = [
    # "Мониторинг",
    "Админ панель"
    # "Управление"
]

admin_menu_stat = [
    # "Мониторинг",
    "Статистика",
    "Текущее состояние",
    "Активные водоматы"
    # "Управление"
]

stat = [
    "Моя статистика",
    "Статистика по водоматам"
]

my_stat = [
    "За сутки",
    "За неделю"
]

stat_menu = [
    "Количество продаж всего за суки",
    "Количество продаж через бот",
    "Количество проданных литров за сутки",
    "Количество проданных литров через бот",
    "Количество бесплатно выданных литров через бот",
    "Продажи в рублях всего за сутки",
    "Продажи в рублях через бот"
]

feedback_menu = [
    "Оставить отзыв"
]

# menu = {
#     "Подключиться к водомату": ["Назад"],
#     "Личный кабинет": ["Баланс", "Оставить отзыв", "Ближайшие водоматы"]
# }
