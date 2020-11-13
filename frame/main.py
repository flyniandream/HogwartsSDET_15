#雪球app首页
import yaml
from selenium.webdriver.common.by import By

from frame.base_page import BasePage
from frame.market import Market


class Main(BasePage):
    def goto_market(self):
        '''
        1)开始编写测试框架2)黑名单模式
        :return:
        '''
        #之前find方法没有click属性，是因为find方法没有指定类型，到其方法中指定就可以了
        #制造假的弹框
        # self.find(By.XPATH, "//*[@resource-id='com.xueqiu.android:id/post_status']").click()
        # self.find(By.XPATH, "//*[@resource-id='android:id/tabs']//*[@text='行情']").click()

        #7)实现步骤的封装
        '''
        with open("./main.yaml", encoding="utf-8") as f:
            data = yaml.load(f)
        #print(data)
        steps = data['goto_market']
        for step in steps:
            if 'click' == step['action']:
                self.find(step['by'],step['locator']).click()
        return Market(self.driver)
        '''
        self.parse_yaml("./main.yaml", "goto_market")
        return Market(self.driver)

        '''
        #3)单例模式
        BasePage.find(By.XPATH, "//*[@resource-id='com.xueqiu.android:id/post_status']").click()

        BasePage.find(By.XPATH, "//*[@resource-id='android:id/tabs']//*[@text='行情']").click()
        return Market()
        '''