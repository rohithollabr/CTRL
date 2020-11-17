from functools import wraps

from telegram import User, Chat, ChatMember, Update, Bot
from telegram import error, ChatAction

from tg_bot import DEL_CMDS, SUDO_USERS, dispatcher


def send_message(message, text,  *args,**kwargs):
	try:
		return message.reply_text(text, *args,**kwargs)
	except error.BadRequest as err:
		if str(err) == "Reply message not found":
			return message.reply_text(text, quote=False, *args,**kwargs)


def typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(bot, Update, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )
        return func(bot, Update, *args, **kwargs)

    return command_func


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(bot, update, *args, **kwargs):
            bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
            return func(bot, update,  *args, **kwargs)
        return command_func

    return decorator


def connection_status(func):

    @wraps(func)
    def connected_status(bot, update: Update, *args,
                         **kwargs):
        conn = connected(
            bot,
            update,
            update.effective_chat,
            update.effective_user.id,
            need_admin=False)

        if conn:
            chat = dispatcher.bot.getChat(conn)
            update.__setattr__("_effective_chat", chat)
            return func(update, *args, **kwargs)
        else:
            if update.effective_message.chat.type == "private":
                update.effective_message.reply_text(
                    "Send /connect in a group that you and I have in common first."
                )
                return connected_status

            return func(update, *args, **kwargs)

    return connected_status


# Workaround for circular import with connection.py
from tg_bot.modules import connection

connected = connection.connected
