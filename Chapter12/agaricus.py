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




XGBoost概述（XGBoost 应用场景、XGBoost优点）
XGBoost使用案例：预测毒蘑菇（使用）
XGBoost调参
XGBoost调参案例：预测糖尿病患者

文本分类概述（发展背景、文本分类定义、常见文本分类方法、分类应用场景、分类原理）

新闻数据预处理全过程

XGBoost分类器
分类器模型评估
新闻文本分类应用