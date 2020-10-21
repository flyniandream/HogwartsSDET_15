#-*- coding:utf-8 -*-
#被测代码，计算器（加 减 乘 除）

def fun(x):
    return x

class Calculator:
    def add(self,a,b):
        return  a + b

    def add1(self,a:int,b:int)->int:
        return  a + b

    def sub(self,a,b):
        return a - b

    def mul(self,a,b):
        return a * b

    def div(self,a,b):
        # assert b != 0 #注意：若定义，raise中就是AssertionError
        return a / b