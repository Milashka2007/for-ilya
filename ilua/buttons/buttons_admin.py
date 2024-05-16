from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
admin_kb=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать встречу'),
            KeyboardButton(text='Отменить/перенести встречу'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Чем могу быть полезен?'
)
change_kb=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить время'),
            KeyboardButton(text='Изменить дату'),
            KeyboardButton(text='Изменить назвнание'),
            KeyboardButton(text='Удалить встречу'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Чем могу быть полезен?'
)
