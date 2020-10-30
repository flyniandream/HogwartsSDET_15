from time import sleep

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait


class TestDemo:
    def setup(self):
        #定义了一个字典
        desired_caps={}
        desired_caps['platformName']='Android'
        desired_caps['deviceName']='127.0.0.1:7555'
        desired_caps['appPackage']='com.tencent.wework'
        desired_caps['appActivity']='.launch.LaunchSplashActivity'
        desired_caps['noReset'] = 'True'
        #desired_caps["settings[waitForIdleTimeout]"] = 0
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)


    def test_daka(self):
        self.driver.find_element(MobileBy.XPATH, "//*[@text='工作台']").click()
        #滑动屏幕到下页：原生定位方式
        self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                                 'new UiScrollable(new UiSelector()\
                                 .scrollable(true).instance(0))\
                                 .scrollIntoView(new UiSelector()\
                                 .text("打卡").instance(0));').click()
        #settings
        self.driver.update_settings({"waitForIdleTimeout": 0})

        self.driver.find_element(MobileBy.XPATH, "//*[@text='外出打卡']").click()
        self.driver.find_element(MobileBy.XPATH, "//*[contains(@text,'次外出')]").click()

        '''
        sleep(3)
        #法1：page_source，前面必须加强等
        assert "上下班打卡成功" in self.driver.page_source
        '''
        #法2：lambda，加显式等待
        WebDriverWait(self.driver, 10).until(lambda x: "外出打卡成功" in x.page_source)

    def teardown(self):
        self.driver.quit()