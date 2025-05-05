from aiogram.fsm.state import StatesGroup, State


class BotMenuStates(StatesGroup):
    select_categories = State()
    select_products = State()
    products_info = State()

class BuyProductStates(StatesGroup):
    enter_amount = State()
    confirm_buy = State()

