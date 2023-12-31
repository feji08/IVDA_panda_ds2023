from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from flask import request
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer
import networkx as nx
from copy import deepcopy
import math
from threading import Lock

# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/stocksdatabase"
pymongo = PyMongo(app)
# Get a reference to the stocks' collection.
stocks: Collection = pymongo.db.stocks
api = Api(app)
app.config["nodes"] = {}
app.config["edges"] = {}
app.config["NETWORK_GRAPH"] = nx.Graph()


class StocksPrice(Resource):
    def get(self):
        # 查询 price 在 1 到 20 之间的数据，并只返回 price 字段的列表
        query = {'$and': [{'date': {'$in': [datetime(2010, 1, 1, 0, 0), datetime(2022, 10, 1, 0, 0)]}}]}
        result = list(stocks.find(query))  # 执行查询并指定返回的字段
        # print(len(result))
        # 从结果中提取 price 字段的值组成列表
        prices = [item['date'] for item in result]

        return jsonify(prices)  # 返回包含 price 字段值的列表作为 JSON 响应


class StocksAttributes(Resource):
    def post(self):
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


def compute_coefficient(df, indicator, node_1, node_2, algorithm):
    # dimension reduction
    # PCA for display, indicator ~ node_1, node_2
    df_display = df[[indicator, node_1, node_2]].copy()
    # handling missing value(ignore on purpose) ~ get all rows without NAN
    # print(
    #     "The dataset before dropping the rows contains {} data records and {} features.".format(df_display.shape[0],
    #                                                                                             df_display.shape[
    #                                                                                                 1]))
    df_display.dropna(inplace=True)
    # print("The dataset now contains {} data records and {} features.".format(df_display.shape[0],
    #                                                                          df_display.shape[1]))
    # 1. Standardization
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df_display)
    # Convert the standardized data back to a DataFrame
    df_scaled = pd.DataFrame(x_scaled, columns=df_display.columns)
    # 2. Dimension reduction
    # Perform PCA with two components
    if algorithm == "PCA":
        pca = PCA(n_components=2)
        x_pca = pca.fit_transform(df_scaled[[node_1, node_2]])
        # Create a DataFrame with the new dimensions
        df_pca = pd.DataFrame(x_pca, columns=['PCA_Component_1', 'PCA_Component_2'])
        # 3. Correlation compute ? which methods to choose
        # Calculate correlation coefficients
        corr_1_2 = df_scaled[indicator].corr(df_scaled[node_1])
        corr_1_3 = df_scaled[indicator].corr(df_scaled[node_2])
        # Calculate correlation between the first dimension and the new dimension
        corr_1_pca = df_scaled[indicator].corr(df_pca['PCA_Component_1'])
        # Correlation values
        correlations = [corr_1_2, corr_1_3, corr_1_pca]
    else:
        # Factor Analysis
        fa = FactorAnalyzer(n_factors=2, rotation=None)
        fa.fit(df_scaled[[node_1, node_2]])

        # Get factor loadings
        loadings = fa.loadings_

        # Transform data using Factor Analysis
        x_fa = fa.transform(df_scaled[[node_1, node_2]])

        # Create DataFrame with new dimensions from Factor Analysis
        df_fa = pd.DataFrame(x_fa, columns=['Factor_Component_1', 'Factor_Component_2'])

        # Correlation compute for Factor Analysis
        # Calculate correlation coefficients
        corr_1_2 = df_scaled[indicator].corr(df_scaled[node_1])
        corr_1_3 = df_scaled[indicator].corr(df_scaled[node_2])
        # Calculate correlation between the indicator and the new factor dimensions from Factor Analysis
        corr_1_fa = df_scaled[indicator].corr(df_fa['Factor_Component_1'])

        # Correlation values
        correlations = [corr_1_2, corr_1_3, corr_1_fa]

    return correlations


class StocksCoefficient(Resource):
    def post(self):
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
        node_1 = json_data.get("nodes", [])[0]
        node_2 = json_data.get("nodes", [])[1]
        indicator = json_data.get("indicator")
        algorithm = json_data.get("algorithm")

        coefficient = compute_coefficient(df, indicator, node_1, node_2, algorithm)
        coefficient_all = compute_coefficient(pd.DataFrame(list(stocks.find())), indicator, node_1, node_2, algorithm)

        coefficients = {
            "values": [coefficient[0], coefficient[1], coefficient[2], coefficient_all[2]]
        }

        return jsonify({"coefficients": coefficients})


def distribute_points_on_circle(radius, num_points, start_angle):
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * (i / num_points + start_angle)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle) * 0.8
        points.append((x, y))
    return points


class NetworkLayout(Resource):
    def post(self):
        global app
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
        result = list(stocks.find(query))
        df = pd.DataFrame(result)
        df = df[['price', 'revenue', 'netIncome', 'researchAndDdevelopementToRevenue', 'researchAndDevelopmentExpenses',
                 'assetTurnover', 'eps', 'grahamNumber', 'grossProfit', 'grossProfitMargin', 'interestCoverage',
                 'cashFlowToDebtRatio', 'operatingIncome', 'workingCapital', 'operatingCashFlowPerShare',
                 'tangibleAssetValue', 'bookValuePerShare', 'priceToSalesRatio']]

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
        threshold = 0.5

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    G.add_edge(corr_matrix.columns[i], corr_matrix.columns[j], weight=corr_matrix.iloc[i, j])

        points_radius_0_3 = distribute_points_on_circle(0.3, 3, 1.0 / 3.0)
        points_radius_0_6 = distribute_points_on_circle(0.6, 5, 1.0 / 5.0)
        points_radius_0_9 = distribute_points_on_circle(0.9, 10, 1 / 24.0)
        all_points = points_radius_0_3 + points_radius_0_6 + points_radius_0_9

        nodes = {}
        for i, node in enumerate(G.nodes(), 1):
            point = all_points[i - 1]
            x, y = point
            nodes[f"node{i}"] = {"name": node, "x": x, "y": y}

        edges = {}
        for i, edge in enumerate(G.edges(data=True), 1):
            source_key = [key for key, value in nodes.items() if value["name"] == edge[0]][0]
            target_key = [key for key, value in nodes.items() if value["name"] == edge[1]][0]
            edges[f"edge{i}"] = {"source": source_key, "target": target_key, "width": edge[2]['weight']}

        app.config["nodes"] = deepcopy(nodes)
        app.config["edges"] = deepcopy(edges)
        app.config["NETWORK_GRAPH"] = deepcopy(G)

        # print("Nodes List:", app.config["nodes"])
        # print("Edges List:", app.config["edges"])

        return jsonify({
            "nodes": nodes,
            "edges": edges
        })


def calculate_middle_point(pos1, pos2):
    return [(pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2]


def adjust_position(pos, existing_positions, delta=0.1):
    adjusted_pos = pos[:]
    while any(all(abs(adjusted_pos[i] - p[i]) < delta for i in range(2)) for p in existing_positions):
        adjusted_pos[0] += delta
        adjusted_pos[1] += delta
    return adjusted_pos


class NetworkAddNode(Resource):
    def post(self):
        global app
        json_data = request.get_json()
        time_conditions = json_data.get("time", [])
        attribute_conditions = json_data.get("attributes", {})
        node_1 = json_data.get("nodes", [])[0]
        node_2 = json_data.get("nodes", [])[1]
        indicator = json_data.get("indicator")
        algorithm = json_data.get("algorithm")

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
        result = list(stocks.find(query))
        df = pd.DataFrame(result)
        coefficient = compute_coefficient(df, indicator, node_1, node_2, algorithm)
        # print("coefficient:", coefficient)

        nodes = app.config["nodes"]
        edges = app.config["edges"]
        G = app.config["NETWORK_GRAPH"]

        lock = Lock()
        with lock:
            # Remove node if it exists
            if any(node["name"] in ["new_pca_node","new_factor_node"] for node in nodes.values()):
                # Find node key
                node_key = [key for key, value in nodes.items() if value["name"] in ["new_pca_node","new_factor_node"]][0]
                # Find edges associated with the removed node and delete them
                edge_keys = [key for key, edge in edges.items() if node_key in (edge["source"], edge["target"])]
                for key in edge_keys:
                    del edges[key]
                del nodes[node_key]

        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        print("Original Node List:", nodes)
        # print("Original Edge List:", edges)
        # print("original number of nodes: ", num_nodes)
        # print("original number of edges: ", num_edges)

        G.add_node('new_node')
        node1_pos = next(({"x": v["x"], "y": v["y"]} for k, v in nodes.items() if v["name"] == node_1), None)
        node2_pos = next(({"x": v["x"], "y": v["y"]} for k, v in nodes.items() if v["name"] == node_2), None)

        if node1_pos is not None and node2_pos is not None:
            middle_pos = calculate_middle_point([node1_pos["x"], node1_pos["y"]], [node2_pos["x"], node2_pos["y"]])
            all_positions = [[v["x"], v["y"]] for v in nodes.values()]
            adjusted_middle_pos = adjust_position(middle_pos, all_positions)
            if algorithm=="PCA":
                new_node_name = "new_pca_node"
            else:
                new_node_name = "new_factor_node"
            new_node_key = f"node{num_nodes + 1}"
            nodes[new_node_key] = {"name": new_node_name, "x": adjusted_middle_pos[0], "y": adjusted_middle_pos[1]}
            node_1_key = [key for key, value in nodes.items() if value["name"] == node_1][0]
            node_2_key = [key for key, value in nodes.items() if value["name"] == node_2][0]
            indicator_key = [key for key, value in nodes.items() if value["name"] == indicator][0]
            edges[f"edge{num_edges + 1}"] = {"source": indicator_key, "target": node_1_key, "width": coefficient[0]}
            edges[f"edge{num_edges + 2}"] = {"source": indicator_key, "target": node_2_key, "width": coefficient[1]}
            edges[f"edge{num_edges + 3}"] = {"source": indicator_key, "target": new_node_key, "width": coefficient[2]}
            print("The new node：", nodes[new_node_key])
            print(f"Edge 1: {edges[f'edge{num_edges + 1}']}\n"
                  f"Edge 2: {edges[f'edge{num_edges + 2}']}\n"
                  f"Edge 3: {edges[f'edge{num_edges + 3}']}")
        else:
            print("'node_1' or 'node2' are not found")

        print("New Node List:", nodes)
        # print("New Edge List:", edges)

        return jsonify({
            "nodes": nodes,
            "edges": edges
        })


api.add_resource(StocksPrice, '/companies')
api.add_resource(StocksAttributes, '/histogram')
api.add_resource(StocksCoefficient, '/barchart')
api.add_resource(NetworkLayout, '/networkGraph/layout')
api.add_resource(NetworkAddNode, '/networkGraph/newNode')
