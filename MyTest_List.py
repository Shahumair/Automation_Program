

class solution():
    def twosum(self,nums,target):
        result = []
        z= len(nums)
        for i in range(z):
            for j in range(i+1,z):
                two_sum = nums[i] + nums[j]
                if two_sum == target:
                    result.append([i,j])

        return result

sol = solution()                       # Create an object of Solution class
result = sol.twosum([1, 4, 5, 7, 8], 12)  # Call the function with a list and target
print("Result:", result)      



        