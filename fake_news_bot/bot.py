import os
import re
from .llm import ask_llm, llm_cache
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
load_dotenv()


def filter_special_characters(text):
    # Define a regular expression pattern to identify special characters
    pattern = r'([_*\[\]()~`>#+\-=|{}.!])'

    # Prepend special characters with a backslash (\)
    filtered_text = re.sub(pattern, r'\\\1', text)

    return filtered_text

# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the FakeNewsAI Bot!")

# Command handler for the /ask command
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_message = await update.message.reply_text(text="We're analyzing your message for authenticity. It'll take a moment as we verify the credibility of the news.", reply_to_message_id=update.message.message_id)
    # try:
      # Call the ask_llm function and get the response
    question = None
    if update.message.text:
      question = update.message.text
    elif update.message.caption:
      question = update.message.caption
    else:
      raise ValueError("No question was found from your message.")
    response = ask_llm(question)
    # Create an InlineKeyboardMarkup
    keyboard = [[InlineKeyboardButton("👍", callback_data='report_correct'), InlineKeyboardButton("👎", callback_data='report_incorrect')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the response to the user
    # update.message.reply_text(response['output'])
    if "Agent stopped due to" in response['output'] or response['output'] == "":
      await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                              message_id=init_message.message_id,
                              text="Sorry, we couldn't process the information. Looks like we have an error. Please try again with a different question.")
      # Delete cache from langchain 
      llm_cache.delete_by_prompt(question)
    else:
      await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                message_id=init_message.message_id,
                                text=response['output'],
                              reply_markup=reply_markup)

    # Get the sources from the zero-shot agent
    results = {}
    for query in (response["intermediate_steps"]):
      if len(query) > 1:
        for result in query[1]:
          try:
            if result:
              title = str(result['title'])
              if title:
                results[title] = f"*[{filter_special_characters(title)}]({filter_special_characters(result['link'])})*"
          except Exception as e:
            print(e, "\n",result)
            continue
    if len(results.keys()) > 0:
      await context.bot.send_message(chat_id=update.effective_chat.id, text="_*Sources:*_\n"+"\n\n".join(results.values()), disable_web_page_preview=True, parse_mode="MarkdownV2")
    # except Exception as e:
    #   print(e)
    #   context.bot.edit_message_text(chat_id=update.effective_chat.id,
    #                             message_id=init_message.message_id, text="Error Occured: "+str(e))

# Define a function to handle the button click
async def report_incorrect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("We'll try to improve next time 🙏")

    # Get the original message that triggered the inline keyboard
    original_message = query.message

    # Edit the message to remove the inline keyboard
    await context.bot.edit_message_reply_markup(
        chat_id=original_message.chat_id,
        message_id=original_message.message_id,
        reply_markup=InlineKeyboardMarkup([])  # Pass an empty InlineKeyboardMarkup to remove the keyboard
    )
    
    # Delete cache from langchain
    # find parent message reply
    parent_message = original_message.reply_to_message
    if parent_message:
      # find the question
      question = None
      if parent_message.text:
        question = parent_message.text
      elif parent_message.caption:
        question = parent_message.caption
      else:
        raise ValueError("No question was found from the message to delete cache response.")
      # delete from cache
      print("Response was marked incorrect, deleting cache response for question:", question)
      llm_cache.delete_by_prompt(question)

async def report_correct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Thank you for the feedback ✅")

    # Get the original message that triggered the inline keyboard
    original_message = query.message

    # Edit the message to remove the inline keyboard
    await context.bot.edit_message_reply_markup(
        chat_id=original_message.chat_id,
        message_id=original_message.message_id,
        reply_markup=InlineKeyboardMarkup([])  # Pass an empty InlineKeyboardMarkup to remove the keyboard
    )


def main() -> None:
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    # Add the command handlers to the dispatcher
    start_handler = CommandHandler('start', start)
    ask_handler = CommandHandler('ask', ask)

    # Create a message handler that triggers the ask function for all non-command messages
    message_handler = MessageHandler(~filters.COMMAND, ask)
    application.add_handler(message_handler)

    application.add_handler(start_handler)
    application.add_handler(ask_handler)

    # Add a callback query handler for handling button clicks
    application.add_handler(CallbackQueryHandler(report_incorrect, pattern='report_incorrect'))
    application.add_handler(CallbackQueryHandler(report_correct, pattern='report_correct'))
    # Start the bot
    application.run_polling()
