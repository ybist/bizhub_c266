#C266打印机计数
#  by 2997
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import datetime,time,locale,os
from lxml import etree

#参考 https://www.jianshu.com/p/1531e12f8852
#览器驱动,放到python目录
#chrome
#https://chromedriver.storage.googleapis.com/index.html

#firefox
#https://github.com/mozilla/geckodriver/releases

list = []
chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(chrome_options=chrome_options)
mainUrl = "http://192.168.2.254/wcd/system_counter.xml"
browser.get(mainUrl)
time.sleep(10)
#print(f"browser text = {browser.page_source}")
webdata = browser.page_source
#print(webdata)
html = etree.HTML(webdata)
#html_data = html.xpath('//th[@width="260px"]')
html_data = html.xpath('//td//div[@align="right"]')
for i in html_data:
    list.append(i.text)
browser.quit()

fist_date = datetime.date(2020,7,6)
#next_date = datetime.date(2021,1,5)
current_date = datetime.date.today()
black_fist_count = 37574
color_fist_count = 5181
black_mum = 5000
color_mum = 300
delta = current_date-fist_date
count_cycle = delta.days // 30 + 1
black_limit = black_fist_count + black_mum * count_cycle
color_limit = color_fist_count + color_mum * count_cycle
print(fist_date)
print(current_date)
print(delta.days)
print(count_cycle)
print(black_limit)
print(color_limit)

print('\n',"C226打印机--打印及复印计数",'\n',time.strftime('%Y年%m月%d日%H时%M分%S秒'),'\n','总计', str(list[103]),'\n','黑色', str(list[104]),'\n','彩色', str(list[105]))

black_count = int(str(list[104]))
color_count = int(str(list[105]))


if (black_count >= (black_limit-500)) or ((current_date.day > 1) and (current_date.day < 5)):
    black_command = 'msg /server:192.168.2.103 * "c226打印机本月黑色上限' + str(black_limit) + ',已使用' + str(list[104]) + '",本月剩余"' + str(black_limit-black_count)
    os.system(black_command)
if (color_count >= (color_limit-50)) or ((current_date.day > 1) and (current_date.day < 5)):
    color_command = 'msg /server:192.168.2.103 * "c226打印机本月彩色上限' + str(color_limit) + ',已使用' + str(list[105]) + '",本月剩余"' +  str(color_limit-color_count)
    os.system(color_command)
  
c226_file = open('c266_print_count.txt', 'r+')
c226_file.read()
#c226_file.write('\n' + time.strftime('%Y年%m月%d日%H时%M分%S秒'))
#c226_file.write('\n' + 'C226打印机复印总数量')
#c226_file.write('\n' + '         ' + '日期' + '              ' + '总计' +'    ' + '黑色' + '    ' + '彩色')
c226_file.write('\n' +  time.strftime('%Y年%m月%d日') + '   ' + str(list[103]) + '   ' + str(list[104]) + '    ' + str(black_limit-black_count) + '         ' + str(list[105]) + '     ' + str(color_limit-color_count))
c226_file.close()
