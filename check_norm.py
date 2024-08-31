import numpy as np
import math

with open('aug-cc-pVTZ-14au/01H_augccpVTZ_14au.orb', 'r') as file:
	lines = file.readlines()

# 找到包含 'Type' 的行的索引
start_index = []
nmesh = None
dr = None
for i, line in enumerate(lines):
	if nmesh is None:
		if 'Mesh' in line:
			nmesh = int(line.split()[1])
			dr = float(lines[i+1].split()[1])
			nlines = math.ceil(nmesh / 4)
	if 'Type' in line:
		start_index.append(i)
print(start_index)

for start in start_index:
	values = []
	for line in lines[start + 2:start + 2 + nlines]:
		values.extend(map(float, line.split()))
	# 将 values 转换为 np.array
	values = np.array(values)
	# 打印结果以验证
	# print(values)
	x=np.arange(0, nmesh)*dr
	norm = np.sum(x**2 * values**2 * dr)
	print(norm)