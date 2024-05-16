from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from buttons.buttons_admin import admin_kb, change_kb
from aiogram.fsm.context import FSMContext
from database.meet import Database1

db=Database1('fio.db')
admin_router = Router()

class AddMeet(StatesGroup):
    # Шаги состояний
    date = State()
    name = State()
    time = State()

class ChangeMeet(StatesGroup):
    # Шаги состояний
    date = State()
    name = State()
    time = State()
    vvod = State()





admins=[916539100, 578879909, 676770835, 1286948809]
@admin_router.message(Command('admin'))
async def start(message: types.Message):
    if message.from_user.id in admins:
        await message.answer('Дарова, босс!', reply_markup=admin_kb)

@admin_router.message(F.text=='Создать встречу')
async def make_meet(message: types.Message, state: FSMContext):
    await message.answer('Выберите дату в формате день.месяц.год',reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddMeet.date)

@admin_router.message(AddMeet.date, F.text)
async def select_time(message:types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer('Как назовем мероприятие?')
    await state.set_state(AddMeet.name)

@admin_router.message(AddMeet.name, F.text)
async def select_name(message:types.Message, state: FSMContext):
    if db.meet_exists(message.text)==0:
        await state.update_data(name=message.text)
        await state.set_state(AddMeet.time)
        await message.answer('Введите время')
    if db.meet_exists(message.text)==1:
        await message.answer('Такая встреча уже есть, назовите ее по другому')
        await state.set_state(AddMeet.name)


@admin_router.message(AddMeet.time, F.text)
async def select_name(message:types.Message, state: FSMContext):
    status1='Можно записаться'
    status2='None'
    await state.update_data(time=message.text)
    meet = await state.get_data()
    name = meet['name']
    date = meet['date']
    time = meet['time']
    db.add_name_meet(name)
    db.add_date_meet(name, date)
    db.add_time_meet(name, time)
    db.add_zapis_meet(status1,name)
    db.add_client_meet(status2,name)
    await state.clear()
    await message.answer('Отлично! Встреча создана!', reply_markup=admin_kb)

@admin_router.message(F.text=='Отменить/перенести встречу')
async def much_meet(message: types.Message, state: FSMContext):
    meet=db.name_meet()
    message_to_answer=''
    number=1
    if len(meet)==0:
        await message.answer('Встреч пока нет!')
    else:
        for names in range(0,len(meet)-2,4):
            client = meet[names]
            name = meet[names+1]
            time = meet[names+2]
            date = meet[names+3]
            message_to_answer+=f'{number}.Название встречи: {name}\nДата: {date}\nВремя: {time}\nКлиент: {client}\n' # и тут тоже дз
            number+=1
        await message.answer('Выберите название интересующей вас встречи')
        await message.answer(message_to_answer, reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(ChangeMeet.vvod)

@admin_router.message(ChangeMeet.vvod, F.text)
async def change_meet(message: types.Message, state: FSMContext):
    await state.clear()
    global chose
    chose=message.text
    await message.answer('Что вы хотите с ней сделать?', reply_markup=change_kb)

@admin_router.message(F.text=='Удалить встречу')
async def delete_meet(message: types.Message):
    if db.meet_exists(chose):
        db.delete_meet(chose)
        await message.answer('Встреча успешно удалена!', reply_markup=admin_kb)
    else:
        await message.answer('Такой встречи нет!')

@admin_router.message(F.text=='Изменить время')
async def change_time(message: types.Message, state: FSMContext):
    if db.meet_exists(chose):
        await state.set_state(ChangeMeet.time)
        await message.answer('Введите новое время')
    else:
        await message.answer('Такой встречи нет')

@admin_router.message(F.text=='Изменить дату')
async def change_date(message: types.Message, state: FSMContext):
    if db.meet_exists(chose):
        await state.set_state(ChangeMeet.date)
        await message.answer('Введите новую дату')
    else:
        await message.answer('Такой встречи нет')

@admin_router.message(F.text=='Изменить назвнание')
async def change_name(message: types.Message, state: FSMContext):
    if db.meet_exists(chose):
        await state.set_state(ChangeMeet.name)
        await message.answer('Введите новое название')
    else:
        await message.answer('Такой встречи нет')

@admin_router.message(ChangeMeet.time, F.text)
async def change_time1(message:types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    meet = await state.get_data()
    time = meet['time']
    db.add_time_meet(chose, time)
    await state.clear()
    await message.answer('Время успешно изменено!', reply_markup=admin_kb)


@admin_router.message(ChangeMeet.date, F.text)
async def change_date1(message:types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    meet = await state.get_data()
    date = meet['date']
    db.add_date_meet(chose, date)
    await state.clear()
    await message.answer('Дата успешно изменена!', reply_markup=admin_kb)

@admin_router.message(ChangeMeet.name, F.text)
async def change_name1(message:types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    meet = await state.get_data()
    name=meet['name']
    db.rename_meet(chose, name)
    await state.clear()
    await message.answer('Название успешно изменено!', reply_markup=admin_kb)

