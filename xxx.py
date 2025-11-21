

list = [2,3,5,6,9,20,13,15,16,20]
target = 28
len = len(list)
print(len)
print("umair")

for j in range (len):
    for k in range (len + 1,len):
         sum = list[j] + list[k]
         print(sum)
         if sum == target:
            print(j,k)


