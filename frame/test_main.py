from frame.main import Main


class TestMain:
    def test_main(self):
        #这种连续传递的方式，会暴露driver，中途改driver会有些麻烦。解决方法：单例模式，让全局唯一，将继承改成组合
        #main = Main().goto_market().goto_search()
        Main().goto_market().goto_search()

