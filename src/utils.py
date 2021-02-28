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
	arr_str=""
	for k in range(len(arr)):
		arr_str = arr_str + "неделя: "+str(k+1)+"-я"+"\n"
		for i in range(len(arr[0])):
			if i>1:
				for x in range(len(arr[0][i])):
					if arr[0][i][x] !="":
						if x==0:
							arr_str = arr_str +  arr[0][i][x] +"\n"
						else:
							arr_str = arr_str +  arr[0][0][x] + arr[0][i][x] + arr[0][1][x]  +"\n"
	return arr_str

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

	#a={'0451-01': 'http://rasp.pskgu.ru/Inst4/1.html', '0202-01': 'http://rasp.pskgu.ru/Inst4/2.html', '0203-01': 'http://rasp.pskgu.ru/Inst4/3.html', '0204-01': 'http://rasp.pskgu.ru/Inst4/4.html', '0205-01': 'http://rasp.pskgu.ru/Inst4/5.html', '0451-02': 'http://rasp.pskgu.ru/Inst4/6.html', '0202-02': 'http://rasp.pskgu.ru/Inst4/7.html', '0203-02': 'http://rasp.pskgu.ru/Inst4/8.html', '0204-03': 'http://rasp.pskgu.ru/Inst4/9.html', '0205-02': 'http://rasp.pskgu.ru/Inst4/10.html', '0451-03': 'http://rasp.pskgu.ru/Inst4/11.html', '0202-04': 'http://rasp.pskgu.ru/Inst4/12.html', '0203-03': 'http://rasp.pskgu.ru/Inst4/13.html', '0204-04': 'http://rasp.pskgu.ru/Inst4/14.html', '0205-03': 'http://rasp.pskgu.ru/Inst4/15.html', '0451-04': 'http://rasp.pskgu.ru/Inst4/16.html', '0202-05': 'http://rasp.pskgu.ru/Inst4/17.html', '0203-04': 'http://rasp.pskgu.ru/Inst4/18.html', '0204-05': 'http://rasp.pskgu.ru/Inst4/19.html', '0205-13': 'http://rasp.pskgu.ru/Inst4/20.html', '0451-06': 'http://rasp.pskgu.ru/Inst4/21.html', '0202-06': 'http://rasp.pskgu.ru/Inst4/22.html', '0203-05': 'http://rasp.pskgu.ru/Inst4/23.html', '0204-11': 'http://rasp.pskgu.ru/Inst4/24.html', '0205-16': 'http://rasp.pskgu.ru/Inst4/25.html', '0451-11': 'http://rasp.pskgu.ru/Inst4/26.html', '0202-11': 'http://rasp.pskgu.ru/Inst4/27.html', '0203-11': 'http://rasp.pskgu.ru/Inst4/28.html', '0204-12': 'http://rasp.pskgu.ru/Inst4/29.html', '0451-12': 'http://rasp.pskgu.ru/Inst4/30.html', '0202-12': 'http://rasp.pskgu.ru/Inst4/31.html', '0203-12(1)': 'http://rasp.pskgu.ru/Inst4/32.html', '0204-13': 'http://rasp.pskgu.ru/Inst4/33.html', '0451-15': 'http://rasp.pskgu.ru/Inst4/34.html', '0202-13': 'http://rasp.pskgu.ru/Inst4/35.html', '0203-12(2)': 'http://rasp.pskgu.ru/Inst4/36.html', '0204-15': 'http://rasp.pskgu.ru/Inst4/37.html', '0451-16': 'http://rasp.pskgu.ru/Inst4/38.html', '0202-14': 'http://rasp.pskgu.ru/Inst4/39.html', '0203-13': 'http://rasp.pskgu.ru/Inst4/40.html', '0204-16': 'http://rasp.pskgu.ru/Inst4/41.html', '0441-02': 'http://rasp.pskgu.ru/Inst4/42.html', '0202-15': 'http://rasp.pskgu.ru/Inst4/43.html', '0203-15': 'http://rasp.pskgu.ru/Inst4/44.html', '0154-01': 'http://rasp.pskgu.ru/Inst4/45.html', '0441-03': 'http://rasp.pskgu.ru/Inst4/46.html', '0202-16': 'http://rasp.pskgu.ru/Inst4/47.html', '0203-16': 'http://rasp.pskgu.ru/Inst4/48.html', '0154-02': 'http://rasp.pskgu.ru/Inst4/49.html', '0441-04': 'http://rasp.pskgu.ru/Inst4/50.html', '0152-01': 'http://rasp.pskgu.ru/Inst4/51.html', '0153-01': 'http://rasp.pskgu.ru/Inst4/52.html', '0154-03': 'http://rasp.pskgu.ru/Inst4/53.html', '0441-01М': 'http://rasp.pskgu.ru/Inst4/54.html', '0152-02': 'http://rasp.pskgu.ru/Inst4/55.html', '0153-02': 'http://rasp.pskgu.ru/Inst4/56.html', '0214-14': 'http://rasp.pskgu.ru/Inst4/57.html', '0451-11М': 'http://rasp.pskgu.ru/Inst4/58.html', '0152-03': 'http://rasp.pskgu.ru/Inst4/59.html', '0153-03': 'http://rasp.pskgu.ru/Inst4/60.html', '0451-12М': 'http://rasp.pskgu.ru/Inst4/61.html', '0152-04': 'http://rasp.pskgu.ru/Inst4/62.html', '0213-14': 'http://rasp.pskgu.ru/Inst4/63.html', '0202-01М': 'http://rasp.pskgu.ru/Inst4/64.html', '0202-02М': 'http://rasp.pskgu.ru/Inst4/65.html', '0202-11М': 'http://rasp.pskgu.ru/Inst4/66.html', '0152-01М': 'http://rasp.pskgu.ru/Inst4/67.html'}
	#a = get_html('http://rasp.pskgu.ru/Inst6/studrasp.html')

	
	#url = 'http://rasp.pskgu.ru/Inst4/studrasp.html'
	#print(a)
	#for z,x in a.items():
	#	h=url_to_array(x)
	#	print(arr_print(h))


	#import psycopg2


	data = grub_all_urls()



	print(data)

	#print( "Расписание преподавателей".lower().find("препод"))
if __name__ == '__main__': 
	test()