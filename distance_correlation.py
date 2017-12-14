# coding=utf-8
# 20160510
# __author__ = 'xhcao'
import numpy as np
import scipy.spatial as sp

#    A=self.method.distance_correction_for_one_matrix(X, dimension)\
 #       B=self.method.distance_correction_for_one_matrix(Y, dimension)\
  #      corr_matrix[i,j]=self.method.distance_correlation(A,B) "


def distance_correction_for_one_matrix(x, dimension):
    # X是一个样本,ndarray类型，矩阵的每列为样本的一个特征属性
    # akl
    n = x.shape[0]
    akl = sp.distance.cdist(x, x, 'minkowski', p = dimension) #norm - d minkowski distance

    #ak*
    ak_ = np.zeros(n)
    for i in range(0,n):
        ak_[i] = np.sum(akl[i,:])/n

    #a*l
    a_l = np.zeros(n)
    for i in range(0,n):
        a_l[i] = np.sum(akl[:,i])/n

    #a**
    a__ = np.mean(akl)

    res = akl - (np.ones((n,n))*ak_).T
    res = res - np.ones((n,n))*a_l
    res = res + np.ones((n,n))*a__
    return res

def distance_correlation(A,B):
    #计算两个样本之间的相关系数矩阵
    A_B = np.mean(A*B)
    A_A = np.mean(A*A)
    B_B = np.mean(B*B)

    if A_A*B_B>0:
        return A_B/np.sqrt(A_A*B_B)
    else:
        return 0
