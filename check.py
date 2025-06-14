import numpy as np
import math
import os
import sys
import matplotlib.pyplot as plt
#plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
orbital_dict = {
    0: 'S',
    1: 'P',
    2: 'D',
    3: 'F',
    4: 'G',
    5: 'H',
    6: 'I'
}

class orb:
	def __init__(self, l, n, values):
		self.l = l  # 角量子数
		self.n = n  # 主量子数
		self.values = values  # 基函数值

	def __repr__(self):
		return f"orb(l={self.l}, n={self.n}, values={self.values})"

Lmax: int = None
nmesh: int = None
dr: float = None
element = 'el'
angular_list: list[int] = []
orb2angular_list: list[int] = []
orb_list = np.array([], dtype=orb)
start_index = [] # 记录基函数的起始行索引

def main():
	# 检查是否有足够的命令行参数
	if len(sys.argv) < 2:
		print("Usage: python check.py <inputfile>")
		sys.exit(1)
	inputfile = sys.argv[1]  # 从命令行参数获取参数

	parse_file(inputfile)
	plot_orb(orb_list, angular_list, element)

def parse_file(inputfile):
	global Lmax, nmesh, dr, element
	global angular_list, orb2angular_list, orb_list, start_index
	with open(inputfile, 'r') as file:
		lines = file.readlines()	
	nlines = 0 # 一个基函数的行数
	for i, line in enumerate(lines):
		#print(line)
		if element == 'el' and 'Element' in line:
			element = line.split()[-1]
			print(element)
			continue
		if (Lmax is None) and ('Lmax' in line):
			Lmax = int(line.split()[-1])
			for j in range(Lmax + 1):
				angular_list.append(int(lines[i+1+j].split()[-1]))
			print("angular_list:", angular_list)
			orb2angular_list = [i for i, count in enumerate(angular_list) for _ in range(count)] #两层列表推导式
			continue
		if (nmesh is None) and ('Mesh' in line):
			nmesh = int(float(line.split()[1]))
			dr = float(lines[i+1].split()[1])
			nlines = math.ceil(nmesh / 4)
			continue
		# 找到包含 'Type' 的行的索引
		if 'Type' in line:
			start_index.append(i)
			continue
	print(sum(angular_list), len(start_index))
	assert(sum(angular_list) == len(start_index))

	for start in start_index:
		l, n = map(int, lines[start + 1].split()[1:3])
		values = []
		for line in lines[start + 2:start + 2 + nlines]:
			values.extend(map(float, line.split()))
		# 将 values 转换为 np.array
		values = np.array(values)
		# print(values)
		assert(values.size == nmesh)
		orb_tmp = orb(l, n, values)
		orb_list = np.append(orb_list, orb_tmp)

def plot_orb(orb_list, angular_list, element):
	global nmesh, dr
	x=np.arange(0, nmesh)*dr
	fig, axs = plt.subplots(1, len(angular_list), figsize=(len(angular_list) * 3, 4))
	plt.subplots_adjust(left=0.07, right=0.95, bottom=None, top=None, wspace=0, hspace=0)  # 调整子图之间的宽度和高度间距
	for i, orb in enumerate(orb_list):
		l = orb.l
		assert(l == orb2angular_list[i])
		values = orb.values
		norm = np.sum(x**2 * values**2 * dr) # 检查是否归一化
		print("check norm: l=", l,' n=', orb.n,' norm=', norm)
		axs[l].plot(x, values, label= r"$\zeta$ ="+ str(orb.n))
		if orb.n == angular_list[l]-1:
			axs[l].set_title(orbital_dict[l]+'type')
			axs[l].set_xlabel('r (a.u.)')
			# axs[l].set_ylabel('Orbital Value')
			axs[l].legend()

	fig.suptitle('Radial part of ' + element + ' orbital')

	combined_str = "".join([f"{angular_list[i]}{orbital_dict[i].lower()}" for i in range(len(angular_list))])

	plt.savefig(element +'_'+ combined_str + '.png', dpi=300)


if __name__ == "__main__":
	main()