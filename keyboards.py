from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
greet_kb = ReplyKeyboardMarkup()

button_1 = KeyboardButton('Доставка')
button_2 = KeyboardButton('Бронь столика')
button_3 = KeyboardButton('Обратный звонок')
button_4 = KeyboardButton('Отзывы')
button_5 = KeyboardButton('Контакты')
button_6 = KeyboardButton('Часто задаваемые вопросы')



greet_kb.row(button_1)
greet_kb.row(button_2, button_3)
greet_kb.row(button_4, button_5)
greet_kb.row(button_6)


review_btn_1 = KeyboardButton('Оставить отзыв')
review_btn_2 = KeyboardButton('Читать отзывы')
review_btn_3 = KeyboardButton('Назад в меню')

review_kb = ReplyKeyboardMarkup().row(review_btn_1).row(review_btn_2).row(review_btn_3)

admin_btn_1 = KeyboardButton('Создать рассылку')
admin_btn_2 = KeyboardButton('Редактировать меню')
admin_btn_3 = KeyboardButton('Редактировать текста')
admin_btn_4 = KeyboardButton('Модерация отзывов')
admin_btn_5 = KeyboardButton('Назад в меню')

admin_kb = ReplyKeyboardMarkup().row(admin_btn_1).row(admin_btn_2).row(admin_btn_3).row(admin_btn_4).row(admin_btn_5)

admin_kb_text_1 = KeyboardButton('Изменение title')
admin_kb_text_2 = KeyboardButton('Изменение text')
admin_kb_text_3 = KeyboardButton('Назад в Админ панель')

admin_kb_text = ReplyKeyboardMarkup().row(admin_kb_text_1).row(admin_kb_text_2).row(admin_kb_text_3)


button_ask_1 = KeyboardButton('Часто задаваемый вопрос 1')
button_ask_2 = KeyboardButton('Часто задаваемый вопрос 2')
button_ask_3 = KeyboardButton('Часто задаваемый вопрос 3')
button_ask_4 = KeyboardButton('Часто задаваемый вопрос 4')
button_ask_5 = KeyboardButton('Часто задаваемый вопрос 5')
button_ask_6 = KeyboardButton('Назад в меню')
ask_kb = ReplyKeyboardMarkup().row(button_ask_1).row(button_ask_2).row(button_ask_3).row(button_ask_4).row(button_ask_4).row(button_ask_5).row(button_ask_6)

admin_menu_btn_1 = KeyboardButton('Добавление')
admin_menu_btn_2 = KeyboardButton('Редактирование')
admin_menu_btn_3 = KeyboardButton('Удаление')
admin_menu_back_btn = KeyboardButton('Вернуться в редактирование меню')

admin_menu_kb = ReplyKeyboardMarkup().row(admin_menu_btn_1).row(admin_menu_btn_2).row(admin_menu_btn_3).row(admin_kb_text_3)

admin_menu_add_btn_1 = KeyboardButton('Добавить основные категории')
admin_menu_add_btn_2 = KeyboardButton('Добавить подкатегории')
admin_menu_add_btn_3 = KeyboardButton('Добавить конкретное блюдо')

admin_menu_add_kb = ReplyKeyboardMarkup().row(admin_menu_add_btn_1).row(admin_menu_add_btn_2).row(admin_menu_add_btn_3).row(admin_menu_back_btn)

admin_menu_del_btn_1 = KeyboardButton('Удалить основные категории')
admin_menu_del_btn_2 = KeyboardButton('Удалить подкатегории')
admin_menu_del_btn_3 = KeyboardButton('Удалить конкретное блюдо')

admin_menu_del_kb = ReplyKeyboardMarkup().row(admin_menu_del_btn_1).row(admin_menu_del_btn_2).row(admin_menu_del_btn_3).row(admin_menu_back_btn)

admin_menu_red_btn_1 = KeyboardButton('Редактировать основные категории')
admin_menu_red_btn_2 = KeyboardButton('Редактировать подкатегории')
admin_menu_red_btn_3 = KeyboardButton('Редактировать конкретное блюдо')

admin_menu_red_kb = ReplyKeyboardMarkup().row(admin_menu_red_btn_1).row(admin_menu_red_btn_2).row(admin_menu_red_btn_3).row(admin_menu_back_btn)

admin_menu_edit_prod_1 = KeyboardButton('Редактировать Артикул')
admin_menu_edit_prod_2 = KeyboardButton('Редактировать Название')
admin_menu_edit_prod_3 = KeyboardButton('Редактировать Описание')
admin_menu_edit_prod_4 = KeyboardButton('Редактировать Вес')
admin_menu_edit_prod_5 = KeyboardButton('Редактировать Цену')
admin_menu_edit_prod_6 = KeyboardButton('Редактировать Фото')


admin_menu_edit_prod_kb = ReplyKeyboardMarkup().row(admin_menu_edit_prod_1).row(admin_menu_edit_prod_2).row(admin_menu_edit_prod_3).row(admin_menu_edit_prod_4).row(admin_menu_edit_prod_5).row(admin_menu_edit_prod_6)

var_to_pay_btn_1 = KeyboardButton('Наличная оплата при доставке')
var_to_pay_btn_2 = KeyboardButton('Безналичная оплата')

var_to_pay_kb = ReplyKeyboardMarkup().row(var_to_pay_btn_1).row(var_to_pay_btn_2)
