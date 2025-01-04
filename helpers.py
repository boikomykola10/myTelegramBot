matching_the_number_of_classes = {
    "1": "клас",
    "2": "класи",
    "3": "класи",
    "4": "класи",
    "5": "класів",
    "6": "класів"
}

welcome_message = (
    "Привіт. Це бот-калькулятор для підрахунку "
    "вартості реєстрації товарного знаку(ТМ). \n"
)
choose_number_of_classes_message = (
    "Оберіть кількість класів МКТП. Дізнатися інформацію про класи "
    "МКТП можна перейшовши за цим посиланням: "
    "https://nice.nipo.gov.ua/info/classes"
)
last_step_message = (
    "Дякую. Ваші вибори збережено. Оберіть дію, яку бажаєте виконати."
)
message_for_legal_services = (
    "Вартість юридичних послуг складає <b>4000</b> грн без проведення "
    "попереднього пошуку. \nЗ проведенням попереднього пошуку вартість "
    "юридичних послуг складає <b>5000</b> грн. \nПри виникненні питань "
    "звертайтесь за телефоном: \n<b>+380 96 244 56 35</b>. \n"
)


def get_additional_message_for_history(user):
    return (
        f"Ви вже користувалися послугами боту і востаннє Ви шукали "
        f"інформацію про ТМ з такими параметрами: \n"
        f"Кількість класів: <b>{user.number_of_classes}</b>. \n"
        f"Кольорова/чорно-біла: <b>{user.color}</b>. \n"
        f"Позначення словесне/зображувальне чи комбіноване: "
        f"<b>{user.type_of_mark}</b>. \n"
        f"Якщо Ви бажаєте змінити параметри пошуку, натисніть <b>'Перейти "
        f"до калькулятора'</b>. \nЯкщо Ви бажаєте отримати інформацію про "
        f"вартість за попереднім вибором параметрів, "
        f"натисніть <b>'Історія'</b>"
    )


def get_reply_message_for_classes(selected_number):
    return (
        f"Ви обрали <b>{selected_number}</b> "
        f"{matching_the_number_of_classes.get(str(selected_number))} МКТП. "
        f"Ваша ТМ кольорова чи чорно-біла?"
    )


def get_reply_message_for_color(selected_color):
    return (
        f"Ваша ТМ <b>{selected_color}</b>. Виберіть вид Вашого позначення."
    )


def get_reply_message_for_person(selected_person):
    return (
        f"Ваше позначення <b>{selected_person}</b>. "
        f"Заявку подає одна особа чи декілька?"
    )


def calculate_cost_for_apply(client_choices):
    number_of_classes = client_choices["number_of_classes"]
    cost = 3000 * number_of_classes

    if client_choices["color"] == "Кольорова":
        cost += 1000

    if client_choices["person"] == "Декілька осіб":
        cost *= 1.3

    return int(cost)


def calculate_cost_for_publication(client_choices):
    number_of_classes = client_choices["number_of_classes"]
    cost = 600 * number_of_classes

    return cost


def get_final_message(cost_for_apply, cost_for_publication, total_cost):
    return (
        f"Збір за подання заявки: <b>{cost_for_apply}</b> грн.\n"
        f"Збір за публікацію заявки: <b>{cost_for_publication}</b> грн.\n"
        f"Державне мито за видачу свідоцтва про реєстрацію ТМ: <b>85</b> грн.\n"
        f"Разом: <b>{total_cost}</b> грн.\n"
    )


def get_message_for_search(cost):
    return f"Вартість попереднього пошуку: <b>{cost}</b> грн. \n"
