# C266打印机计数
# Author: 2997@YBZN
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import datetime,time,locale,os
from lxml import etree
import requests
#参考 https://www.jianshu.com/p/1531e12f8852
#览器驱动,放到python目录
#chrome
#https://chromedriver.storage.googleapis.com/index.html

#firefox
#https://github.com/mozilla/geckodriver/releases

def get_print_count():
    list = []
    all_count = ''
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

    begin_date = datetime.date(2020,12,11)
    #next_date = datetime.date(2021,6,10)
    current_date = datetime.date.today()
    black_first_count = 53520
    color_first_count = 6093
    black_num = 5000
    color_num = 300
    delta = current_date-begin_date
    count_cycle = delta.days // 30 + 1
    black_limit = black_first_count + black_num * count_cycle
    color_limit = color_first_count + color_num * count_cycle
    black_all_count = black_num * 6
    color_all_count = color_num * 6
    black_color_all_count = black_first_count + color_first_count + black_all_count + color_all_count
    print(begin_date)
    print(current_date)
    print(delta.days)
    print(count_cycle)
    print(black_limit)
    print(color_limit)

    black_count = int(str(list[104]))
    color_count = int(str(list[105]))

    print('\n',"柯尼卡美能C266打印统计",'\n',time.strftime('%Y年%m月%d日%H时%M分%S秒'),'\n','总计', str(list[103]),'\n','黑色', str(list[104]),'\n','彩色', str(list[105]),'\n')
    first_count = '本期结算数量' +' ' + '截止2021年06月10日' + '\n' + '半年可用总计' + str(black_color_all_count) + '    黑色' + str(black_first_count + black_all_count) + '    彩色' + str(color_first_count + color_all_count) + '\n'
    all_count = '当前数量统计  ' + time.strftime('%Y年%m月%d日%H时%M分') + '\n' + '当前使用计数' + str(list[103]) + '    ' + '黑色' + str(list[104]) + '    ' + '彩色' + str(list[105])
    remainder1 = '本月剩余数量  ' + '本月6号至下月5号' + '\n' + '本月剩余总计' + str((black_limit-black_count) + (color_limit-color_count)) + '     ' + '黑色' + str(black_limit-black_count) + '     ' + '彩色' + str(color_limit-color_count)
    remainder2 = '半年剩余数量  ' + '截止2021年06月10日' + '\n' + '半年剩余总计' + str(91412 - int(str(list[103]))) + '     ' + '黑色' + str(83520 - int(str(list[104]))) + '     ' + '彩色' + str(7892 - int(str(list[105])))
        
    print_all = '\n' + first_count + '\n' + all_count + '\n\n' + remainder1 + '\n\n' + remainder2
    print(print_all)

    if (black_count >= (black_limit-500)) or ((current_date.day > 1) and (current_date.day < 5)):
        black_command = 'msg /server:192.168.2.16 * "c226打印机本月黑色上限' + str(black_limit) + ',已使用' + str(list[104]) + '",本月剩余"' + str(black_limit-black_count)
        os.system(black_command)
    if (color_count >= (color_limit-50)) or ((current_date.day > 1) and (current_date.day < 5)):
        color_command = 'msg /server:192.168.2.16 * "c226打印机本月彩色上限' + str(color_limit) + ',已使用' + str(list[105]) + '",本月剩余"' +  str(color_limit-color_count)
        os.system(color_command)
    
    c226_file = open('c266_print_count.txt', 'r+')
    c226_file.read()
    #c226_file.write('\n' + time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    #c226_file.write('\n' + 'C226打印机复印总数量')
    #c226_file.write('\n' + '         ' + '日期' + '              ' + '总计' +'    ' + '黑色' + '    ' + '彩色')
    c226_file.write('\n' +  time.strftime('%Y年%m月%d日') + '   ' + str(list[103]) + '   ' + str(list[104]) + '    ' + str(black_limit-black_count) + '         ' + str(list[105]) + '     ' + str(color_limit-color_count))
    c226_file.close()

    c226_file = open('F:\工作文件夹\租赁打印机c226使用计数\c266_print_count.txt', 'r+')
    c226_file.read()
    #c226_file.write('\n' + time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    #c226_file.write('\n' + 'C226打印机复印总数量')
    #c226_file.write('\n' + '         ' + '日期' + '              ' + '总计' +'    ' + '黑色' + '    ' + '彩色')
    c226_file.write('\n' +  time.strftime('%Y年%m月%d日') + '   ' + str(list[103]) + '   ' + str(list[104]) + '    ' + str(black_limit-black_count) + '         ' + str(list[105]) + '     ' + str(color_limit-color_count))
    c226_file.close()
    
    Synology_Chat(print_all)


def Synology_Chat(count):
    #curl -X POST  --data-urlencode 'payload={"text": "This is a test"}'  "http://192.168.2.241:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22PItBdaWoWjoC1VDXCIg5lS9g52JJY4aBnL5C1vJwwf3kzhr4yVG7ro2gifvmwMaF%22"
    chat_url = "http://192.168.2.241:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22Z6iYpGndUs3oq9MRmhcNJZuefJNEVGaFDpHxeKxdrIrGWUdjE6fjUBzdNsWDKGJJ%22"
    #payload = 'payload={"text": "This is a test"}'
    #payload = 'payload={"text": "这是一个测试"}'
    payload = 'payload={"text": "' + count + '"}'
    payload = payload.encode("utf-8").decode("latin1")
    r = requests.post(chat_url, payload).text

if __name__ == '__main__':
    get_print_count()