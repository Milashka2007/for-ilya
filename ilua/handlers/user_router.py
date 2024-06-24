from aiogram import types, Router, F
from aiogram.filters import CommandStart

from buttons.buttons_user import start_kb, profile
from database.client import Database
from database.meet import Database1
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
user_router = Router()
db1=Database1('fio.db')
db=Database('fio.db')


class SelectMeet(StatesGroup):
    # Шаги состояний
    select_meet = State()

@user_router.message(CommandStart())
async def start(message: types.Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await message.answer('Для дальнейшего использования бота, укажите ФИО')
    else:
        user_nickname = db.get_nickname(message.from_user.id)
        await message.answer(f'Привет, {user_nickname}, вы в главном меню!', reply_markup=start_kb)

@user_router.message(F.text=='Мои записи')
async def profil(message: types.Message):
    client=db1.client_exists()
    nickname=db.get_nickname(message.from_user.id)
    if nickname in client:
        meet= db1.meet_by_client(nickname)
        time = db.time_zapis(meet)
        date = db.date_zapis(meet)
        await message.answer(f'Ваши записи: {meet}\n'
                             f'Время: {time}\n'
                             f'Дата: {date}', reply_markup=start_kb)
    else:
        await message.answer('У вас пока не записей', reply_markup=start_kb)
@user_router.message(F.text=='Профиль')
async def profil(message: types.Message):
    user_nickname = 'Ваше ФИО: ' + db.get_nickname(message.from_user.id)
    await message.answer(user_nickname, reply_markup=profile)

@user_router.message(F.text=='Отменить запись')
async def no_zapis(message: types.Message):
    zapis_na_vstrechy = db1.client_exists()
    nickname=db.get_nickname(message.from_user.id)
    if nickname in zapis_na_vstrechy:
        zapis = db1.meet_by_client(nickname)
        null='None'
        status='Можно записаться'
        db1.add_zapis_meet(status, zapis)
        db.update_zapis(zapis, null)
        await message.answer('Запись успешно удалена!',reply_markup=start_kb)
    else:
        await message.answer('Записей пока нет(', reply_markup=start_kb)


@user_router.message(F.text=='Изменить ник')
async def changenick(message: types.Message):
    await message.answer('напишите свое ФИО')
    db.set_signup(message.from_user.id, 'setnickname')

@user_router.message(F.text=='В меню')
async def menu(message: types.Message):
    await message.answer('Перевожу вас в главное меню!', reply_markup=start_kb)

@user_router.message(F.text=='Записаться на встречу')
async def zapis(message: types.Message, state: FSMContext):
        zapis_na_vstrechy=db1.client_exists()
        if not(db.get_nickname(message.from_user.id) in zapis_na_vstrechy):
            meet = db1.name_meet1()
            message_to_answer = ''
            number = 1
            if len(meet)==0:
                await message.answer('Встреч пока нет, но скоро будут!')
            else:
                for names in range(0, len(meet) - 2, 4):
                    zapis = meet[names]
                    name = meet[names + 1]
                    time = meet[names + 2]
                    date = meet[names + 3]
                    message_to_answer += f'{number}.Название встречи: {name}\nДата: {date}\nВремя: {time}\nСтатус: {zapis}\n'  #дз ваше
                    number += 1
                await message.answer('Выберите название встречи, в которую хотите записаться.\n'
                                     'Можно записаться лишь в одну группу!\n'
                                     'Если же вы передумали записываться, то просто напишите "Назад"')
                await message.answer(message_to_answer, reply_markup=types.ReplyKeyboardRemove())
                await state.set_state(SelectMeet.select_meet)
        else:
            await message.answer('Вы уже записаны на встречу, сначала отменитe запись!')

@user_router.message(F.text.lower()=='назад')
async def back(message: types.Message, state: FSMContext):
    await message.answer('Перевожу вас в главное меню!', reply_markup=start_kb)
    await state.clear()


@user_router.message(SelectMeet.select_meet, F.text)
async def zapis(message: types.Message, state: FSMContext):
    await state.update_data(select_meet=message.text)
    chose=message.text
    if db1.meet_exists(chose):
        if db.zapis_for_registration(chose)=='Можно записаться':
            status='Мест нет'
            meet= await state.get_data()
            zapis=meet['select_meet']
            user_name=db.get_nickname(message.from_user.id)
            db.zapis_meet(zapis,user_name)
            db1.add_zapis_meet(status, zapis)
            await message.answer('Вы успешно записаны на эту встречу', reply_markup=start_kb)
            await state.clear()
        else:
            await message.answer('На эту встречу мест нет')
    else:
        await message.answer('Такой встречи нет(')






@user_router.message()
async def bot_message(message: types.Message):
    if db.get_signup(message.from_user.id)=='setnickname':
        if len(message.text) > 50:
            await message.answer('ФИО должно быть меньше 50 символов')
        else:
            old_nick=db.get_nickname(message.from_user.id)
            db.set_nickname(message.from_user.id, message.text)
            new_nick = db.get_nickname(message.from_user.id)
            db.change_nickname(new_nick, old_nick)
            db.set_signup(message.from_user.id, 'done')
            await message.answer('Регистраци прошла успешно', reply_markup=start_kb)
    else:
        await message.answer('Не знаю чего вы хотите, идите лучше в главное меню', reply_markup=start_kb)