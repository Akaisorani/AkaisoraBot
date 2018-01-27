from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import logging,os
import scraper_manga

def start(bot, update):
	update.message.reply_text('Hello! I\'m AkaisoraBot.')
	return 1
	
def hello(bot, update):
	update.message.reply_text(
		'Hello {}'.format(update.message.from_user.first_name))

def echo(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot,update,args):
	test_caps=' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=test_caps)

def pixiv(bot,update,args,user_data):
	user_data["classi"]=""
	user_data["tag"]=""
	user_data["type"]="photo"
	if ">file" in args: user_data["type"]="file";args.remove(">file")
	if ">photo" in args: args.remove(">photo")
	
	if len(args)==0 or (args[0].lower() not in {"normalrank","tag","r18rank","id"}):
		update.message.reply_text("Require classification",reply_markup=ReplyKeyboardMarkup([["normalrank","tag","id"]], one_time_keyboard=True))
		return 0
	user_data["classi"]=args[0]
	
	if args[0].lower() in {"tag","id"}:
		if len(args)==1:
			update.message.reply_text("Require "+args[0].lower())
			return 1
		else: 
			if args[0].lower()=="tag": user_data["tag"]=" ".join(args[1:])
			elif args[0].lower()=="id": user_data["tag"]=args[1]
	
	pixiv_send_picture(bot,update,user_data)
	
	return ConversationHandler.END

def pixiv_get_classi(bot,update,user_data):
	user_data["classi"]=update.message.text
	if user_data["classi"] in {"tag","id"}:
		update.message.reply_text("Require "+user_data["classi"],reply_markup=ReplyKeyboardRemove())
		return 1
	else:
		pixiv_send_picture(bot,update,user_data)
		
	return ConversationHandler.END
	
def pixiv_get_tag(bot,update,user_data):
	user_data["tag"]=update.message.text
	pixiv_send_picture(bot,update,user_data)
	
	return ConversationHandler.END
	
def pixiv_send_picture(bot,update,user_data):
	if user_data["classi"]=="id":filename=scraper_manga.get_one_by_id(user_data["tag"])
	else: filename=scraper_manga.random_one_by_classfi(user_data["classi"],user_data["tag"])
	if filename:
		update.message.reply_text("illust_id = "+os.path.splitext(os.path.basename(filename))[0].split('_')[0],reply_markup=ReplyKeyboardRemove())
		with open(filename,"rb") as f:
			if user_data["type"]=="file": update.message.reply_document(f)
			else: update.message.reply_photo(f)
	else:
		update.message.reply_text("Fetch error",reply_markup=ReplyKeyboardRemove())
	user_data.clear()

def cancel(bot, update):
	user = update.message.from_user
	logger.info("User %s canceled the conversation." % user.first_name)
	update.message.reply_text('Canceled',reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END	
	
def cancel_nothing(bot, update):
	user = update.message.from_user
	logger.info("User %s canceled the conversation." % user.first_name)
	update.message.reply_text('No active command to cancel.',reply_markup=ReplyKeyboardRemove())
	

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Unknown Command.")


updater = Updater(open("token.txt","r").read())
dp=updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger=logging.getLogger(__name__)

pixiv_conv_handler=ConversationHandler(
	entry_points=[CommandHandler('pixiv',pixiv,pass_args=True,pass_user_data=True)],
	states={
		0:[RegexHandler('^(normalrank|r18rank|tag|id)$',pixiv_get_classi,pass_user_data=True)],
		1:[MessageHandler(Filters.text,pixiv_get_tag,pass_user_data=True)]
	},
	fallbacks=[CommandHandler('cancel',cancel)]
)

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('hello', hello))

# dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_handler(CommandHandler('caps', caps,pass_args=True))
dp.add_handler(pixiv_conv_handler)

dp.add_handler(CommandHandler('cancel', cancel_nothing))
dp.add_error_handler(error)
# dp.add_handler(MessageHandler(Filters.command, unknown))


updater.start_polling()
updater.idle()