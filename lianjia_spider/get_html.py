def fill_data(locs):
    seg = '<tr><td align="center">{}</td><td align="center">{}</td><td align="center">{}</td><td align="center">{}</td><td align="center">{}</td></tr>\n'.format(
        *locs)
    return seg


seg1 = '''
<!DOCTYPE HTML>
<html>
<body>
<meta charset="utf-8">
<h2 align="center">链家信息</h2>
<table border='1' align="center" width="70%">
<tr bgcolor='yellow'>
'''

seg2 = "</tr>\n"
seg3 = "</table>\n</body>\n</html>"

filename = input("请输入要读取的文件名（包括路径和扩展名）：")
try:
    with open(filename, "r", encoding='utf-8') as fr:
        ls = []
        for line in fr:
            line = line.replace("\n", "")
            ls.append(line.split(","))
except FileNotFoundError:
    print("文件不存在或路径错误！")
    exit()

fw = open("lianjia.html", "w", encoding='utf-8')
fw.write(seg1)
fw.write(
    '<th width="25%" bgcolor="yellow">序号</th>\n<th width="25%" bgcolor="yellow">标题</th>\n<th width="25%" bgcolor="yellow">房屋详细信息</th>\n<th width="25%" bgcolor="yellow">总价</th>\n<th width="25%" bgcolor="yellow">单价</th>\n')
fw.write(seg2)
for data in ls[1:]:
    fw.write(fill_data(data[:4] + [','.join(data[4:])]))
fw.write(seg3)
fw.close()

with open("lianjia.html", "r", encoding='utf-8') as f:
    content = f.read()

content = content.replace("<tr><td align=\"center\">", "<tr bgcolor=\"lightgreen\"><td align=\"center\">")

with open("lianjia.html", "w", encoding='utf-8') as f:
    f.write(content)
