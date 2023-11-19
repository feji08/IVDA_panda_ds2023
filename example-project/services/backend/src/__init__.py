from datetime import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from flask import request
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.ar_model import AutoReg
import networkx as nx

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


def compute_coefficient(df, indicator, node_1, node_2):
    # dimension reduction
    # PCA for display, indicator ~ node_1, node_2
    df_display = df[[indicator, node_1, node_2]].copy()
    # handling missing value(ignore on purpose) ~ get all rows without NAN
    print(
        "The dataset before dropping the rows contains {} data records and {} features.".format(df_display.shape[0],
                                                                                                df_display.shape[
                                                                                                    1]))
    df_display.dropna(inplace=True)
    print("The dataset now contains {} data records and {} features.".format(df_display.shape[0],
                                                                             df_display.shape[1]))
    # 1. Standardization
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_display)
    # Convert the standardized data back to a DataFrame
    df_scaled = pd.DataFrame(X_scaled, columns=df_display.columns)
    # 2. Dimension reduction
    # Perform PCA with two components
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    # Create a DataFrame with the new dimensions
    df_pca = pd.DataFrame(X_pca, columns=['PCA_Component_1', 'PCA_Component_2'])
    # 3. Correlation compute ? which methods to choose
    # Calculate correlation coefficients
    corr_1_2 = df_scaled[indicator].corr(df_scaled[node_1])
    corr_1_3 = df_scaled[indicator].corr(df_scaled[node_2])
    # Calculate correlation between the first dimension and the new dimension
    corr_1_pca = df_scaled[indicator].corr(df_pca['PCA_Component_1'])
    # Correlation values
    correlations = [corr_1_2, corr_1_3, corr_1_pca]

    return correlations


class StocksCoefficient(Resource):
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
        # 执行查询并指定返回的字段
        result = list(stocks.find(query))  # 执行查询并指定返回的字段
        df = pd.DataFrame(result)

        # 提取出算法和node，然后返回值
        # 获取 "Node1" 和 "Node2" 键对应的值
        node_1 = json_data.get("nodes", {}).get("Node1")
        node_2 = json_data.get("nodes", {}).get("Node2")
        indicator = json_data.get("indicator")
        algorithm = json_data.get("algorithm")

        coefficient = compute_coefficient(df, indicator, node_1, node_2)
        coefficient_all = compute_coefficient(pd.DataFrame(list(stocks.find())), indicator, node_1, node_2)

        coefficients = {
            "values": [coefficient[0], coefficient[1], coefficient[2], coefficient_all[2]]
        }

        return jsonify({"coefficients": coefficients})

class NetworkLayout(Resource):
    def get(self):
        json_data = request.get_json()
        time_conditions = json_data.get("time", [])
        attribute_conditions = json_data.get("attributes", {})
        date_objects = [datetime.strptime(date_str, "%Y-%m") for date_str in time_conditions]
        date_query = {"date": {"$gte": date_objects[0], "$lte": date_objects[1]}}
        attribute_queries = []
        attribute_name = []

        for attr, details in attribute_conditions.items():
            if "name" in details and "range" in details:
                query = {details["name"]: {"$gte": details["range"][0], "$lte": details["range"][1]}}
                attribute_queries.append(query)
                attribute_name.append(details["name"])

        query = {"$and": [date_query] + attribute_queries}
        result = list(stocks.find(query))  # 执行查询并指定返回的字段
        df = pd.DataFrame(result)
        df = df[['price', 'revenue', 'netIncome', 'researchAndDdevelopementToRevenue', 'researchAndDevelopmentExpenses',
                 'assetTurnover', 'eps', 'grahamNumber', 'grossProfit', 'grossProfitMargin', 'interestCoverage',
                 'cashFlowToDebtRatio', 'operatingIncome', 'bookValuePerShare', 'operatingCashFlowPerShare',
                 'tangibleAssetValue', 'workingCapital', 'priceToSalesRatio']]

        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        corr_matrix = df.corr()
        # print("corr_matrix:", corr_matrix)

        # create network graph
        G = nx.Graph()

        # add nodes
        for var in corr_matrix.columns:
            G.add_node(var)

        # add edges, only when corresponding correlation is greater than 0.3
        threshold = 0.3

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    G.add_edge(corr_matrix.columns[i], corr_matrix.columns[j], weight=corr_matrix.iloc[i, j])

        # attribute coordinates for each nodes
        pos = nx.spring_layout(G)

        nodes = {}
        for i, node in enumerate(G.nodes(), 1):
            nodes[f"node{i}"] = {"name": node, "x": pos[node][0], "y": pos[node][1]}

        edges = {}
        for i, edge in enumerate(G.edges(data=True), 1):
            edges[f"edge{i}"] = {"source": edge[0], "target": edge[1], "width": edge[2]['weight']}

        print("Nodes List:", nodes)
        print("Edges List:", edges)
        print("---------------------")

        return jsonify({
            "nodes": nodes,
            "edges": edges
        })

api.add_resource(StocksPrice, '/companies')
api.add_resource(StocksAttributes, '/histogram')
api.add_resource(StocksCoefficient, '/barchart')
api.add_resource(NetworkLayout, '/networkGraph/layout')