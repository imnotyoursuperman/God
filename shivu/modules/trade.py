from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from shivu import user_collection, shivuu

pending_trades = {}


@shivuu.on_message(filters.command("trade"))
async def trade(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("🤦‍♂️ 𝘠𝘰𝘶 𝘯𝘦𝘦𝘥 𝘵𝘰 𝘳𝘦𝘱𝘭𝘺 𝘵𝘰 𝘢 𝘶𝘴𝘦𝘳'𝘴 𝘮𝘦𝘴𝘴𝘢𝘨𝘦 𝘵𝘰 𝘵𝘳𝘢𝘥𝘦 𝘢 𝘤𝘩𝘢𝘳𝘢𝘤𝘵𝘦𝘳")
        return

    receiver_id = message.reply_to_message.from_user.id

    if sender_id == receiver_id:
        await message.reply_text("🤦‍♂️ 𝘠𝘰𝘶 𝘤𝘢𝘯'𝘵 𝘵𝘳𝘢𝘥𝘦 𝘢 𝘤𝘩𝘢𝘳𝘢𝘤𝘵𝘦𝘳 𝘸𝘪𝘵𝘩 𝘺𝘰𝘶𝘳𝘴𝘦𝘭𝘧")
        return

    if len(message.command) != 3:
        await message.reply_text("🤦‍♂️ 𝘠𝘰𝘶 𝘯𝘦𝘦𝘥 𝘵𝘰 𝘱𝘳𝘰𝘷𝘪𝘥𝘦 𝘵𝘸𝘰 [𝘊𝘏𝘈𝘙𝘈𝘊𝘛𝘌𝘙 𝘐𝘋'𝘴]")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    sender = await user_collection.find_one({'id': sender_id})
    receiver = await user_collection.find_one({'id': receiver_id})

    sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
    receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

    if not sender_character:
        await message.reply_text("😮‍💨 𝘠𝘰𝘶 𝘥𝘰𝘯'𝘵 𝘰𝘸𝘯 𝘵𝘩𝘦 𝘤𝘩𝘢𝘳𝘢𝘤𝘵𝘦𝘳 𝘺𝘰𝘶'𝘳𝘦 𝘵𝘳𝘺𝘪𝘯𝘨 𝘵𝘰 𝘵𝘳𝘢𝘥𝘦")
        return

    if not receiver_character:
        await message.reply_text("😮‍💨 𝘛𝘩𝘦 𝘰𝘵𝘩𝘦𝘳 𝘶𝘴𝘦𝘳 𝘥𝘰𝘦𝘴𝘯'𝘵 𝘰𝘸𝘯 𝘵𝘩𝘦 𝘤𝘩𝘢𝘳𝘢𝘤𝘵𝘦𝘳 𝘵𝘩𝘦𝘺'𝘳𝘦 𝘵𝘳𝘺𝘪𝘯𝘨 𝘵𝘰 𝘵𝘳𝘢𝘥𝘦")
        return






    if len(message.command) != 3:
        await message.reply_text("/trade [ʏᴏᴜʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪᴅ] [ᴏᴛʜᴇʀ ᴜsᴇʀ's ᴄʜᴀʀᴀᴄᴛᴇʀ ɪᴅ]!")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    
    pending_trades[(sender_id, receiver_id)] = (sender_character_id, receiver_character_id)

    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ᴄᴏɴғɪʀɴ ᴛʀᴀᴅᴇ", callback_data="confirm_trade")],
            [InlineKeyboardButton("ᴄᴀɴᴄᴇʟ ᴛʀᴀᴅᴇ", callback_data="cancel_trade")]
        ]
    )

    await message.reply_text(f"{message.reply_to_message.from_user.mention}, ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴀᴄᴄᴇᴘᴛ ᴛʜᴇ ᴛʀᴀᴅᴇ ?", reply_markup=keyboard)


@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_trade", "cancel_trade"]))
async def on_callback_query(client, callback_query):
    receiver_id = callback_query.from_user.id

    
    for (sender_id, _receiver_id), (sender_character_id, receiver_character_id) in pending_trades.items():
        if _receiver_id == receiver_id:
            break
    else:
        await callback_query.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ!", show_alert=True)
        return

    if callback_query.data == "confirm_trade":
        
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
        receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

        
        
        sender['characters'].remove(sender_character)
        receiver['characters'].remove(receiver_character)

        
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        
        sender['characters'].append(receiver_character)
        receiver['characters'].append(sender_character)

        
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"🎊🍾 ʏᴏᴜʀ ᴛʀᴀᴅᴇ ᴡɪᴛʜ {callback_query.message.reply_to_message.from_user.mention} ᴡᴀs sᴜᴄᴄᴇssғᴜʟ! 🎊🎉")

    elif callback_query.data == "cancel_trade":
        
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text("😭 ᴛʀᴀᴅᴇ ᴄᴀɴᴄᴇʟʟᴇᴅ....")




pending_gifts = {}


@shivuu.on_message(filters.command("gift"))
async def gift(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("🤦‍♂️ 𝘠𝘰𝘶 𝘯𝘦𝘦𝘥 𝘵𝘰 𝘳𝘦𝘱𝘭𝘺 𝘵𝘰 𝘢 𝘶𝘴𝘦𝘳'𝘴 𝘮𝘦𝘴𝘴𝘢𝘨𝘦 𝘵𝘰 𝘨𝘪𝘧𝘵 𝘢 𝘤𝘩𝘢𝘳𝘢𝘤𝘵𝘦𝘳")
        return

    receiver_id = message.reply_to_message.from_user.id
    receiver_username = message.reply_to_message.from_user.username
    receiver_first_name = message.reply_to_message.from_user.first_name

    if sender_id == receiver_id:
        await message.reply_text("🤦‍♂️ 𝘠𝘰𝘶 𝘤𝘢𝘯'𝘵 𝘨𝘪𝘧𝘵 𝘢 𝘤𝘩𝘢𝘳𝘢𝘤𝘵𝘦𝘳 𝘵𝘰 𝘺𝘰𝘶𝘳𝘴𝘦𝘭𝘧")
        return

    if len(message.command) != 2:
        await message.reply_text("🤦‍♂️ 𝘠𝘰𝘶 𝘯𝘦𝘦𝘥 𝘵𝘰 𝘱𝘳𝘰𝘷𝘪𝘥𝘦 𝘢 [𝘊𝘏𝘈𝘙𝘈𝘊𝘛𝘌𝘙 𝘐𝘋]")
        return

    character_id = message.command[1]

    sender = await user_collection.find_one({'id': sender_id})

    character = next((character for character in sender['characters'] if character['id'] == character_id), None)

    if not character:
        await message.reply_text("😮‍💨 𝘠𝘰𝘶 𝘥𝘰𝘯'𝘵 𝘰𝘸𝘯 𝘵𝘩𝘪𝘴 𝘤𝘩𝘢𝘳𝘢𝘤𝘵𝘦𝘳 𝘪𝘯 𝘺𝘰𝘶𝘳 𝘤𝘰𝘭𝘭𝘦𝘤𝘵𝘪𝘰𝘯")
        return

    
    pending_gifts[(sender_id, receiver_id)] = {
        'character': character,
        'receiver_username': receiver_username,
        'receiver_first_name': receiver_first_name
    }

    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ᴄᴏɴғɪʀᴍ ɢɪғᴛ", callback_data="confirm_gift")],
            [InlineKeyboardButton("ᴄᴀɴᴄᴇʟ ɢɪғᴛ", callback_data="cancel_gift")]
        ]
    )

    await message.reply_text(f"ᴅᴏ ʏᴏᴜ ʀᴇᴀʟʟʏ ᴡᴀɴɴᴀ ɢɪғᴛ ʏᴏᴜʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴛᴏ {message.reply_to_message.from_user.mention} ?", reply_markup=keyboard)

@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_gift", "cancel_gift"]))
async def on_callback_query(client, callback_query):
    sender_id = callback_query.from_user.id

    
    for (_sender_id, receiver_id), gift in pending_gifts.items():
        if _sender_id == sender_id:
            break
    else:
        await callback_query.answer("𝚃𝙷𝙸𝚂 𝙸𝚂 𝙽𝙾𝚃 𝙵𝙾𝚁 𝚈𝙾𝚄!", show_alert=True)
        return

    if callback_query.data == "confirm_gift":
        
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        
        sender['characters'].remove(gift['character'])
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})

        
        if receiver:
            await user_collection.update_one({'id': receiver_id}, {'$push': {'characters': gift['character']}})
        else:
            
            await user_collection.insert_one({
                'id': receiver_id,
                'username': gift['receiver_username'],
                'first_name': gift['receiver_first_name'],
                'characters': [gift['character']],
            })

        
        del pending_gifts[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"You have successfully gifted your character to [{gift['receiver_first_name']}](tg://user?id={receiver_id})!")


