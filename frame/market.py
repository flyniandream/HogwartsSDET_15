from selenium.webdriver.common.by import By

from frame.base_page import BasePage
from frame.search import Search


#1）2）继承的方式
class Market(BasePage):
    def goto_search(self):
        #self.find(By.XPATH, "//*[@resource-id='com.xueqiu.android:id/action_search']").click()
        self.parse_yaml("./market.yaml", "goto_search")
        return Search(self.driver)

'''
#3）组合的方式
class Market:
    def goto_search(self):
        BasePage.find(By.XPATH, "//*[@resource-id='com.xueqiu.android:id/action_search']").click()
        return Search()
'''

