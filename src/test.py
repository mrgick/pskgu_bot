import asyncio
from aiohttp import ClientSession
from lxml import html

#для второго массива
from datetime import datetime
import re
import time

# ссылки
#dict_urls = {'0431-01': 'http://rasp.pskgu.ru/Inst6/1.html', '0022-01': 'http://rasp.pskgu.ru/Inst6/2.html', '0023-01': 'http://rasp.pskgu.ru/Inst6/3.html', '0024-01': 'http://rasp.pskgu.ru/Inst6/4.html', '0431-02': 'http://rasp.pskgu.ru/Inst6/5.html', '0022-02': 'http://rasp.pskgu.ru/Inst6/6.html', '0023-02': 'http://rasp.pskgu.ru/Inst6/7.html', '0024-02': 'http://rasp.pskgu.ru/Inst6/8.html', '0431-03': 'http://rasp.pskgu.ru/Inst6/9.html', '0022-03': 'http://rasp.pskgu.ru/Inst6/10.html', '0023-03': 'http://rasp.pskgu.ru/Inst6/11.html', '0024-03': 'http://rasp.pskgu.ru/Inst6/12.html', '0431-04': 'http://rasp.pskgu.ru/Inst6/13.html', '0022-04': 'http://rasp.pskgu.ru/Inst6/14.html', '0023-04': 'http://rasp.pskgu.ru/Inst6/15.html', '0024-04': 'http://rasp.pskgu.ru/Inst6/16.html', '0431-05': 'http://rasp.pskgu.ru/Inst6/17.html', '0022-05': 'http://rasp.pskgu.ru/Inst6/18.html', '0023-05': 'http://rasp.pskgu.ru/Inst6/19.html', '0024-05': 'http://rasp.pskgu.ru/Inst6/20.html', '0431-06': 'http://rasp.pskgu.ru/Inst6/21.html', '0022-06': 'http://rasp.pskgu.ru/Inst6/22.html', '0023-06': 'http://rasp.pskgu.ru/Inst6/23.html', '0024-06': 'http://rasp.pskgu.ru/Inst6/24.html', '0431-07': 'http://rasp.pskgu.ru/Inst6/25.html', '0032-01': 'http://rasp.pskgu.ru/Inst6/26.html', '0033-01': 'http://rasp.pskgu.ru/Inst6/27.html', '0034-01': 'http://rasp.pskgu.ru/Inst6/28.html', '0431-08': 'http://rasp.pskgu.ru/Inst6/29.html', '0032-03': 'http://rasp.pskgu.ru/Inst6/30.html', '0033-02': 'http://rasp.pskgu.ru/Inst6/31.html', '0034-03': 'http://rasp.pskgu.ru/Inst6/32.html', '0431-09': 'http://rasp.pskgu.ru/Inst6/33.html', '0032-04': 'http://rasp.pskgu.ru/Inst6/34.html', '0033-04': 'http://rasp.pskgu.ru/Inst6/35.html', '0034-04': 'http://rasp.pskgu.ru/Inst6/36.html', '0431-11': 'http://rasp.pskgu.ru/Inst6/37.html', '0032-05': 'http://rasp.pskgu.ru/Inst6/38.html', '0033-05': 'http://rasp.pskgu.ru/Inst6/39.html', '0034-05': 'http://rasp.pskgu.ru/Inst6/40.html', '0431-13': 'http://rasp.pskgu.ru/Inst6/41.html', '0032-06': 'http://rasp.pskgu.ru/Inst6/42.html', '0033-08': 'http://rasp.pskgu.ru/Inst6/43.html', '0034-06': 'http://rasp.pskgu.ru/Inst6/44.html', '0431-03М': 'http://rasp.pskgu.ru/Inst6/45.html', '0032-08': 'http://rasp.pskgu.ru/Inst6/46.html', '0034-08': 'http://rasp.pskgu.ru/Inst6/47.html', '0431-08М': 'http://rasp.pskgu.ru/Inst6/48.html', '0032-09': 'http://rasp.pskgu.ru/Inst6/49.html', '0034-09': 'http://rasp.pskgu.ru/Inst6/50.html', '0431-09М': 'http://rasp.pskgu.ru/Inst6/51.html', '0022-09М': 'http://rasp.pskgu.ru/Inst6/52.html', '0431-11М': 'http://rasp.pskgu.ru/Inst6/53.html', '0032-07М': 'http://rasp.pskgu.ru/Inst6/54.html', '2431-03М': 'http://rasp.pskgu.ru/Inst6/55.html', '2032-01М': 'http://rasp.pskgu.ru/Inst6/56.html', '2431-09М': 'http://rasp.pskgu.ru/Inst6/57.html'}
dict_urls = {'0431-01': 'http://rasp.pskgu.ru/Inst6/1.html'}
# Сюда будем складывать результат.
result = {}


async def get_one(url, group_name, session):
	async with session.get(url) as response:
		# Ожидаем ответа и блокируем таск.
		page_content = await response.text()
		# Получаем информацию о таблице
		table = html_tables_to_array(page_content)
		#записываем результат
		result.update({group_name:table})


async def bound_fetch(sm, url, group_name, session):
	try:
		async with sm:
			await get_one(url, group_name, session)
	except Exception as e:
		print(e)


async def run(urls):
	tasks = []
	# Лок
	sm = asyncio.Semaphore(50)
	headers = {"User-Agent": "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"}
	# Опять же оставляем User-Agent, чтобы не получить ошибку
	async with ClientSession(
			headers=headers) as session:
		for key,value in urls.items():
			# Собираем таски и добавляем в лист для дальнейшего ожидания.
			task = asyncio.ensure_future(bound_fetch(sm, value, key, session))
			tasks.append(task)
		# Ожидаем завершения всех наших задач.
		await asyncio.gather(*tasks)



#перобразуем массив во второй раз
def arr_print(arr):
	name_month=['янв','фев','мар','апр','ма','июн','июл','авг','сен','окт','ноя','дек']
	arr_new={}
	arr_str=""
	for k in range(len(arr)):

		#print(arr[k][2][0])
		try:
			name_arr = arr[k][2][0].split(",")[1].split(" ")
			day = int(name_arr[0])
			d=0
			#print(name_arr[2])
			while re.match(r''+name_month[d]+'',name_arr[2]) == None:
				d=d+1
			month = d+1
			t = datetime(2021, month, day)
			name_time=int(time.mktime(t.timetuple()))
			
		except:
			name_time=k


		for i in range(len(arr[k])):
			if i>1:
				for x in range(len(arr[k][i])):
					if arr[k][i][x] !="":
						if x==0:
							arr_str = arr_str+arr[k][i][0] +"\n"
						else:
							arr_str = arr_str +  str(x)+")" + arr[k][i][x] +"\n"
		arr_new.update({name_time:arr_str})
		arr_str=""
	return arr_new

#преобразуем страницу в таблицу
def html_tables_to_array(html_data):

	#нормализуем html комментарии
	html_data=html_data.replace("--!>","-->")

	#собираем огромный первоначальный массив (для откладки есть print)
	root = html.fromstring(html_data)
	data=list()
	for tables in root.xpath('/html/body/table'):
		value1=list()
		for tr in tables.xpath('tr'):
			value2=list()
			for td in tr.xpath('td'):
				value2.append(td.text_content().replace("\r\n",""))
			#print(value2)
			value1.append(value2)
		#print(value1)
		data.append(value1)
	del value1,value2
	#print(data)
	

	data=arr_print(data)
	print(data)

		
	return data


def main():
	#Запускаем наш парсер.
	loop = asyncio.get_event_loop()
	future = asyncio.ensure_future(run(dict_urls))
	loop.run_until_complete(future)
	# Выводим результат. Можете сохранить его куда-нибудь в файл.
	return result
	#print('Over')


if __name__ == "__main__":
	main()
