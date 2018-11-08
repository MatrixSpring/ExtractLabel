from py2neo import Graph, Node, Relationship

test_graph = Graph(
    "http://localhost:7474",
    username="123456",
    password="123456"
)

# 节点的建立
test_node_1 = Node("Person", name="test_node_1")  # 上述链接中有点问题，这里改正过来了
test_node_2 = Node("Person", name="test_node_2")  # 同上
test_graph.create(test_node_1)
test_graph.create(test_node_2)

# 节点间关系的建立
node_1_call_node_2 = Relationship(test_node_1, 'CALL', test_node_2)
node_1_call_node_2['count'] = 1
node_2_call_node_1 = Relationship(test_node_2, 'CALL', test_node_1)
node_2_call_node_1['count'] = 2
test_graph.create(node_1_call_node_2)
test_graph.create(node_2_call_node_1)

# 节点/关系的属性赋值以及属性值的更新
node_1_call_node_2['count'] += 1
test_graph.push(node_1_call_node_2)

# 通过属性值来查找节点和关系（find,find_one）
find_code_1 = test_graph.find_one(
    label="Person",
    property_key="name",
    property_value="test_node_1"
)

find_code_3 = test_graph.find_one(
    label="Person",
    property_key="name",
    property_value="test_node_2"
)

print(find_code_1['name'])

# 通过节点/关系查找相关联的节点/关系
find_relationship = test_graph.match_one(start_node=find_code_1, end_node=find_code_3, bidirectional=False)
print(find_relationship)

# match和match_one的参数包括start_node,Relationship，end_node中的至少一个。

match_relation = test_graph.match(start_node=find_code_1, bidirectional=True)
for i in match_relation:
    print(i)
    i['count'] += 1
    test_graph.push(i)
