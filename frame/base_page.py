#12-3、4、5、6节课，main.py market.py search.py test_main.py
import yaml
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


#引进了singleton（装饰器模式）后，类变成了单例类

from frame.hand_black import handle_black



'''
@singleton
'''
class BasePage:
    #封装一个黑名单，将resource-id引进去。注意它是一个元组
    black_list = [(By.XPATH, "//*[@resource-id='com.xueqiu.android:id/iv_close']")]
    max_num = 3 #加下划线,保护数据类型
    error_num = 0

    def __init__(self, driver: WebDriver = None):
        '''
        初始化应用
        '''
        if driver is None:
            desired_caps = {}
            desired_caps['platformName'] = 'Android'
            desired_caps['deviceName'] = '127.0.0.1:7555'
            desired_caps['appPackage'] = 'com.xueqiu.android'
            desired_caps['appActivity'] = '.view.WelcomeActivityAlias'
            desired_caps['noReset'] = 'True'
            # desired_caps["settings[waitForIdleTimeout]"] = 0
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            self.driver.implicitly_wait(10)
        else:
            self.driver = driver

    '''
    #1)2)
    #by查找方法，locator查找的定位方式
    def find(self,by,locator=None):
        try:
            if locator is None:
                #如果传的参数是一个，只有by，就解元组
                result = self.driver.find_element(*by)
            else:
                #如果传的元素有两个，既有by，又有locator
                result = self.driver.find_element(by,locator)
            self._error_num = 0
            return result
        #捕获黑名单中的元素
        except Exception as e:
            #超过最大查找次数会抛异常，若不超过会一直查找
            if self._error_num > self._max_num:
                raise e
            self._error_num +=1
            #从黑名单中遍历元素，依次进行处理
            for black_ele in self._black_list:
                ele = self.driver.find_elements(*black_ele)
                if len(ele) > 0:
                    ele[0].click()
                    #处理完黑名单后，再次查找原来的元素
                    return self.find(by,locator)
            raise e
    '''
    #4)封装find方法
    @handle_black
    def find(self, by, locator=None):
        if locator is None:
            # 如果传的参数是一个，只有by，就解元组
            result = self.driver.find_element(*by)
        else:
            # 如果传的元素有两个，既有by，又有locator
            result = self.driver.find_element(by, locator)
        return result

    def parse_yaml(self, path, func_name):
        with open(path, encoding="utf-8") as f:
            data = yaml.load(f)
        self.parse(data[func_name])

    def parse(self, steps):
        for step in steps:
            if 'click' == step['action']:
                self.find(step['by'],step['locator']).click()
            elif 'send' == step['action']:
                self.find(step['by'], step['locator']).send_keys(step['content'])


