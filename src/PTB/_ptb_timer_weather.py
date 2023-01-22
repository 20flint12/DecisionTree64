#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

from datetime import datetime, time
from pprint import pprint

import src.ephem_routines.ephem_package.geo_place as geo
import src.boto3_package.mainDB_weather as mr
import src.PTB._ptb_observer_persist_conversation as opc


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



def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def callback_repeating(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    text = job.name + ' @ ' + str(job.next_t)[:19] + "\n" + str(context.job_queue.jobs())[25:]
    # logger.info(text)
    # init_id, out_str = mr.main_put_record(_chat_job=job.name)


    if opc.key_Geoloc in context.chat_data:
        geo_name = context.chat_data[opc.key_Geoloc]
    else:
        geo_name = "Mragowo"

    if opc.key_Moment in context.chat_data:
        moment = context.chat_data[opc.key_Moment]
    else:
        moment = "5"
    logger.info("callback_repeating -> geo_name=%s moment=%s", geo_name, moment)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)


    data_dict, out_text = mr.main_put_record(observer=observer_obj, _chat_job=job.name)
    text += "\n" + str(data_dict)
    text += out_text
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


#     application.add_handler(CommandHandler("rep", set_repeat_timer))
#     application.add_handler(CommandHandler("pause", pause_repeat_timer))
#     application.add_handler(CommandHandler("run", run_repeat_timer))
#     application.add_handler(CommandHandler("urep", unset_repeat_timer))


