import copy
import time
from config import * 

# ------ 基础函数 ------ #
# 两个集合，求补集
def complement(rangea,fullrange):
    rangeb = []
    for i in fullrange:
        if not rangea.count(i):
            rangeb.append(i)
    return rangeb

# 输入两个值域，求交集
def intersection(rangea,rangeb):
	rangec = []
	for i in rangea:
		for j in rangeb:
			if i == j:
				rangec.append(i)
	return rangec

# 九宫格转置函数，将一个数独列表，转化为对应的九宫格列表
def matrix_invert(lista):
    listb = [[] for i in range(9)]
    for i in range(9):
        for j in range(9):
            if [0,1,2].count(i) and [0,1,2].count(j):
                listb[0].append(lista[i][j])
            elif [0,1,2].count(i) and [3,4,5].count(j):
                listb[1].append(lista[i][j])
            elif [0,1,2].count(i) and [6,7,8].count(j):
                listb[2].append(lista[i][j])
            elif [3,4,5].count(i) and [0,1,2].count(j):
                listb[3].append(lista[i][j])
            elif [3,4,5].count(i) and [3,4,5].count(j):
                listb[4].append(lista[i][j])
            elif [3,4,5].count(i) and [6,7,8].count(j):
                listb[5].append(lista[i][j])
            elif [6,7,8].count(i) and [0,1,2].count(j):
                listb[6].append(lista[i][j])
            elif [6,7,8].count(i) and [3,4,5].count(j):
                listb[7].append(lista[i][j])
            else:
                listb[8].append(lista[i][j])
    return listb

# ------ 值域函数 ------ #
# 行值域函数
def rowValueRange(soduku):
    s_row_vrange = []
    for row in soduku:
        row_temp = []
        row_vrange = []
        row_Range = []
        for i in row:
            if i != '':
                row_temp.append([i])
                row_Range.append(i)
            else:
                row_temp.append(list(range(1,10)))
        for j in row_temp:
            if len(j) > 1:
                k = copy.deepcopy(j)
                k = complement(row_Range,k)
                row_vrange.append(k)
            else:
                row_vrange.append(j)
        s_row_vrange.append(row_vrange)
    return s_row_vrange

# 列值域函数
def colValueRange(soduku):
    soduku_invert = list(zip(*soduku))
    temp = rowValueRange(soduku_invert)
    s_column_vrange = list(zip(*temp))
    return s_column_vrange

# 九宫格值域函数
def matrixValueRange(soduku):
    matrix = matrix_invert(soduku)
    temp = rowValueRange(matrix)
    matrix_vrange = matrix_invert(temp)
    return matrix_vrange

# 总值域函数
def valueRange(soduku):
    rowrange = rowValueRange(soduku)
    columnrange = colValueRange(soduku)
    matrixrange = matrixValueRange(soduku)
    temp = [[] for i in range(9)]
    s_valuerange = [[] for i in range(9)]
    for i in range(9):
        for j in range(9):
            temp[i].append(intersection(rowrange[i][j],columnrange[i][j]))
    for i in range(9):
        for j in range(9):
            s_valuerange[i].append(intersection(temp[i][j],matrixrange[i][j]))
    return s_valuerange 

# ------ 值域更新函数 ------ #
# 输入一个值和某个单元格的值域，然后更新该单元格的值域（该值不会出现在本单元格）
def refreshCellValue(value,valuerange):
	for i in valuerange:
		if i == value:
			valuerange.remove(value)
	return valuerange

# coupling函数里使用的更新值域函数
def couplingRefreshValue(value,valuerange):
	for v in valuerange:
		refreshCellValue(value,v)
	return valuerange

# 输入一行每个单元格的值域组成的列表，检测是否有耦合单元格，如果有则更新值域列表；如果没有，则返回原值域列表
# 耦合单元格类似[3,9][3,9]，说明3和9必然出现在这两个单元格，其它单元格不可能出现3和9；
def coupling(valuerange):
	result = []
	for i in range(9):
		equal = []
		for j in valuerange[i:]:
			if j == valuerange[i]:
				equal.append(j)
		if len(equal) > 1:
			if len(equal) == len(equal[0]):
				result.append(equal[0])	
	if len(result):
		for k in result:
			temp = copy.deepcopy(k)# 深拷贝
			for l in k[:]:
				couplingRefreshValue(l,valuerange)
			# 处理耦合单元格，会把原本的耦合单元格值域变为空，因此需要在处理后恢复耦合单元格
			for v in valuerange:
				if len(v) == 0:
					v.extend(temp)
	return valuerange

# 通用更新值域函数；若更新值域后，值域长度为1，则递归进行一次更新值域操作；
def refreshValue(value,valuerange):
	for v in valuerange:
		for i in v:
			if i == value and len(v) > 1:
				v.remove(value)
				if len(v) == 1:
					refreshValue(v[0],valuerange)
	return valuerange

# 输入值域列表；检测是否有值域长度为1的单元格，如果有，则该单元格数值确定，更新该行值域
def checkValue(valuerange):
	coupling(valuerange)
	for v in valuerange:
		if len(v) == 1:
			refreshValue(v[0],valuerange)
	return valuerange

# 寻找一行中唯一的值，若该值仅在行值域列表中出现了一次，则其所在单元格取值为该值
def checkUnique(list):
    listb = copy.deepcopy(list)
    templist = []
    for i in listb:
        templist.extend(i)
    for i in range(len(list)):
        for j in list[i]:
            if templist.count(j) == 1:
                listb[i] = [j]
    list = listb
    return list

# 寻找每一行的唯一值，更新值域列表
def soduku_checkUnique(s_row_vrange):
    temp = []
    for list in s_row_vrange:
        temp.append(checkUnique(list))
    s_row_vrange = temp
    return s_row_vrange

# 检查值域列表每一行、每一列、每一个九宫格的值域，并寻找唯一值，更新值域列表
def soduku_checkValue(s_row_vrange):
    temp = []
    temp_b = []
    for vrange in s_row_vrange:
        checkValue(vrange)
    s_row_vrange = soduku_checkUnique(s_row_vrange)
    for i in list(zip(*s_row_vrange)):
        temp.append(list(i))
    for vrange in temp:
        checkValue(vrange)
    temp = soduku_checkUnique(temp)
    for i in list(zip(*temp)):
        temp_b.append(list(i))
    temp_c = matrix_invert(temp_b)
    for vrange in temp_c:
        checkValue(vrange)
    temp_c = soduku_checkUnique(temp_c)
    temp_d = matrix_invert(temp_c)
    return temp_d

# 循环更新值域函数，当更新前与更新后值域列表相同时，跳出循环
def cycle(s_row_vrange):
    for i in range(100):
        temp = copy.deepcopy(s_row_vrange)
        s_row_vrange = soduku_checkValue(s_row_vrange)
        if temp == s_row_vrange:
            break
    return s_row_vrange

# 检查值域列表是否合法：行检测，列检测，九宫格检测
def checkRepeat(s_value_range):
    for i in s_value_range:
        temp = []
        for j in i:
            if len(j) == 1:
                temp.append(j[0])
        len_temp = len(temp)
        if len_temp != len(list(set(temp))):
            return False
    for k in list(zip(*s_value_range)):
        temp = []
        for l in k:
            if len(l) == 1:
                temp.append(l[0])
        len_temp = len(temp)
        if len_temp != len(list(set(temp))):
            return False
    for m in matrix_invert(s_value_range):
        temp = []
        for n in m:
            if len(n) == 1:
                temp.append(n[0])
        len_temp = len(temp)
        if len_temp != len(list(set(temp))):
            return False
    return True

# 计算值域列表取值总的组合数（各单元格值域长度相乘）
def sodukuRate(s_row_vrange):
    rate = 1
    for i in s_row_vrange:
        for j in i:
            rate *= len(j)
    return rate

# ------ 主函数 ------ #
# 主函数，输入值域列表，如遇到多个取值的单元格，依次尝试值域里的每个值，通过递归的方法检测值是否正确
# 当通过多次递归，值域列表rate变为1时，检测值域列表是否合法，如果合法说明上一次取值合法；
# 当通过递归的方法确定第一个取值后，再通过递归的方法，返回最终正确答案
def trial(s_row_vrange):
    if sodukuRate(s_row_vrange) == 1:
        if checkRepeat(s_row_vrange):
            return s_row_vrange
        else:
            return False
    else:  
        for i in range(9):
            for j in range(9):
                if len(s_row_vrange[i][j]) > 1:
                    for k in s_row_vrange[i][j]:
                        test_value = copy.deepcopy(s_row_vrange)
                        test_value[i][j] = [k]
                        test_value = cycle(test_value)
                        if checkRepeat(test_value):
                            if trial(test_value):
                                return trial(test_value)
                            else:
                                continue
                        else:
                            continue
                    return False

if __name__ == '__main__':
    t1 = time.time()

    for i in soduku:
        print(i)

    s_row_vrange = soduku_checkValue(valueRange(soduku))
    cycle(s_row_vrange)

    for i in trial(s_row_vrange):
        print(i)

    print("代码执行完毕，用时{}秒".format(round(time.time() - t1,2)))
