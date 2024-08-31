import numpy as np
import os
import sys
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
# 检查是否有足够的命令行参数
if len(sys.argv) < 4:
    print("Usage: python aims2abacus_gaussian.py <inputfile> <outputfile> <rcut>")
    sys.exit(1)
inputfile = sys.argv[1]  # 从命令行参数获取参数
outputfile = sys.argv[2]
rcut = float(sys.argv[3])
# 检查文件是否存在，如果存在则删除
if os.path.exists(outputfile+'.orb'):
    os.remove(outputfile+'.orb')

dr = 0.01
nmesh = int(rcut/dr + 1)
element = 'el'
x_values = np.arange(0, nmesh)*dr # Wrong if np.arange(0,16.01,0.01).But right if np.arange(0,1601)*0.01
basis_content = 'Mesh                        '+str(nmesh)+'\ndr                          '+str(dr)+'\n'
head_content = '---------------------------------------------------------------------------\n'

def f(n,x,a,c,l):
    y = 0
    for i in range(0,n):
        y += x**l * c[i] * np.exp(-a[i] * x**2)
    # print(y)
    norm = np.sum(x**2 * y**2 * dr)
    print("before norm:", norm)
    return y/np.sqrt(norm)

def add_basis(lno,lcoe):
    global basis_content
    basis_content +='                Type                   L                   N\n'
    basis_content +='                   0                   '+str(lcoe)+'                   '+str(lno)+'\n'
    for j, z in enumerate(y_values, 1):
        # 写入值，每4个数换行
        basis_content +=f'   {z:.14e}' #python的格式化字符串
        if j % 4 == 0:
            basis_content +='\n'
    # 写入空行
    basis_content +='\n'

fig, axs = plt.subplots(1, 2, figsize=(7,4))
plt.subplots_adjust(left=0.07,right=0.95,bottom=None, top=None, wspace=0, hspace=0) # 调整子图之间的宽度和高度间距
axs[0].set_xlim(0, 4)
axs[1].set_ylim(-0.5, 0.5)
l_no = -1 # 计l层基函数的编号
l_coe = -1 # 计当前l量子数
l_num = [] # 记录l层基函数的数量
with open(inputfile, 'r') as file:
    for line in file:
        if ('species' in line and 'Element' not in head_content):
            parts = line.split()
            element = parts[1]
            print("=============\nelement:",element)
            head_content +='Element                     '+element+'\nEnergy Cutoff(Ry)           100\nRadius Cutoff(a.u.)         '+str(rcut)+'\n'
            fig.suptitle('Radial part of '+element+' orbital')
        if 'gaussian' in line:
            a_coe = []
            c_coe = []
            num_pgf = 0                         # 记录PGF的数量
            parts = line.split()
            if (l_coe != int(parts[1])):    # 判断是否是新的l量子数
                # print(l_coe, "!=", int(parts[1]))
                l_no = 0                    # 重置l层基函数的编号
                l_num.append(1)             # 在记录l层基函数的数量的数组中添加一个元素
            elif (l_coe == int(parts[1])):  # 如果是同一个l量子数
                # print(l_coe, "==", int(parts[1]))
                l_no = l_no + 1
                l_num[-1] = l_num[-1] + 1
            l_coe=int(parts[1])
            num_pgf=int(parts[2])
            if num_pgf !=1:                     # 跳过包含'gaussian 0 !1'的行，读取CGF
                for i in range(0,num_pgf):
                    line = file.readline()
                    parts = line.split()
                    a_coe.append(float(parts[0]))
                    c_coe.append(float(parts[1]))
            elif num_pgf == 1:                  # 读取PGF
                c_coe.append(1)
                a_coe.append(float(parts[3]))
            print("a:", [f"{a:.12e}" for a in a_coe], "c:", [f"{c:.12e}" for c in c_coe])
            y_values = f(num_pgf,x_values,a_coe,c_coe,l_coe)
            add_basis(l_no,l_coe)
            axs[0].plot(x_values, y_values)
            axs[1].plot(x_values, y_values)
            norm = np.sum(x_values**2 * y_values**2 * dr)
            print("after_norm:",norm)
            print(x_values.shape, y_values.shape)

head_content +='Lmax                        '+str(l_coe)+'\n'
orbital_dict = {
    0: 'S',
    1: 'P',
    2: 'D',
    3: 'F',
    4: 'G',
    5: 'H',
    6: 'I'
}
for i in range(0,l_coe+1):
    head_content +='Number of '+orbital_dict[i]+'orbital-->       '+str(l_num[i])+'\n'
head_content +='---------------------------------------------------------------------------\n'
head_content +='SUMMARY  END\n\n'

with open(outputfile+'.orb', 'w') as file:
    file.write(head_content)
    file.write(basis_content)

plt.savefig(outputfile+'.png', dpi=300)