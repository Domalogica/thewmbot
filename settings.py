import json

# file = open("/opt/key.json")

# text = file.read()sa

# config = json.loads(text)

wada = "1. г. Махачкала ул. Гамидова 81\n2. г. Махачкала ул. Батырая 136\n3. г. Махачкала ул. А. Султана 1\n4. г. Махачкала ул. Акушинского 28\n5. г. Махачкала ул. Акушинского 30\n6. г. Махачкала ул. Научный Городок 1\n7. г. Махачкала ул. Насрутдиного 107\n8. г. Махачкала ул. Петра первого 49д\n9. г. Махачкала ул. Ирчи Казака 49 к5\n10. г. Махачкала ул. Ирчи Казака 49 к9"

opp = "🤦"

f = "\nВ разделы Отзывы вы можете указать желаемое место установки водомата.\nМы делаем все, чтобы вам было удобно!;)"

# token = config["token"]

# pswd = config["pswd"]


text_welcome = "Добро пожаловать!\nПрисоединяйтесь к нам в соцсетях и получайте новые " \
			   "идеи!\ninstagram.com/domalogica/\nfb.com/domalogica "

text_start = "Добро пожаловать!\nВы получили 25 литров воды бесплатно!\nПрисоединяйтесь к нам в соцсетях и получайте " \
             "новые идеи!\ninstagram.com/domalogica/\nfb.com/domalogica "

text_get = "Выберите один из пунктов меню"

text_id = "Введите ID водомата"

text_price = "Введите цену за литр:"

text_vol = "Введите объем"

command_error = "Ошибка ввода!"

balance_empty = "Недостаточно средств для совершения покупки ("

text_water = "Подключение прошло успешно\n\n1. Поднесите тару к водомату\n\n2. Нажмите кноку \"Старт\" на аппарате.\n\n Цена за 1 литр 4₽\n\nЧтобы пополнить баланс используйте купюроприемник и монетоприемник."

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
	"Ближайшие водоматы",
	"Статистика"
]

admin_menu_list = [
	# "Мониторинг",
	"Статистика"#,
	# "Управление"
]


stat = [
	"Моя статистика",
	"Статистика по водоматам"
]

my_stat = [
	"За день",
	"За неделю",
	"За месяц"
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
	"Оставить отзыв",
	"Рекомендовать место"
]

# menu = {
#     "Подключиться к водомату": ["Назад"],
#     "Личный кабинет": ["Баланс", "Оставить отзыв", "Ближайшие водоматы"]
# }
