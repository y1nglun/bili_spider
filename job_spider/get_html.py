def fill_data(locs):
    seg = '<tr><td align="center">{}</td><td align="center">{}</td><td align="center">{}</td><td align="center">{}</td><td align="center">{}</td></tr>\n'.format(
        *locs)
    return seg


seg1 = '''
<!DOCTYPE HTML>
<html>
<body>
<meta charset="utf-8">
<h2 align="center">招聘岗位</h2>
<table border='1' align="center" width="70%">
<tr bgcolor='yellow'>
'''

seg2 = "</tr>\n"
seg3 = "</table>\n</body>\n</html>"

filename = input("请输入要读取的文件名（包括路径和扩展名）：")
try:
    with open(filename, "r", encoding="utf-8") as fr:
        ls = []
        for line in fr:
            line = line.replace("\n", "")
            ls.append(line.split(","))
except FileNotFoundError:
    print("文件不存在或路径错误！")
    exit()


def generate_html_table(data):
    table_header = '<th width="25%" bgcolor="yellow">{}</th>\n'.format(
        '</th>\n<th width="25%" bgcolor="yellow">'.join(data[0]))
    table_rows = ''

    for row in data[1:]:
        table_row = fill_data(row)
        table_rows += table_row

    html_content = seg1 + table_header + seg2 + table_rows + seg3
    return html_content


html_table = generate_html_table(ls)

# 将HTML表格保存到文件
with open("job.html", "w", encoding="utf-8") as fw:
    fw.write(html_table)

# 修改表格其他数据的背景色为浅绿色
with open("job.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("<tr><td align=\"center\">", "<tr bgcolor=\"lightgreen\"><td align=\"center\">")

with open("job.html", "w", encoding="utf-8") as f:
    f.write(content)
