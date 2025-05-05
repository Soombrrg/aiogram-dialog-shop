from aiogram_dialog import DialogManager

from tgbot.misc.states import BotMenuStates
from tgbot.services.repo import Repo


async def get_categories(dialog_manager:DialogManager, **middleware_data):
    session = middleware_data.get('session')
    repo: Repo = middleware_data.get('repo')
    db_categories = await repo.get_categories(session)


    data = {
        "categories": [
            (f'{category.name} ({len(category.items)})', category.category_id)
            for category in db_categories
        ]
    }

    return data


async def get_products(dialog_manager:DialogManager, **middleware_data):
    session = middleware_data.get('session')
    repo: Repo = middleware_data.get('repo')

    context = dialog_manager.current_context()

    category_id = context.dialog_data.get('category_id')
    if not category_id:
        await dialog_manager.event.answer("Please, select a category first.")
        await dialog_manager.switch_to(BotMenuStates.select_categories)
        return
    category_id = int(category_id)
    db_products = await repo.get_products(session, category_id)

    data = {
        "products": db_products
    }

    return data


async def get_product_info(dialog_manager:DialogManager, **middleware_data):
    context = dialog_manager.current_context()
    product_id = context.dialog_data.get('product_id')
    if not product_id:
        await dialog_manager.event.answer('Please select a product first.')
        await dialog_manager.switch_to(BotMenuStates.select_products)
        return
    session = middleware_data.get('session')
    repo: Repo = middleware_data.get('repo')
    product = await repo.get_product(session, int(product_id))

    data = {
        "product": product,

    }
    return data

async def get_buy_product(dialog_manager:DialogManager, **middleware_data):
    context = dialog_manager.current_context()
    product_id = context.start_data.get('product_id')

    session = middleware_data.get('session')
    repo: Repo = middleware_data.get('repo')
    product = await repo.get_product(session, int(product_id))
    quantity = context.dialog_data.get('quantity')
    data = {
        "product": product,
        "quantity": quantity,
        "total_amount": product.price * quantity if quantity else None,

    }
    return data
