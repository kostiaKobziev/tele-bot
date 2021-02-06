from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
greet_kb = ReplyKeyboardMarkup()

button_1 = KeyboardButton('Доставка')
button_2 = KeyboardButton('Забронювати столик')
button_3 = KeyboardButton('Зворотний дзвінок')
button_4 = KeyboardButton('Відгуки')
button_5 = KeyboardButton('Контакти')
button_6 = KeyboardButton('Часто задавані питання')



greet_kb.row(button_1)
greet_kb.row(button_2, button_3)
greet_kb.row(button_4, button_5)
greet_kb.row(button_6)


review_btn_1 = KeyboardButton('Залишити відгук')
review_btn_2 = KeyboardButton('Читати відгук')
review_btn_3 = KeyboardButton('Назад в меню')

review_kb = ReplyKeyboardMarkup().row(review_btn_1).row(review_btn_2).row(review_btn_3)

admin_btn_1 = KeyboardButton('Створити розсилку')
admin_btn_2 = KeyboardButton('Редагувати меню')
admin_btn_3 = KeyboardButton('Редагувати текст')
admin_btn_4 = KeyboardButton('Модерація відгуків')
admin_btn_5 = KeyboardButton('Назад в меню')

admin_kb = ReplyKeyboardMarkup().row(admin_btn_1).row(admin_btn_2).row(admin_btn_3).row(admin_btn_4).row(admin_btn_5)

admin_kb_text_1 = KeyboardButton('Зміна title')
admin_kb_text_2 = KeyboardButton('Зміна text')
admin_kb_text_3 = KeyboardButton('Назад в Адмін панель')

admin_kb_text = ReplyKeyboardMarkup().row(admin_kb_text_1).row(admin_kb_text_2).row(admin_kb_text_3)


button_ask_1 = KeyboardButton('Часто задаваемый вопрос 1')
button_ask_2 = KeyboardButton('Часто задаваемый вопрос 2')
button_ask_3 = KeyboardButton('Часто задаваемый вопрос 3')
button_ask_4 = KeyboardButton('Часто задаваемый вопрос 4')
button_ask_5 = KeyboardButton('Часто задаваемый вопрос 5')
button_ask_6 = KeyboardButton('Назад в меню')
ask_kb = ReplyKeyboardMarkup().row(button_ask_1).row(button_ask_2).row(button_ask_3).row(button_ask_4).row(button_ask_4).row(button_ask_5).row(button_ask_6)

admin_menu_btn_1 = KeyboardButton('Додавання')
admin_menu_btn_2 = KeyboardButton('Редагування')
admin_menu_btn_3 = KeyboardButton('Видалення')
admin_menu_back_btn = KeyboardButton('Повернутися в редагування меню')

admin_menu_kb = ReplyKeyboardMarkup().row(admin_menu_btn_1).row(admin_menu_btn_2).row(admin_menu_btn_3).row(admin_kb_text_3)

admin_menu_add_btn_1 = KeyboardButton('Додати основні категорії')
admin_menu_add_btn_2 = KeyboardButton('Додати підкатегорії')
admin_menu_add_btn_3 = KeyboardButton('Додати конкретну страву')

admin_menu_add_kb = ReplyKeyboardMarkup().row(admin_menu_add_btn_1).row(admin_menu_add_btn_2).row(admin_menu_add_btn_3).row(admin_menu_back_btn)

admin_menu_del_btn_1 = KeyboardButton('Видалити основні категорії')
admin_menu_del_btn_2 = KeyboardButton('Видалити підкатегорії')
admin_menu_del_btn_3 = KeyboardButton('Видалити конкретну страву')

admin_menu_del_kb = ReplyKeyboardMarkup().row(admin_menu_del_btn_1).row(admin_menu_del_btn_2).row(admin_menu_del_btn_3).row(admin_menu_back_btn)

admin_menu_red_btn_1 = KeyboardButton('Редагувати основні категорії')
admin_menu_red_btn_2 = KeyboardButton('Редагувати підкатегорії')
admin_menu_red_btn_3 = KeyboardButton('Редагувати конкретну страву')

admin_menu_red_kb = ReplyKeyboardMarkup().row(admin_menu_red_btn_1).row(admin_menu_red_btn_2).row(admin_menu_red_btn_3).row(admin_menu_back_btn)

admin_menu_edit_prod_1 = KeyboardButton('Редагувати Артикул')
admin_menu_edit_prod_2 = KeyboardButton('Редагувати Назву')
admin_menu_edit_prod_3 = KeyboardButton('Редагувати Опис')
admin_menu_edit_prod_4 = KeyboardButton('Редагувати Вагу')
admin_menu_edit_prod_5 = KeyboardButton('Редагувати Ціну')
admin_menu_edit_prod_6 = KeyboardButton('Редагувати Фото')


admin_menu_edit_prod_kb = ReplyKeyboardMarkup().row(admin_menu_edit_prod_1).row(admin_menu_edit_prod_2).row(admin_menu_edit_prod_3).row(admin_menu_edit_prod_4).row(admin_menu_edit_prod_5).row(admin_menu_edit_prod_6)

var_to_pay_btn_1 = KeyboardButton('Готівкова оплата при доставці')
var_to_pay_btn_2 = KeyboardButton('Безготівкова оплата')

var_to_pay_kb = ReplyKeyboardMarkup().row(var_to_pay_btn_1).row(var_to_pay_btn_2)
