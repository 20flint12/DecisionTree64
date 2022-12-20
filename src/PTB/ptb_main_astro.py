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


from datetime import datetime
import src.ephem_routines.ephem_package.moon_day as md
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd
import src.weather_package.main_openweathermap as wt

import src.PTB.ptb_observer_persist_conversation as opc


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
                "\n/echo - just echo command" \
                "\n/mph - calculates current moon phase for Kharkiv" \
                "\n/md - calculates moon day at current time and current place" \
                "\n/sr - sunrise and sunset for Mragowo" \
                "\n/zod Moon - calculates zodiac of Moon" \
                "\n/zod Sun - calculates zodiac of Sun" \
                "\n/wt <CITY> - current weather in the CITY" \
                "\n\ndeveloped by Serhii Surmylo (Ukraine)"
    await update.message.reply_text(help_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    logger.info("echo from %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(update.message.text)


async def moon_phase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_day to the user message."""
    user = update.effective_user
    md_dict, str_head = md.main_moon_phase("Kharkiv", datetime.today())
    update.message.text = str_head
    logger.info("moon_day of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(update.message.text)


async def moon_day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_day to the user message."""
    user = update.effective_user
    md_dict, str_head = md.main_moon_day("Kharkiv", datetime.today())
    update.message.text = str_head
    logger.info("moon_day of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(update.message.text)


async def sur_rise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_day to the user message."""
    user = update.effective_user
    update.message.text = sr.main_sun_rise_sett("Mragowo", datetime.today())
    logger.info("moon_day of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(update.message.text)


async def zodiac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return moon_day to the user message."""
    user = update.effective_user

    try:
        planet = str(context.args[0])
        logger.info("planet: %s", planet)

        ecl_dict, str_head = zd.main_zodiac_body("Mragowo", datetime.today(), planet)
        update.message.text = str_head
        logger.info("moon_zodiac of %s: %s", user.first_name, update.message.text)

        await update.message.reply_text(update.message.text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /zod <GEO_PLACE> Moon/Sun")


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return current weather to the user message."""
    user = update.effective_user

    if len(context.args) > 0:
        city = str(context.args[0])
    else:
        # {'geo place': 'london', 'datetime': 'tomorrow', 'choice': 'additional'}
        city = context.user_data["geo place"]
    logger.info("weather for city: %s", city)

    try:
        wth_dict, str_head = wt.main_weather_now(city, datetime.today())
        update.message.text = str_head
        logger.info("weather of %s: %s", user.first_name, update.message.text)

        await update.message.reply_text(update.message.text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /wt <CITY>")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        logger.info("due: %s", context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


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
    application.add_handler(CommandHandler("sr", sur_rise))
    application.add_handler(CommandHandler("zod", zodiac))          # /zod <GEO_PLACE>
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("wt", weather))

    application.add_handler(opc.observer_conversation_handler)      # /obs
    application.add_handler(opc.show_data_handler)

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
