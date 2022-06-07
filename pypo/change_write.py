import json
from telebot import types
from pypo.data_list import regions_list, vilage_list , citi_list, area_list ,street_list ,home_list
from pypo.text import areaCode_func_text , vilageCode_func_text ,settlementCode_func_text ,citiCode_func_text ,streetCode_func
import pypo.getdata as gd #импорт функция из файла getdata в pypo

item_start =types.InlineKeyboardButton("в начало",callback_data='start_t')



#get_adres
def get_adres_text(call , database_user):
	for i in call.message.json['reply_markup']['inline_keyboard']:
		if len(i[0]["callback_data"].split()) >1:
			if i[0]["callback_data"].split()[1] == call.data.split()[1]:
				database_user[str(call.message.chat.id)]["adres"]  = database_user[str(call.message.chat.id)]["adres"]+" "+i[0]["text"]

				return i[0]["text"]



#генератор кнопок - button_gen
def button_gen(database_user,bot , call , text_msg ,a ,main_bt ,second_bt):
	
	get_adres_text(call,database_user)

				
	markup=types.InlineKeyboardMarkup()

	for i in a:
		item1=types.InlineKeyboardButton(i[0],callback_data=(main_bt+"Code " + i[1]))
		markup.add(item1)

	item1=types.InlineKeyboardButton("назад",callback_data=main_bt+' -')
	item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)][second_bt+"_numb"])\
		+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
	item2=types.InlineKeyboardButton("далее",callback_data=main_bt+' +')
	markup.add(item1,item3,item2)
	markup.add(item_start)
	bot.delete_message(str(call.message.chat.id), call.message.id)
	bot.send_message(str(call.message.chat.id),text_msg,reply_markup=markup)



def button_gen_long(database_user,bot , call , text_msg ,a ,main_bt ,second_bt):
	
	get_adres_text(call,database_user)

				
	markup=types.InlineKeyboardMarkup()

	for i in a:
		item1=types.InlineKeyboardButton(i[0],callback_data=("data " + i[1]))
		markup.add(item1)
	# if len(aa) <7:
	# 	markup.add(aa)


	item1=types.InlineKeyboardButton("назад",callback_data=main_bt+' -')
	item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)][second_bt+"_numb"])\
		+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
	item2=types.InlineKeyboardButton("далее",callback_data=main_bt+' +')
	markup.add(item1,item3,item2)
	markup.add(item_start)
	bot.delete_message(str(call.message.chat.id), call.message.id)
	bot.send_message(str(call.message.chat.id),text_msg,reply_markup=markup)
def button_gen_long_v(database_user,bot , call , text_msg ,a ,main_bt ,second_bt):
	
	get_adres_text(call,database_user)

				
	markup=types.InlineKeyboardMarkup()

	for i in a:
		item1=types.InlineKeyboardButton(i[0],callback_data=("data_vilage_text " + i[1]))
		markup.add(item1)
	# if len(aa) <7:
	# 	markup.add(aa)


	item1=types.InlineKeyboardButton("назад",callback_data=main_bt+' -')
	item3=types.InlineKeyboardButton("["+str(database_user[str(call.message.chat.id)][second_bt+"_numb"])\
		+"/"+str(int((len(database_user[str(call.message.chat.id)]["cashe"])/7)))+"]",callback_data='chet')
	item2=types.InlineKeyboardButton("далее",callback_data=main_bt+' +')
	markup.add(item1,item3,item2)
	markup.add(item_start)
	bot.delete_message(str(call.message.chat.id), call.message.id)
	bot.send_message(str(call.message.chat.id),text_msg,reply_markup=markup)

#-------------------------

def areaCode_func(bot, call ,database_user):
	database_user[str(call.message.chat.id)]["vilage_numb"] = 0
	database_user[str(call.message.chat.id)]["area"]  = call.data.split()[1]
	database_user[str(call.message.chat.id)]["cashe"] =  gd.get_vilage(\
		database_user[str(call.message.chat.id)]["regions"],\
		database_user[str(call.message.chat.id)]["area"]
		)
	a=vilage_list(database_user[str(call.message.chat.id)]["cashe"],0)
	button_gen(database_user,bot , call , areaCode_func_text ,a , "vilage" , "area")

def vilageCode_func(bot, call,database_user):
	database_user[str(call.message.chat.id)]["settlement_numb"] = 0
	database_user[str(call.message.chat.id)]["settlementCode"]  = call.data.split()[1]
	database_user[str(call.message.chat.id)]["cashe"] =  gd.get_vilage_streat(\
		database_user[str(call.message.chat.id)]["regions"],\
		database_user[str(call.message.chat.id)]["area"],
		database_user[str(call.message.chat.id)]["settlementCode"]

		)
	a=vilage_list(database_user[str(call.message.chat.id)]["cashe"],0)
	button_gen(database_user,bot , call , vilageCode_func_text ,a , "settlement" , "area")

def settlementCode_func(bot, call,database_user):
	database_user[str(call.message.chat.id)]["streetCode_numb"] = 0
	database_user[str(call.message.chat.id)]["streetCode"]  = call.data.split()[1]
	database_user[str(call.message.chat.id)]["cashe"] =  gd.get_vilage_streat_home(\
		database_user[str(call.message.chat.id)]["regions"],\
		database_user[str(call.message.chat.id)]["area"],
		database_user[str(call.message.chat.id)]["settlementCode"],
		database_user[str(call.message.chat.id)]["streetCode"]


		)
	print("--------------------------------------------")
	a=home_list(database_user[str(call.message.chat.id)]["cashe"],0)
	#button_gen(database_user,bot , call , settlementCode_func_text ,a , "settlement_v" , "streetCode")
	button_gen_long_v(database_user,bot , call , streetCode_func ,a , "settlement_v" , "streetCode")


def citiCode_func(bot, call,database_user):
	database_user[str(call.message.chat.id)]["street_numb"] = 0


	database_user[str(call.message.chat.id)]["citi"]  = call.data.split()[1]
	database_user[str(call.message.chat.id)]["cashe"] =  gd.get_streat(\
		database_user[str(call.message.chat.id)]["regions"],\
		database_user[str(call.message.chat.id)]["citi"]
		)

	a=street_list(database_user[str(call.message.chat.id)]["cashe"],0)
	button_gen(database_user,bot , call , citiCode_func_text ,a , "street" , "street")
	
def streetCode_func(bot, call,database_user):
	database_user[str(call.message.chat.id)]["home_numb"] = 0
	database_user[str(call.message.chat.id)]["street"]  = call.data.split()[1]
	database_user[str(call.message.chat.id)]["cashe"] =  gd.get_home(\
		database_user[str(call.message.chat.id)]["regions"],\
		database_user[str(call.message.chat.id)]["citi"],\
		database_user[str(call.message.chat.id)]["street"],\
		)

	a=home_list(database_user[str(call.message.chat.id)]["cashe"],0)
	print(a)
	#button_gen(database_user,bot , call , citiCode_func_text ,a , "street" , "data")
	button_gen_long(database_user,bot , call , streetCode_func ,a , "home" , "home")
