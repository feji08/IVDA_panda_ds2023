import unittest
from __init__ import app  # 导入你的 Flask 应用


class TestYourApp(unittest.TestCase):
    def setUp(self):
        # 创建测试客户端
        self.app = app.test_client()

    def test_get_method(self):
        # 模拟发送 Get 请求
        response = self.app.get('/histogram', json={
            "time": ["2010-01", "2022-10"],
            "attributes": {
                "price": {
                    "name": "price",
                    "range": [10, 20]
                },
                "roe": {
                    "name": "roe",
                    "range": [0, 1]
                },
                "roic": {
                    "name": "roic",
                    "range": [0, 1]
                }
            }
        })

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)  # 例如，检查响应状态码是否为 200

        # 检查其他预期结果
        print(len(response.get_json()['price']))


if __name__ == '__main__':
    unittest.main()
