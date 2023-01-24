#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.


import src.ephem_routines.ephem_package.geo_place as geo


"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
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

key_Geolocation = "Геолокація"
key_Interval = "Інтервал"
key_Reminder = "Нагадування"
key_Addition = "Додатково"

reply_keyboard = [
    [key_Geolocation, key_Interval],
    [key_Reminder, key_Addition],
    ["Готово"],
]
markup = ReplyKeyboardMarkup(reply_keyboard,
                             one_time_keyboard=True,
                             )


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def observer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation, display any stored data and ask user for input."""
    reply_text = "Вітаю! Потрібно задаті географічне місце та час (момент відліку для цього місця)"

    await update.message.reply_text(reply_text, reply_markup=markup)

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

    logger.info("%s: text=%s context.user_data=%s", user.first_name, text, context.user_data)
    await update.message.reply_text(reply_text)

    return TYPING_REPLY


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Create a new observer object and save to context"""
    user = update.effective_user

    logger.info("%s: context.user_data=%s", user.first_name, context.user_data)
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    text = update.message.text
    category = context.user_data["choice"]
    context.user_data[category] = text.upper()
    del context.user_data["choice"]

    # context.chat_data.update(context.user_data)     # !!!

    await update.message.reply_text(
        "Задані параметри:"
        f"{facts_to_str(context.chat_data)}"
        "Можна змінювати ці параметри.",
        reply_markup=markup,
    )

    return CHOOSING


async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the gathered info."""

    # context.chat_data.update(context.user_data)
    await update.message.reply_text(
        f"Збережені параметри: {facts_to_str(context.chat_data)}"
    )


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    if "choice" in context.user_data:
        del context.user_data["choice"]

    # context.chat_data.update(context.user_data)  # !!!

    await update.message.reply_text(
        f"Задані параметри: {facts_to_str(context.chat_data)}",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


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
    entry_points=[CommandHandler("obs", observer)],
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

show_data_handler = CommandHandler("show_data", show_data)


