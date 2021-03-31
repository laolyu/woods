import os
import time

import allure
import pytest
from loguru import logger


@allure.feature('test_module_解锁')
class TestHi:
    @allure.story('解锁成功')
    def test_case_01(self):
        """
        用例描述：Test case 01
        """

        cc01 = 10
        logger.info('case_01执行')
        assert cc01 == 10

    @allure.story('识别截图')
    @pytest.fixture()
    def message(self):
        message = '我们是中国人'
        return message

    @allure.story('点赞成功')
    def test_case_02(self, message):
        """
        用例描述：Test case 02
        """
        logger.info('case_02执行')
        assert '国人' in message


if __name__ == '__main__':
    # 执行pytest单元测试，生成 Allure 报告需要的数据存在 /temp 目录
    pytest.main(['-s', '--alluredir', './temp'])
    # 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
    os.system('allure generate ./temp -o ./report --clean')
