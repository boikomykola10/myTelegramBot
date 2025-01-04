import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

from keyboards import (
    first_keyboard, main_keyboard, number_keyboard, color_keyboard,
    type_of_trade_mark_keyboard, person_keyboard, additional_first_keyboard
)
from helpers import (
    calculate_cost_for_apply, calculate_cost_for_publication, welcome_message,
    choose_number_of_classes_message, get_reply_message_for_classes,
    get_reply_message_for_color, get_reply_message_for_person,
    last_step_message, get_final_message, get_message_for_search,
    message_for_legal_services, get_additional_message_for_history
)
from models import Base, UserChoice

BOT_TOKEN = config.BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)

engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

client_choices = {}


@bot.message_handler(commands=["start", "hello", "restart"])
def send_welcome(message):
    user = session.query(
        UserChoice
    ).filter(
        UserChoice.user_id == message.chat.id
    ).order_by(
        UserChoice.date_of_creation.desc()
    ).first()

    keyboard = first_keyboard
    additional_message = ""

    if user:
        additional_message = get_additional_message_for_history(user)
        keyboard = additional_first_keyboard

    bot.send_message(
        message.chat.id,
        welcome_message + additional_message,
        reply_markup=keyboard,
        parse_mode="html"
    )

    client_choices[message.chat.id] = {}


@bot.message_handler(
    func=lambda message: message.text == "Перейти до калькулятора"
)
def handle_calculation_button(message):
    bot.send_message(
        message.chat.id,
        choose_number_of_classes_message,
        reply_markup=number_keyboard
    )


@bot.message_handler(
    func=lambda message: message.text in ["1", "2", "3", "4", "5"]
)
def handle_number_selection(message):
    selected_number = int(message.text)
    reply_message = get_reply_message_for_classes(selected_number)

    bot.send_message(
        message.chat.id, reply_message, reply_markup=color_keyboard,
        parse_mode="html"
    )

    client_choices[message.chat.id]["number_of_classes"] = selected_number


@bot.message_handler(
    func=lambda message: message.text in ["Кольорова", "Чорно-біла"]
)
def handle_color_selection(message):
    selected_color = message.text
    reply_message = get_reply_message_for_color(selected_color)

    bot.send_message(
        message.chat.id, reply_message,
        reply_markup=type_of_trade_mark_keyboard, parse_mode="html"
    )

    client_choices[message.chat.id]["color"] = selected_color


@bot.message_handler(
    func=lambda message: message.text in [
        "Словесне/Зображувальне", "Комбіноване"
    ]
)
def handle_color_selection(message):
    selected_type_of_mark = message.text
    reply_message = get_reply_message_for_person(selected_type_of_mark)

    bot.send_message(
        message.chat.id, reply_message,
        reply_markup=person_keyboard, parse_mode="html"
    )

    client_choices[message.chat.id]["type_of_mark"] = selected_type_of_mark


@bot.message_handler(
    func=lambda message: message.text in ["Одна особа", "Декілька осіб"]
)
def handle_person_selection(message):
    selected_person = message.text
    client_choices[message.chat.id]["person"] = selected_person

    bot.send_message(
        message.chat.id,
        last_step_message,
        reply_markup=main_keyboard, parse_mode="html"
    )


@bot.message_handler(
    func=lambda message:
    message.text == "Адміністративні збори за реєстрацію ТМ"
)
def handle_calculation_admin_costs_button(message):
    cost_for_apply = calculate_cost_for_apply(client_choices[message.chat.id])
    cost_for_publication = calculate_cost_for_publication(
        client_choices[message.chat.id]
    )

    total_cost = int(cost_for_apply) + int(cost_for_publication) + 85

    reply_message = get_final_message(
        cost_for_apply, cost_for_publication, total_cost
    )

    bot.send_message(
        message.chat.id, reply_message,
        reply_markup=main_keyboard, parse_mode="html"
    )


@bot.message_handler(
    func=lambda message:
    message.text == "Адміністративні збори за попередній пошук"
)
def handle_calculation_previous_search_costs_button(message):
    if client_choices[message.chat.id].get("type_of_mark") != "Комбіноване":

        if client_choices[message.chat.id].get("number_of_classes") == "1":
            cost = 864
        else:
            cost = 864 + (
                int(client_choices[message.chat.id].get(
                    "number_of_classes")) * 174
            )

    else:

        if client_choices[message.chat.id].get("number_of_classes") == "1":
            cost = 1728
        else:
            cost = 1728 + (
                int(client_choices[message.chat.id].get(
                    "number_of_classes")) * 348
            )

    reply_message = get_message_for_search(cost)

    bot.send_message(
        message.chat.id, reply_message, parse_mode="html"
    )

    user = UserChoice(
        user_id=message.chat.id,
        number_of_classes=client_choices[message.chat.id].get(
            "number_of_classes"
        ),
        color=client_choices[message.chat.id].get("color"),
        type_of_mark=client_choices[message.chat.id].get("type_of_mark"),
        cost_for_apply=calculate_cost_for_apply(
            client_choices[message.chat.id]
        ),
        cost_for_publication=calculate_cost_for_publication(
            client_choices[message.chat.id]
        ),
        cost_for_search=cost
    )
    session.add(user)
    session.commit()


@bot.message_handler(
    func=lambda message: message.text == "Вартість юридичних послуг"
)
def handle_cost_of_legal_services_button(message):
    bot.send_message(
        message.chat.id,
        message_for_legal_services,
        parse_mode="html"
    )


@bot.message_handler(func=lambda message: message.text == "Історія")
def handle_history_button(message):
    user = session.query(
        UserChoice
    ).filter(
        UserChoice.user_id == message.chat.id
    ).order_by(
        UserChoice.date_of_creation.desc()
    ).first()

    reply_message = (
        "Вартість за попереднім вибором параметрів складає: \n" +
        get_final_message(
            user.cost_for_apply, user.cost_for_publication, user.cost_for_search
        ) + get_message_for_search(user.cost_for_search) +
        message_for_legal_services
    )

    bot.send_message(
        message.chat.id,
        reply_message,
        parse_mode="html"
    )


bot.infinity_polling()
