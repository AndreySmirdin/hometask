# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    ans = []
    ans.append(lst[0])
    last = lst[0]
    for i in lst:
        if last != i:
            ans.append(i)
        last = i;
    return ans

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    ans = []
    a = 0
    b = 0
    while a < len(lst1) or b < len(lst2):
        if a != len(lst1) and (b == len(lst2) or lst1[a] < lst2[b]):
            ans.append(lst1[a])
            a += 1
        else:
            ans.append(lst2[b])
            b += 1       
    return ans


