

list = [2,3,5,6,9,8,20,13,15,16,20]
target = 28
even_list =[]
odd_list =[]
result_pair = []

for i in list:
    if i  % 2 == 0:
     even_list.append(i)
    else:
     odd_list.append(i)

print(even_list)
print(odd_list)

len = len(list)
print(len)
print("umair")

for j in range (len):
    for k in range (j + 1,len):
         sum = list[j] + list[k]
         if sum == target:
            result_pair.append([j,k])
print(result_pair)




