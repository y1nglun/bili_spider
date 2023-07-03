def fill_data(locs):
    seg = '<tr><td align="center">{}</td><td align="center">{}</td><td align="center">{}</td><td align="center">{}</td></tr>\n'.format(
        *locs)
    return seg


seg1 = '''
<!DOCTYPE HTML>
<html>
<body>
<meta charset="gb2312">
<h2 align="center">豆瓣电影top250</h2>
<table border='1' align="center" width="70%">
<tr bgcolor='yellow'>
'''

seg2 = "</tr>\n"
seg3 = "</table>\n</body>\n</html>"

fr = open("output.csv", "r", encoding='utf-8')
ls = []
for line in fr:
    line = line.replace("\n", "")
    ls.append(line.split(","))
fr.close()

fw = open("douban.html", "w")
fw.write(seg1)
fw.write(
    '<th width="25%" bgcolor="yellow">{}</th>\n<th width="25%" bgcolor="yellow">{}</th>\n<th width="25%" bgcolor="yellow">{}</th>\n<th width="25%" bgcolor="yellow">{}</th>\n'.format(
        *ls[0]))
fw.write(seg2)
for data in ls[1:]:
    fw.write(fill_data(data))
fw.write(seg3)
fw.close()

# 修改表格其他数据的背景色为浅绿色
with open("douban.html", "r") as f:
    content = f.read()

content = content.replace("<tr><td align=\"center\">", "<tr bgcolor=\"lightgreen\"><td align=\"center\">")

with open("douban.html", "w") as f:
    f.write(content)
