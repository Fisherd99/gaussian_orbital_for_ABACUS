import numpy as np
import os
import sys
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
# 检查是否有足够的命令行参数
if len(sys.argv) < 4:
    print("Usage: python aims2abacus_gaussian.py <inputfile> <outputfile> <rcut> [basis_label]")
    sys.exit(1)
inputfile = sys.argv[1]  # 从命令行参数获取参数
outputfile = sys.argv[2]
rcut = float(sys.argv[3])
basis_label = sys.argv[4] if len(sys.argv) > 4 else "MOLOPT"
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
l_no = -1 # 计当前CGF系列中l层基函数的编号
l_coe = -1 # 计当前l量子数
l_num_all = [0,0,0,0,0,0,0] # 记录l层基函数的数量,暂时支持记录s,p,d,f,g,h,i
l_max_all = -1              # 记录所有CGF系列中的最大l量子数
with open(inputfile, 'r') as file:
    for line in file:
        if ('#' not in line and basis_label in line and 'Element' not in head_content):
            parts = line.split()
            element = parts[0]
            print("=============\nelement:",element)
            head_content +='Element                     '+element+'\nEnergy Cutoff(Ry)           100\nRadius Cutoff(a.u.)         '+str(rcut)+'\n'
            fig.suptitle('Radial part of '+element+' orbital')

            num_cgf_series = int(file.readline())   # 读取CGF系列的数量
            cgf_i = 0                           # 记录CGF系列的编号
            while( cgf_i < num_cgf_series):
                line = file.readline()
                parts = line.split()
                l_min = int(parts[1])
                l_max = int(parts[2])           # 读取CGF的l量子数范围
                if l_max > 6:
                    raise ValueError("Error: l_max不能大于6")
                num_pgf = int(parts[3])
                l_num = list(map(int,parts[4:(5+l_max-l_min)])) # l_num = [num_lmin,...,num_lmax]
                num_cgf = sum(l_num)                    # 记录该系列中CGF的数量
                lines = [file.readline() for _ in range(num_pgf)]
                ac = np.array([list(map(float, line.split())) for line in lines])# 读取PGF的系数为二维数组
                if ac.shape != (num_pgf, num_cgf+1):
                    raise ValueError("Error: 读取的数据形状不符合预期")
                #l_coes = [[l+l_min]*l_num[l] for l in range(0,l_max-l_min+1)]  # 记录每个CGF的l量子数[[lmin,lmin...],...,[lmax,lmax...]]
                a_coe = ac[:,0]
                for l_coe in range(l_min, l_max+1):
                    for l_no in range(l_num[l_coe-l_min]):
                        print(sum(l_num[0:l_coe-l_min])+l_no+1)
                        c_coe = ac[:,sum(l_num[0:l_coe-l_min])+l_no+1]
                        print("a:", [f"{a:.12e}" for a in a_coe], "c:", [f"{c:.12e}" for c in c_coe])
                        y_values = f(num_pgf,x_values,a_coe,c_coe,l_coe)
                        add_basis(l_num_all[l_coe],l_coe)
                        axs[0].plot(x_values, y_values)
                        axs[1].plot(x_values, y_values)
                        norm = np.sum(x_values**2 * y_values**2 * dr)
                        print("after_norm:",norm)
                        print(x_values.shape, y_values.shape)
                        l_num_all[l_coe] += 1
                cgf_i += 1
                l_max_all = max(l_max,l_max_all)    # 记录所有CGF系列中的最大l量子数
            break

head_content +='Lmax                        '+str(l_max_all)+'\n'
orbital_dict = {
    0: 'S',
    1: 'P',
    2: 'D',
    3: 'F',
    4: 'G',
    5: 'H',
    6: 'I'
}
for i in range(0,l_max_all+1):
    head_content +='Number of '+orbital_dict[i]+'orbital-->       '+str(l_num_all[i])+'\n'
head_content +='---------------------------------------------------------------------------\n'
head_content +='SUMMARY  END\n\n'

with open(outputfile+'.orb', 'w') as file:
    file.write(head_content)
    file.write(basis_content)

plt.savefig(outputfile+'.png', dpi=300)