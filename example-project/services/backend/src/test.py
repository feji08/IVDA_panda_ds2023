import unittest
from __init__ import app  # 导入你的 Flask 应用


class TestYourApp(unittest.TestCase):
    def setUp(self):
        # 创建测试客户端
        self.app = app.test_client()

    def test_get_method(self):
        # 模拟发送 Get 请求
        response = self.app.post('/histogram', json={
            "time": ["2010-01", "2022-10"],
            "attributes": {
                "attribute1": {
                    "name": "price",
                    "range": [10, 20]
                },
                "attribute2": {
                    "name": "roe",
                    "range": [0, 1]
                },
                "attribute3": {
                    "name": "roic",
                    "range": [0, 1]
                }
            }
        })

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)  # 例如，检查响应状态码是否为 200

        # 检查其他预期结果
        print(len(response.get_json()['price']))

    def test_bar_chart(self):
        # 模拟发送 Get 请求
        response = self.app.post('/barchart', json={
            "time": ["2010-01", "2022-10"],
            "attributes": {
                "attribute1": {
                    "name": "price",
                    "range": [10, 20]
                },
                "attribute2": {
                    "name": "roe",
                    "range": [0, 1]
                },
                "attribute3": {
                    "name": "roic",
                    "range": [0, 1]
                }
            },
            "nodes": ["returnOnAssets", "grossProfitMargin"],
            "indicator": "price",
            "algorithm": "PCA"
        })

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)  # 例如，检查响应状态码是否为 200

        # 检查其他预期结果
        print(response.get_json())

    def test_Network_Layout(self):
        # 模拟发送 Get 请求
        response = self.app.post('/networkGraph/layout', json={
            "time": ["2010-01", "2022-10"],
            "attributes": {
                "attribute1": {
                    "name": "price",
                    "range": [10, 20]
                },
                "attribute2": {
                    "name": "roe",
                    "range": [0, 1]
                },
                "attribute3": {
                    "name": "roic",
                    "range": [0, 1]
                }
            }
        })

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)  # 例如，检查响应状态码是否为 200

        # 检查其他预期结果
        print(response.get_json())
        print("---------------------")

    def test_Network_Add_Node(self):
        # only after calling the NetworkLayout API, will app.config["xxx"] in NetworkAddNode API be successfully set.
        self.app.post('/networkGraph/layout', json={
            "time": ["2010-01", "2022-10"],
            "attributes": {
                "attribute1": {
                    "name": "price",
                    "range": [10, 20]
                },
                "attribute2": {
                    "name": "roe",
                    "range": [0, 1]
                },
                "attribute3": {
                    "name": "roic",
                    "range": [0, 1]
                }
            }
        })

        response = self.app.post('/networkGraph/newNode', json={
            "time": ["2010-01", "2022-10"],
            "attributes": {
                "attribute1": {
                    "name": "price",
                    "range": [10, 20]
                },
                "attribute2": {
                    "name": "roe",
                    "range": [0, 1]
                },
                "attribute3": {
                    "name": "roic",
                    "range": [0, 1]
                }
            },
            "nodes": ["netIncome", "assetTurnover"],
            "indicator": "revenue",
            "algorithm": "PCA"
        })

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)  # 例如，检查响应状态码是否为 200

        # 检查其他预期结果
        print(response.get_json())
        print("---------------------")


if __name__ == '__main__':
    unittest.main()
