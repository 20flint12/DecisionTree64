#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

from datetime import datetime, time
from pprint import pprint

import src.ephem_routines.ephem_package.geo_place as geo
import src.PTB._ptb_observer_persist_conversation as opc
import src.PTB.ptb_main_astro as pma
import src.boto3_package.mainDB_weather as mr
import src.boto3_package.botDB_users as bdbu


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


async def callback_timer_REP(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    data_user_chat_id = job.data

    # user_db_data = bdbu.get_user_db_data(pk=data_user_chat_id)
    #
    # # print(chat_id, ":: ", context.chat_data, "\n*************************", user_db_data)
    # if context.chat_data == user_db_data:
    #     pass
    #     # print("++++++")
    # else:
    #     print("------")
    #     print(data_user_chat_id, ":: \n", context.chat_data, "---------------\n", user_db_data)
    #
    #     if context.chat_data is None:
    #         pass
    #         # context.chat_data.clear()
    #         # context.chat_data = {}
    #     else:
    #         context.chat_data.clear()
    #     context.chat_data.update(user_db_data)
    #
    #     if context.user_data is None:
    #         pass
    #         # context.user_data.clear()
    #         # context.user_data = {}
    #     else:
    #         context.user_data.clear()
    #     context.user_data.update(user_db_data['context_user_data'])

    text = job.name + ' @ ' + str(job.next_t)[:19] + "\n" + str(context.job_queue.jobs())[25:]
    # logger.info(text)

    (valid_geo_name, geo_name), (valid_interval, interval) = pma.parse_Geolocation_Interval(context, parse_args=False)

    logger.info("%s: callback_timer_REP -> geo_name=%s moment=%s", data_user_chat_id, geo_name, interval)

    observer_obj = geo.Observer(geo_name=geo_name, unaware_datetime=datetime.today())
    text = ""
    text += str(observer_obj)

    data_dict, out_text = mr.main_put_record(observer=observer_obj, job_name=job.name)
    text += "\n" + str(data_dict)
    text += out_text
    try:
        await context.bot.send_message(chat_id=job.chat_id, text=text)
    except Exception as e:
        print(data_user_chat_id, ":: callback_timer_REP *** Exception *** - ", e)


async def setup_timer_REP(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job_rep to the queue."""
    user_id = update.effective_user.id
    chat_id = update.effective_message.chat_id
    bot = context.bot
    user_bot_id = str(chat_id) + "#" + str(bot.id)
    job_name = user_bot_id + "#REP"

    text = ""
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(job_name, context)
        if job_removed:
            text += "\nСтарий таймер видалено."

        job_rep = context.job_queue.run_repeating(
            callback_timer_REP,
            interval=due,
            name=user_bot_id + "#REP",
            user_id=chat_id,
            chat_id=chat_id,
            data=user_bot_id,
            first=10
        )
        job_rep.job.misfire_grace_time = 30

        text += "\n" + str(job_rep.name) + " " + str(job_rep.next_t)[:19]
        # text += str(job_rep.name) + " timer successfully set."

        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /rep <seconds>")


async def pause_timer_REP(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def run_timer_REP(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def unset_timer_REP(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


