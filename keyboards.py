from telebot import types


first_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
calculator_button = types.KeyboardButton("Перейти до калькулятора")
first_keyboard.add(calculator_button)

additional_first_keyboard = types.ReplyKeyboardMarkup(
    row_width=2, resize_keyboard=True
)
calculator_button = types.KeyboardButton("Перейти до калькулятора")
history_button = types.KeyboardButton("Історія")
additional_first_keyboard.add(calculator_button, history_button)

main_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
calculation_admin_costs_button = types.KeyboardButton(
    "Адміністративні збори за реєстрацію ТМ"
)
calculation_previous_search_costs_button = types.KeyboardButton(
    "Адміністративні збори за попередній пошук"
)
cost_of_legal_services_button = types.KeyboardButton(
    "Вартість юридичних послуг"
)
main_keyboard.add(
    calculation_admin_costs_button,
    calculation_previous_search_costs_button,
    cost_of_legal_services_button
)

# Second-level keyboard with number selection
number_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
for i in range(1, 6, 2):  # Iterate in steps of 2
    button1 = types.KeyboardButton(str(i))
    button2 = types.KeyboardButton(str(i + 1))
    number_keyboard.add(button1, button2)

color_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
color_button1 = types.KeyboardButton("Кольорова")
color_button2 = types.KeyboardButton("Чорно-біла")
color_keyboard.add(color_button1, color_button2)

type_of_trade_mark_keyboard = types.ReplyKeyboardMarkup(
    row_width=2, resize_keyboard=True
)
type_of_trade_mark_button1 = types.KeyboardButton("Словесне/Зображувальне")
type_of_trade_mark_button2 = types.KeyboardButton("Комбіноване")
type_of_trade_mark_keyboard.add(
    type_of_trade_mark_button1, type_of_trade_mark_button2
)

person_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
person_button1 = types.KeyboardButton("Одна особа")
person_button2 = types.KeyboardButton("Декілька осіб")
person_keyboard.add(person_button1, person_button2)
