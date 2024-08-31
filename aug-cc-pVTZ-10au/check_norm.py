import numpy as np
# 打开文件并读取所有行
with open('H_gga_8au_100Ry_3s2p.orb', 'r') as file:
	lines = file.readlines()

# 找到包含 'Type' 的行的索引
start_index = None
end_index = None
for i, line in enumerate(lines):
	if 'Type' in line:
		if start_index is None:
			start_index = i
		else:
			end_index = i
			break

# 提取 start_index 和 end_index 之间的数值
values = []
n=3
if end_index is not None:
	for line in lines[start_index + 2+203*n:end_index+203*n]:
		values.extend(map(float, line.split()))
else:
	for line in lines[start_index + 2+203*n:]:
		values.extend(map(float, line.split()))
# 将 values 转换为 np.array
values = np.array(values)
# 打印结果以验证
# print(values)
x=np.arange(0, 8.01, 0.01)
norm = np.sum(x**2 * values**2 * 0.01)
print(norm)