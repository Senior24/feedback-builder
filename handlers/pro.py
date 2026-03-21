from aiogram import Router, F
from aiogram.types import Message, LabeledPrice

from database.sql import db
from keyboards.reply import start_keyboard

router = Router()

@router.message(F.text == "💎 Buy Pro")
async def pro(message: Message):
    if not db.check_pro(message.from_user.id):
        await message.answer_invoice(
            title="Pro",
            description="This purchase allows you to add more bots",
            payload="pro",
            currency="XTR",
            prices=[LabeledPrice(label="Pro", amount=200)],
        )

        await message.answer("Stars won't be refunded. Since its a demo use /free command to get it for free")
    else:
        await message.answer("You already purchased Pro")


@router.message(F.successful_payment)
@router.message(F.text == "/free")
async def grant_pro(message: Message):
    db.give_pro(message.from_user.id)
    await message.answer("Successfully purchased Pro", reply_markup=start_keyboard(message.from_user.id))
