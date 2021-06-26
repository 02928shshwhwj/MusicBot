
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

def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()

 #For private messages        
 #Ignore commands
 #No bots also allowed
@Jebot.on_message(filters.private & ~filters.bot & ~filters.command("help") & ~filters.command("start") & ~filters.command("song"))  
#Lets Keep this Simple
async def song(client, message):
  # Hope this will fix the args issue
  # defining args as a array instead of direct defining
  # also splitting text for correct yt search
  

    message.chat.id
    user_id = message.from_user["id"]
    args = message.text.split(None, 1)
    args = str(args)
    # Adding +song for better  searching
    args = args + " " + "song"
    #Defined above.. THINK USELESS
    #args = get_arg(message) + " " + "song"

    #Added while callback... I think Useless    
    #if args.startswith("/help"):
        #return ""    
    status = await message.reply(
             text="<b>عم نزللللك الغنية طولك بالك وجن مابهمني انا بوت مو لطيف😒😒\n\n تم تكويد البوت بكل ❤️ من قبل @Mr00lucifer 🇸🇾</b>",
             disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        "حساب معلمي🙈", url="https://www.facebook.com/mohammedsjnoube")
                                ]]
                        ),
               parse_mode="html",
        reply_to_message_id=message.message_id
      )
    video_link = yt_search(args)
    if not video_link:
        await status.edit("<b>مالقيتا تلاعب بلكلمات وترتيبن شو بسويلك😑</b>")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("<b>مشكلة بحسابك🤕اذا استمرت حكي عمو المطور يزبطلك ياها هووون @Mr00lucifer</b>")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await Jebot.send_chat_action(message.chat.id, "upload_audio")
    await Jebot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")    
    
    
    
@Jebot.on_message(filters.command("song"))
async def song(client, message):
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("<b>اي شووو ماحطيت مسافة وحدة واسم الغنية🙂.. لماشي ابعت الاسم مباشرة</b>")
        return ""
    status = await message.reply(
             text="<b>عم نزللللك الغنية طولك بالك وجن مابهمني انا بوت مو لطيف😒😒\n\n تم تكويد البوت بكل ❤️ من قبل @Mr00lucifer 🇸🇾</b>",
             disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        "حساب معلمي🙈", url="https://www.facebook.com/mohammedsjnoube")
                                ]]
                        ),
               parse_mode="html",
        reply_to_message_id=message.message_id
      )
    video_link = yt_search(args)
    if not video_link:
        await status.edit("<b>مالقيتا تلاعب بلكلمات وترتيبن شو بسويلك😑</b>")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("<b>مشكلة بحسابك🤕اذا استمرت حكي عمو المطور يزبطلك ياها هووون @Mr00lucifer</b>")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await Jebot.send_chat_action(message.chat.id, "upload_audio")
    await Jebot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")

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
                                            "اخي اللطيف🙂", callback_data="help"),
                                        InlineKeyboardButton(
                                            "صفحتنا عالفيس☺️", url="https://www.facebook.com/solu404tion")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
   else:

       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>Song Downloader Online\n\n</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "اخي اللطيف🙂", callback_data="help")
                                        
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
               text="<b>اي شووو ماحطيت مسافة وحدة واسم الغنية🙂.. لماشي ابعت الاسم مباشرة</b>",
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

Join @sjnoin
"""
)

Jebot.run()
