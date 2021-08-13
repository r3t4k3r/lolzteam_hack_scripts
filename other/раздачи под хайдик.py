from requests import session, get
from threading import Thread
import json

token = "ed80d1bbe217fecf1e44952718a9a0e98b312fab" # g1fl3x
thread_id = "1533196"
count = 5 # по сколько раздаем
r = 1 # каждому?
number = 0 # начиная с

f = open("users.txt", "r")
accounts = []
for line in f:
	accounts.append(line[:-1])
f.close()
print(len(accounts))


sendings_arr = []
names = []

def send_msg():
	global names, thread_id, token, number, accounts, count
	s = session()
	data = {
        "oauth_token":token,
        "post_body":""
	}
	s.post("https://lolzteam.online/api/index.php?threads")
	while True:
		if names != []:
			name = names[0]
			if name != "g1fl3x":
				try:
					ss = ""
					for i in range(count):
						ss += accounts[number+i]+"\n"
					text = "Акки:\n"+ss+":2011_like:"
				except:
					print("Раздача окончена")
					break
				data = {
                    "oauth_token":token,
                    "post_body":"[USERS="+name+"] "+text+" [/USERS]",
                    "thread_id":thread_id
				}
				response = s.post("https://lolzteam.online/api/index.php?posts",data = data).text
				if "errors" not in response:
					print(name+" съела хуила")
					number += count
					del names[0]
			else:
				del names[0]

def get_posts(thread_id):
	try:
		response = get(f"https://lolzteam.online/api/index.php?posts&thread_id={thread_id}&page=0").json()
		try:
			pages = int(response["links"]["pages"])
		except:
			pages = 1
		data = []
		for i in range(1,pages+1):
			data.append({"id":str(i),"uri":f"index.php?posts&thread_id={thread_id}&page={str(i)}","method":"GET"})
		s = session()
		posts_arr = []
		response = json.loads(s.post("https://lolzteam.online/api/index.php?batch", data=json.dumps(data)).text)

		for job in range(1, len(response["jobs"])+1):
			if response["jobs"][str(job)]["_job_result"] == "ok":
				for post in response["jobs"][str(job)]["posts"]:
					posts_arr.append([post["post_id"],post["poster_username"]])

		return posts_arr
	except:pass

def main():
	global thread_id, r, names
	while True:
		try:
			posts_arr = get_posts(thread_id)
			for i in range(len(posts_arr)):
				post_id = posts_arr[i][0]
				name = posts_arr[i][1]
				if (i+1)%r == 0 and post_id not in sendings_arr:
					sendings_arr.append(post_id)
					names.append(name)
		except:pass

Thread(target=main, args=()).start()
Thread(target=send_msg, args=()).start()
