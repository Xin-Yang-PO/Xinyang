# -- coding: utf-8
# author: JianCui
# start data: 2022-08-29-21:37
# over data: 2022-08-30-19:40
"""
获取余票信息：
        车辆名称：train_name
        始发站： from_station
        发车时间： from_time
        到达时间： to_time
        终点站： to_station
        耗时：need_time
        一等座: ticket_1,price_1
        二等座:ticket_2,price_2
        硬座:ticket_3,price_3
        无座:ticket_4,price_4
        软卧:ticket_5,price_5
        硬卧:ticket_6,price_6
        换乘时间/总历时：time_list
"""
import time
import SendInformation
import prettytable
from colorama import init, Fore
from selenium.webdriver.common.by import By
init(autoreset=True)
browser = SendInformation.browser
"""以免此次车票不满足要求，重新运行程序"""
print('重新查询请输入“XXX”退出程序！继续输入任意。')
re = str(input('请输入：'))
if re == 'XXX':
    print('\033[31m即将退出程序！\033[0m')
    time.sleep(1)
    browser.close()
    exit()
else:
    pass


class GetTicket:
    """获取余票信息"""
    print('\033[32m余票信息获取中...\033[0m')  # 反映状态

    # noinspection PyProtectedMember
    def __init__(self):
        self.browser = browser
        self.time = SendInformation._from_time
        self.train_no = []
        self.from_station_no = []
        self.to_station_no = []
        self.seat_type = []
        self.table = prettytable.PrettyTable()
        self.hc_dc = SendInformation._hc_dc

    def show_ticket(self):
        """获取余票信息"""
        page_url = self.browser.current_url  # 获取当前网址
        print('当前访问：', page_url)  # 反映状态
        print('\033[35m正在加载余票信息...\033[0m')  # 反映状态
        """判断票类型"""
        if self.hc_dc == 'Y':
            try:
                train = self.browser.find_elements(By.XPATH, '//*[@class="train"]/div/a')  # 火车名称
                first_station = self.browser.find_elements(By.XPATH, '//*[@class="cdz"]/strong[1]')  # 第一站
                second_station = self.browser.find_elements(By.XPATH, '//*[@class="cdz"]/strong[2]')  # 第二站
                first_time = self.browser.find_elements(By.XPATH, '//*[@class="cds"]/strong[1]')  # 发车时间
                second_time = self.browser.find_elements(By.XPATH, '//*[@class="cds"]/strong[2]')  # 到达时间
                need_time = self.browser.find_elements(By.XPATH, '//*[@class="time color666"]')  # 消耗时间
                ticket_1 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[3]")  # 一等座
                ticket_2 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[4]")  # 二等座
                ticket_3 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[10]")  # 硬座
                ticket_4 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[11]")  # 无座
                ticket_5 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[6]")  # 软卧
                ticket_6 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[8]")  # 硬卧
                interval_time = self.browser.find_elements(By.XPATH, '//*[@class="colorA"]')  # 换乘时间
                total_time = self.browser.find_elements(By.XPATH, '//*[@class="alltime"]')  # 总历时
                """设置字体颜色"""
                time_list = []
                for j in range(len(total_time)):
                    a = '换乘时间：' + interval_time[j + 1].text[5:]
                    b = '总历时：' + total_time[j].text
                    a = Fore.LIGHTRED_EX + a + Fore.RESET  # 字体颜色设置
                    b = Fore.LIGHTGREEN_EX + b + Fore.RESET
                    time_list.append(a)
                    time_list.append(b)
                t_l = []
                f_s_l = []
                s_s_l = []
                f_t_l = []
                s_t_l = []
                for f in range(len(train)):
                    t = train[f].text
                    f_s = first_station[f].text
                    s_s = second_station[f].text
                    f_t = first_time[f].text
                    s_t = second_time[f].text
                    t = Fore.LIGHTYELLOW_EX + t + Fore.RESET
                    f_s = Fore.LIGHTRED_EX + f_s + Fore.RESET
                    s_s = Fore.LIGHTGREEN_EX + s_s + Fore.RESET
                    f_t = Fore.LIGHTRED_EX + f_t + Fore.RESET
                    s_t = Fore.LIGHTGREEN_EX + s_t + Fore.RESET
                    t_l.append(t)
                    f_s_l.append(f_s)
                    s_s_l.append(s_s)
                    f_t_l.append(f_t)
                    s_t_l.append(s_t)
                globals()['train'] = t_l
                header = ['车辆名称', '始发站', '发车时间', '到达时间', '终点站', '耗时',
                          '一等座', '二等座', '硬座', '无座', '软卧', '硬卧', '']  # 表头
                self.table.field_names = header  # 输出表格表头设置
                """设置表格内容"""
                for i in range(len(train)):
                    data_1 = [t_l[i], f_s_l[i], f_t_l[i], s_t_l[i],
                              s_s_l[i], need_time[i].text, ticket_1[i].text,
                              ticket_2[i].text, ticket_3[i].text, ticket_4[i].text,
                              ticket_5[i].text, ticket_6[i].text, time_list[i]]
                    self.table.add_row(data_1)
                print(self.table)
            except Exception as e:  # 异常处理
                e = e  # 异常检测
                print('\033[31m加载失败！退出程序\033[0m')  # 反映状态
                self.browser.close()  # 关闭浏览器
                exit()  # 弹窗程序

        time.sleep(1)
        if self.hc_dc == 'N':
            try:
                train = self.browser.find_elements(By.XPATH, '//*[@class="train"]/div/a')  # 火车名称
                first_station = self.browser.find_elements(By.XPATH, '//*[@class="cdz"]/strong[1]')  # 第一站
                second_station = self.browser.find_elements(By.XPATH, '//*[@class="cdz"]/strong[2]')  # 第二站
                first_time = self.browser.find_elements(By.XPATH, '//*[@class="cds"]/strong[1]')  # 发车时间
                second_time = self.browser.find_elements(By.XPATH, '//*[@class="cds"]/strong[2]')  # 到达时间
                need_time = self.browser.find_elements(By.XPATH, '//*[@class="ls"]/strong')  # 消耗时间
                need_time_ = self.browser.find_elements(By.XPATH, '//*[@class="ls"]/span')  # 消耗时间
                ticket_1 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[3]")  # 一等座
                ticket_2 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[4]")  # 二等座
                ticket_3 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[10]")  # 硬座
                ticket_4 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[11]")  # 无座
                ticket_5 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[6]")  # 软卧
                ticket_6 = self.browser.find_elements(By.XPATH, "//*[contains(@id,'ticket_')]/td[8]")  # 硬卧
                """设置字体颜色"""
                t_l = []
                f_s_l = []
                s_s_l = []
                f_t_l = []
                s_t_l = []
                for f in range(len(train)):
                    t = train[f].text
                    f_s = first_station[f].text
                    s_s = second_station[f].text
                    f_t = first_time[f].text
                    s_t = second_time[f].text
                    t = Fore.LIGHTYELLOW_EX + t + Fore.RESET
                    f_s = Fore.LIGHTRED_EX + f_s + Fore.RESET
                    s_s = Fore.LIGHTGREEN_EX + s_s + Fore.RESET
                    f_t = Fore.LIGHTRED_EX + f_t + Fore.RESET
                    s_t = Fore.LIGHTGREEN_EX + s_t + Fore.RESET
                    t_l.append(t)
                    f_s_l.append(f_s)
                    s_s_l.append(s_s)
                    f_t_l.append(f_t)
                    s_t_l.append(s_t)
                print('\033[35m正在加载余票信息...\033[0m')  # 反映状态
                header = ['车辆名称', '始发站', '发车时间', '到达时间', '终点站', '耗时', '',
                          '一等座', '二等座', '硬座', '无座', '软卧', '硬卧']  # 表头
                self.table.field_names = header  # 输出表格表头设置
                """设置表格内容"""
                for i in range(len(train)):
                    data_1 = [t_l[i], f_s_l[i], f_t_l[i], s_t_l[i],
                              s_s_l[i], need_time[i].text, need_time_[i].text, ticket_1[i].text,
                              ticket_2[i].text, ticket_3[i].text, ticket_4[i].text,
                              ticket_5[i].text, ticket_6[i].text]
                    self.table.add_row(data_1)
                print(self.table)
            except Exception as e:  # 异常处理
                e = e # 异常检测
                print('\033[31m加载失败！退出程序\033[0m')  # 反映状态
                self.browser.close()  # 关闭浏览器
                exit()


c = GetTicket()  # 启动GetTicket()
c.show_ticket()  # 展示余票
train_ = globals()['train']  # 再次声明全局变量，便于其他python file调用
