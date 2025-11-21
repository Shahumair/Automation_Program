

class Solution(object):
    def twoSum(self, nums, target):
        result = []  # Step 1: Empty list to store index pairs
        z = len(nums)
        for i in range(z):
            for j in range(i + 1, z):
                pair_sum = nums[i] + nums[j]
                if pair_sum == target:
                    result.append([i, j])  # Step 2: Append valid pair
        return resultmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
   


sol = Solution()                       # Create an object of Solution class
result = sol.twoSum([1, 4, 5, 7, 8], 12)  # Call the function with a list and target
print("Result:", result)              # Print the output
