class script(object):
    START_TXT = """
<b>𝖧𝖾𝗒 👋 {} 𝖨 𝖠𝗆 <a href=https://t.me/{}>{}</a> 𝖧𝖺𝗉𝗉𝗒 🖤 𝖳𝗈 𝖧𝖺𝗏𝖾 𝖸𝗈𝗎

𝖨 𝖠𝗆 𝖯𝗈𝗐𝖾𝗋 𝖥𝗎𝗅𝗅 𝖠𝗎𝗍𝗈 𝖥𝗂𝗅𝗍𝖾𝗋 + 𝖬𝗈𝗏𝗂𝖾 𝖲𝖾𝖺𝗋𝖼𝗁 + 𝖬𝖺𝗇𝗎𝖺𝗅 𝖥𝗂𝗅𝗍𝖾𝗋 𝖡𝗈𝗍 ⚙

𝖨 𝖠𝗆 𝖠 𝖡𝗈𝗍 𝖯𝗋𝗈𝗏𝗂𝖽𝗂𝗇𝗀 𝖬𝗈𝗏𝗂𝖾𝗌 𝖠𝗇𝖽 𝖲𝖾𝗋𝗂𝖾𝗌 𝖲𝗈 𝖠𝖽𝖽 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖥𝖺𝗆. 𝖳𝗁𝖾𝗇 𝖨 𝖶𝗂𝗅𝗅 𝗌𝖾𝗇𝗍 𝖳𝗁𝖾 𝖬𝗈𝗏𝗂𝖾𝗌⏳

𝖢𝗅𝗂𝖼𝗄 𝖡𝖾𝗅𝗈𝗐 𝖴𝗌𝖾𝖿𝗎𝗅 𝖡𝗎𝗍𝗍𝗈𝗇𝗌 🫶</b>"""
    
    HELP_TXT = """<b>Hᴇʏ {} 𝖨𝖺𝗆 𝖧𝖺𝗉𝗉𝗒 🖤 𝖳𝗈 𝖧𝖺𝗏𝖾 𝖸𝗈𝗎
    
𝖶𝗂𝗍𝗁 𝖳𝗁𝗂𝗌 𝖧𝖾𝗅𝗉 𝖸𝗈𝗎 𝖶𝗂𝗅𝗅 𝖴𝗇𝖽𝖾𝗋𝗌𝗍𝖺𝗇𝖽 𝖧𝗈𝗐 𝖳𝗈 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖡𝗈𝗍🏌️
    
𝖢𝗁𝖾𝖼𝗄 𝖡𝖾𝗅𝗈𝗐 𝖧𝖾𝗅𝗉 𝖥𝗎𝗇𝖼𝗍𝗂𝗈𝗇𝗌🤍</b>"""

    ABOUT_TXT = """<b>🤖 𝑴𝒚 𝑵𝒂𝒎𝒆 : <a href=https://t.me/{}>{}</a>
    
📝 𝑳𝒂𝒏𝒈𝒖𝒂𝒈𝒆 : <a href='https://t.me/+JRWRXAzDwkc2NDA1'>𝑷𝒚𝒕𝒉𝒐𝒏</a>

📚 𝑭𝒓𝒂𝒎𝒆𝒘𝒐𝒓𝒌 : <a href='https://t.me/+uGkuM2x4Bf4yM2Zl'>𝑷𝒚𝒓𝒐𝒈𝒓𝒂𝒎</a>

📡 𝑯𝒐𝒔𝒕𝒆𝒅 𝑶𝒏 : 𝑯𝑬𝑹𝑲𝑼𝑶

👨‍💻 𝑫𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒓 : <a href='http://t.me/MCU_ADMIN_V1_BOT'>𝐍𝐚𝐳𝐫𝐢𝐲𝐚 𝐀𝐝𝐦𝐢𝐧</a>

👥 𝑺𝒖𝒑𝒑𝒐𝒓𝒕 𝑮𝒓𝒐𝒖𝒑 : <a href=https://t.me/+3P_LfAbmDv5jMzM1> 𝐆𝐑𝐎𝐔𝐏 </a>

📢 𝑼𝒑𝒅𝒂𝒕𝒆 𝑪𝒉𝒂𝒏𝒏𝒆𝒍 : <a href=https://t.me/MCUupdatesLINKS> 𝐎𝐓𝐓 𝐔𝐏𝐃𝐀𝐓𝐄𝐒 </a></b>"""

    BOTINFO_TXT = """<b>𝖧𝖾𝗒 𝖡𝗋𝗈 𝖨𝖺𝗆 𝖧𝖺𝗉𝗉𝗒 🖤 𝖳𝗈 𝖧𝖺𝗏𝖾 𝖸𝗈𝗎
 
✪ സിനിമകൾ ഇഷ്ടപ്പെടുന്നവർക്കും സിനിമ ഡൗൺലോഡ് ചെയ്യുന്നവർക്കും വേണ്ടിയുള്ള മാത്രം ഉള്ള ബോട്ടാണ് ആണിത് 🤩

✫ This bot is only for movie lovers and movie downloaders 🤗</b>"""
    
    SORCE_TXT = """<b>കൊട്ക്ക്ണില്ല്യാ...... [PRIVATE REPO]
    
 ️📌 𝗔𝗻𝘆 𝗛𝗲𝗹𝗽 𝗣𝗹𝗲𝗮𝘀𝗲 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗔𝗱𝗺𝗶𝗻 : @MCU_ADMIN_V1_BOT</b>"""
    
    MOVDOW_TXT = """<b> 1. 𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐌𝐨𝐯𝐢𝐞𝐬 𝐆𝐫𝐨𝐮𝐩 - <a href=https://t.me/+3P_LfAbmDv5jMzM1>𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞</a>

2. 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝖨𝗇 𝖤𝗇𝗀𝗅𝗂𝗌𝗁 𝖫𝖾𝗍𝗍𝖾𝗋𝗌. 𝖬𝗎𝗌𝗍 𝖥𝗈𝗅𝗅𝗈𝗐𝗂𝗇𝗀 𝖧𝗈𝗐 𝖳𝗈 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 ⚙

3. 𝖸𝗈𝗎 𝖢𝖺𝗇 𝖢𝗅𝗂𝖼𝗄 𝖮𝗇 𝖳𝗁𝖾 𝖬𝗈𝗏𝗂𝖾 𝖡𝗎𝗍𝗍𝗈𝗇 𝖥𝗂𝗅𝖾𝗌 𝖨𝗇 𝖳𝗁𝖾 𝖰𝗎𝖺𝗅𝗂𝗍𝗒 𝖸𝗈𝗎 𝖶𝖺𝗇𝗍 𝖨𝗇 𝖬𝗒 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖳𝗁𝖺𝗍 𝖢𝗈𝗆𝖾𝗌 𝖠𝗌 𝖠 𝖱𝖾𝗉𝗅𝗒 𝖳𝗈 𝖳𝗁𝖾 𝗆𝗈𝗏𝗂𝖾 𝖸𝗈𝗎 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽🎯

4. 𝖳𝗁𝖾𝗇 𝖢𝗅𝗂𝖼𝗄 𝖲𝗍𝖺𝗋𝗍 𝖡𝖾𝗅𝗈𝗐 𝖮𝗋 𝖠𝗎𝗍𝗈 𝖲𝗍𝖺𝗋𝗍. 𝖥𝗂𝗇𝖺𝗅𝗅𝗒 𝖸𝗈𝗁 𝖶𝗂𝗅𝗅 𝖦𝖾𝗍 𝖳𝗁𝖾 𝖥𝗂𝗅𝖾𝗌 🌎

𝖭𝖡: 𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖮𝗇𝗅𝗒 𝖨𝗇 𝖬𝗒 𝖬𝗈𝗏𝗂𝖾𝗌 𝖦𝗋𝗈𝗎𝗉 𝖫𝗂𝗇𝗄 𝖢𝗁𝖾𝖼𝗄 𝗂𝗇 𝖠𝖻𝗈𝗏𝖾..!!</b>"""

    MOVREQ_TXT = """<b>⚠️ 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗂𝗇𝗀 𝖥𝗈𝗅𝗅𝗈𝗐 𝖱𝗎𝗅𝖾𝗌 👇🏻

𝖠𝗌𝗄 𝖥𝗈𝗋 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀

𝖬𝗎𝗌𝗍 𝖢𝗁𝖾𝖼𝗄 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗂𝗇 𝖦𝗈𝗈𝗀𝗅𝖾 

𝖠𝗌𝗄 𝖥𝗈𝗋 𝖬𝗈𝗏𝗂𝖾𝗌 𝖨𝗇 𝖤𝗇𝗀𝗅𝗂𝗌𝗁 𝖫𝖾𝗍𝗍𝖾𝗋𝗌 𝖮𝗇𝗅𝗒

𝖣𝗈𝗇'𝗍 𝖠𝗌𝗄 𝖥𝗈𝗋 𝖴𝗇𝗋𝖾𝗅𝖾𝖺𝗌𝖾𝖽 𝖬𝗈𝗏𝗂𝖾𝗌

[𝖬𝗈𝗏𝗂𝖾 𝖭𝖺𝗆𝖾, 𝖸𝖾𝖺𝗋, 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾] 𝖠𝗌𝗄 𝖳𝗁𝗂𝗌 𝖶𝖺𝗒

𝖣𝗈 𝖭𝗈𝗍 𝖴𝗌𝖾 𝖶𝗈𝗋𝖽𝗌 𝖫𝗂𝗄𝖾 𝖣𝗎𝖻, 𝖬𝗈𝗏𝗂𝖾, 𝖫𝗂𝗇𝗄, 𝖯𝗅𝗌𝗌, 𝖲𝖾𝗇𝗍 𝖾𝗍𝖼 𝖮𝗍𝗁𝖾𝗋 𝖳𝗁𝖺𝗇 𝖳𝗁𝖾 𝖶𝖺𝗒 𝖬𝖾𝗇𝗍𝗂𝗈𝗇𝖾𝖽 𝖠𝖻𝗈𝗏𝖾

𝖣𝗈𝗇'𝗍 𝖴𝗌𝖾 𝖲𝗍𝗒𝗅𝗂𝗌𝗁 𝖥𝗈𝗇𝗍 𝖶𝗁𝗂𝗅𝖾 𝖱𝖾𝗊𝗎𝖾𝗌𝗍

𝖣𝗈𝗇'𝗍 𝖴𝗌𝖾 𝖲𝗒𝗆𝖻𝗈𝗅𝗌 𝖶𝗁𝗂𝗅𝖾 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖬𝗈𝗏𝗂𝖾𝗌 𝗅𝗂𝗄𝖾 (+:;'!-|...𝖾𝗍𝖼)

𝖨𝖿 𝖸𝗈𝗎 𝖣𝗈𝗇'𝗍 𝖦𝖾𝗍 𝖬𝗈𝗏𝗂𝖾𝗌 𝖠𝗇𝖽 𝖲𝖾𝗋𝗂𝖾𝗌⌛️
𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖠𝖽𝗆𝗂𝗇 - @MCU_ADMIN_V1_BOT

𝖬𝗈𝗏𝗂𝖾𝗌 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗂𝗇𝗀 𝖥𝗈𝗋𝗆𝖺𝗍
𝖪𝗎𝗋𝗎𝗉 𝖬𝗈𝗏𝗂𝖾❌
𝖪𝗎𝗋𝗎𝗉 2021 ✅
𝖪𝗀𝖿: 𝖢𝗁𝖺𝗉𝗍𝖾𝗋 2❌
𝖪𝗀𝖿 𝖢𝗁𝖺𝗉𝗍𝖾𝗋 2✅

𝖲𝖾𝗋𝗂𝖾𝗌 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝗂𝗇𝗀 𝖱𝗎𝗅𝖾𝗌
𝖲𝗍𝖺𝗇𝗀𝖾𝗋 𝖳𝗁𝗂𝗇𝗀𝗌 𝗌𝖾𝖺𝗌𝗈𝗇 1❌
𝖲𝗍𝖺𝗇𝗀𝖾𝗋 𝖳𝗁𝗂𝗇𝗀𝗌 𝖲01✅
𝖲𝗍𝖺𝗇𝗀𝖾𝗋 𝖳𝗁𝗂𝗇𝗀𝗌 𝖤𝗉𝗂𝗌𝗈𝖽𝖾 1❌
𝖲𝗍𝖺𝗇𝗀𝖾𝗋 𝖳𝗁𝗂𝗇𝗀𝗌 𝖲01𝖤01✅

𝖢𝗅𝗂𝖼𝗄 𝖡𝖾𝗅𝗈𝗐 𝖡𝗎𝗍𝗍𝗈𝗇𝗌 𝖠𝗇𝖽 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖬𝗈𝗏𝗂𝖾𝗌 𝗈𝗋 𝖲𝖾𝗋𝗂𝖾𝗌 𝖨𝗇 𝖬𝗈𝗏𝗂𝖾𝗌 𝖦𝗋𝗈𝗎𝗉💡</b>"""
   
    COMMUN_TXT = """<b>✰ സിനിമയെ ഇഷ്ടപ്പെടുന്നവർക്കായി നിങ്ങൾക്ക് ഞങ്ങളുടെ സിനിമ കൂട്ടായ്മയിലേക്ക് എല്ലാവരും ജോയിൻ ചെയ്യുക..🤍</b>"""
    
    AUTOFILTER_TXT = """Help: <b>Auto Filter
    
NOTE:
1. Make me the admin of your channel if it's private.
2. make sure that your channel does not contains camrips, porn and fake files.
3. Forward the last message to me with quotes.
 I'll add all the files in that channel to my db.

️📌 𝗔𝗻𝘆 𝗛𝗲𝗹𝗽 𝗣𝗹𝗲𝗮𝘀𝗲 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗔𝗱𝗺𝗶𝗻 : @MCU_ADMIN_V1_BOT</b>"""
    
    MCAHU_TXT = """<b>The new command features are listed below. More features coming soon
    
/start - Welcome🤗 (Help , About and others)
    
/setchat - force Sub Channel ID

/viewchat - which force sub running chek

/delchat - Delete Requests (force Sub)

/stats - Check Stats

/deletefiles - Movie name all Files delete 

/ping - Bot Speed , Cpu etc

/restart - Restart ✅

/logs - bot logs txt</b>"""

    CAPTION = """<b>𝐻𝑒𝑙𝑙𝑜 👋 {mention} 😍</b>

<b>📂 Fɪʟᴇ ɴᴀᴍᴇ : <code>{file_name}</code></b>

<b> ⚡Thanks For Using RAMANAN🤖♥️</b>

<b> Note : <tt>Files Are Not Owned By Us⚠️</tt></b>

<b> [🤖ʀᴀᴍᴀɴᴀɴ ʙᴏᴛ🤖](http://t.me/Cinemalokam071_bot)</b>"""
    
    STATUS_TXT = """★ 𝚃𝙾𝚃𝙰𝙻 𝙵𝙸𝙻𝙴𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝙲𝙷𝙰𝚃𝚂: <code>{}</code>
★ 𝚄𝚂𝙴𝙳 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱
★ 𝙵𝚁𝙴𝙴 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱"""
    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
@JERRYCINEMABOT
"""
    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
@JERRYCINEMABOT
"""
