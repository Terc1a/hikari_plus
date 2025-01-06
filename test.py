list2 = ['2024-12-20', '2024-12-20', '2024-12-20', '2024-12-21', '2024-12-21']
list1 = set(list2)
matches = [{a:list2.count(a) for a in list1}]
print(matches)