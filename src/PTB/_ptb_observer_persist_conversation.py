#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

from pprint import pprint

import src.ephem_routines.ephem_package.geo_place as geo
import src.boto3_package.botDB_users as bdbu


import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

# key_Geolocation = u"Геолокація"
# key_Interval = u"Інтервал"
# key_Reminder = u"Нагадування"
# key_Addition = u"Додатково"
key_Geolocation = u"Geolocation"
key_Interval = u"Interval"
key_Reminder = u"Reminder"
key_Addition = u"Додатково"

reply_keyboard = [
    [key_Geolocation, key_Interval],
    [key_Reminder, key_Addition],
    [u"Готово"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,)


def dict_fields_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    dfields = [f"'{key}': {value}" for key, value in user_data.items()]
    return "\n".join(dfields).join(["\n", "\n"])


async def observer_setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation, display any stored data and ask user for input."""
    text = "Задайте географічне місце та час (момент відліку для цього місця)"
    logger.info("observer> %s:", text)

    await update.message.reply_text(text, reply_markup=markup)

    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    user = update.effective_user
    text = update.message.text  # .lower()
    context.user_data["choice"] = text
    if context.user_data.get(text):
        reply_text = f'Параметер "{text}" має значення: {context.user_data[text]}'
    else:
        reply_text = f'Параметер "{text}" не був заданий'

    logger.info("regular_choice> %s: text=%s context.user_data=%s", user.first_name, text, context.user_data)
    await update.message.reply_text(reply_text)

    return TYPING_REPLY


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Create a new observer object and save to context"""
    user = update.effective_user

    logger.info("custom_choice> %s: context.user_data=%s", user.first_name, context.user_data)
    await update.message.reply_text('Alright, please send me skill')

    return TYPING_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    # user_id = str(update.effective_user.id)
    user = update.effective_user
    bot = context.bot
    user_bot_id = str(user.id) + "#" + str(bot.id)

    text = update.message.text

    if "choice" in context.user_data and context.user_data["choice"] and context.user_data["choice"] is not None:
        category = context.user_data["choice"]
        context.user_data[category] = text.upper()
        del context.user_data["choice"]

    # user_db_data = bdbu.get_user_db_data(pk=user_bot_id)    # get old data
    # pprint(user_db_data)

    user_db_data = {}
    user_db_data['context_user_data'] = context.user_data   # update field

    if "activity" in user_db_data and user_db_data["activity"] and user_db_data["activity"] is not None:
        att = int(user_db_data["activity"]["attempts"])    # !!! when wrong request !!!
        user_db_data["activity"]["attempts"] = att + 1
        if att >= 5:
            user_db_data["activity"]["state"] = False      # !!! check this state to know how work with user !!!
        else:
            user_db_data["activity"]["state"] = True
            user_db_data["activity"]["attempts"] = 0

    bdbu.update_user_record(update=update, context=context, user_db_data=user_db_data)

    user_db_data = bdbu.get_user_db_data(pk=user_bot_id)    # get new data in context.chat_data
    context.chat_data.clear()                               # to delete a value from chat_data
    context.chat_data.update(user_db_data)                  # contain current updated user_db_data to work with

    await update.message.reply_text(
        f"Задані параметри збережені: {dict_fields_to_str(context.user_data)} \nМожна змінювати ці параметри.",
        reply_markup=markup,)

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""

    if "choice" in context.user_data:
        del context.user_data["choice"]

    await update.message.reply_text(
        f"Задані параметри збережені: {dict_fields_to_str(context.user_data)}", reply_markup=ReplyKeyboardRemove(),)

    return ConversationHandler.END


async def show_user_db_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the gathered info."""
    user = update.effective_user
    bot = context.bot
    user_bot_id = str(user.id) + "#" + str(bot.id)

    user_db_data = bdbu.get_user_db_data(pk=user_bot_id)
    print(user_bot_id, user_db_data)

    text = "Збережені параметри:"
    text += "\n*** context.user_data ***" + dict_fields_to_str(context.user_data)
    text += "\n*** context.chat_data ***" + dict_fields_to_str(context.chat_data)
    text += "\n*** user_db_data ***" + dict_fields_to_str(user_db_data)

    await update.message.reply_text(text)


async def repair_user_db_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Download user data to context.user_data"""
    user = update.effective_user
    bot = context.bot
    user_bot_id = str(user.id) + "#" + str(bot.id)

    user_db_data = bdbu.get_user_db_data(pk=user_bot_id)
    # if len(user_db_data) == 0:

    if "context_user_data" in user_db_data:
        context.user_data.clear()
        context.user_data.update(user_db_data['context_user_data'])

        context.chat_data.clear()
        context.chat_data.update(user_db_data)
    else:
        context.user_data.clear()
        context.chat_data.clear()

    text = "Збережені параметри:"
    text += "\n*** context.user_data ***" + dict_fields_to_str(context.user_data)
    text += "\n*** context.chat_data ***" + dict_fields_to_str(context.chat_data)
    text += "\n*** user_db_data ***" + dict_fields_to_str(user_db_data)

    await update.message.reply_text(text)



# def main_conversation_handler() -> None:
#     """Run the bot."""
#     # Create the Application and pass it your bot's token.
#     # persistence = PicklePersistence(filepath="conversationbot")
#     # application = Application.builder().token("TOKEN").persistence(persistence).build()
#
#     # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
#     observer_conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("obs", observer)],
#         states={
#             CHOOSING: [
#                 MessageHandler(
#                     filters.Regex("^(Age|Favourite colour|Number of siblings)$"), regular_choice
#                 ),
#                 MessageHandler(filters.Regex("^Something else...$"), custom_choice),
#             ],
#             TYPING_CHOICE: [
#                 MessageHandler(
#                     filters.TEXT & ~(filters.COMMAND | filters.Regex("^Готово$")), regular_choice
#                 )
#             ],
#             TYPING_REPLY: [
#                 MessageHandler(
#                     filters.TEXT & ~(filters.COMMAND | filters.Regex("^Готово$")),
#                     received_information,
#                 )
#             ],
#         },
#         fallbacks=[MessageHandler(filters.Regex("^Готово$"), done)],
#         name="my_conversation",
#         persistent=True,
#     )
#     application.add_handler(observer_conv_handler)
#
#     show_data_handler = CommandHandler("show_data", show_data)
#     application.add_handler(show_data_handler)
#
#     # Run the bot until the user presses Ctrl-C
#     application.run_polling()


# if __name__ == "__main__":
#     main_conversation_handler()


observer_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("obs", observer_setup)],
    states={
        CHOOSING: [
            # key_Geoloc, key_Moment, key_Notify, key_Addition
            MessageHandler(filters.Regex(f"^({key_Geolocation}|{key_Interval}|{key_Reminder})$"), regular_choice),
            MessageHandler(filters.Regex(f"^{key_Addition}$"), custom_choice),
        ],
        TYPING_CHOICE: [
            MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Готово$")), regular_choice)
        ],
        TYPING_REPLY: [
            MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Готово$")), received_information)
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Готово$"), done)],
    name="astro_conversation",
    persistent=True,
)

observer_handler = CommandHandler("obs", observer_setup)
show_user_db_data_handler = CommandHandler("show_data", show_user_db_data)
repair_user_db_data_handler = CommandHandler("repair_data", repair_user_db_data)


