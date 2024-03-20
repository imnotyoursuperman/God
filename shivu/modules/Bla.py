from pymongo import  ReturnDocument
from pyrogram.enums import ChatMemberStatus, ChatType
from shivu import application, user_totals_collection, shivuu
from telegram import Update
from telegram.ext import CommandHandler,CallbackContext
from pyrogram import Client, filters
from pyrogram.types import Message


async def changetime(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in OWNER_ID :
        await update.message.reply_text('You are not my master!')
        return

    try:
        args = message.command
        if len(args) != 2:
            await update.message.reply_text('Please use: /changetime NUMBER')
            return

        new_frequency = int(args[1])
        if new_frequency < 10:
            await update.message.reply_text('The message frequency must be greater than or equal to 75.')
            return

    
        chat_frequency = await user_totals_collection.find_one_and_update(
            {'chat_id': str(chat_id)},
            {'$set': {'message_frequency': new_frequency}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        await update.message.reply_text(f'Successfully changed {new_frequency}')
    except Exception as e:
        await update.message.reply_text(f'Failed to change {str(e)}')
        
application.add_handler(CommandHandler("changetime", changetime))
