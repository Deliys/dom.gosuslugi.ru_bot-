import requests
import json

#ссыль куда мы гидаем запросы
start_url = 'https://dom.gosuslugi.ru/nsi/api/rest/services/nsi/fias/v4'

def get_citis(regionCode):
	url = start_url+'/cities?actual=true&itemsPerPage=100&page=1&regionCode='+regionCode+'&searchString='

	s = requests.Session()
	loging = s.get(url)


	return json.loads(loging.text)
	# with open("1.json", "w",encoding='utf-8') as file:
	# 	json.dump(json.loads(loging.text), file, indent=4, ensure_ascii=False)


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
def get_compuni(regionCode,cityCode,streetCode,homeCode):
	url = 'https://dom.gosuslugi.ru/ppa/api/rest/services/ppa/public/organizations/searchByTerritory?pageIndex=1&elementsPerPage=10'

	s = requests.Session()

	with open('5.json', 'r',encoding='utf-8') as fp:
		datas = json.load(fp)

	datas["regionCode"]=regionCode
	datas["cityCode"]=cityCode
	datas["streetCode"]=streetCode
	datas["houseCode"]=homeCode
	
	loging = s.post(url,json=datas)

	

	with open("4.json", "w",encoding='utf-8') as file:
		json.dump(json.loads(loging.text), file, indent=4, ensure_ascii=False)


	if json.loads(loging.text)["organizationSummaryWithNsiList"] == 0:
		return "нет компаний"
	else:

		print(len(json.loads(loging.text)["organizationSummaryWithNsiList"]))

		text = 'спискок организаций:'
		g = 0
		for i in json.loads(loging.text)["organizationSummaryWithNsiList"]:
			g = g +1
			text = text + "\n["+str(g)+"]" +i["shortName"]+"\n\n"
		return text

	return


