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


from datetime import datetime, time
import pytz
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
                "\n/rep [SS] - run weather recorder timer" \
                "\n/urep - reset weather recorder timer" \
                "\n/cod - colors of days" \
                "\n" \
                "\ndeveloped by Serhii Surmylo (Ukraine), 2023"
    await update.message.reply_text(help_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    bdbu.monitor_user_record(update=update, context=context)
    user = update.effective_user

    text = f"{user.id} <{user.first_name} {user.last_name}> echo: {update.message.text}"
    logger.info(text)
    await update.message.reply_text(text)


def parse_args(context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) > 0:
        geo_name = str(context.args[0])
    else:
        if opc.key_Geolocation in context.user_data:
            geo_name = context.user_data[opc.key_Geolocation]
        else:
            geo_name = "Mragowo"

    if opc.key_Interval in context.user_data:
        moment = context.user_data[opc.key_Interval]
    else:
        moment = "5"

    return geo_name, moment


def get_chat_params(param_dict=None):
    if param_dict is None:
        return

    if opc.key_Geolocation in param_dict:
        geo_name = param_dict[opc.key_Geolocation]
    else:
        geo_name = "Mragowo"

    if opc.key_Interval in param_dict:
        moment = param_dict[opc.key_Interval]
    else:
        moment = "5.0"

    return geo_name, moment


async def moon_phase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_phase to the user message."""
    user = update.effective_user
    bdbu.monitor_user_record(update=update, context=context)

    geo_name, moment = parse_args(context)
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
    bdbu.monitor_user_record(update=update, context=context)

    geo_name, moment = parse_args(context)
    logger.info("moon day for geo_name:  %s at %s", geo_name, moment)

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
    bdbu.monitor_user_record(update=update, context=context)

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
    bdbu.monitor_user_record(update=update, context=context)

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
    descr_str = list_of_items[0]["description_0"]
    text += "\n\n" + dbmz.string_between_tags(input_string=descr_str, tag_index=0)

    logger.info("moon_zodiac of %s: %s", user.first_name, text)
    await update.message.reply_text(text)


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return current weather to the user message."""
    user = update.effective_user
    bdbu.monitor_user_record(update=update, context=context)

    geo_name, moment = parse_args(context)
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
    bdbu.monitor_user_record(update=update, context=context)

    geo_name, moment = parse_args(context)
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
    chat_id = str(job.chat_id)
    chat_job_name = chat_id + "#REP"
    photo_name = chat_id + "_photo.png"     # 442763659_photo.jpg

    sett_dict = bdbu.get_user_sett(pk=chat_id)
    # logger.info("photo: %s === %s", photo_name, str(sett_dict))

    if opc.key_Geolocation in sett_dict:
        geo_name = sett_dict[opc.key_Geolocation]
    else:
        geo_name = "Mragowo"

    if opc.key_Interval in sett_dict:
        moment = sett_dict[opc.key_Interval]
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
    mp.plot_color_of_the_days(observer=observer_obj, days=5, file_name=photo_name, chat_job=chat_job_name)

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


def get_dt_hhmm(hhmm=""):

    dt_hhmm = datetime.strptime("2000-01-01 0000", "%Y-%m-%d %H%M")

    try:
        dt_hhmm = datetime.strptime("2000-01-01 " + hhmm, "%Y-%m-%d %H%M")

    except ValueError:

        return False, dt_hhmm

    return True, dt_hhmm


async def set_daily_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    user = update.effective_user

    chat_id = update.effective_message.chat_id

    # timezone = context.user_data["time zone"]
    # print(timezone)

    text = ""
    dt_hhmm = None
    try:
        hhmm = context.args[0]

        result, dt_hhmm = get_dt_hhmm(hhmm=hhmm)
        if result:
            text += "Заданий час: " + str(dt_hhmm.time())
            logger.info(text)
        else:
            text += "Вибачте, задайте час в форматі [HHMM]"
            logger.info(text)
            await update.effective_message.reply_text(text)
            return

    except (IndexError, ValueError):

        sett_dict = bdbu.get_user_sett(pk=str(chat_id))
        # print("###", sett_dict, sett_dict[opc.key_Reminder])

        if opc.key_Reminder in sett_dict.keys():
            hhmm = sett_dict[opc.key_Reminder]
            result, dt_hhmm = get_dt_hhmm(hhmm=hhmm)
            text += "Збережені настройки часу нагадування: " + str(dt_hhmm.time())
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

    bdbu.monitor_user_record(update=update, context=context)

    await update.effective_message.reply_text(text)


async def color_of_the_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.effective_user
    bdbu.monitor_user_record(update=update, context=context)

    chat_id = update.message.chat_id
    chat_job_name = str(chat_id) + "#REP"           # 442763659#REP
    photo_name = str(chat_id) + "_photo.png"        # 442763659_photo.jpg

    geo_name, moment = parse_args(context)
    logger.info("color_of_the_days -> geo_name=%s moment=%s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)
    # ++++++++++++++++++++++
    mp.plot_color_of_the_days(observer=observer_obj, days=5, file_name=photo_name, chat_job=chat_job_name)

    logger.info("color_of_the_days - %s", photo_name)
    await update.message.reply_photo(photo=open(photo_name, 'rb'))


initial_pass = False


async def maintenance_service(context: ContextTypes.DEFAULT_TYPE):
    global initial_pass

    if not initial_pass:
        initial_pass = True

        list_of_items, count = bdbu.user_scan_filter()

        if count > 0:
            for item_dict in list_of_items:

                chat_id = item_dict[bdbu.botUsers_table.partition_key]      # string
                user_setting = item_dict["user_setting"]
                reminder_hhmm = user_setting[opc.key_Reminder]
                print("::", chat_id, reminder_hhmm)

                text = chat_id + ': bot re-started...'

                # Restore timer for weather grabber
                job_rep = context.job_queue.run_repeating(
                    rwt.callback_repeating,
                    interval=3600,
                    name=chat_id + "#REP",
                    chat_id=chat_id,
                    first=10
                )
                text += "\n" + str(job_rep.name) + " " + str(job_rep.next_t)[:19]

                # Restore timer for reminder
                if opc.key_Reminder in user_setting.keys():
                    reminder_hhmm = user_setting[opc.key_Reminder]
                    result, dt_hhmm = get_dt_hhmm(hhmm=reminder_hhmm)

                    job_daily = context.job_queue.run_daily(
                        alarm,
                        time=time(
                            hour=dt_hhmm.hour,
                            minute=dt_hhmm.minute,
                            second=10,
                            tzinfo=pytz.timezone('Europe/Warsaw')),
                        days=(0, 1, 2, 3, 4, 5, 6),
                        name=chat_id + "#DAILY",
                        chat_id=chat_id,
                        job_kwargs={},
                    )
                    text += "\n" + str(job_daily.name) + " " + str(job_daily.next_t)[:19]

                await context.bot.send_message(chat_id=chat_id, text=text)


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
    # application.add_handler(opc.observer_handler)
    application.add_handler(opc.show_data_handler)

    application.add_handler(CommandHandler("rep", rwt.set_repeat_timer))
    application.add_handler(CommandHandler("pause", rwt.pause_repeat_timer))
    application.add_handler(CommandHandler("run", rwt.run_repeat_timer))
    application.add_handler(CommandHandler("urep", rwt.unset_repeat_timer))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Schedule the function to run every 10 seconds
    # job = context.job_queue.run_repeating(callback_repeating, interval=due, name=job_name, chat_id=chat_id, first=10)
    application.job_queue.run_repeating(maintenance_service, interval=30, first=5)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
