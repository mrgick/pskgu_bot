from bs4 import BeautifulSoup
import requests

#get array data using beatifulsoap
def html_tables_to_array(html_data):
	soup = BeautifulSoup (html_data, 'html.parser')
	data = list()
	for table in soup.find_all('table'):
		value1 = list()
		for tr in table.find_all('tr'):
			value2 = list()
			for td in tr.find_all('td'):
				txt = td.text.replace("\n","")
				if txt == "  _  " or txt==" " or txt=="_":
					txt = ""
				value2.append(txt)
			value1.append(value2)
		data.append(value1)
	return data

#get html data using requests
def get_html(url):
	r = requests.get(url)
	
	# need for correct text response, often there is windows-1251
	if len(r.text.split("charset="))!=1:
		r.encoding = r.text.split("charset=")[1].split('"')[0]
	else:
		r.encoding="windows-1251"
	return r.text

#get urls using beatifulsoap
def get_urls_from_html(html_data,url):

	#clear url (delete for example studrasp.html from url)
	url = url[0:url.rindex("/")]+"/"


	soup = BeautifulSoup (html_data, 'html.parser')
	urls = dict() 
	for link in soup.find_all('a'):
	    urls.update({link.text:url+link.get('href').replace("\\","/")})
	return urls

# parse url and return array
def url_to_array(url):
	html_data = get_html(url)
	return html_tables_to_array(html_data)

def get_urls_from_url(url):
	html_data = get_html(url)
	return get_urls_from_html(html_data,url)

def arr_print(arr):
	arr_new=[]
	arr_str=""
	for k in range(len(arr)):
		for i in range(len(arr[k])):
			if i>1:
				for x in range(len(arr[k][i])):
					if arr[k][i][x] !="":
						if x==0:
							arr_str = arr_str+arr[k][i][0] +"\n"
						else:
							arr_str = arr_str +  str(x)+")" + arr[k][i][x] +"\n"
		arr_new.append(arr_str)
		arr_str=""
	return arr_new

def grub_all_urls():
	url_rasp = "http://rasp.pskgu.ru/"
	data = get_urls_from_url(url_rasp)
	for key, value in data.items():
		data[key]=get_urls_from_url(value)

		if key.lower().find("препод")==-1:
			for key2, value2 in data[key].items():
				data[key][key2]=get_urls_from_url(value2)
	return data


# for testing
def test():

	url = 'http://rasp.pskgu.ru/Inst6/21.html'
	arr = url_to_array(url)
	a = arr_print(arr)
	print(a[0])

	#print(a)



	#import psycopg2

	#print(1)
	#print(1)
	"""
	data = grub_all_urls()
	#print(data)
	k=0
	for key, value in data['Расписание преподавателей'].items():
		#print(key)
		k=k+1
	#print(k)
"""
	#print( "Расписание преподавателей".lower().find("препод"))
if __name__ == '__main__': 
	test()