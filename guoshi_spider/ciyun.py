import re
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

stop_words = ['的', '和', '是', '等']  # 停用词列表，用于过滤掉一些常见词语

for year in range(2020, 2024):  # 遍历2020年到2023年的范围
    with open(f'{year}年政府工作报告.txt', 'r', encoding='utf-8') as file:
        text = file.read()  # 读取政府工作报告文本内容

    cleaned_text = re.sub(r'\s+|[^\w\s]', '', text)  # 使用正则表达式去除文本中的空白字符和标点符号

    seg_list = jieba.cut(cleaned_text)  # 使用结巴分词对文本进行分词
    filtered_seg_list = [word for word in seg_list if word not in stop_words]  # 过滤掉停用词

    segmented_text = ' '.join(filtered_seg_list)  # 将过滤后的分词结果拼接成一个字符串

    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='C:/Windows/Fonts/STHUPO.TTF').generate(segmented_text)
    # 创建词云对象，设置词云图的宽度、高度、背景颜色和字体路径，并生成词云图

    output_file = f'{year}年词云图.png'  # 输出文件名
    wordcloud.to_file(output_file)  # 将词云图保存为图片文件

    plt.figure(figsize=(10, 6))  # 设置画布大小
    plt.imshow(wordcloud, interpolation='bilinear')  # 显示词云图
    plt.axis('off')  # 不显示坐标轴
    plt.show()  # 显示图像
