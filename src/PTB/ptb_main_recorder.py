#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
# https://docs.python-telegram-bot.org/en/v20.0a6/telegram.ext.jobqueue.html
# https://github.com//python-telegram-bot/python-telegram-bot/wiki/Storing-bot%2C-user-and-chat-related-data

from datetime import datetime
from pprint import pprint

import src.boto3_package.mainDB_recorder as mr
import src.mathplot_package.plot_DB_attr as mp

import socket
hostname = socket.gethostname()     # DELL-DEV
print(hostname)

"""
Simple Bot to send timed Telegram messages.

This Bot uses the Application class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

Note:
To use arbitrary callback data, you must install ptb via
`pip install python-telegram-bot[callback-data]`
"""

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
from telegram import ForceReply, Update
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


# Define a few command handlers. These usually take the two arguments update and
# context.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    logger.info("echo from %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(update.message.text)


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(chat_id=job.chat_id, text=f"Beep! {job.data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_once_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
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


async def unset_once_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


async def callback_repeating(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    text = job.name + ' @ ' + str(job.next_t)[:19] + "\n" + str(context.job_queue.jobs())[25:]
    # logger.info(text)
    init_id, out_str = mr.main_put_record(_chat_job=job.name)
    text += out_str
    await context.bot.send_message(chat_id=job.chat_id, text=text)


async def set_repeat_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    job_name = str(chat_id) + "#REP"
    text = ""
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(job_name, context)
        if job_removed:
            text += " Old one was removed.\n"

        job = context.job_queue.run_repeating(callback_repeating, interval=due, name=job_name, chat_id=chat_id, first=10)
        text += str(job.name) + " timer successfully set."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /rep <seconds>")


async def pause_repeat_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Pause the job if the user changed their mind."""
    chat_id = update.message.chat_id
    context_job_name = str(chat_id) + "#REP"
    current_jobs = context.job_queue.get_jobs_by_name(context_job_name)

    text = ""
    if not current_jobs:
        text += "no job"

        logger.info("%s", text)
        await update.message.reply_text(text)

    for job in current_jobs:
        job.enabled = False  # Temporarily disable this job
        text += job.name + " timer paused."

        logger.info("%s", text)

        # text += str(context.job_queue)
        text += "\n" + str(current_jobs)[25:]

        await update.message.reply_text(text)


async def run_repeat_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ran the job if the user changed their mind."""
    chat_id = update.message.chat_id
    context_job_name = str(chat_id) + "#REP"
    current_jobs = context.job_queue.get_jobs_by_name(context_job_name)

    text = ""
    if not current_jobs:
        text += "no job"

        logger.info("%s", text)
        await update.message.reply_text(text)

    for job in current_jobs:
        job.enabled = True  # Enable this job
        text += job.name + " timer ran."

        logger.info("%s", text)

        # text += str(context.job_queue)
        text += "\n" + str(current_jobs)[25:]

        await update.message.reply_text(text)


async def unset_repeat_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    context_job_name = str(chat_id) + "#REP"
    job_removed = remove_job_if_exists(context_job_name, context)

    text = ""

    if job_removed:
        text += context_job_name + " removed."
    else:
        text += "You have no active repeating timer."

    # text += "Timer successfully cancelled!" if job_removed else "You have no active timer."

    await update.message.reply_text(text)


async def reply_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    chat_id = update.message.chat_id
    job_name = str(chat_id) + "#REP"            # 442763659#REP
    photo_name = str(chat_id) + "_photo.png"    # 442763659_photo.jpg
    # print(job_name)

    list_of_items, text = mr.main_query_range(job_name, "2022-12-11 21:11:17", "2023-12-13 07:00:17")
    # pprint(list_of_items)
    data_list = mr.main_query_filter(list_of_items, attr="weather", field="T")
    # print(data_list)

    mp.plot_list(data_list, file_name=photo_name)

    text = "reply_photo"
    logger.info("%s", text)
    await update.message.reply_photo(photo=open(photo_name, 'rb'))


def main() -> None:
    """
    Start the bot.
    """
    if hostname == "DELL-DEV":
        token = "1261633346:AAHC4ctXxjZ4hdATaP_Of0608Ju7lIn5sxE"  # @FlintSmart_bot
        persist_filepath = "ptb_main_recorder_dev"
    else:
        token = "1796700435:AAG_RgjpPYOedk8iFzgN7DXZ0tYcwU39LvQ"  # @InspectorBiblyka_bot
        persist_filepath = "ptb_main_recorder_prod"
    persistence = PicklePersistence(filepath=persist_filepath)
    application = Application.builder().token(token).persistence(persistence).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_once_timer))
    application.add_handler(CommandHandler("unset", unset_once_timer))
    application.add_handler(CommandHandler("rep", set_repeat_timer))
    application.add_handler(CommandHandler("pause", pause_repeat_timer))
    application.add_handler(CommandHandler("run", run_repeat_timer))
    application.add_handler(CommandHandler("urep", unset_repeat_timer))

    application.add_handler(CommandHandler("photo", reply_photo))


    # job_queue.run_once, job_queue.run_repeating, job_queue.run_daily and job_queue.run_monthly

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
