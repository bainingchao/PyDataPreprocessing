import xgboost as xgb
# 读取数据
dtrain = xgb.DMatrix(r'data/agaricus.txt.train')
dtest = xgb.DMatrix(r'data/agaricus.txt.test')
# 通过 map 指定参数
param = {
            'max_depth':2,
            'eta':1,
            'silent':1,
            'objective':'binary:logistic'
        }
num_round = 10
bst = xgb.train(param, dtrain, num_round)
# 预测
preds = bst.predict(dtest)
# print('预测结果:\n',[round(pred) for pred in preds])

# 验证数据集
watch_list = [(dtest, 'eval'), (dtrain, 'train')]
# 模型训练
bst = xgb.train(param, dtrain, num_round,watch_list)