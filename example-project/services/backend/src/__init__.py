from datetime import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from flask import request
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg

# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/stocksdatabase"
pymongo = PyMongo(app)
# Get a reference to the stocks collection.
stocks: Collection = pymongo.db.stocks
api = Api(app)


class StocksPrice(Resource):
    def get(self):
        # 查询 price 在 1 到 20 之间的数据，并只返回 price 字段的列表
        query = {'$and': [{'date': {'$in': [datetime(2010, 1, 1, 0, 0), datetime(2022, 10, 1, 0, 0)]}}]}
        result = list(stocks.find(query))  # 执行查询并指定返回的字段
        print(len(result))
        # 从结果中提取 price 字段的值组成列表
        prices = [item['date'] for item in result]

        return jsonify(prices)  # 返回包含 price 字段值的列表作为 JSON 响应


class StocksAttributes(Resource):
    def get(self):
        json_data = request.get_json()  # 获取前端传入的 JSON 数据
        time_conditions = json_data.get("time", [])  # 获取时间条件
        attribute_conditions = json_data.get("attributes", {})  # 获取属性条件

        # 将字符串转换为日期类型
        date_objects = [datetime.strptime(date_str, "%Y-%m") for date_str in time_conditions]

        # 构建日期查询条件
        date_query = {"date": {"$gte": date_objects[0], "$lte": date_objects[1]}}

        attribute_queries = []
        attribute_name = []
        # 根据前端传入的属性条件构建查询条件
        for attr, details in attribute_conditions.items():
            if "name" in details and "range" in details:
                query = {details["name"]: {"$gte": details["range"][0], "$lte": details["range"][1]}}
                attribute_queries.append(query)
                attribute_name.append(details["name"])

        # 通过日期和属性条件进行查询
        query = {"$and": [date_query] + attribute_queries}
        print(query)
        # 执行查询并指定返回的字段
        result = list(stocks.find(query))  # 执行查询并指定返回的字段

        # 从结果中提取满足条件的 attributes 字段的值组成三个列表
        attribute1_values = [item[attribute_name[0]] for item in result]
        attribute2_values = [item[attribute_name[1]] for item in result]
        attribute3_values = [item[attribute_name[2]] for item in result]

        return jsonify({
            attribute_name[0]: attribute1_values,
            attribute_name[1]: attribute2_values,
            attribute_name[2]: attribute3_values
        })  # 返回满足条件的三个 attributes 的值，分别作为三个列表组成的 JSON 响应


api.add_resource(StocksPrice, '/companies')
api.add_resource(StocksAttributes, '/histogram')

# class CompaniesList(Resource):
#     def get(self, args=None):
#         # retrieve the arguments and convert to a dict
#         args = request.args.to_dict()
#         print(args)
#         # If the user specified category is "All" we retrieve all companies
#         if args['category'] == 'All':
#             cursor = companies.find()
#         # In any other case, we only return the companies where the category applies
#         else:
#             cursor = companies.find(args)
#         # we return all companies as json
#         return [Company(**doc).to_json() for doc in cursor]
#
#
# class Companies(Resource):
#     def get(self, id):
#         # search for the company by ID
#         cursor = companies.find_one_or_404({"id": id})
#         company = Company(**cursor)
#         # retrieve args
#         args = request.args.to_dict()
#         # retrieve the profit
#         profit = company.profit
#         # add to df
#         profit_df = pd.DataFrame(profit).iloc[::-1]
#         if args['algorithm'] == 'random':
#             # retrieve the profit value from 2021
#             prediction_value = int(profit_df["value"].iloc[-1])
#             # add the value to profit list at position 0
#             company.profit.insert(0, {'year': 2022, 'value': prediction_value})
#         elif args['algorithm'] == 'regression':
#             # create model
#             model_ag = AutoReg(endog=profit_df['value'], lags=1, trend='c', seasonal=False, exog=None, hold_back=None,
#                                period=None, missing='none')
#             # train the model
#             fit_ag = model_ag.fit()
#             # predict for 2022 based on the profit data
#             prediction_value = fit_ag.predict(start=len(profit_df), end=len(profit_df), dynamic=False).values[0]
#             # add the value to profit list at position 0
#             company.profit.insert(0, {'year': 2022, 'value': prediction_value})
#         return company.to_json()
#
#
# api.add_resource(CompaniesList, '/companies')
# api.add_resource(Companies, '/companies/<int:id>')
