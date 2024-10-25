# Kanged From @TroJanZheX
import asyncio
import re
import ast
import math
import random
lock = asyncio.Lock()
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.filters_mdb import find_gfilter, get_gfilters
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}

BTN = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🎥NEW MOVIES 🎥", url="https://t.me/+yKqnKrklurtkNTI1"),
                    InlineKeyboardButton("💥Sʜᴀʀᴇ💥", url="https://t.me/share/url?url=https://t.me/Cinemalokamramanan2024")
                ]
		        
            ]
)

@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filters(client, message):
    k = await global_filters(client, message)    
    if k == False:
        await auto_filter(client, message)    

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
    await message.reply_text("<b>Just type the movie name in the group. I can only work in groups\n\nഇവിടെ ചോദിച്ചാൽ സിനിമ കിട്ടില്ല ഗ്രൂപ്പിൽ മാത്രം സിനിമ ചോദിക്കുക\n\n ask in Group Link👇\nhttps://t.me/Cinemalokamramanan2024\n https://t.me/Cinemalokamramanan2024</b>")
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>#PM_MSG\n\nName : {user}\n\nID : {user_id}\n\nMessage : {content}</b>"
)
	    
@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("oKda", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] ⊳ {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("↲ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📖 𝑷𝒂𝒈𝒆𝒔 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"📖 𝑷𝒂𝒈𝒆𝒔 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("Nᴇxᴛ ⤷", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("↲ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"📖 𝑷𝒂𝒈𝒆𝒔 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("Nᴇxᴛ ⤷", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit('This Movie Not Found In DataBase')
            await asyncio.sleep(10)
            await k.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('Piracy Is Crime')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return await query.answer('Piracy Is Crime')

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer('Piracy Is Crime')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('Piracy Is Crime')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer('Piracy Is Crime')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('Piracy Is Crime')
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('Piracy Is Crime')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('Piracy Is Crime')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name        
        size = get_size(files.file_size)   
        f_caption = files.file_name
        settings = await get_settings(query.message.chat.id)     
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption, mention=query.from_user.mention)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        try:
            if (AUTH_CHANNEL or REQ_CHANNEL) and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("checksub"):
        if (AUTH_CHANNEL or REQ_CHANNEL) and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.file_name
        if CUSTOM_FILE_CAPTION:
            try:
               f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption, mention=query.from_user.mention)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False,
	    reply_markup=InlineKeyboardMarkup(
                          [
                            [                            
                            InlineKeyboardButton("🎥 NEW MOVIES 🎥", url="https://t.me/+yKqnKrklurtkNTI1")
                          ],[     
                            InlineKeyboardButton("🖥 𝐎𝐓𝐓 𝐈𝐍𝐒𝐓𝐆𝐑𝐀𝐌 🖥", url='https://www.instagram.com/new_ott__updates?igsh=MTMxcmhwamF4eGp6eg==')
                           ]
                        ]
                    )
    )
            	    
	    
    elif query.data.startswith("killfilesdq"):
        ident, keyword = query.data.split("#")
        #await query.message.edit_text(f"<b>Fetching Files for your query {keyword} on DB... Please wait...</b>")
        files, total = await get_bad_files(keyword)
        await query.message.edit_text("<b>File deletion process will start in 5 seconds !</b>")
        await asyncio.sleep(5)
        deleted = 0
        async with lock:
            try:
                for file in files:
                    file_ids = file.file_id
                    file_name = file.file_name
                    result = await Media.collection.delete_one({
                        '_id': file_ids,
                    })
                    if result.deleted_count:
                        logger.info(f'File Found for your query {keyword}! Successfully deleted {file_name} from database.')
                    deleted += 1
                    if deleted % 20 == 0:
                        await query.message.edit_text(f"<b>Process started for deleting files from DB. Successfully deleted {str(deleted)} files from DB for your query {keyword} !\n\nPlease wait...</b>")
            except Exception as e:
                logger.exception(e)
                await query.message.edit_text(f'Error: {e}')
            else:
                await query.message.edit_text(f"<b>Process Completed for file deletion !\n\nSuccessfully deleted {str(deleted)} files from database for your query {keyword}.</b>")
    
    elif query.data == "pages":	    
        await query.answer()

    elif query.data == "mfna":
        await query.answer("𝑴𝒂𝒏𝒖𝒂𝒍 𝑭𝒊𝒍𝒕𝒆𝒓 𝒊𝒔 𝑪𝒖𝒓𝒓𝒆𝒏𝒕𝒍𝒚 𝑫𝒊𝒔𝒂𝒃𝒍𝒆𝒅..!!", show_alert=True)
    
    elif query.data == "qinfo":
        await query.answer("𝑮𝒍𝒐𝒃𝒂𝒍 𝑭𝒊𝒍𝒕𝒆𝒓𝒔 𝒊𝒔 𝑪𝒖𝒓𝒓𝒆𝒏𝒕𝒍𝒚 𝑫𝒊𝒔𝒂𝒃𝒍𝒆𝒅..!!", show_alert=True)  

    elif query.data == "oooi":
        xd = query.message.reply_to_message.text.replace(" ", "+")
        btn = [[                
            InlineKeyboardButton("𝗖𝗹𝗶𝗰𝗸 𝗛𝗲𝗿𝗲 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗠𝗼𝘃𝗶𝗲 𝗡𝗮𝗺𝗲", url=f"https://www.google.com/search?q={xd}")
            ],[   
            InlineKeyboardButton('𝖻𝖺𝖼𝗄', callback_data='nlang')
            ]]
        await query.message.edit_text(text=f"<u><b>𝗛𝗲𝘆 {query.from_user.mention} 👋 𝗣𝗹𝗲𝗮𝘀𝗲 𝗙𝗼𝗹𝗹𝗼𝘄 𝗕𝗲𝗹𝗼𝘄 𝗠𝗼𝘃𝗶𝗲𝘀 𝗢𝗿 𝗦𝗲𝗿𝗶𝗲𝘀 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗶𝗻𝗴 𝗥𝘂𝗹𝗲𝘀</b></u>\n\n𝗠𝗮𝗸𝗲 𝗦𝘂𝗿𝗲 𝗧𝗵𝗲 𝗠𝗼𝘃𝗶𝗲 𝗶𝘀 𝗥𝗲𝗹𝗲𝗮𝘀𝗲𝗱 𝗢𝗻 𝗢𝗧𝗧 𝗣𝗹𝗮𝘁𝗳𝗼𝗿𝗺𝘀\n\n𝖠𝗌𝗄 𝖥𝗈𝗋 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀\n\n𝖬𝗎𝗌𝗍 𝖢𝗁𝖾𝖼𝗄 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗂𝗇 𝖦𝗈𝗈𝗀𝗅𝖾 \n\n𝖠𝗌𝗄 𝖥𝗈𝗋 𝖬𝗈𝗏𝗂𝖾𝗌 𝖨𝗇 𝖤𝗇𝗀𝗅𝗂𝗌𝗁 𝖫𝖾𝗍𝗍𝖾𝗋𝗌 𝖮𝗇𝗅𝗒\n\n𝖣𝗈𝗇'𝗍 𝖠𝗌𝗄 𝖥𝗈𝗋 𝖴𝗇𝗋𝖾𝗅𝖾𝖺𝗌𝖾𝖽 𝖬𝗈𝗏𝗂𝖾𝗌\n\n[𝖬𝗈𝗏𝗂𝖾 𝖭𝖺𝗆𝖾, 𝖸𝖾𝖺𝗋, 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾] 𝖠𝗌𝗄 𝖳𝗁𝗂𝗌 𝖶𝖺𝗒\n\n𝖣𝗈 𝖭𝗈𝗍 𝖴𝗌𝖾 𝖶𝗈𝗋𝖽𝗌 𝖫𝗂𝗄𝖾 𝖣𝗎𝖻, 𝖬𝗈𝗏𝗂𝖾, 𝖫𝗂𝗇𝗄, 𝖯𝗅𝗌𝗌, 𝖲𝖾𝗇𝗍 𝖾𝗍𝖼 𝖮𝗍𝗁𝖾𝗋 𝖳𝗁𝖺𝗇 𝖳𝗁𝖾 𝖶𝖺𝗒 𝖬𝖾𝗇𝗍𝗂𝗈𝗇𝖾𝖽 𝖠𝖻𝗈𝗏𝖾\n\n𝖣𝗈𝗇'𝗍 𝖴𝗌𝖾 𝖲𝗍𝗒𝗅𝗂𝗌𝗁 𝖥𝗈𝗇𝗍 𝖶𝗁𝗂𝗅𝖾 𝖱𝖾𝗊𝗎𝖾𝗌𝗍\n\n𝖣𝗈𝗇'𝗍 𝖴𝗌𝖾 𝖲𝗒𝗆𝖻𝗈𝗅𝗌 𝖶𝗁𝗂𝗅𝖾 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖬𝗈𝗏𝗂𝖾𝗌 𝗅𝗂𝗄𝖾 (+:;'!-|...𝖾𝗍𝖼)\n\n𝗜𝗳 𝘆𝗼𝘂 𝗱𝗼𝗻'𝘁 𝗴𝗲𝘁 𝘁𝗵𝗮𝘁 𝗠𝗼𝘃𝗶𝗲𝘀 𝗼𝗿 𝗦𝗲𝗿𝗶𝗲𝘀 𝗲𝘃𝗲𝗻 𝗮𝗳𝘁𝗲𝗿 𝗳𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 𝘁𝗵𝗲 𝗿𝘂𝗹𝗲𝘀 𝗮𝗯𝗼𝘃𝗲, 𝘂𝗽𝗹𝗼𝗮𝗱 𝘁𝗵𝗲 𝗺𝗼𝘃𝗶𝗲 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - <a href=https://t.me/MCU_ADMIN_V1_BOT>𝗖𝗟𝗜𝗖𝗞 𝗛𝗘𝗥𝗘</a>\n\n<u><b>𝖬𝗈𝗏𝗂𝖾𝗌 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗂𝗇𝗀 𝖥𝗈𝗋𝗆𝖺𝗍</b></u>\n𝖪𝗎𝗋𝗎𝗉 𝖬𝗈𝗏𝗂𝖾❌\n𝖪𝗎𝗋𝗎𝗉 2021 ✅\n𝖪𝗀𝖿: 𝖢𝗁𝖺𝗉𝗍𝖾𝗋 2❌\n𝖪𝗀𝖿 𝖢𝗁𝖺𝗉𝗍𝖾𝗋 2✅\n\n<u><b>𝖲𝖾𝗋𝗂𝖾𝗌 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗂𝗇𝗀 𝖱𝗎𝗅𝖾𝗌</b></u>\n𝖲𝗍𝖺𝗇𝗀𝖾𝗋 𝖳𝗁𝗂𝗇𝗀𝗌 𝗌𝖾𝖺𝗌𝗈𝗇 1❌\n𝖲𝗍𝖺𝗇𝗀𝖾𝗋 𝖳𝗁𝗂𝗇𝗀𝗌 𝖲01✅\n𝖲𝗍𝖺𝗇𝗀𝖾𝗋 𝖳𝗁𝗂𝗇𝗀𝗌 𝖤𝗉𝗂𝗌𝗈𝖽𝖾 1❌\n𝖲𝗍𝖺𝗇𝗀𝖾𝗋 𝖳𝗁𝗂𝗇𝗀𝗌 𝖲01𝖤01✅\n\n<b>🎬ഫസ്റ്റ് ആയിട്ട് നിങ്ങൾ ശ്രദ്ധിക്കേണ്ടത് മൂവി നെയിം ആണ് അതിനായി താക്കെ കാണുന്ന ബട്ടൺ ക്ലിക്കോ ചെയ്ത്  ഗൂഗിൾ പോയി നെയിം സെർച്ച് ചെയ്ത കറക്റ്റ് മൂവി നെയിം കോപ്പി ചെയ്തിട്ട് ഗ്രൂപ്പ് ൽ ഇട്ടാൽ കിട്ടും🤍\n\n💡മുകളിൽ ഉള്ള കാര്യങ്ങൾ ഫോളോ ചെയ്തിട്ടും മൂവി കിട്ടുന്നില്ല എനിക്കിൽ മൂവി 👉<a href=https://t.me/MCU_ADMIN_V1_BOT>𝗠𝗦𝗚 𝗛𝗘𝗥𝗘</a> msg അയയ്ക്കുക 30 min ശേഷം മൂവി ബോട്ട് ഇൽ അപ്ലോഡ് ആക്കുന്നതാണ് 🎉</b>", reply_markup=InlineKeyboardMarkup(btn))
 
	    
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('× ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ×', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('Cᴏᴍᴍᴜɴɪᴛʏ', callback_data='commun'),
            InlineKeyboardButton('Bᴏᴛ ɪɴғᴏ', callback_data='about')
            ],[
            InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help'),            
            InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='botinfo')  
            ],[
            InlineKeyboardButton('ᴀᴅᴍɪɴs ᴇxᴛʀᴀ ғᴇᴀᴛᴜʀᴇs', callback_data='machu')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer('Piracy Is Crime') 
    elif query.data == "commun":
        buttons = [[
            InlineKeyboardButton("👥 𝗚𝗥𝗢𝗨𝗣 - 𝟭", url=f"https://t.me/+JRWRXAzDwkc2NDA1"),
            InlineKeyboardButton("👥 𝗚𝗥𝗢𝗨𝗣 - 𝟮", url=f"https://t.me/+uGkuM2x4Bf4yM2Zl")
            ],[
            InlineKeyboardButton("👥 𝗚𝗥𝗢𝗨𝗣 - 𝟯", url=f"https://t.me/+XZq5smozmoA1ZDNl"),
            InlineKeyboardButton("👥 𝗚𝗥𝗢𝗨𝗣 - 𝟰", url=f"https://t.me/Cinemalokamramanan2024")  
            ],[
            InlineKeyboardButton("🖥 𝗡𝗘𝗪 𝗢𝗧𝗧 𝗨𝗣𝗗𝗔𝗧𝗘𝗦 🖥", url="https://t.me/+XzVIX3lhqzAyYTQ1")
            ],[
            InlineKeyboardButton("🖥 𝐎𝐓𝐓 𝐈𝐍𝐒𝐓𝐆𝐑𝐀𝐌 🖥", url='https://www.instagram.com/new_ott__updates?igsh=MTMxcmhwamF4eGp6eg==')                  
            ],[       
            InlineKeyboardButton('🪬 ʜᴏᴍᴇ 🪬', callback_data='start'),
            InlineKeyboardButton('🗣 ᴀᴅᴍɪɴ', url=f"https://t.me/MCU_ADMIN_V1_BOT")
            ],[
            InlineKeyboardButton('🤷‍♂️ 𝐇𝐎𝐖 𝐓𝐎 𝐑𝐄𝐐𝐔𝐄𝐒𝐓 𝐌𝐎𝐕𝐈𝐄𝐒 🤷🏻', callback_data='movereq'),
        
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)          
        await query.message.edit_text(
            text=script.COMMUN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "movedow":
        buttons = [[
            InlineKeyboardButton("👥 𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐆𝐫𝐨𝐮𝐩", url=f"https://t.me/+3P_LfAbmDv5jMzM1"),
            InlineKeyboardButton('⬅️ ʙᴀᴄᴋ', callback_data='help')
        ]]        
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=script.MOVDOW_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "machu":
        if query.from_user.id not in ADMINS:
            await query.answer("മോനെ അത് ലോക്കാ ❌", show_alert=True)
            return
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=script.MCAHU_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "movereqs":
        buttons = [[
            InlineKeyboardButton("👥 𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐆𝐫𝐨𝐮𝐩", url=f"https://t.me/+3P_LfAbmDv5jMzM1"),
            InlineKeyboardButton('⬅️ ʙᴀᴄᴋ', callback_data='help')
        ]]        
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=script.MOVREQ_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "movereq":
        buttons = [[
            InlineKeyboardButton("👥 𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐆𝐫𝐨𝐮𝐩", url=f"https://t.me/+3P_LfAbmDv5jMzM1"),
            InlineKeyboardButton('⬅️ ʙᴀᴄᴋ', callback_data='commun')
        ]]        
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=script.MOVREQ_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
	)
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('🕹 𝑴𝒂𝒏𝒖𝒂𝒍 𝑭𝒊𝒍𝒕𝒆𝒓', 'mfna'),
            InlineKeyboardButton('🌏 𝑮𝒍𝒐𝒃𝒂𝒍 𝑭𝒊𝒍𝒕𝒆𝒓𝒔', 'qinfo'),
            InlineKeyboardButton('𝑨𝒖𝒕𝒐 𝒇𝒊𝒍𝒕𝒆𝒓 📥', callback_data='autofilter')                   
            ],[
            InlineKeyboardButton('🤷‍♂️ 𝐇𝐎𝐖 𝐓𝐎 𝐑𝐄𝐐𝐔𝐄𝐒𝐓 🤷🏻', callback_data='movereqs')
            ],[
            InlineKeyboardButton('🤷‍♂️ 𝐇𝐎𝐖 𝐓𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 🤷🏻', callback_data='movedow')           
            ],[
            InlineKeyboardButton('⬅️ ʙᴀᴄᴋ', callback_data='start'),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)           
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "botinfo":
        buttons = [[                             
            InlineKeyboardButton('📈 sᴛᴀᴛᴜs', callback_data='stats'),
            InlineKeyboardButton('☠ sᴏᴜʀᴄᴇ', callback_data='sorce')
            ],[
            InlineKeyboardButton("🤴🏻 ᴀᴅᴍɪɴ", url=f"https://t.me/MCU_ADMIN_V1_BOT"),
            ],[
            InlineKeyboardButton('🪬 ʜᴏᴍᴇ 🪬', callback_data='start'),
            InlineKeyboardButton('⬅️ ʙᴀᴄᴋ', callback_data='help')                       
        ]]        
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=script.BOTINFO_TXT.format(temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons = [[            
            InlineKeyboardButton('🪬 ʜᴏᴍᴇ 🪬', callback_data='start'),
            InlineKeyboardButton('⬅️ ʙᴀᴄᴋ', callback_data='help')                                    
        ]]        
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )        
    elif query.data == "sorce":
        buttons = [[
            InlineKeyboardButton('⬅️ ʙᴀᴄᴋ', callback_data='botinfo')
        ]]        
        reply_markup = InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=script.SORCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('⬅️ ʙᴀᴄᴋ', callback_data='help')
        ]]        
        reply_markup = InlineKeyboardMarkup(buttons)       
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )                 
        	    
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
	)
    elif query.data == "eng":
       xd = query.message.reply_to_message.text.replace(" ", "+")
       btn = [
           [
               InlineKeyboardButton("Search on Google", url=f"https://www.google.com/search?q={xd}"),
               InlineKeyboardButton("back", callback_data="nlang")
           ]
       ]
       await query.message.edit_text(text=f"Hey {query.from_user.mention} 👋<b><u> If you want to get the movie, follow the below…</u>👇\n\n<i>🔹Ask for correct spelling. (English Letters)\n\n🔸Ask for movies in English Lettes only.\n\n🔹Don't ask for unreleased movies.\n\n🔸 [Movie Name, Year, Language] Ask this way.\n\n🔹 Don't Use symbols while requesting movies. (+:;'!-`|...etc)\n\n🌏 Use the Google Button below for your movie details\n\n📌 𝗔𝗻𝘆 𝗛𝗲𝗹𝗽 𝗣𝗹𝗲𝗮𝘀𝗲 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗔𝗱𝗺𝗶𝗻 : @MCU_ADMIN_V1_BOT</b></i>", reply_markup=InlineKeyboardMarkup(btn))    

    elif query.data == "mal":
       xd = query.message.reply_to_message.text.replace(" ", "+")
       btn = [
           [
               InlineKeyboardButton("Search on Google", url=f"https://www.google.com/search?q={xd}"),
               InlineKeyboardButton("back", callback_data="nlang")
           ]
       ]
       await query.message.edit_text(text=f"Hey {query.from_user.mention}👋 <b><u>നിങ്ങൾക്ക് സിനിമ കിട്ടണമെങ്കിൽ, താഴെ പറയുന്ന കാര്യങ്ങളിൽ ശ്രദ്ധിക്കുക...👇</u><I>\n\n🔹കറക്റ്റ് സ്പെല്ലിംഗിൽ ചോദിക്കുക. (ഇംഗ്ലീഷിൽ മാത്രം)\n\n🔸സിനിമകൾ ഇംഗ്ലീഷിൽ Type ചെയ്ത് മാത്രം ചോദിക്കുക.\n\n🔹റിലീസ് ആകാത്ത സിനിമകൾ ചോദിക്കരുത്.\n\n🔸[സിനിമയുടെ പേര്, വർഷം, ഭാഷ] ഈ രീതിയിൽ ചോദിക്കുക.\n\n🔹സിനിമ Request ചെയ്യുമ്പോൾ Symbols ഒഴിവാക്കുക. [+:;'*!-`&.. etc]\n\n🌏 നിങ്ങളുടെ സിനിമ വിശദാംശങ്ങൾക്കായി ചുവടെയുള്ള ഗൂഗിൾ ബട്ടൺ ഉപയോഗിക്കുക\n\n📌 എന്തെങ്കിലും സഹായം ദയവായി അഡ്മിനെ ബന്ധപ്പെടുക : @MCU_ADMIN_V1_BOT</b></i>", reply_markup=InlineKeyboardMarkup(btn))

    elif query.data == "tam":
       xd = query.message.reply_to_message.text.replace(" ", "+")
       btn = [
           [
               InlineKeyboardButton("Search on Google", url=f"https://www.google.com/search?q={xd}"),
               InlineKeyboardButton("back", callback_data="nlang")
           ]
       ]    
       await query.message.edit_text(text=f"Hey {query.from_user.mention}👋 <b><u>நீங்கள் திரைப்படத்தைப் பெற விரும்பினால், கீழே குறிப்பிடப்பட்டுள்ள விஷயங்களைப் பின்பற்றவும்...👇</u><i>\n\n🔹சரியான எழுத்துப்பிழை கேட்கவும். (ஆங்கிலத்தில் மட்டும்)\n\n🔸திரைப்படங்களை ஆங்கிலத்தில் டைப் செய்து மட்டும் கேட்கவும்.\n\n🔹வெளியாத திரைப்படங்களைக் கேட்காதீர்கள்.\n\n🔸 [திரைப்படத்தின் பெயர், ஆண்டு, மொழி] இந்த வழியில் கேளுங்கள்.\n\n🔹திரைப்படங்களைக் கோரும் போது சின்னங்களைத் தவிர்க்கவும். [+:;'*!-&.. etc]\n\n🌎 உங்கள் திரைப்பட விவரங்களுக்கு கீழே உள்ள Google பட்டனைப் பயன்படுத்தவும்\n\n📌 ஏதேனும் உதவி இருந்தால் நிர்வாகியைத் தொடர்பு கொள்ளவும் : @MCU_ADMIN_V1_BOT</b></i>", reply_markup=InlineKeyboardMarkup(btn))
     
    elif query.data == "tel":
       xd = query.message.reply_to_message.text.replace(" ", "+")
       btn = [
           [
               InlineKeyboardButton("Search on Google", url=f"https://www.google.com/search?q={xd}"),
               InlineKeyboardButton("back", callback_data="nlang")
           ]
       ]
       await query.message.edit_text(text=f"Hey {query.from_user.mention}👋 <b><u>రు సినిమాని పొందాలనుకుంటే, క్రింద పేర్కొన్న విషయాలను అనుసరించండి...👇</u><i>\n\n🔹సరైన స్పెల్లింగ్ కోసం అడగండి. (ఇంగ్లీష్‌లో మాత్రమే)\n\n🔸సినిమాలను ఆంగ్లంలో టైప్ చేసి మాత్రమే అడగండి.\n\n🔹విడుదల కాని సినిమాలను అడగవద్దు.\n\n🔸 [సినిమా పేరు, సంవత్సరం, భాష] ఈ విధంగా అడగండి.\n\n🔹సినిమాలను అభ్యర్థించేటప్పుడు చిహ్నాలను నివారించండి. [+:;'*!-&.. etc]\n\n🌎 మీ సినిమా వివరాల కోసం దిగువన ఉన్న Google బటన్‌ని ఉపయోగించండి\n\n📌 ఏదైనా సహాయం దయచేసి నిర్వాహకుడిని సంప్రదించండి : @MCU_ADMIN_V1_BOT</b></i>", reply_markup=InlineKeyboardMarkup(btn))

    elif query.data == "hin":
       xd = query.message.reply_to_message.text.replace(" ", "+")
       btn = [
           [
               InlineKeyboardButton("Search on Google", url=f"https://www.google.com/search?q={xd}"),
               InlineKeyboardButton("back", callback_data="nlang")
           ]
       ]
       await query.message.edit_text(text=f"Hey {query.from_user.mention}👋 <b><u>यदि आप मूवी प्राप्त करना चाहते हैं, तो नीचे दिए गए चरणों का पालन करें...</u><i>👇\n\n🔹सही वर्तनी के लिए पूछें। (केवल अंग्रेज़ी में)\n\n🔸फिल्में अंग्रेजी में टाइप करें और केवल पूछें।\n\n🔹अप्रकाशित फिल्मों के लिए न पूछें।\n\n🔸 [मूवी का नाम, वर्ष, भाषा] इस तरह पूछें।\n\n🔹फिल्मों का अनुरोध करते समय प्रतीकों से बचें। [+:;'*!-&.. आदि]\n\n🌎अपनी मूवी के विवरण के लिए नीचे दिए गए Google बटन का उपयोग करें\n\n📌 किसी भी मदद के लिए कृपया व्यवस्थापक से संपर्क करें : @MCU_ADMIN_V1_BOT</b></i>", reply_markup=InlineKeyboardMarkup(btn))
    elif query.data == "nlang":
       xd = query.message.reply_to_message.text.replace(" ", "+")  
       btn_duction = InlineKeyboardButton("𝖬𝗎𝗌𝗍 𝖱𝖾𝖺𝖽", callback_data="endio")
       btn_ductior = InlineKeyboardButton("𝖱𝗎𝗅𝖾𝗌", callback_data="oooi")  
       btn_dadduco = InlineKeyboardButton("𝖥𝗈𝗋𝗆𝖺𝗍", callback_data="minfo")
        
       intro_row = [btn_duction, btn_ductior, btn_dadduco]
       btn_eng = InlineKeyboardButton("ᴇɴɢ", callback_data="eng")
       btn_mal = InlineKeyboardButton("ᴍᴀʟ", callback_data="mal")
       btn_hin = InlineKeyboardButton("ʜɪɴ", callback_data="hin")
       btn_tam = InlineKeyboardButton("ᴛᴀᴍ", callback_data="tam")
       btn_tel = InlineKeyboardButton("ᴛᴇʟ", callback_data="tel")

       language_row = [btn_eng, btn_mal, btn_hin, btn_tam, btn_tel]
       btn_google = InlineKeyboardButton("𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗦𝗽𝗲𝗹𝗹𝗶𝗻𝗴 (𝗀𝗈𝗈𝗀𝗅𝖾)", url=f"https://www.google.com/search?q={xd}")

       google_row = [btn_google]

       keyboard = InlineKeyboardMarkup(inline_keyboard=[intro_row, language_row, google_row])
 
       await query.message.edit_text(text=f"<b>❝ 𝖧𝖾𝗒 {query.from_user.mention} 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝖨𝗌 𝖶𝗋𝗈𝗇𝗀 ❞\n\n➪ 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝖮𝖿 𝖬𝗈𝗏𝗂𝖾 <u>𝖢𝗁𝖾𝖼𝗄 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 (𝗀𝗈𝗈𝗀𝗅𝖾)</u> 𝖡𝗎𝗍𝗍𝗈𝗇 𝖡𝖾𝗅𝗈𝗐 𝖶𝗂𝗅𝗅 𝖧𝖾𝗅𝗉 𝖸𝗈𝗎..𓁉\n\n➪ 𝖲𝖾𝗅𝖾𝖼𝗍 𝖸𝗈𝗎𝗋 𝖫𝖺𝗇𝗀𝖺𝗎𝗀𝖾 𝖥𝗋𝗈𝗆 𝖳𝗁𝖾 𝖫𝗂𝗌𝗍 𝖡𝖾𝗅𝗈𝗐 𝖳𝗈 𝖬𝗈𝗋𝖾 𝖧𝖾𝗅𝗉..☃︎</b>", reply_markup=keyboard)
         
    elif query.data == "minfo":
       await query.answer(
       text=(
            "🥇𝐆𝐨 𝐓𝐨 𝐆𝐨𝐨𝐠𝐥𝐞 𝐂𝐨𝐩𝐲 𝐂𝐨𝐫𝐫𝐞𝐜𝐭 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠 𝐢𝐧 𝗢𝗻𝗹𝘆 𝗘𝗻𝗴𝗹𝗶𝘀𝗵 𝗟𝗲𝘁𝘁𝗲𝗿𝘀 𝐀𝐧𝐝 𝐒𝐞𝐧𝐭 𝐢𝐭🎯\n\n"
            "𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐅𝐨𝐫𝐦𝐚𝐭:-\n"
            "Movies - Varisu 2023\n"
            "Series - Dark S01E01\n\n"
            "𝗠𝗼𝗿𝗲 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 :- 𝖢𝗅𝗂𝖼𝗄 𝖮𝗇 𝖳𝗁𝖾 𝖡𝗎𝗍𝗍𝗈𝗇 𝖨𝗇 𝖸𝗈𝗎𝗋 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 𝖻𝖾𝗅𝗈𝗐🪝"
        ),
        show_alert=True
    )
    elif query.data == "endio": 
       await query.answer(f"കിട്ടോ.. ഉണ്ടോ.. തരുമോ.അയക്കാമോ. sent. ലിങ്ക്.. Plz. Movie... എന്നിങ്ങനെ ഉള്ള വാക്കുകൾ ഒഴിവാക്കുക. മൂവിയുടെ പേര് വർഷം ഭാഷ✍️. വേറേ ഒന്നും കൂട്ടി എഴുതരുത്.🔎",show_alert=True)

    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer('Piracy Is Crime')

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer('Piracy Is Crime')


async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)

            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] ⊳ {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
            ]
            for file in files
        ]

    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"📖 𝑷𝒂𝒈𝒆𝒔 1/{math.ceil(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="Nᴇxᴛ ⤷", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="📖 𝑷𝒂𝒈𝒆𝒔 1/1", callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>𝖧𝖾𝗒 : {msg.from_user.mention}\n𝖥𝗂𝗅𝗆 : {search}\n𝖱𝖾𝗌𝗎𝗅𝗍𝗌 : {total_results}\n\n[Usᴇ Bᴇʟᴏᴡ Nᴇxᴛ Bᴜᴛᴛᴏɴ]</b>"
    if imdb and imdb.get('poster'):
        try:
            await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    if spoll:
        await msg.message.delete()
	    

async def advantage_spell_chok(msg):
    spl = f"<b>❝ 𝖧𝖾𝗒 : {msg.from_user.mention} 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝖨𝗌 𝖶𝗋𝗈𝗇𝗀 ❞ \n\n➪ 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝖮𝖿 𝖬𝗈𝗏𝗂𝖾 <u>𝖢𝗁𝖾𝖼𝗄 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 (𝗀𝗈𝗈𝗀𝗅𝖾)</u> 𝖡𝗎𝗍𝗍𝗈𝗇 𝖡𝖾𝗅𝗈𝗐 𝖶𝗂𝗅𝗅 𝖧𝖾𝗅𝗉 𝖸𝗈𝗎..𓁉\n\n➪ 𝖲𝖾𝗅𝖾𝖼𝗍 𝖸𝗈𝗎𝗋 𝖫𝖺𝗇𝗀𝖺𝗎𝗀𝖾 𝖥𝗋𝗈𝗆 𝖳𝗁𝖾 𝖫𝗂𝗌𝗍 𝖡𝖾𝗅𝗈𝗐 𝖳𝗈 𝖬𝗈𝗋𝖾 𝖧𝖾𝗅𝗉..☃︎</b>"        
    message = msg
    mv_rqst = msg.text
    search = msg.text.replace(" ", "+")      
    btn = [[
        InlineKeyboardButton("𝖬𝗎𝗌𝗍 𝖱𝖾𝖺𝖽", callback_data="endio"),
        InlineKeyboardButton("𝖱𝗎𝗅𝖾𝗌", callback_data="oooi"), 
        InlineKeyboardButton("𝖥𝗈𝗋𝗆𝖺𝗍", callback_data="minfo")
        ],[
        InlineKeyboardButton("ᴇɴɢ", callback_data="eng"),
        InlineKeyboardButton("ᴍᴀʟ", callback_data="mal"),
        InlineKeyboardButton("ʜɪɴ", callback_data="hin"),
        InlineKeyboardButton("ᴛᴀᴍ", callback_data="tam"),
        InlineKeyboardButton("ᴛᴇʟ", callback_data="tel")
        ],[
        InlineKeyboardButton(
            text="📢 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗦𝗽𝗲𝗹𝗹𝗶𝗻𝗴 (𝗚𝗼𝗼𝗴𝗹𝗲) 📢",
            url=f"https://google.com/search?q={search}"
        )
            
    ]]
    await msg.reply_text(spl, reply_markup=InlineKeyboardMarkup(btn))
    #await msg.delete()
    return   

async def global_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            knd3 = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep()
                            await knd3.delete()
                            await message.delete()

                        else:
                            button = eval(btn)
                            knd2 = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep()
                            await knd2.delete()
                            await message.delete()

                    elif btn == "[]":
                        knd1 = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep()
                        await knd1.delete()
                        await message.delete()

                    else:
                        button = eval(btn)
                        knd = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep()
                        await knd.delete()
                        await message.delete()

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
