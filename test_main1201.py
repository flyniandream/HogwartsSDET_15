#context模块假设已定义，这里仅加载
#第一步：定义yaml文件
#第二步：在test_main中调用yaml
#第三步：写yaml

import pytest

from context import Context

class TestMain:
    context = Context()
    context.load("./1201tmp.yaml")

    @pytest.mark.parametrize("testcase",context.store.testcase.values(),ids=context.store.testcase.keys())
    def test_main1201(self,testcase):
        self.context.run_steps_by_testcase(testcase)