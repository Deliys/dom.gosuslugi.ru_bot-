import requests
import json

#ссыль куда мы гидаем запросы
start_url = 'https://dom.gosuslugi.ru/nsi/api/rest/services/nsi/fias/v4'



""" функции ниже отправляют get запросы с помощью того что подставляют коды 
в изначальную ссылку . С каждым выбором мы добавляем новые данные в ссылку и 
сохроняем пребедущие
"""

def get_citis(regionCode):
	url = start_url+'/cities?actual=true&itemsPerPage=100&page=1&regionCode='+regionCode+'&searchString='

	s = requests.Session()
	loging = s.get(url)


	return json.loads(loging.text)

def get_area(regionCode):
	url = start_url+'/areas?actual=true&itemsPerPage=100&page=1&regionCode='+regionCode+'&searchString='

	s = requests.Session()
	loging = s.get(url)
	return json.loads(loging.text)

def get_vilage(regionCode,areaCode):
	url = start_url+'/settlements?actual=true&areaCode='+areaCode+'&itemsPerPage=100&page=1&regionCode='+regionCode+'&searchString='

	s = requests.Session()
	loging = s.get(url)


	return json.loads(loging.text)


def get_vilage_streat(regionCode,areaCode,settlementCode):
	print(regionCode)
	print(areaCode)
	print(settlementCode)
	url = start_url+'/streets?actual=true&areaCode='+areaCode+'&itemsPerPage=100&page=1&regionCode='+regionCode+'&searchString=&settlementCode='+settlementCode

	s = requests.Session()
	loging = s.get(url)


	return json.loads(loging.text)


def get_vilage_streat_home(regionCode,areaCode,settlementCode,streetCode):
	print(regionCode)
	print(areaCode)
	print(settlementCode)
	url = start_url+'/numbers?actual=true&areaCode='+areaCode+'&itemsPerPage=100&page=1&regionCode='+regionCode+'&searchString=&settlementCode='+settlementCode+"&streetCode="+streetCode

	s = requests.Session()
	loging = s.get(url)


	return json.loads(loging.text)

#https://dom.gosuslugi.ru/nsi/api/rest/services/nsi/fias/v4/settlements?actual=true&areaCode=71bdc088-53f4-40a7-92dc-004499965dfa&itemsPerPage=10&page=1&regionCode=db9c4f8b-b706-40e2-b2b4-d31b98dcd3d1&searchString=


def get_streat(regionCode,cityCode):
	url = start_url+'/streets?actual=true&cityCode='+cityCode+'&itemsPerPage=10000&page=1&regionCode='+regionCode+'&searchString='

	s = requests.Session()
	loging = s.get(url)

	return json.loads(loging.text)


def get_home(regionCode,cityCode,streetCode):
	url = start_url+'/numbers?actual=true&cityCode='+cityCode+'&itemsPerPage=100000&page=1&regionCode='+regionCode+'&searchAggregatedAddresses=true&searchString=&streetCode='+ streetCode

	s = requests.Session()
	loging = s.get(url)

	return json.loads(loging.text)


"""
ниже функции отправляют пост запросы на сйт и данные в формате json в которые подставляются значения 
ранее полученые  дынные из прошлых запросов 
"""

def get_compuni(regionCode,cityCode,streetCode,homeCode):
	url = 'https://dom.gosuslugi.ru/ppa/api/rest/services/ppa/public/organizations/searchByTerritory?pageIndex=1&elementsPerPage=10'

	s = requests.Session()

	with open('file/5.json', 'r',encoding='utf-8') as fp:
		datas = json.load(fp)

	datas["regionCode"]=regionCode
	datas["cityCode"]=cityCode
	datas["streetCode"]=streetCode
	datas["houseCode"]=homeCode
	
	loging = s.post(url,json=datas)

	if json.loads(loging.text)["organizationSummaryWithNsiList"] == 0:
		return "нет компаний"
	else:
		text = 'спискок организаций:'
		g = 0
		for i in json.loads(loging.text)["organizationSummaryWithNsiList"]:
			g = g +1
			text = text + "\n["+str(g)+"]" +i["shortName"]+"\n" 
			if i["phone"] != None:
				text = text +"\n" + str(i["phone"])+"\n"
			
			if i["url"] != None:
				text = text +"\n" + str(i["url"])+"\n"
			else:
				text = text + "\n"
		return text


def get_compuni_vilage(regionCode,areaCode,settlementCode,streetCode ,houseCode):
	url = 'https://dom.gosuslugi.ru/ppa/api/rest/services/ppa/public/organizations/searchByTerritory?pageIndex=1&elementsPerPage=10'

	s = requests.Session()

	with open('file/6.json', 'r',encoding='utf-8') as fp:
		datas = json.load(fp)

	datas["regionCode"]=regionCode
	datas["areaCode"]=areaCode
	datas["settlementCode"]=settlementCode
	datas["streetCode"]=streetCode
	datas["houseCode"]=houseCode

	
	loging = s.post(url,json=datas)

	if json.loads(loging.text)["organizationSummaryWithNsiList"] == 0:
		return "нет компаний"
	else:
		text = 'спискок организаций:'
		g = 0
		for i in json.loads(loging.text)["organizationSummaryWithNsiList"]:
			g = g +1
			text = text + "\n["+str(g)+"]" +i["shortName"]+"\n"
			if i["phone"] != None:
				text = text +"\n" + str(i["phone"])+"\n"
			
			if i["url"] != None:
				text = text +"\n" + str(i["url"])+"\n"
			else:
				text = text + "\n"


		return text

