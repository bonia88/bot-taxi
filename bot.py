from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '8065089437:AAGikOk9QLq3FUymIRN5ducHbxsTg6KV3Kc'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(
    types.KeyboardButton('🚕 Рассчитать стоимость'),
    types.KeyboardButton('📝 Заказать трансфер'),
)
menu_keyboard.add(
    types.KeyboardButton('ℹ️ О компании'),
    types.KeyboardButton('📞 Контакты'),
)

class OrderTransfer(StatesGroup):
    waiting_for_phone = State()
    waiting_for_name = State()
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_comment = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Здравствуйте! Мы занимаемся междугородними перевозками из городов КМВ.\n"
        "Выберите действие:",
        reply_markup=menu_keyboard
    )

@dp.message_handler(lambda message: message.text == 'ℹ️ О компании')
async def about_company(message: types.Message):
    await message.reply(
        "Мы занимаемся междугородними перевозками из Минеральных Вод по Северному Кавказу и России.\n"
        "Комфортные авто и минивэны."
    )

@dp.message_handler(lambda message: message.text == '📞 Контакты')
async def send_contacts(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="Написать в Telegram",
            url="https://t.me/rrrrrvvvggg"
        )
    )
    await message.reply(
        "📞 Наш телефон:\n+79283223366\n\n"
        "Или напишите нам в Telegram по кнопке ниже.",
        reply_markup=keyboard
    )

@dp.message_handler(lambda message: message.text == '📝 Заказать трансфер')
async def order_transfer(message: types.Message):
    await message.reply("Пожалуйста, укажите ваш номер телефона:")
    await OrderTransfer.waiting_for_phone.set()

@dp.message_handler(state=OrderTransfer.waiting_for_phone, content_types=types.ContentTypes.TEXT)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await message.reply("Введите ваше имя:")
    await OrderTransfer.waiting_for_name.set()

@dp.message_handler(state=OrderTransfer.waiting_for_name, content_types=types.ContentTypes.TEXT)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.reply("Укажите дату поездки (например, 12.06):")
    await OrderTransfer.waiting_for_date.set()

@dp.message_handler(state=OrderTransfer.waiting_for_date, content_types=types.ContentTypes.TEXT)
async def process_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text.strip())
    await message.reply("Введите время подачи автомобиля (например, 13:00):")
    await OrderTransfer.waiting_for_time.set()

@dp.message_handler(state=OrderTransfer.waiting_for_time, content_types=types.ContentTypes.TEXT)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text.strip())
    await message.reply("Добавьте комментарий к заказу или введите '-' если комментариев нет:")
    await OrderTransfer.waiting_for_comment.set()

@dp.message_handler(state=OrderTransfer.waiting_for_comment, content_types=types.ContentTypes.TEXT)
async def process_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text.strip())
    data = await state.get_data()

    await message.reply(
        f"Телефон: *{data['phone']}*\n"
        f"Имя: *{data['name']}*\n"
        f"Дата: *{data['date']}*\n"
        f"Время подачи: *{data['time']}*\n"
        f"Комментарий: *{data['comment']}*\n\n"
        "✅ Спасибо, Ваша заявка принята!\n"
        "В ближайшее время с Вами свяжется диспетчер.",
        parse_mode="Markdown"
    )
    await state.finish()

@dp.message_handler(lambda message: message.text == '🚕 Рассчитать стоимость')
async def start_route(message: types.Message):
    await message.reply(
        "Для расчета стоимости, пожалуйста, свяжитесь с диспетчером по телефону или в Telegram."
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
