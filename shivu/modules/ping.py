import time

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, SUDO_USERS

async def ping(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text("This order is not for you to use, lil bro!")
        return
    start_time = time.time()
    message = await update.message.reply_text('PONG!')
    end_time = time.time()
    elapsed_time = round((end_time - start_time) * 1000, 3)
    await message.edit_text(f'PONG! - {elapsed_time}ms')

application.add_handler(CommandHandler("ping", ping))
