import json
f = open("ban_list.txt", "r")
data = json.loads(f.read())
arr = list(set(data))
del arr[0]
print(len(arr))
out_text = ' @'.join(arr)
f.close()
f = open("out_list.txt", "w")
f.write(out_text)
f.close()
