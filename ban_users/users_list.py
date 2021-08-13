from selenium import webdriver as wb
import time
import json

path_to_driver = "/home/g1fl3x/Рабочий стол/chromedriver"

browser = wb.Chrome(path_to_driver)
source = ""
arr = []

page = 1
while "Ничего не найдено" not in source:
	browser.get(f"https://lolzteam.online/online/?type=registered&page={page}")
	time.sleep(1)
	source = browser.page_source
	while "username StatusTooltip" in source:
		link = source[source.find("username StatusTooltip"):]
		link = link[:link.find("</span>")]
		link = link[link.rfind(">")+1:]
		arr.append(link)
		source = source[source.find("username StatusTooltip")+10:]
	page += 1

f = open("ban_list.txt", "r")
old_list = json.loads(f.read())
f.close()


f = open("ban_list.txt", "w")
f.write(json.dumps(list(set(old_list + arr))))
f.close()
