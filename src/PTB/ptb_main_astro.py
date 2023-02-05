# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
# logger.info("Bio of %s: %s", user.first_name, update.message.text)
# 1261633346:AAHC4ctXxjZ4hdATaP_Of0608Ju7lIn5sxE

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
# https://docs.python-telegram-bot.org/en/v20.0a6/telegram.ext.jobqueue.html
# https://github.com//python-telegram-bot/python-telegram-bot/wiki/Storing-bot%2C-user-and-chat-related-data


"""
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the bot.
"""

from pprint import pprint

from datetime import datetime, time
import pytz
import time as t

import src.ephem_routines.ephem_package.geo_place as geo
import src.ephem_routines.ephem_package.moon_day as md
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd
import src.weather_package.main_openweathermap as wt
import src.PTB._ptb_observer_persist_conversation as opc
import src.PTB._ptb_timer_weather as rwt
import src.mathplot_package.plot_astro_summary as mp
import src.boto3_package.mainDB_moon_zodiac as dbmz
import src.boto3_package.mainDB_moon_day as dbmd
import src.boto3_package.botDB_users as bdbu


import html
import json
import logging
import traceback

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
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

from telegram.error import Forbidden, TimedOut, NetworkError, ChatMigrated, TelegramError

import socket
hostname = socket.gethostname()     # DELL-DEV
print(hostname)

DEVELOPER_CHAT_ID = 442763659


# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
# logger.addFilter((lambda s: not s.msg.endswith('A TelegramError was raised while processing the Update'))


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # # Log the error before we do anything else, so we can see it even if something breaks.
    # logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    text = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=text, parse_mode=ParseMode.HTML)


async def handle_exception(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    text = ""

    if update is not None:
        user_id = update.effective_user.id
    else:
        user_id = -1

    try:
        raise context.error
    # except Unauthorized:
    #     # remove update.message.chat_id from conversation list
    #     print("Unauthorized!!!!!")
    except Forbidden:
        text += str(user_id) + ":: *** Forbidden *** !!!"
    except TimedOut:            # handle slow connection problems
        text += str(user_id) + ":: *** TimedOut *** !!!"
    except NetworkError:        # handle other connection problems
        text += str(user_id) + ":: *** NetworkError *** !!!"
    except ChatMigrated as e:   # the chat_id of a group has changed, use e.new_chat_id instead
        text += str(user_id) + ":: *** ChatMigrated *** !!!" + str(e)
    except TelegramError as e:  # handle all other telegram related errors
        text += str(user_id) + ":: *** TelegramError *** !!!" + str(e)
    # except Exception as e:
    #     text += str(user_id) + ":: *** Exception *** !!!" + str(e)

    print(text)

    # Finally, send the message
    await context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=text, parse_mode=ParseMode.HTML)


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
                "\n/rep [SS] - run weather recorder timer" \
                "\n/urep - reset weather recorder timer" \
                "\n/cod - colors of days" \
                "\n" \
                "\ndeveloped by Serhii Surmylo (Ukraine), 2023"
    await update.message.reply_text(help_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # bdbu.update_user_record(update=update, context=context)
    user = update.effective_user

    text = f"{user.id} <{user.first_name} {user.last_name}> echo: {update.message.text}"
    logger.info(text)
    await update.message.reply_text(text)


def get_user_bot_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    bot = context.bot
    user_bot_id = str(chat_id) + "#" + str(bot.id)
    return user_bot_id


def parse_Geolocation_Interval(context: ContextTypes.DEFAULT_TYPE, parse_args=False, user_bot_id=""):

    if not context.chat_data:
        print("!!!!!!!!!!!! not hasattr(context, 'chat_data') or not context.chat_data !!!!!!!!!!!")

        user_db_data = bdbu.get_user_db_data(pk=user_bot_id)

        context.chat_data.clear()
        context.chat_data.update(user_db_data)

    context.chat_data["context_user_data"].setdefault(opc.key_Geolocation, "OLSZTYN")
    context.chat_data["context_user_data"].setdefault(opc.key_Interval, "5.555")
    # context.user_data.setdefault(opc.key_Reminder, "0000")

    # ---------------------------------------------------
    geo_name = context.chat_data["context_user_data"][opc.key_Geolocation]
    if geo_name == context.chat_data["context_user_data"][opc.key_Geolocation]:
        valid_geo_name = bdbu.PrmOrig.SET
    else:
        valid_geo_name = bdbu.PrmOrig.DEF

    interval = context.chat_data["context_user_data"][opc.key_Interval]
    if interval == context.chat_data["context_user_data"][opc.key_Interval]:
        valid_interval = bdbu.PrmOrig.SET
    else:
        valid_interval = bdbu.PrmOrig.DEF

    # ===================================================
    if hasattr(context, 'args') and parse_args:
        arg_len = len(context.args)

        if arg_len == 1:
            geo_name = str(context.args[0])
            valid_geo_name = bdbu.PrmOrig.ARG

        elif arg_len == 2:
            geo_name = str(context.args[0])
            valid_geo_name = bdbu.PrmOrig.ARG
            interval = str(context.args[1])
            valid_interval = bdbu.PrmOrig.ARG

    print(user_bot_id, ":: parse_Geolocation_Interval> (", valid_geo_name, geo_name, "), (", valid_interval, interval, ")")

    return (valid_geo_name, geo_name), (valid_interval, interval)


def parse_Reminder(update: Update, context: ContextTypes.DEFAULT_TYPE, observer=None):

    user_bot_id = context.chat_data[bdbu.botUsers_table.partition_key]
    user_name = context.chat_data[bdbu.botUsers_table.sort_key]

    context.chat_data["context_user_data"].setdefault(opc.key_Reminder, "0000")

    # ---------------------------------------------------
    reminder = context.chat_data["context_user_data"][opc.key_Reminder]
    if reminder == context.chat_data["context_user_data"][opc.key_Reminder]:
        valid_reminder = bdbu.PrmOrig.SET
    else:
        valid_reminder = bdbu.PrmOrig.DEF

    # ===================================================
    if hasattr(context, 'args'):
        arg_len = len(context.args)

        if arg_len == 1:
            reminder = str(context.args[0])
            valid_reminder = bdbu.PrmOrig.ARG

    # Check validity of time string
    dt_hhmm_unaware = datetime.strptime("2000-01-01 0000", "%Y-%m-%d %H%M")
    dt_hhmm_utc = datetime.strptime("2000-01-01 0000", "%Y-%m-%d %H%M")

    try:
        dt_hhmm_unaware = datetime.strptime("2000-01-01 " + reminder, "%Y-%m-%d %H%M")

        # valid_reminder = bdbu.ParamOrigin.VALID_TIME
        dt_hhmm_utc = observer.dt_unaware_to_utc(dt_hhmm_unaware)

        user_db_data = context.chat_data        # ???
        user_db_data["activity"]["daily_utc_time"] = [dt_hhmm_utc.hour, dt_hhmm_utc.minute, dt_hhmm_utc.second]
        bdbu.update_user_context_db(pk_sk_id={'pk': user_bot_id, 'sk': user_name}, user_db_data=user_db_data)

    except ValueError:

        valid_reminder = bdbu.PrmOrig(valid_reminder) + bdbu.PrmOrig.INVALID_TIME

    print(user_bot_id, " :: parse_Reminder> (", bdbu.PrmOrig(valid_reminder), ") ", dt_hhmm_unaware.time(), " utc:", dt_hhmm_utc.time())

    return valid_reminder, dt_hhmm_unaware, dt_hhmm_utc


async def moon_phase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_phase to the user message."""
    user = update.effective_user
    bot = context.bot
    print(user, bot.id, bot.name, bot.first_name)
    # bdbu.update_user_record(update=update, context=context)

    user_bot_id = get_user_bot_id(update, context)
    (valid_geo_name, geo_name), (valid_interval, interval) = parse_Geolocation_Interval(context, parse_args=True,
                                                                                        user_bot_id=user_bot_id)
    logger.info("moon day for geo_name: %s at %s", geo_name, interval)

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
    # bdbu.update_user_record(update=update, context=context)

    (valid_geo_name, geo_name), (valid_interval, interval) = parse_Geolocation_Interval(context, parse_args=True)
    logger.info("moon day for geo_name:  %s at %s", geo_name, interval)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    md_dict, md_text = md.main_moon_day(observer=observer_obj)
    text += md_text[0]
    text += md_text[2]

    item_dict = dbmd.moonDay_table.table_query(partition_key=md_dict['moon_day'])

    descr_str = item_dict[0]["description_0"]
    text += "\n\n" + dbmd.string_between_tags(input_string=descr_str, tag_index=0)

    descr_str = item_dict[0]["description_1"]
    text += "\n\n" + dbmd.string_between_tags(input_string=descr_str, tag_index=0)

    logger.info("moon_day of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def sun_rise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_day to the user message."""
    user = update.effective_user
    # bdbu.update_user_record(update=update, context=context)

    (valid_geo_name, geo_name), (valid_interval, interval) = parse_Geolocation_Interval(context, parse_args=True)
    logger.info("sun rise for geo_name: %s at %s", geo_name, interval)

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
    # bdbu.update_user_record(update=update, context=context)

    (valid_geo_name, geo_name), (valid_interval, interval) = parse_Geolocation_Interval(context, parse_args=True)
    logger.info("zodiac for geo_name: %s at %s", geo_name, interval)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    zodiac_dict, zodiac_text = zd.main_zodiac_sun_moon(observer=observer_obj)
    text += zodiac_text

    zod_id = int((zodiac_dict['moon_lon'] % 360) / 30) + 1
    list_of_items = dbmz.moonZodiac_table.table_query(partition_key=zod_id)
    descr_str = list_of_items[0]["description_0"]
    text += "\n\n" + dbmz.string_between_tags(input_string=descr_str, tag_index=0)

    logger.info("moon_zodiac of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return current weather to the user message."""
    user = update.effective_user
    # bdbu.update_user_record(update=update, context=context)

    user_bot_id = get_user_bot_id(update, context)
    (valid_geo_name, geo_name), (valid_interval, interval) = parse_Geolocation_Interval(context, parse_args=True,
                                                                                        user_bot_id=user_bot_id)
    logger.info("weather for geo_name %s at %s", geo_name, interval)

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
    # bdbu.update_user_record(update=update, context=context)

    (valid_geo_name, geo_name), (valid_interval, interval) = parse_Geolocation_Interval(context, parse_args=True)
    logger.info("summary -> geo_name=%s moment=%s", geo_name, interval)

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


async def callback_timer_DAILY(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    bot_id = context.bot.id
    user_bot_id = str(job.chat_id) + "#" + str(bot_id)
    # user_bot_id = context.chat_data[bdbu.botUsers_table.partition_key]    # undef when wrong context!
    user_name = context.chat_data[bdbu.botUsers_table.sort_key]

    photo_name = job.name + "_photo.png"     # 442763659_photo.jpg
    pk_sk_user_id = job.data

    (valid_geo_name, geo_name), (valid_interval, interval) = \
        parse_Geolocation_Interval(context, parse_args=False, user_bot_id=user_bot_id)
    logger.info("%s:: callback_timer_DAILY> geo_name=%s moment=%s", job.name, geo_name, interval)

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

    try:
        await context.bot.send_message(chat_id=job.chat_id, text=text)
    except Exception as e:
        pass
        print(job.chat_id, "alarm:: An exception occurred ************** !!!!!!!!!!!!!!!!!!!!!", e)

    # ++++++++++++++++++++++
    mp.plot_color_of_the_days(observer=observer_obj, days=4, file_name=photo_name, job_name=job.name)

    logger.info("send_photo %s", photo_name)

    try:
        await context.bot.send_photo(chat_id=job.chat_id, photo=open(photo_name, 'rb'))
    except Exception as e:
        pass
        print(job.chat_id, "alarm:: An exception occurred ************** !!!!!!!!!!!!!!!!!!!!!", e)


def remove_job_if_exists(job_name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def setup_timer_DAILY(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""

    # user = update.effective_user
    chat_id = update.effective_message.chat_id
    # bot = context.bot
    # user_bot_id = str(chat_id) + "#" + str(bot.id)
    # user_bot_id = user_db_data[bdbu.botUsers_table.partition_key]  # string
    # user_name = context.chat_data['sk_user_bot_name']
    user_bot_id = context.chat_data[bdbu.botUsers_table.partition_key]
    user_name = context.chat_data[bdbu.botUsers_table.sort_key]

    job_name = user_bot_id + "#DAILY"

    (valid_geo_name, geo_name), (valid_interval, interval) = parse_Geolocation_Interval(context, parse_args=False)
    logger.info("weather for geo_name %s at %s", geo_name, interval)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++

    text = ""
    valid_reminder, dt_hhmm_unaware, dt_hhmm_utc = parse_Reminder(update, context, observer=observer_obj)

    if valid_reminder in (bdbu.PrmOrig.DEF, bdbu.PrmOrig.SET, bdbu.PrmOrig.ARG):
        text += "Заданий час: " + str(dt_hhmm_unaware.time()) + " | " + str(dt_hhmm_utc.time()) + " UTC"
        logger.info(text)

    elif valid_reminder in (bdbu.PrmOrig.DEF_INVALID, bdbu.PrmOrig.SET_INVALID,
                            bdbu.PrmOrig.ARG_INVALID):
        text += "Вибачте, задайте час в форматі [HHMM] / " + str(bdbu.PrmOrig(valid_reminder))
        logger.info(text)
        await update.effective_message.reply_text(text)
        return


    # ############# Specify timer with valid [HHMM] ###############
    job_removed = remove_job_if_exists(job_name, context)
    if job_removed:
        text += "\nСтарий таймер видалено."

    job_daily = context.job_queue.run_daily(
        callback_timer_DAILY,
        time=time(hour=dt_hhmm_utc.hour, minute=dt_hhmm_utc.minute,
                  second=dt_hhmm_utc.second, tzinfo=pytz.timezone('UTC')),
        days=(0, 1, 2, 3, 4, 5, 6),
        name=user_bot_id + "#DAILY",
        chat_id=int(chat_id),
        user_id=int(chat_id),
        # data={'pk': user_bot_id, 'sk': user_name},
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
    text += "\n" + str(job_daily.name) + " - " + str(job_daily.next_t.time())

    user_db_data = context.chat_data  # ???
    user_db_data["activity"]["enable_daily"] = True
    bdbu.update_user_context_db(pk_sk_id={'pk': user_bot_id, 'sk': user_name}, user_db_data=user_db_data)

    await update.effective_message.reply_text(text)


async def color_of_the_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.effective_user
    # bdbu.update_user_record(update=update, context=context)

    chat_id = update.message.chat_id
    chat_job_name = str(chat_id) + "#REP"           # 442763659#REP
    photo_name = str(chat_id) + "_photo.png"        # 442763659_photo.jpg

    (valid_geo_name, geo_name), (valid_interval, interval) = parse_Geolocation_Interval(context, parse_args=True)
    logger.info("color_of_the_days -> geo_name=%s moment=%s", geo_name, interval)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    mp.plot_color_of_the_days(observer=observer_obj, days=4, file_name=photo_name, job_name=chat_job_name)

    logger.info("color_of_the_days - %s", photo_name)
    await update.message.reply_photo(photo=open(photo_name, 'rb'))


initial_pass = False


async def restart_service(context: ContextTypes.DEFAULT_TYPE):

    global initial_pass

    if not initial_pass:
        initial_pass = True

        bot_name = context.bot.name

        list_of_items, count = bdbu.user_service_query(bot_name=bot_name)

        pers_data = context.application.chat_data
        # pprint(pers_data)
        for itm in pers_data:
            print('>>>>>>', itm)
            if not isinstance(itm, str):
                # The variable is a string
                print('>>>', itm, pers_data[itm]['context_user_data'])
                pass
                # del context.appication.chat_data['itm']
                # delattr(context.application, 'chat_data')

        user_counter = -1

        if count > 0:
            for user_db_data in list_of_items:
                user_counter += 1
                # print(user_db_data)

                user_bot_id = user_db_data[bdbu.botUsers_table.partition_key]      # string
                user_name = user_db_data[bdbu.botUsers_table.sort_key]
                chat_id = user_bot_id.split("#")[0]

                # Get "context_user_data" from DB of set defaults
                user_db_data.setdefault('context_user_data', "{}")          # for non-existent fields in the database !!!
                context_user_data = json.loads(user_db_data['context_user_data'])
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ defaults
                context_user_data.setdefault(opc.key_Geolocation, "OLSZTYN")
                context_user_data.setdefault(opc.key_Interval, "4.567")
                context_user_data.setdefault(opc.key_Reminder, "0123")

                print(user_counter, "::", user_bot_id, user_name, context_user_data)

                text = user_bot_id + ': bot re-started...'

                job_rep = context.job_queue.run_repeating(
                    rwt.callback_timer_REP,
                    interval=3600 + 10*user_counter,     # 3 sec divergence
                    name=user_bot_id + "#REP",
                    user_id=int(chat_id),
                    chat_id=int(chat_id),
                    # data={'pk': user_bot_id, 'sk': user_name},
                    first=10,
                )
                job_rep.job.misfire_grace_time = 300
                t.sleep(1)
                text += "\n" + str(job_rep.name) + " - " + str(job_rep.next_t.time())[:8]

                # Restore timer for reminder
                user_db_data.setdefault('activity', "{}")                   # for non-existent fields in the database !!!
                activity = json.loads(user_db_data['activity'])
                print(user_counter, "::", user_bot_id, activity)
                enable_daily = activity.get('enable_daily', False)
                daily_utc_time = activity.get('daily_utc_time', [10, 10, 10])

                if enable_daily:
                    job_daily = context.job_queue.run_daily(
                        callback_timer_DAILY,
                        time=time(
                            hour=daily_utc_time[0],
                            minute=daily_utc_time[0],
                            second=daily_utc_time[0],
                            tzinfo=pytz.timezone('UTC')),
                        days=(0, 1, 2, 3, 4, 5, 6),
                        name=user_bot_id + "#DAILY",
                        user_id=int(chat_id),
                        chat_id=int(chat_id),
                        # data={'pk': user_bot_id, 'sk': user_name},
                        job_kwargs={},
                    )
                    job_daily.job.misfire_grace_time = 300
                    t.sleep(1)
                    text += "\n" + str(job_daily.name) + " - " + str(job_daily.next_t.time())

                try:
                    await context.bot.send_message(chat_id=int(chat_id), text=text)

                except Exception as e:
                    pass
                    print(user_bot_id, "restart_service:: Exception -", e)


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
    # persistence.flush()
    application = Application.builder().token(token).persistence(persistence).build()
    # application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mph", moon_phase))
    application.add_handler(CommandHandler("md", moon_day))
    application.add_handler(CommandHandler("sr", sun_rise))
    application.add_handler(CommandHandler("zod", zodiac))          # /zod <GEO_PLACE>
    application.add_handler(CommandHandler("wt", weather))
    application.add_handler(CommandHandler("sum", summary))
    application.add_handler(CommandHandler("set", setup_timer_DAILY))
    application.add_handler(CommandHandler("cod", color_of_the_days))

    application.add_handler(opc.observer_conversation_handler)      # /obs
    # application.add_handler(opc.observer_handler)
    application.add_handler(opc.show_bot_user_db_data_handler)      # /show_data
    application.add_handler(opc.repair_bot_data_handler)            # /repair_bot_data
    application.add_handler(opc.repair_user_db_data_handler)        # /repair_db_data

    application.add_handler(CommandHandler("rep", rwt.setup_timer_REP))
    application.add_handler(CommandHandler("pause", rwt.pause_timer_REP))
    application.add_handler(CommandHandler("run", rwt.run_timer_REP))
    application.add_handler(CommandHandler("urep", rwt.unset_timer_REP))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Schedule the function to run every 10 seconds
    # application.job_queue.run_repeating(maintenance_service, interval=30, first=5)
    application.job_queue.run_once(restart_service, 1)
    # t.sleep(20)

    # ...and the error handler
    # application.add_error_handler(error_handler)
    # application.add_error_handler(handle_exception)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
