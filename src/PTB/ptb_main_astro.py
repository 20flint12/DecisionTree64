# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
# logger.info("Bio of %s: %s", user.first_name, update.message.text)
# 1261633346:AAHC4ctXxjZ4hdATaP_Of0608Ju7lIn5sxE

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
# https://docs.python-telegram-bot.org/en/v20.0a6/telegram.ext.jobqueue.html
# https://github.com//python-telegram-bot/python-telegram-bot/wiki/Storing-bot%2C-user-and-chat-related-data


"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


from datetime import datetime, time
import pytz
import src.ephem_routines.ephem_package.geo_place as geo
import src.ephem_routines.ephem_package.moon_day as md
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd
import src.weather_package.main_openweathermap as wt
import src.PTB._ptb_observer_persist_conversation as opc
import src.mathplot_package.plot_astro_summary as mp
import src.boto3_package.mainDB_moon_zodiac as dbmz




import socket
hostname = socket.gethostname()     # DELL-DEV
print(hostname)

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = "Available comands:" \
                "\n/mph <CITY> - calculates moon phase for geoplace" \
                "\n/zod <CITY> - calculates zodiac of Sun and Moon" \
                "\n/md <CITY> - calculates moon day for geoplace" \
                "\n/sr <CITY> - sunrise and sunset for geoplace" \
                "\n/wt <CITY> - current weather for geoplace" \
                "\n/sum <CITY> - summarize info for geoplace" \
                "\n/obs - specify Observer and moment time" \
                "\n/set [HHMM] - set notification time" \
                "\n/cod - colors of days" \
                "\n" \
                "\ndeveloped by Serhii Surmylo (Ukraine)"
    await update.message.reply_text(help_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    logger.info("echo from %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(update.message.text)


def parse_args(context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) > 0:
        geo_name = str(context.args[0])
    else:
        if opc.key_Geoloc in context.chat_data:
            geo_name = context.chat_data[opc.key_Geoloc]
        else:
            geo_name = "Mragowo"

    if opc.key_Moment in context.chat_data:
        moment = context.chat_data[opc.key_Moment]
    else:
        moment = "5"

    return geo_name, moment


async def moon_phase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_phase to the user message."""
    user = update.effective_user

    geo_name, moment = parse_args(context)
    # if len(context.args) > 0:
    #     geo_name = str(context.args[0])
    # else:
    #     if opc.key_Geoloc in context.chat_data:
    #         geo_name = context.chat_data[opc.key_Geoloc]
    #     else:
    #         geo_name = "Mragowo"
    #
    # if opc.key_Moment in context.chat_data:
    #     moment = context.chat_data[opc.key_Moment]
    # else:
    #     moment = "5"
    logger.info("moon day for geo_name: %s at %s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    mph_dict, mph_text = md.main_moon_phase(observer=observer_obj)
    text += mph_text

    logger.info("moon_day of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def moon_day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_day to the user message."""
    user = update.effective_user

    geo_name, moment = parse_args(context)
    # if len(context.args) > 0:
    #     geo_name = str(context.args[0])
    # else:
    #     if opc.key_Geoloc in context.chat_data:
    #         geo_name = context.chat_data[opc.key_Geoloc]
    #     else:
    #         geo_name = "Mragowo"
    #
    # if opc.key_Moment in context.chat_data:
    #     moment = context.chat_data[opc.key_Moment]
    # else:
    #     moment = "5"
    logger.info("moon day for geo_name:  %s at %s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    md_dict, md_text = md.main_moon_day(observer=observer_obj)
    text += md_text[0]
    text += md_text[2]

    logger.info("moon_day of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def sun_rise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_day to the user message."""
    user = update.effective_user

    geo_name, moment = parse_args(context)
    logger.info("sun rise for geo_name: %s at %s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer_obj)     # at noon
    text += sun_text

    logger.info("sun rise of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def zodiac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_day to the user message."""
    user = update.effective_user

    geo_name, moment = parse_args(context)
    logger.info("zodiac for geo_name: %s at %s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    zodiac_dict, zodiac_text = zd.main_zodiac_sun_moon(observer=observer_obj)
    text += zodiac_text

    zod_id = int((zodiac_dict['moon_lon'] % 360) / 30) + 1
    list_of_items = dbmz.moonZodiac_table.table_query(partition_key=zod_id)
    # item_dict, text = dbmz.main_get_item_moon_zodiac(partition_key=zod_id)
    text += "\n" + list_of_items[0]["description"]

    logger.info("moon_zodiac of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return current weather to the user message."""
    user = update.effective_user

    geo_name, moment = parse_args(context)
    # if len(context.args) > 0:
    #     geo_name = str(context.args[0])
    # else:
    #     if opc.key_Geoloc in context.chat_data:
    #         geo_name = context.chat_data[opc.key_Geoloc]
    #     else:
    #         geo_name = "Mragowo"
    #
    # if opc.key_Moment in context.chat_data:
    #     moment = context.chat_data[opc.key_Moment]
    # else:
    #     moment = "5"
    logger.info("weather for geo_name %s at %s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    wt_dict, wt_text = wt.main_weather_now(observer=observer_obj)
    text += wt_text

    logger.info("weather of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return summary info to the user message."""
    user = update.effective_user

    geo_name, moment = parse_args(context)
    # if len(context.args) > 0:
    #     geo_name = str(context.args[0])
    # else:
    #     if opc.key_Geoloc in context.chat_data:
    #         geo_name = context.chat_data[opc.key_Geoloc]
    #     else:
    #         geo_name = "Mragowo"
    #
    # if opc.key_Moment in context.chat_data:
    #     moment = context.chat_data[opc.key_Moment]
    # else:
    #     moment = "5"
    logger.info("summary -> geo_name=%s moment=%s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    mph_dict, mph_text = md.main_moon_phase(observer=observer_obj)
    text += mph_text
    # ++++++++++++++++++++++
    md_dict, md_text = md.main_moon_day(observer=observer_obj)
    # text += md_text[0]
    text += md_text[2]
    alt_dict, alt_text = zd.main_moon_altitude(observer=observer_obj)
    text += alt_text
    # ++++++++++++++++++++++
    sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer_obj)  # at noon
    text += sun_text
    alt_dict, alt_text = sr.main_sun_altitude(observer=observer_obj)
    text += alt_text
    # ++++++++++++++++++++++
    zodiac_dict, zodiac_text = zd.main_zodiac_sun_moon(observer=observer_obj)
    text += zodiac_text
    zod_id = int((zodiac_dict['moon_lon'] % 360) / 30) + 1
    # item_dict, text = dbmz.main_get_item_moon_zodiac(partition_key=zod_id)
    # text += item_dict[0]["description"]
    # ++++++++++++++++++++++
    wt_dict, wt_text = wt.main_weather_now(observer=observer_obj)
    text += wt_text

    logger.info("moon_zodiac of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    photo_name = str(job.chat_id) + "_photo.png"  # 442763659_photo.jpg
    # logger.info("photo: %s === %s --- %s", photo_name, str(context.chat_data), str(context.chat_data))

    # geo_name, moment = parse_args(context)
    if opc.key_Geoloc in context.chat_data:
        geo_name = context.chat_data[opc.key_Geoloc]
    else:
        geo_name = "Mragowo"

    if opc.key_Moment in context.chat_data:
        moment = context.chat_data[opc.key_Moment]
    else:
        moment = "5"
    logger.info("summary -> geo_name=%s moment=%s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    mph_dict, mph_text = md.main_moon_phase(observer=observer_obj)
    text += mph_text
    # ++++++++++++++++++++++
    md_dict, md_text = md.main_moon_day(observer=observer_obj)
    # text += md_text[0]
    text += md_text[2]
    # ++++++++++++++++++++++
    sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer_obj)  # at noon
    text += sun_text
    # ++++++++++++++++++++++
    zodiac_dict, zodiac_text = zd.main_zodiac_sun_moon(observer=observer_obj)
    text += zodiac_text
    # ++++++++++++++++++++++
    wt_dict, wt_text = wt.main_weather_now(observer=observer_obj)
    text += wt_text

    await context.bot.send_message(chat_id=job.chat_id, text=text)

    # ++++++++++++++++++++++
    mp.plot_color_of_the_days(observer=observer_obj, days=5, file_name=photo_name)

    logger.info("send_photo %s", photo_name)
    await context.bot.send_photo(chat_id=job.chat_id, photo=open(photo_name, 'rb'))


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_daily_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id

    # timezone = context.chat_data["time zone"]
    # print(timezone)

    text = ""
    dt_hhmm = None
    try:
        hhmm = context.args[0]
        try:
            dt_hhmm = datetime.strptime("2000-01-01 " + hhmm, "%Y-%m-%d %H%M")
            context.chat_data[opc.key_Notify] = hhmm
            text += "Заданий час: " + str(dt_hhmm.time())
            logger.info(text)
        except ValueError:
            text += "Вибачте, задайте час в форматі [HHMM]"
            logger.info(text)
            await update.effective_message.reply_text(text)
            return

    except (IndexError, ValueError):
        if opc.key_Notify in context.chat_data.keys():
            hhmm = context.chat_data[opc.key_Notify]
            dt_hhmm = datetime.strptime("2000-01-01 " + hhmm, "%Y-%m-%d %H%M")
            text += "Збережені настройки часу нагадування [" + hhmm + "]"
            logger.info(text)
        else:
            await update.effective_message.reply_text("Usage: /set HHMM")

    # ############# Specify timer with valid [HHMM] ###############
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_daily(
        alarm,
        time=time(
            hour=dt_hhmm.hour,
            minute=dt_hhmm.minute,
            second=10,
            tzinfo=pytz.timezone('Europe/Warsaw')),
        days=(0, 1, 2, 3, 4, 5, 6),
        name=str(chat_id),
        chat_id=chat_id,
        job_kwargs={
            # 'trigger': 'cron',
            # 'days': 'mon-fri,sun',
            # 'hour': '11,15,19,23',
            # 'minute': 55,
        },
    )
    # context.job_queue.run_custom(
    #     alarm,
    #     job_kwargs={
    #         'trigger': 'cron',
    #         'days': 'mon-fri,sun',
    #         'hour': '11,15,19,23',
    #         'minute': 55,
    #     },
    # )

    text += "\nТаймер нагадування запущений!"
    if job_removed:
        text += "\nСтарий таймер видалено."

    await update.effective_message.reply_text(text)


async def color_of_the_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    chat_id = update.message.chat_id
    job_name = str(chat_id) + "#REP"            # 442763659#REP
    photo_name = str(chat_id) + "_photo.png"    # 442763659_photo.jpg

    geo_name, moment = parse_args(context)
    # if len(context.args) > 0:
    #     geo_name = str(context.args[0])
    # else:
    #     if opc.key_Geoloc in context.chat_data:
    #         geo_name = context.chat_data[opc.key_Geoloc]
    #     else:
    #         geo_name = "Mragowo"
    #
    # if opc.key_Moment in context.chat_data:
    #     moment = context.chat_data[opc.key_Moment]
    # else:
    #     moment = "5"
    logger.info("summary at %s", moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    mp.plot_color_of_the_days(observer=observer_obj, days=5, file_name=photo_name)

    text = "reply_photo"
    logger.info("%s", text)
    await update.message.reply_photo(photo=open(photo_name, 'rb'))


def main() -> None:
    """
    Start the bot.
    """
    if hostname == "DELL-DEV":
        token = "1042106378:AAFrhuhaLOtcDEU4Jq11u8jgp41Ll_xzG8w"    # @biblika_bot
        persist_filepath = "ptb_main_astro_dev"
    else:
        token = "345369460:AAEjHUhRMdT-E44Xbd82YG_I2C5-uCjR8Wg"     # @scsdvwervdbot astro_bot
        persist_filepath = "ptb_main_astro_prod"
    persistence = PicklePersistence(filepath=persist_filepath)
    application = Application.builder().token(token).persistence(persistence).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mph", moon_phase))
    application.add_handler(CommandHandler("md", moon_day))
    application.add_handler(CommandHandler("sr", sun_rise))
    application.add_handler(CommandHandler("zod", zodiac))          # /zod <GEO_PLACE>
    application.add_handler(CommandHandler("wt", weather))
    application.add_handler(CommandHandler("sum", summary))
    application.add_handler(CommandHandler("set", set_daily_timer))
    application.add_handler(CommandHandler("cod", color_of_the_days))

    application.add_handler(opc.observer_conversation_handler)      # /obs
    application.add_handler(opc.show_data_handler)

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
