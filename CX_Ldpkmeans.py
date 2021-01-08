import numpy as np
from sklearn.datasets import make_blobs
from collections import  Counter
from sklearn import preprocessing
from sklearn import metrics
import random
def bernoulli(probability):
    arr_ber = np.random.rand(1, 1)
    if arr_ber<=probability:
        return 1
    else:
        return 0


def euclidean_distance(a,b):
    sum=0
    for x in range(a.shape[0]):

        sum+=(a[x]-b[x])**2

    return sum


def perturb(list,privacy_cost):

    unperturb_list=list.reshape(-1,1)
    probility = np.exp(privacy_cost) / (np.exp(privacy_cost) + 1)
    print(probility)
    perturb_list = []
    for x in unperturb_list:
        if bernoulli(probility):
            perturb_list.append(x)
        else:
            perturb_list.append(1-x)
    return np.array(perturb_list).reshape(list.shape)


def aggregeate(unaggregeate_list,privacy_cost):
    probility = 2 / (np.exp(privacy_cost) + 1)
    #print("******************f=",probility)
    list=np.sum(unaggregeate_list,axis=0)
    num=unaggregeate_list.shape[0]
    aggregeate_list=[]
    for x in list:
        a=(x-(0.5*probility*num))/(1-probility)
        aggregeate_list.append(a)
    aggregeate_list=np.array(aggregeate_list)/unaggregeate_list.shape[0]

    return aggregeate_list


# def group(true_list,centroids_list):
#
#     swap_k_list=[]
#     for x in range(centroids_list.shape[0]):
#         swap_k_list.append([])
#
#     for x in true_list:
#         upper=1000
#         k=0
#         for i,xx in enumerate(centroids_list):
#             distance=euclidean_distance(x,xx)
#             if distance< upper:
#                 upper = distance
#                 k = i
#         swap_k_list[k].append(x)
#
#     return swap_k_list

def group1(true_list,centroids_list,pertutb_list):

    swap_k_list=[]
    for x in true_list:
        upper=1000
        k=0
        for i,xx in enumerate(centroids_list):
            distance=euclidean_distance(x,xx)
            if distance< upper:
                upper = distance
                k = i
        swap_k_list.append(k)
    print(Counter(swap_k_list))


    group_list = []
    for x in range(centroids_list.shape[0]):
        group_list.append([])
    for x in range(len(swap_k_list)):
        group_list[swap_k_list[x]].append(pertutb_list[x])


    return group_list,np.array(swap_k_list)

def compute_norm(norm,T):
    result=0
    for x in range(T):
        result=result+norm[x]*(0.5**(x+1))

    return result

def measurescore(test_data, y_true,y_pred):
    print(y_pred.shape)
    y_pred=y_pred.reshape(-1,)
    # 无label_true:
    # 1.CH分数 Calinski Harabasz Score, 取值越大越好
    score_ch=metrics.calinski_harabasz_score(test_data, y_pred)

    # 2.轮廓系数（Silhouette Coefficient, 取值-1, 1之间 取值越大越好
   # score_sc = metrics.silhouette_score(test_data, y_pred)
    # 戴维森堡丁指数(DBI)——davies_bouldin_score, 取值越小越好
    score_db=metrics.davies_bouldin_score(test_data, y_pred)


    # label_true:
    # 1.Mutual Information based scores 互信息 [0,1] 取值越大越好
    score_mi=metrics.adjusted_mutual_info_score(y_true,y_pred)
    # 调整兰德系数 （Adjusted Rand index） [-1,1]取值越大越好
    score_adi= metrics.adjusted_rand_score(y_true, y_pred)
    # v_measure_score homogeneity+completeness [0,1] 取值越大越好
    score_vm=metrics.v_measure_score(y_true,y_pred)

    result_score=[score_ch,score_db,score_mi,score_adi,score_vm]

    return result_score

T=10
Epsilon=1
K=3
Time=300
m=2
data_set3="D:\\data_gen\\dataset1\\small_small_perturb_20_test1_norm_01.csv"
method1_data3 = np.loadtxt(open(data_set3,"rb"),delimiter=",",skiprows=0,dtype=int)

data_set2="D:\\data_gen\\dataset1\\small_small_test1_norm.csv"
method1_data2 = np.loadtxt(open(data_set2,"rb"),delimiter=",",skiprows=0)

data_set1="D:\\data_gen\\dataset1\\small_lable.csv"
method1_data1 = np.loadtxt(open(data_set1,"rb"),delimiter=",",skiprows=0,dtype=int)

print(method1_data3.shape,np.sum(method1_data3,axis=0))
print(method1_data2.shape,method1_data1.shape)

# centroids0=[[0.24921172, 0.77609598],
#  [0.54118091, 0.21936071],
#  [0.83313437 ,0.77611087]]
# centroids=[[0.00294825, 0.95033923],
#  [0.57762487 ,0.87937011],
#  [0.54204068, 0.99572044]]
# cen=np.array(centroids)

centroids=[[0.40918427, 0.37177903],
 [0.76578402, 0.90017164],
 [0.17774417 ,0.25584798]]
cen=np.array(centroids)


#cen=np.random.random((K,2))
print(cen)

flag=0
for i in range(Time):

    group_list,swap_k_list=group1(method1_data2,cen,method1_data3)
    score=measurescore(method1_data2,method1_data1 ,swap_k_list)
    print(score)

    if flag==score[0]:
        break

    flag=score[0]
    # 计算new 中心点
    new_cen=[]
    for x in group_list:
        if not x:
            new_cen.append(np.random.random(2))
            print("warning__1")
        else:
            x = np.array(x)
            # print(x.shape)

            agg_list = aggregeate(x, Epsilon).reshape(-1, T)
            # print(agg_list)
            temp = []
            for xx in agg_list:
                xx_result = compute_norm(xx, T)
                if xx_result>1 or xx_result<0:
                    temp.append(random.random())
                    print("warning__2 is :",xx_result)

                else:
                    temp.append(xx_result)

                # print(xx,xx.shape)
            new_cen.append(temp)

    cen = np.array(new_cen)

    #print(new_cen)
















# 模拟数据
# list1=np.ones((10000, 1))
# list=np.append(list1,np.zeros((90000,1))).reshape(-1,1)
# np.random.shuffle(list)
# list2=np.ones((80000, 1))
# l1=np.append(list2,np.zeros((20000,1))).reshape(-1,1)
# np.random.shuffle(l1)
# list3=np.ones((40000, 1))
# l2=np.append(list3,np.zeros((60000,1))).reshape(-1,1)
# np.random.shuffle(l2)
# test_list=np.hstack((list,l1,l2))
# print(np.sum(test_list,axis=0),test_list.shape)
# # 初始聚类中心
# cen=np.random.random((K,test_list.shape[1]))
# #扰动
# perturb_list=perturb(test_list,Epsilon)
# print(np.sum(perturb_list,axis=0),perturb_list.shape)
#
# #聚合
# result=aggregeate(perturb_list,Epsilon)
# print(result)

#2

# centers=np.array([[-.2, .7], [-.2, -.2], [.2, .2], [.7,.7]])
# centers=np.random.random((4,2))
# print(centers)
#
# method3_data, y_true = make_blobs(n_samples=5000000, n_features=2, centers=[[.5, -.5], [-.5, .5], [.0, -.5]],
#                   cluster_std=[0.06, 0.08, 0.08], random_state=9)
#
# method3_data_minmax= preprocessing.MinMaxScaler().fit_transform(method3_data)
#
# #print(method3_data_minmax.shape,method3_data_minmax[:],method3_data)
#
# perturb_list2=perturb(method3_data,Epsilon)
#
# group_result1=group1(method3_data,centers,perturb_list2)
# for x in group_result1:
#     print(len(x))








# 数据扰动

# data_set3="D:\\data_gen\\dataset1\\small_small_test1_norm_01.csv"
# method1_data3 = np.loadtxt(open(data_set3,"rb"),delimiter=",",skiprows=0,dtype=int)
#
# print(method1_data3.shape,np.sum(method1_data3,axis=0))
#
# perturb_method1_data3=perturb(method1_data3,Epsilon)
#
# print(perturb_method1_data3.shape,np.sum(perturb_method1_data3,axis=0))
#
# np.savetxt('D:\\data_gen\\dataset1\\small_small_perturb_20_test1_norm_01.csv',perturb_method1_data3,delimiter=',')