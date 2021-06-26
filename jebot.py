
import os
import aiohttp
import asyncio
import json
import sys
import time
from youtubesearchpython import SearchVideos
from pyrogram import filters, Client
from sample_config import Config
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent

Jebot = Client(
   "Song Downloader",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)


 #For private messages        
 #Ignore commands
 #No bots also allowed
@Jebot.on_message(filters.private & ~filters.bot & ~filters.command("help") & ~filters.command("start") & ~filters.command("song"))
async def song(client, message):
 #ImJanindu #JEBotZ
    cap = "برمج بكل ❤️ من قبل @Mr00lucifer"
    url = message.text
    rkp = await message.reply("عم نزلااااا لاتجن يابقرة🙂...")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("اسف مالقيت هيك غنية 🙂 جرب تضيف كلمات أكتر😝")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("جن جن يابقرة جن😝😝عم تنزل...")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`كاتبلي كلمة لحتى نزلا 🥺 رجاع ضيف كلمات اكتر.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`اسف الغنية لي عم تحاول تنزلها عليها قيود جغرافية وموجهة لدول معينة😥مافيي نزلتا`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`تم الوصول إلى الحد الأقصى لعدد التنزيلات حكي عمو المطور ليساعدك @Mr00lucifer.`")
        return
    except PostProcessingError:
        await rkp.edit("خطأ غير معروف بحسابك يرجى التواصل مع المطور لحلها @Mr00lucifer")
        return
    except UnavailableVideoError:
        await rkp.edit("`الاغنية غير متاحة بالصيغة لي بشتغل عليها انا كبوت ولي هيي MP3🙂.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`يوجد مشكلة اثناء استخراجي لمعلومات الأغنية يرجى المحاولة بشكل اخر🥺.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("هدي عم ارفعا ع التيليجرام🙈") #ImJanindu
        lol = "./thumb.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["uploader"]),
                 thumb=lol,
                 caption=cap)  #Mr00lucifer
        await rkp.delete()
  
    
@Jebot.on_message(filters.command("song") & ~filters.edited & filters.group)
async def song(client, message):
    cap = "@Mr00lucifer"
    url = message.text.split(None, 1)[1]
    rkp = await message.reply("عم نزلااا لاتجن يابقرة🙂")
    if not url:
        await rkp.edit("أي شو الأغنية لي بدك نزلا؟؟أكتب اسما يلا🙈 بعد الأمر`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("اسف مالقيتااا جرب غير بالكلمات 🥺")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("جن جن يابقرة عم نزلاا😝")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`كاتبلي كلمة لحتى نزلا 🥺 رجاع ضيف كلمات اكتر.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`اسف الغنية لي عم تحاول تنزلها عليها قيود جغرافية وموجهة لدول معينة😥مافيي نزلتا`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`تم الوصول إلى الحد الأقصى لعدد التنزيلات حكي عمو المطور ليساعدك @Mr00lucifer.`")
        return
    except PostProcessingError:
        await rkp.edit("خطأ غير معروف بحسابك يرجى التواصل مع المطور لحلها @Mr00lucifer")
        return
    except UnavailableVideoError:
        await rkp.edit("`الاغنية غير متاحة بالصيغة لي بشتغل عليها انا كبوت ولي هيي MP3🙂.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`يوجد مشكلة اثناء استخراجي لمعلومات الأغنية يرجى المحاولة بشكل اخر🥺.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("هدي عم ارفعا ع التيليجرام🙈") #ImJanindu
        lol = "./thumb.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["uploader"]),
                 thumb=lol,
                 caption=cap)  #JEBotZ
        await rkp.delete()
 
    
@Jebot.on_message(filters.command("start"))
async def start(client, message):
   if message.chat.type == 'private':
       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>مرحبا انا بوت مو لطيف فهماااان 👿 بس بنزلك لغنية لي بدك بس ابعت الاسم مباشرة

هاد معلمي لي صنعني اذا بتحب تسألو شي @Mr00lucifer 🇸🇾

ضغاط ع زر  اخي التاني لتشوف البوت تاني اللطيف 🙂🙂</b>""", 
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            " اخي الطيف🙂", callback_data="help"),
                                        InlineKeyboardButton(
                                            "حساب معلمي🙈", url="https://www.facebook.com/mohammedsjnoube")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
   else:

       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>أنا جاااهز للأغاني🤩💛.\n\n</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "اخي التاني", callback_data="help")
                                        
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )

@Jebot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>هاد اخي اللطيف اذا بتحب تحكي معو برد عليك ع مزاجو 😒❤️

🤤 @songs404_bot</b>""",
            reply_to_message_id=message.message_id
        )
    else:
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="<b>Song Downloader Help.\n\nSyntax: `/song guleba`</b>",
            reply_to_message_id=message.message_id
        )     
        

@Jebot.on_callback_query()
async def button(Jebot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(Jebot, update.message)

print(
    """
Bot Started!

@Mr00lucifer
"""
)

Jebot.run()
