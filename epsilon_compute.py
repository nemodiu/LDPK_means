import math
import matplotlib.pyplot as plt # 导入matplotlib包的子模块pyplot，并将其重命名为plt
import numpy as np # 导入numpy，并将其重命名为np

def fun_trans_c(epsilon,m,n,d):
    #print(type(epsilon),epsilon)
    a=math.exp(epsilon/(2*(m+1)))+1
    a1=14*math.log(4*(m+1)/d)
    #a=((n-1)*)**0.5
    a2=a*a1/(n-1)
    #a3=math.sqrt(a2)*(2*(m+1))
    a3 = math.sqrt(a2)
    print(a3)
    b=27*a/(n-1)
    return a3
    #print(b)


def fun_trans_l(epsilon_l,m,n,d):
    a=(epsilon_l/(2*m+2))**2
    a1 = 14 * math.log(4 * (m + 1) / d)
    a2=a/a1*(n-1)-1
    print(a,a1,a2)
    a3=math.log(a2)*(2*(m+1))
    print(a3)



# 每位所满足的隐私预算（本地）
epsilon_l = 1
epsilon_c=2.1
# 特征数
m=4
# 数据总量
n=10000
#print(math.sqrt(4))
fun_trans_c(epsilon_l,m,n,0.01)

fun_trans_l(epsilon_c,m,n,0.01)

# 画图
x = np.linspace(1, 1000 , 100) # 生成-5到5之间的51个点的一维元组
#print(x)
y=[]
for i in x:
    y.append(fun_trans_c(i,m,n,0.01))

plt.plot(x, y)  # 画图
plt.show()
#plt.savefig(r"D:\u_career\i_coder\i_python_course_1026\figure.jpg") #
