from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button

from tgbot.misc.states import BotMenuStates, BuyProductStates
from tgbot.misc.constants import SwitchToWindow
from tgbot.services.repo import Repo


async def on_chosen_category(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    context = manager.current_context()
    context.dialog_data.update(category_id=item_id)
    await manager.switch_to(BotMenuStates.select_products)


async def on_chosen_product(callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    context = manager.current_context()
    context.dialog_data.update(product_id=item_id)
    await manager.switch_to(BotMenuStates.products_info)

async def on_buy_product(callback: CallbackQuery, widget: Button, manager: DialogManager):
    context = manager.current_context()
    product_id = context.dialog_data.get('product_id')
    await manager.start(BuyProductStates.enter_amount, data={'product_id': product_id})


async def on_entered_amount(message: Message, widget: TextInput, manager: DialogManager, quantity: str):
    context = manager.current_context()
    if not quantity.isdigit():
        await message.answer("Please enter a number.")
        return
    repo: Repo = manager.middleware_data.get("repo")
    quantity = int(quantity)
    product_id = int(context.start_data.get('product_id'))
    session = manager.middleware_data.get("session")
    product_info = await repo.get_product(session, product_id)
    if product_info.stock < quantity:
        await message.answer("Sorry, you don't have enough stock.")
        return
    context.dialog_data.update(quantity=quantity)
    await manager.switch_to(BuyProductStates.confirm_buy)


async def on_confirm_buy(callback: CallbackQuery, widget: Button, manager: DialogManager):
    context = manager.current_context()
    repo: Repo = manager.middleware_data.get("repo")
    session = manager.middleware_data.get("session")
    product_id = int(context.start_data.get('product_id'))

    quantity = int(context.dialog_data.get('quantity'))

    await repo.buy_product(session, product_id, quantity)
    product = await repo.get_product(session, product_id)
    await callback.answer(f"You bought {quantity} {product.name} ")
    await manager.done(
        result={
            'switch_to_window': SwitchToWindow.SelectProducts

        }
    )

