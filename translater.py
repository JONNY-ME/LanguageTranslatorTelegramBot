'''
		Installation 
			- pip install python-telegram-bot
			- pip install translate

'''


import logging 
import time 
from telegram import *
from telegram import utils 
from telegram.ext import *  
import sqlite3 as sl 
from translate import Translator

languages = {'Afar': 'aa', 'Abkhazian': 'ab', 'Afrikaans': 'af', 'Amharic': 'am', 'Arabic': 'ar', 'Assamese': 'as', 'Aymara': 'ay',
	 		'Azeri': 'az', 'Bashkir': 'ba', 'Belarusian': 'be', 'Bulgarian': 'bg', 'Bihari': 'bh', 'Bislama': 'bi', 'Bengali': 'bn', 
	 		'Tibetan': 'bo', 'Breton': 'br', 'Catalan': 'ca', 'Corsican': 'co', 'Czech': 'cs', 'Welsh': 'cy', 'Danish': 'da', 
	 		'German': 'de', 'Divehi': 'div', 'Bhutani': 'dz', 'Greek': 'el', 'English': 'en', 'Esperanto': 'eo', 'Spanish': 'es', 
	 		'Estonian': 'et', 'Basque': 'eu', 'Farsi': 'fa', 'Finnish': 'fi', 'Fiji': 'fj', 'Faeroese': 'fo', 'French': 'fr', 
	 		'Frisian': 'fy', 'Irish': 'ga', 'Gaelic': 'gd', 'Galician': 'gl', 'Guarani': 'gn', 'Gujarati': 'gu', 'Hausa': 'ha', 
	 		'Hebrew': 'iw', 'Hindi': 'hi', 'Croatian': 'hr', 'Hungarian': 'hu', 'Armenian': 'hy', 'Interlingua': 'ia', 'Indonesian': 'in', 
	 		'Interlingue': 'ie', 'Inupiak': 'ik', 'Icelandic': 'is', 'Italian': 'it', 'Japanese': 'ja', 'Yiddish': 'yi', 'Javanese': 'jw', 
	 		'Georgian': 'ka', 'Kazakh': 'kk', 'Greenlandic': 'kl', 'Cambodian': 'km', 'Kannada': 'kn', 'Korean': 'ko', 'Konkani': 'kok', 
	 		'Kashmiri': 'ks', 'Kurdish': 'ku', 'Kirghiz': 'ky', 'Kyrgyz': 'kz', 'Latin': 'la', 'Lingala': 'ln', 'Laothian': 'lo', 
	 		'Slovenian': 'sl', 'Lithuanian': 'lt', 'Latvian': 'lv', 'Malagasy': 'mg', 'Maori': 'mi', 'FYRO Macedonian': 'mk', 'Malayalam': 'ml',
	 		'Mongolian': 'mn', 'Moldavian': 'mo', 'Marathi': 'mr', 'Malay': 'ms', 'Maltese': 'mt', 'Burmese': 'my', 'Nauru': 'na', 'Nepali': 'ne',
	 		'Dutch': 'nl', 'Norwegian': 'no', 'Occitan': 'oc', 'Afan-Oromo': 'om', 'Oriya': 'or', 'Punjabi': 'pa', 'Polish': 'pl', 
	 		'Pashto/Pushto': 'ps', 'Portuguese': 'pt', 'Quechua': 'qu', 'Rhaeto-Romanic': 'rm', 'Kirundi': 'rn', 'Romanian': 'ro', 
	 		'Russian': 'ru', 'Kinyarwanda': 'rw', 'Sanskrit': 'sa', 'Sorbian': 'sb', 'Sindhi': 'sd', 'Sangro': 'sg', 'Serbo-Croatian': 'sh',
	 		'Singhalese': 'si', 'Slovak': 'sk', 'Samoan': 'sm', 'Shona': 'sn', 'Somali': 'so', 'Albanian': 'sq', 'Serbian': 'sr', 
	 		'Siswati': 'ss', 'Sesotho': 'st', 'Sundanese': 'su', 'Swedish': 'sv', 'Swahili': 'sw', 'Sutu': 'sx', 'Syriac': 'syr', 
	 		'Tamil': 'ta', 'Telugu': 'te', 'Tajik': 'tg', 'Thai': 'th', 'Tigrinya': 'ti', 'Turkmen': 'tk', 'Tagalog': 'tl', 'Tswana': 'tn',
	 		'Tonga': 'to', 'Turkish': 'tr', 'Tsonga': 'ts', 'Tatar': 'tt', 'Twi': 'tw', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz',
	 		'Vietnamese': 'vi', 'Volapuk': 'vo', 'Wolof': 'wo', 'Xhosa': 'xh', 'Yoruba': 'yo', 'Chinese': 'zh', 'Zulu': 'zu'
	 }
codes_to_lang = {j:i for i, j in languages.items()}
from math import ceil
lang = sorted(languages.keys())
keyboards = []
P = 11   # language displayed in a single page
sz = 3*(P-1)
ln = ceil(len(languages)/sz)
for i in range(ln):
    keyboards.append(lang[i*sz:(i+1)*sz])





Admin_id = None # your telegram id
con = sl.connect('bot_users.db', check_same_thread=False)
try:
    con.execute("""
            CREATE TABLE USER (
                id TEXT NOT NULL PRIMARY KEY,
                name TEXT,
                role TEXT, 
                lang TEXT,
                deleted TEXT

            );
        """)
except:
    pass
sql = 'INSERT INTO USER (id, name, role, lang, deleted) values(?, ?, ?, ?, ?)'



'''

		helper functions for the Database Managment

'''

def load_default(user_id, context):
	com = 'SELECT lang FROM USER WHERE id="'+str(user_id)+'"'
	cur = con.cursor()
	data = cur.execute(com)
	lang = None
	for i in data:
		lang = i[0]
	context.user_data['lang'] = lang


def get_users():
	com = 'SELECT COUNT(*) FROM USER WHERE deleted="NO"'
	cur = con.cursor()
	data = cur.execute(com)
	num1 = None
	for i in data:
		num1 = i[0]
	com = 'SELECT COUNT(*) FROM USER WHERE deleted="YES"'
	cur = con.cursor()
	data = cur.execute(com)
	num2 = None
	for i in data:
		num2 = i[0]
	return num1, num2


def change_default(user_id, language):
	com = 'UPDATE USER SET lang="'+language+'" WHERE id="'+str(user_id)+'"'
	cur = con.cursor()
	data = cur.execute(com)





''' 

		Bot Functions   

'''

def start(update, context):
	data = (str(update.message.chat_id), update.message.from_user['first_name'], 'user', 'English', 'NO')
	try:
		cur = con.cursor()
		cur.execute(sql, data)
		con.commit()
		name = utils.helpers.mention_html(update.message.chat_id, update.message.from_user['first_name'])
		context.bot.send_message(chat_id=Admin_id, 
		 	text=f"new user:-\n{name} started the bot",
		 	parse_mode=ParseMode.HTML)
		context.user_data['lang'] = 'English'
	except Exception as e:
		com = 'UPDATE USER SET deleted="NO" WHERE id="'+str(update.message.chat_id)+'"'
		cur = con.cursor()
		cur.execute(com)
		if 'lang' in context.user_data:
			load_default(update.message.chat_id, context)
	finally:
		update.message.reply_text(
			"welcome! by using this bot you can translate from any language to any language\n use /change_default to change your default language")


def no_of_users(update, context):
	user_id = update.message.from_user['id']
	if user_id == Admin_id:
		active, deleted = get_users()
		update.message.reply_text(f"the number of users is {active+deleted}\nactive = {active}\ndeleted = {deleted}")


def help(update, context):
	user_id = update.message.from_user['id']
	if user_id == Admin_id:
		update.message.reply_text(
			"list of commands\n/start to restart the bot\n/set_default to change default language\n/users to get number of users\n/message send message to users"
			) 
	else:
		update.message.reply_text(
			"list of commands\n/start to restart the bot\n/set_default to change default language"
			)


def change_lang(update, context):
	pos = 0 
	context.user_data['pos'] = pos 
	keyboard = []
	keys = keyboards[pos]
	for i in range(len(keys)//3):
		keyboard_adds = []
		for j in range(3):
			try:
				keyboard_adds.append(InlineKeyboardButton(f"{keys[3*i+j]}", callback_data=f'{keys[3*i+j]}'))
			except:
				break
		keyboard.append(keyboard_adds)
	keyboard.append([InlineKeyboardButton("➡️", callback_data='-->')])
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('choose your default language', reply_markup=reply_markup)



def button(update, context):
	if 'pos' in context.user_data:
	    query = update.callback_query
	    query.answer()
	    inp = query.data
	    if inp == '-->' or inp == '<--':
	    	pos = context.user_data['pos'] + 1
	    	if inp == '<--':
	    		pos -= 2
	    	context.user_data['pos'] = pos 
	    	keyboard = []
	    	keys = keyboards[pos]
	    	for i in range(len(keys)//3):
	    		keyboard_adds = []
	    		for j in range(3):
	    			try:
	    				keyboard_adds.append(InlineKeyboardButton(f"{keys[3*i+j]}", callback_data=f'{keys[3*i+j]}'))
	    			except:
	    				break
	    		keyboard.append(keyboard_adds)
	    	if pos == 0:
	    		keyboard.append([InlineKeyboardButton("➡️", callback_data='-->')])
	    	elif pos == ln-1:
	    		keyboard.append([InlineKeyboardButton("⬅️", callback_data='<--')])
	    	else:
	    		keyboard.append([
	    			InlineKeyboardButton("⬅️", callback_data='<--'),
	    			InlineKeyboardButton("➡️", callback_data='-->')
	    			])
	    	reply_markup = InlineKeyboardMarkup(keyboard)
	    	query.message.edit_reply_markup(reply_markup)
	    else:
	    	query.delete_message()
	    	user_id = query.message.chat_id
	    	prev_lang = context.user_data.get('lang', load_default(user_id, context))
	    	change_default(user_id, inp)
	    	query.message.reply_text(f'succesfully changed your default language form {prev_lang} to {inp}')
	    	del context.user_data['pos']
	    	context.user_data['lang'] = inp

	    	



def func(update, context):
	text = update.message.text
	if 'done' in context.user_data and update.message.chat_id == Admin_id:
		if text == 'cancel':
			update.message.reply_text("canceled", reply_markup=ReplyKeyboardRemove())
			del context.user_data['done']
			del context.user_data['message']
		else:
			com = 'SELECT * FROM USER'
			cur = con.cursor()
			data = cur.execute(com)
			mess = context.user_data['message']
			for id, name, _, delt in data:
				out = f"Hello {utils.helpers.mention_html(id, name)}\n"+mess
				if delt == "NO":
					try:
						context.bot.send_message(chat_id=int(id), text=out, parse_mode=ParseMode.HTML)
					except:
						com = 'UPDATE USER SET deleted="YES" WHERE id="'+id+'"'
						cur = con.cursor()
						cur.execute(com)
			del context.user_data['message']
			del context.user_data['done']
			update.message.reply_text("succesfully sent to all users", reply_markup=ReplyKeyboardRemove())
	elif 'message' in context.user_data and update.message.chat_id == Admin_id:
		if text == 'cancel':
			update.message.reply_text("canceled", reply_markup=ReplyKeyboardRemove())
			del context.user_data['message']
		else:
			update.message.reply_text("the message will be sent to all users if you enter done else enter cancel", 
				reply_markup=ReplyKeyboardMarkup([["done", 'cancel']], one_time_keyboard=True, resize_keyboard=True)
				)
			context.user_data['message'] = text
			context.user_data['done'] = 1
	else:	
		to_lang = languages[context.user_data.get('lang', load_default(update.message.chat_id, context))]
		translator= Translator(to_lang=to_lang)
		# print(translator.available_providers)
		stt = time.time()
		try:
			translation = translator.translate(text)
			out_text = translation + f'\nfrom {codes_to_lang[translator.from_lang]} To {codes_to_lang[translator.to_lang]}'+'\nby @jonny_bots'
			update.message.reply_text(out_text)
		except:
			update.message.reply_text("sorry couldn't translate!")




def message(update, context):
	user_id = update.message.from_user['id']
	if user_id == Admin_id:
		update.message.reply_text(
			"send me the text that you want to send to the users or send cancel", 
			reply_markup=ReplyKeyboardMarkup([["cancel"]], one_time_keyboard=True, resize_keyboard=True))
		context.user_data['message'] = 1





def main():
	updater = Updater("YOUR-API")
	dispatcher = updater.dispatcher 

	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('change_default', change_lang))
	dispatcher.add_handler(CommandHandler("help", help))
	dispatcher.add_handler(CommandHandler("users", no_of_users))
	dispatcher.add_handler(CommandHandler("message", message))
	dispatcher.add_handler(MessageHandler(Filters.text, func))
	dispatcher.add_handler(CallbackQueryHandler(button))

	updater.start_polling()
	updater.idle()



if __name__ == '__main__':
	main()
