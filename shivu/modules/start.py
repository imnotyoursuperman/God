import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from shivu import application, PHOTO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from shivu import pm_users as collection 


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        
        await context.bot.send_message(chat_id=GROUP_ID, 
                                       text=f"Another user has joined the herd....\nUser: <a href='tg://user?id={user_id}'>{escape(first_name)})</a>", 
                                       parse_mode='HTML')
    else:
        
        if user_data['first_name'] != first_name or user_data['username'] != username:
            
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    

    if update.effective_chat.type== "private":
        
        
        caption = f"""
        ***🎉🍾[Welcome]🎊🎉***

***Time to build your harem and become the ʜᴀʀᴇᴍ ɢᴏᴅ! ✨ Let's spawn some! ✨***
        """
        
        keyboard = [
            [InlineKeyboardButton("Add Me", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("Support", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("Updates", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("Help", callback_data='help')],
            [InlineKeyboardButton("Maintainer", url=f'https://t.me/hitoriiidayo/')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(PHOTO_URL)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        photo_url = random.choice(PHOTO_URL)
        keyboard = [
            [InlineKeyboardButton("Add Me", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("Support", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("Updates", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("Help", callback_data='help')],
            [InlineKeyboardButton("Maintainer", url=f'https://t.me/hitoriiidayo/')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="🍃For more info, open my chat in PM!🍃",reply_markup=reply_markup )

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
    ***Help Section:***
    
***/guess: To capture the Character (only works in groups)***
***/grab: To capture the Character (only works in groups)***
***/collect: To capture the Character (only works in groups)***
***/protecc: To capture the Character (only works in groups)***
***/fav: To add him to your list of favorites***
***/trade : To trade Characters***
***/gift: Giveaway any Character from your harem to another user..are you sure? (only works in groups)***
***/collection: To open up info on your harem***
***/topgroups : To view the top active groups...***
***/top: To view the top potential supreme***
***/ctop : To view the top users in your chat***
***/changetime: Change spawning period (only works in groups)***
   """
        help_keyboard = [[InlineKeyboardButton("⤾ Bᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':

        caption = f"""
        ***[🎊🍾Welcome🎉🎊]***

***Time to build your harem and become the ʜᴀʀᴇᴍ ɢᴏᴅ! ✨ Let's spawn some! ✨***
        """

        
        keyboard = [
            [InlineKeyboardButton("Add Me", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("Support", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("Updates", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("Help", callback_data='help')],
            [InlineKeyboardButton("Maintainer", url=f'https://t.me/hitoriiidayo/')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')


application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
