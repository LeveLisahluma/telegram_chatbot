#!/usr/bin/env python3

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import logging
import spacy

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

nlp = spacy.load('en_core_web_sm')

TOKEN = '7533930721:AAFIibfo2h3Em9JAddem597Ey2T38h35B-k'

questions = [
    {
        'question': "What is the capital of France?",
        'options': ['Berlin', 'Madrid', 'Paris', 'Rome'],
        'answer': 3
    },
    {
        'question': "What is the largest planet in our Solar System?",
        'options': ['Earth', 'Jupiter', 'Mars', 'Venus'],
        'answer': 2
    },
    {
        'question': "What is the chemical symbol for water?",
        'options': ['O2', 'H2O', 'CO2', 'HO2'],
        'answer': 2
    },
    {
        'question': "Which country is known as the Land of the Rising Sun?",
        'options': ['China', 'Japan', 'South Korea', 'Thailand'],
        'answer': 2
    },
    {
        'question': "How many continents are there on Earth?",
        'options': ['5', '6', '7', '8'],
        'answer': 3
    }
]


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['current_question'] = 0
    context.user_data['score'] = 0
    await ask_question(update, context)


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_index = context.user_data['current_question']
    question = questions[question_index]
    options_text = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(question['options'])])
    await update.message.reply_text(f"{question['question']}\n\n{options_text}")


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    doc = nlp(user_input)

    if any(token.like_num for token in doc):
        user_answer = int(user_input)
        question_index = context.user_data['current_question']
        correct_answer = questions[question_index]['answer']

        if user_answer == correct_answer:
            context.user_data['score'] += 1
            await update.message.reply_text("Correct!")
        else:
            await update.message.reply_text("Incorrect.")

        context.user_data['current_question'] += 1
        if context.user_data['current_question'] < len(questions):
            await ask_question(update, context)
        else:
            score = context.user_data['score']
            await update.message.reply_text(f"Quiz finished! Your score is {score}/{len(questions)}.")
    else:
        await update.message.reply_text("Please enter a valid number corresponding to one of the options.")


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start_quiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    application.run_polling()


if __name__ == '__main__':
    main()