import pytest
import yaml

from pythoncode.calculator import Calculator

# 测试数据的数据驱动1-2：解析测试数据文件
# 如果yaml文件中有中文，需要加编码格式encoding='utf-8'
#1-2)-1:解析加法的测试数据文件
def get_datas():
    with open("./datas/calc.yaml", encoding='utf-8') as f:
        datas = yaml.safe_load(f)#只能获取一次
    add_datas = datas['add']['datas']
    add_ids = datas['add']['ids']

    sub_datas = datas['sub']['datas']
    sub_ids = datas['sub']['ids']

    mul_datas = datas['mul']['datas']
    mul_ids = datas['mul']['ids']

    div_datas = datas['div']['datas']
    div_ids = datas['div']['ids']
    return [add_datas, add_ids, sub_datas, sub_ids, mul_datas, mul_ids, div_datas, div_ids]


class TestCalc:
    def setup_class(self):
        print("开始计算")
        self.calc = Calculator()

    def teardown_class(self):
        print("计算结束")

    @pytest.mark.run(order=1) #改变执行顺序：加-减-乘-除
    # 1-3)-1:加法：测试数据的数据驱动的测试用例
    @pytest.mark.parametrize('a,b,expect', get_datas()[0], ids=get_datas()[1])
    def test_add(self, a, b, expect):
        result = self.calc.add(a, b)
        assert result == expect

    @pytest.mark.parametrize('a,b,expect', [
        [0.1, 0.1, 0.2], [0.1, 0.2, 0.3]
    ])
    @pytest.mark.run(order=2)
    def test_add_float(self, a, b, expect):
        result = self.calc.add(a, b)
        assert round(result, 2) == expect

    @pytest.mark.run(order=-2)
    # 1-3)-2:除法：测试数据的数据驱动的测试用例
    @pytest.mark.parametrize('a,b,expect', get_datas()[6], ids=get_datas()[7])
    def test_div(self, a, b, expect):
        result = self.calc.div(a, b)
        assert result == expect

    @pytest.mark.run(order=-1)
    def test_div_zero(self):
        with pytest.raises(ZeroDivisionError):
            result = self.calc.div(1, 0)

    @pytest.mark.run(order=3)
    # 1-3)-3:减法：测试数据的数据驱动的测试用例
    @pytest.mark.parametrize('a,b,expect', get_datas()[2], ids=get_datas()[3])
    def test_sub(self, a, b, expect):
        result = self.calc.sub(a, b)
        assert result == expect

    @pytest.mark.run(order=4)
    # 1-3)-4:乘法：测试数据的数据驱动的测试用例
    @pytest.mark.parametrize('a,b,expect', get_datas()[4], ids=get_datas()[5])
    def test_mul(self, a, b, expect):
        result = self.calc.mul(a, b)
        assert result == expect

    @pytest.mark.run(order=5)
    @pytest.mark.parametrize('a,b,expect', [
        [0.3, 0.1, 0.03],[0.9,0.99,0.891]
    ])
    def test_mul_float(self, a, b, expect):
        result = self.calc.mul(a, b)
        assert round(result, 3) == expect


