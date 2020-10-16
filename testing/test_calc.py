#测试用例量大时，最好将测试用例定义在测试类中，然后用类来管理测试用例，用模块来管理类。因为类能完成继承。
#所以后续创建的测试用例都放在类中

import pytest
from pythoncode.calculator import Calculator

"""
class TestCalc:
    
    def setup_class(self):#如果只有setup那就是方法级别，在每个方法前都有
        print("开始计算")
        self.calc = Calculator()#加self，能让类中的其他方法调用这个类中定义的变量
    def teardown_class(self):
        print("计算结束")

    def test_add(self):
       # calc = Calculator()   #1、首先实例化被测类
        result = self.calc.add(1,1)#完成相加的操作，然后加断言 2、调用想要被测的方法
        assert result == 2   #3、最后加断言

    def test_add1(self):
      #  calc = Calculator()
        result = self.calc.add(100,100)
        assert result == 200

    def test_add2(self):
     #   calc = Calculator()
        result = self.calc.add(0.1,0.1)
        assert result == 0.2

"""

class TestCalc:

    def setup_class(self):
        print("开始计算")
        self.calc = Calculator()

    def teardown_class(self):
        print("计算结束")

    #装饰器@pytest.mark.parametrize()
    @pytest.mark.parametrize('a,b,expect',[
        [1,1,2],[100000,100000,200000],[0.1,0.1,0.2],[-1,-1,-2],[1,0,1],[1,-1,0]
    ],ids=['int_case','bignum_case','float_case','minus_case','zero_case','mix_case'])
    def test_add(self,a,b,expect):
        result = self.calc.add(a, b)
        assert result == expect

    @pytest.mark.parametrize('a,b,expect',[
        [2,1,2],[1,2,0.5],[-3,-1,3],[-1,4,-0.25],[0,1,0]
    ],ids=['int_case','float_case','minus_case','mix_case','zero_case'])
    def test_div(self,a,b,expect):
        result = self.calc.div(a, b)

    def test_zero_div(self):
        with pytest.raises(ZeroDivisionError):
            1 / 0


