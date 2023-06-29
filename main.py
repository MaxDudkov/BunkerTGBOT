import logging

import yaml
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, Update
from telegram.ext import CommandHandler, filters, Application, \
    ContextTypes

from telegram.ext import MessageHandler


class UserContext:
    def __init__(self):
        self.last_command = ""
        self.state = "active"
        self.active_game_id = ""

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_last_command(self):
        return self.last_command

    def set_last_command(self, last_command):
        self.last_command = last_command

    def set_active_game_id(self, id):
        self.active_game_id = id

    def get_active_game_id(self):
        return self.active_game_id


class TGBot(object):

    def __init__(self):
        self.config = yaml.safe_load(open('config.yml'))
        self.data_base = {}
        self.token = self.config["token"]
        logging.basicConfig(level=logging.INFO)

    def get_or_create_context(self, username, nickname=None):
        if username in self.data_base:
            return self.data_base[username]

        else:
            ctx = UserContext()
            if nickname:
                ctx.nickname = nickname
            self.data_base[username] = ctx
            return ctx

    def run(self):
        bot = Application.builder().token(self.token).build()

        for cmd in self.config['commands']:
            if "make_" + cmd['type'] not in dir(self):
                logging.error("cant find method " + "make_" + cmd['type'])
                return

            maker = getattr(self, "make_" + cmd['type'])
            if cmd.get('command_handler', False):
                handler = CommandHandler(cmd['cmd'], maker(cmd))

            else:
                handler = MessageHandler(cmd['cmd'], maker(cmd))

            bot.add_handler(handler)
            logging.info("added handler %s", cmd['cmd'])

        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.get_echo())

        bot.add_handler(echo_handler)

        bot.run_polling()

    def make_interactive_command(self, cmd):
        if cmd.get('callback_data', False):
            if cmd.get('url', False):
                reply_markup = InlineKeyboardMarkup(
                    menu_builder([InlineKeyboardButton(x, url=str(i)) for i, x in
                                  zip(cmd['callback_data'], cmd['buttons'])], cmd['buttons_count']))
            else:
                reply_markup = InlineKeyboardMarkup(
                    menu_builder([InlineKeyboardButton(x, callback_data=str(i)) for i, x in
                                  zip(cmd['callback_data'], cmd['buttons'])], cmd['buttons_count']))
        else:
            reply_markup = ReplyKeyboardMarkup(
                menu_builder([KeyboardButton(x) for x in cmd['buttons']], cmd['buttons_count']))

        async def callback_funk(upd, ctx):
            self.get_or_create_context(upd.message.from_user.id, upd.message.from_user.username).set_last_command(cmd['name'])
            text = cmd['text'].format(msg=upd.message)
            await ctx.bot.send_message(chat_id=upd.effective_chat.id, text=text, reply_markup=reply_markup)

        return callback_funk

    def get_echo(self):
        async def callback_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message:
                if update.message.text:
                    await update.message.reply_text(f'Я пока не знаю, что на это ответить :(')

        return callback_func


def menu_builder(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i: i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, [header_buttons])

    if footer_buttons:
        menu.append([footer_buttons])

    return menu


if __name__ == '__main__':
    TGBot().run()
