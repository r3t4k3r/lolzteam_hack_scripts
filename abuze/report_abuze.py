import json
import requests
from time import sleep
from random import randint
from threading import Thread

#функция отправки репортов из массива
def reports_convert_and_sending(lzt):
    global report_array

    up_arr = ["Неправильное поднятие темы",
    "Поднятие темы словами ап, актуально и т.п",
    "Неверный ап темы",
    "2.20. Поднимать тему словами \"Ап\", \"актуально\" запрещено.",
    "2.20 Неверный ап темы",
    "2.20 Поднятие темы словами \"Ап\" или \"актуально\""]

    while True:
        while report_array != []:
            post = report_array[0][0]
            theme = report_array[0][1]

            if theme == "up":
                message = up_arr[randint(0,len(up_arr)-1)]

            out = lzt.send_report(post,message)
            try:
                if out["status"] == "ok":
                    print(f"[ЖБ] {post}:{message}")
                del report_array[0]
                sleep(5)
            except:
                for i in range(len(out["errors"])):
                    print("err:",out["errors"][i])
                sleep(5)


class Lolzteam:

    def __init__(self,token,server):
        self.token = token
        self.server = server
        self.s = requests.session()

    #проверка 1 сообщения
    def text_filter(self,text):
        filter_ap = ["aп","up!","up","aп!","актуально","актуально!","!up","/up","!ап","/ап"]
        n = False
        for word in filter_ap:
            if word == text:
                n = True
                break
        if n == True:
            return "up"
        else:
            return "nope"

    #отправка репорта
    def send_report(self,post,msg):
        data ={
            "oauth_token":self.token,
            "message":msg
        }
        link = f"{self.server}/api/index.php?posts/{str(post)}/report"
        response = json.loads(self.s.post(link, data=data).text)

        return response

    #получение сообщений
    def get_messages(self,start_post,count):
        link = f"{self.server}/api/index.php?/batch&oauth_token={self.token}"
        arr = [None]*count

        for i in range(count):
            arr[i] = {
                "id":str(i+1),
                "uri":f"index.php?/posts/{str(int(start_post)+i)}",
                "method":"GET"
            }
        data = json.dumps(arr)
        response = json.loads(self.s.post(link,data=data).text)["jobs"]

        out_arr = []
        for i in range(1,len(response)+1):
            resp = response[str(i)]
            if resp["_job_result"] == "ok":
                text = resp["post"]["post_body"].replace("[URL]","").replace("[/URL]","").lower()
                post_id = str(resp["post"]["post_id"])
                out_arr.append([post_id,text])
        print("Получено сообщений: "+str(len(out_arr)))

        return out_arr

    #проверка массива сообщений
    def check_posts(self,posts_list):
        out_arr = []
        for i in range(len(posts_list)):
            out = self.text_filter(posts_list[i][1])
            if out != "nope":
                out_arr.append([posts_list[i][0],out])

        return out_arr

def main(lzt):
    global report_array
    post = 10744334
    pic = 5000
    while True:
        #массив сообщений
        posts_arr = lzt.get_messages(post,pic)
        post += pic
        #фильтрованный массив
        report_array += lzt.check_posts(posts_arr)

if __name__ == "__main__":

    report_array = []
    token = "82d47bdc05a288967ce843babe1184caeb1d0e29" # Крыса
    server = "https://lolz.guru"
    lzt = Lolzteam(token,server)

    Thread(target=main, args=(lzt,)).start()
    Thread(target=reports_convert_and_sending, args=(lzt,)).start()

