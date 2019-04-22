# coding:utf8

"""
Description:XGboost进行回归预测,调参优化
Author：伏草惟存
Prompt: code in Python3 env
"""


'''
项目说明：Kaggle数据分析的比赛上，预测糖尿病的发病
模型评价： AUC：Auc作为数值可以直观的评价分类器的好坏，值越大越好
数据集：
  Pregnancies：怀孕次数
  Glucose：葡萄糖
  BloodPressure：血压 (mm Hg)
  SkinThickness：皮层厚度 (mm)
  nsulin：胰岛素 2小时血清胰岛素（mu U / ml
  BMI：体重指数 （体重/身高）^2
  DiabetesPedigreeFunction：糖尿病谱系功能
  Age：年龄 （岁）
  Outcome：类标变量 （0或1）

numpy,matplotlib,pandas,xgboost,scikit-learn
'''


import pandas as pd # 数据科学计算工具
import xgboost as xgb
from xgboost.sklearn import XGBClassifier,XGBRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score
from xgboost import plot_importance
from matplotlib import pyplot

# 1 加载数据集
def loadData(seed = 7,test_size = 0.3):
    pima = pd.read_csv("./data/diabetes.csv")
    trains = pima.iloc[:,0:8]  # 特征值
    labels = pima.iloc[:,8]    # 标签值

    train_data, test_data, train_label, test_label = train_test_split(trains, labels, test_size=test_size, random_state=seed)
    print("训练样本数目:", len(train_label), " \n测试样本数目::", len(test_label))
    return train_data, test_data, train_label, test_label



# 2 统计信息
def xgboost_train(train_data, test_data, train_label, test_label):
    model = xgb.XGBClassifier(
                max_depth=3,        # 构建树的深度默认6
                min_child_weight=1,  # 值过高欠拟合。参数CV调整。
                learning_rate=0.1,   # 学习率
                n_estimators=500,    # 迭代次数。值太小易欠拟合
                silent=1,            # 取0时表示打印出运行时信息
                objective='binary:logistic', # 二分类的逻辑回归
                gamma=0,             # 控制是否后剪枝的参数
                max_delta_step=0,    # 限制每棵树权重改变的最大步长。
                subsample=0.8,         # 随机采样的比例。值过小会欠拟合。
                colsample_bytree=0.8,  # 控制每棵随机采样的列数的占比
                reg_alpha=0,         # L1正则化参数越大越不容易过拟合
                reg_lambda=0,        # L2 正则的惩罚系数，默认1
                scale_pos_weight=1,  # 类别高度不平衡参数设置0加快收敛。
                seed=1,              # 随机数的种子。缺省值为0
            )
    model.fit(train_data, train_label, eval_metric='auc', verbose=True,
            eval_set=[(test_data, test_label)], early_stopping_rounds=100)
    y_pre = model.predict(test_data)
    y_pro = model.predict_proba(test_data)[:, 1]
    # AUC：Roc曲线下的面积，介于0.1和1之间。Auc作为数值可以直观的评价分类器的好坏，值越大越好。
    print( "AUC Score : %f" % metrics.roc_auc_score(test_label, y_pro))
    print("Accuracy : %.4g" % metrics.accuracy_score(test_label, y_pre))

    # 重要特征
    plot_importance(model)
    pyplot.show()






# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
# 1 最佳迭代次数
def n_estimators():
    param_test = {
            'n_estimators':[5,10,20,30,400,500,700]
        }
    model = xgb.XGBClassifier(
                max_depth=3,        # 构建树的深度默认6
                min_child_weight=1,  # 值过高欠拟合。参数CV调整。
                learning_rate=0.1,   # 学习率
                # n_estimators=500,    # 迭代次数。值太小易欠拟合
                silent=1,            # 取0时表示打印出运行时信息
                objective='binary:logistic', # 二分类的逻辑回归
                gamma=0,             # 控制是否后剪枝的参数
                max_delta_step=0,    # 限制每棵树权重改变的最大步长。
                subsample=0.8,         # 随机采样的比例。值过小会欠拟合。
                colsample_bytree=0.8,  # 控制每棵随机采样的列数的占比
                reg_alpha=0,         # L1正则化参数越大越不容易过拟合
                reg_lambda=0,        # L2 正则的惩罚系数，默认1
                scale_pos_weight=1,  # 类别高度不平衡参数设置0加快收敛。
                seed=1,              # 随机数的种子。缺省值为0
            )
    gsearch = GridSearchCV(estimator = model,param_grid = param_test, scoring='f1', cv=5)
    gsearch.fit(train_data,train_label)
    print('每轮迭代运行结果:\n',gsearch.cv_results_, '\n参数的最佳取值:\n',gsearch.best_params_,'\n最佳模型得分:\n', gsearch.best_score_)




# 2 调试的参数是min_child_weight以及max_depth
def max_depthANDmin_child_weight():
    param_test2 = {
        'max_depth':[1, 2, 3, 4,5],
        'min_child_weight':[0,1, 2, 3]
    }
    model = xgb.XGBClassifier(
                # max_depth=3,        # 构建树的深度默认6
                # min_child_weight=1,  # 值过高欠拟合。参数CV调整。
                learning_rate=0.1,   # 学习率
                n_estimators=30,    # 迭代次数。值太小易欠拟合
                silent=1,            # 取0时表示打印出运行时信息
                objective='binary:logistic', # 二分类的逻辑回归
                gamma=0,             # 控制是否后剪枝的参数
                max_delta_step=0,    # 限制每棵树权重改变的最大步长。
                subsample=0.8,         # 随机采样的比例。值过小会欠拟合。
                colsample_bytree=0.8,  # 控制每棵随机采样的列数的占比
                reg_alpha=0,         # L1正则化参数越大越不容易过拟合
                reg_lambda=0,        # L2 正则的惩罚系数，默认1
                scale_pos_weight=1,  # 类别高度不平衡参数设置0加快收敛。
                seed=1,              # 随机数的种子。缺省值为0
            )
    gsearch2 = GridSearchCV(estimator = model,param_grid = param_test2, scoring='f1', cv=5)
    gsearch2.fit(train_data,train_label)
    print('每轮迭代运行结果:\n',gsearch2.cv_results_, '\n参数的最佳取值:\n',gsearch2.best_params_,'\n最佳模型得分:\n', gsearch2.best_score_)



# 3 调试参数： gamma
def gamma():
    # 在树的叶子节点上进行进一步划分所需的最小损失。越大，算法就越保守。
    param_test3 = {
        'gamma':[0.2,0.3,0.4]
    }
    model = xgb.XGBClassifier(
                max_depth=4,        # 构建树的深度默认6
                min_child_weight=2,  # 值过高欠拟合。参数CV调整。
                learning_rate=0.1,   # 学习率
                n_estimators=30,    # 迭代次数。值太小易欠拟合
                silent=1,            # 取0时表示打印出运行时信息
                objective='binary:logistic', # 二分类的逻辑回归
                # gamma=0,             # 控制是否后剪枝的参数
                max_delta_step=0,    # 限制每棵树权重改变的最大步长。
                subsample=0.8,         # 随机采样的比例。值过小会欠拟合。
                colsample_bytree=0.8,  # 控制每棵随机采样的列数的占比
                reg_alpha=0,         # L1正则化参数越大越不容易过拟合
                reg_lambda=0,        # L2 正则的惩罚系数，默认1
                scale_pos_weight=1,  # 类别高度不平衡参数设置0加快收敛。
                seed=1,              # 随机数的种子。缺省值为0
            )
    gsearch3 = GridSearchCV(estimator = model,param_grid = param_test3, scoring='f1', cv=5)
    gsearch3.fit(train_data,train_label)
    print('每轮迭代运行结果:\n',gsearch3.cv_results_, '\n参数的最佳取值:\n',gsearch3.best_params_,'\n最佳模型得分:\n', gsearch3.best_score_)


# 4 subsample以及colsample_bytree
def subsample_colsample_bytree():
    param_test4 = {
        'subsample':[0.6, 0.7, 0.8, 0.9],
        'colsample_bytree': [0.6, 0.7, 0.8, 0.9]
    }
    model = xgb.XGBClassifier(
                max_depth=4,        # 构建树的深度默认6
                min_child_weight=2,  # 值过高欠拟合。参数CV调整。
                learning_rate=0.1,   # 学习率
                n_estimators=30,    # 迭代次数。值太小易欠拟合
                silent=1,            # 取0时表示打印出运行时信息
                objective='binary:logistic', # 二分类的逻辑回归
                gamma=0.3,             # 控制是否后剪枝的参数
                max_delta_step=0,    # 限制每棵树权重改变的最大步长。
                # subsample=0.8,         # 随机采样的比例。值过小会欠拟合。
                # colsample_bytree=0.8,  # 控制每棵随机采样的列数的占比
                reg_alpha=0,         # L1正则化参数越大越不容易过拟合
                reg_lambda=0,        # L2 正则的惩罚系数，默认1
                scale_pos_weight=1,  # 类别高度不平衡参数设置0加快收敛。
                seed=1,              # 随机数的种子。缺省值为0
            )
    gsearch4 = GridSearchCV(estimator = model,param_grid = param_test4, scoring='f1', cv=5)
    gsearch4.fit(train_data,train_label)
    print('每轮迭代运行结果:\n',gsearch4.cv_results_, '\n参数的最佳取值:\n',gsearch4.best_params_,'\n最佳模型得分:\n', gsearch4.best_score_)




import pickle as pkl
# 调参后的模型
def new_xgboost_train(x_train, x_test, y_train, y_test):
    model = xgb.XGBClassifier(
                max_depth=4,        # 构建树的深度默认6
                min_child_weight=2,  # 值过高欠拟合。参数CV调整。
                learning_rate=0.1,   # 学习率
                n_estimators=30,    # 迭代次数。值太小易欠拟合
                silent=1,            # 取0时表示打印出运行时信息
                objective='binary:logistic', # 二分类的逻辑回归
                gamma=0.3,             # 控制是否后剪枝的参数
                max_delta_step=0,    # 限制每棵树权重改变的最大步长。
                subsample=0.8,         # 随机采样的比例。值过小会欠拟合。
                colsample_bytree=0.8,  # 控制每棵随机采样的列数的占比
                reg_alpha=0,         # L1正则化参数越大越不容易过拟合
                reg_lambda=0,        # L2 正则的惩罚系数，默认1
                scale_pos_weight=1,  # 类别高度不平衡参数设置0加快收敛。
                seed=1,              # 随机数的种子。缺省值为0
            )
    model.fit(train_data, train_label, eval_metric='auc', verbose=True,
            eval_set=[(test_data, test_label)], early_stopping_rounds=100)
    y_pre = model.predict(test_data)
    y_pro = model.predict_proba(test_data)[:, 1]
    # AUC：Roc曲线下的面积，介于0.1和1之间。Auc作为数值可以直观的评价分类器的好坏，值越大越好。
    print( "AUC Score : %f" % metrics.roc_auc_score(test_label, y_pro))
    print("Accuracy : %.4g" % metrics.accuracy_score(test_label, y_pre))

    pkl.dump(model, open("xgb_model.pkl", "wb"))
    best_model = pkl.load(open("xgb_model.pkl", "rb"))



if __name__ == '__main__':
    # train_data, test_data, train_label, test_label =loadData()
    # print(train_data,train_label)
    # xgboost_train(train_data,test_data,train_label,test_label)
    # AUC Score : 0.838354
    # Accuracy : 0.7749

    # n_estimators()  #  {'n_estimators': 30}
    # max_depthANDmin_child_weight() # {'max_depth': 4, 'min_child_weight': 2}
    # gamma() #   {'gamma': 0.3}
    # subsample_colsample_bytree() #{'colsample_bytree': 0.8, 'subsample': 0.8}
    # new_xgboost_train(train_data,test_data,train_label,test_label)
    # AUC Score : 0.841270
    # Accuracy : 0.7879

    train_data, test_data, train_label, test_label =loadData(1,0.3)
    new_xgboost_train(train_data,test_data,train_label,test_label)
    # AUC Score : 0.884665
    # Accuracy : 0.8117


'''
1 仅仅靠参数的调整和模型的小幅优化，想要让模型的表现有个大幅度提升是不可能的。
2 要想模型的表现有一个质的飞跃，需要依靠其他的手段，如特征工程 ，模型组合,以及堆叠等
3 与随机种子和数据集划分也有关系
'''




# estimator：所使用的分类器，不同分类器的评分标准
# https://segmentfault.com/a/1190000014040317