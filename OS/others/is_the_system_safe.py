
available = [1, 5, 2, 0]

current_allocation = [[0, 0, 1, 2],
                      [1, 0, 0, 1],
                      [1, 3, 0, 4],
                      [0, 6, 3, 2],
                      [0, 0, 1, 1]]

maximum_demand = [[0, 0, 1, 2],
                  [1, 5, 1, 1],
                  [2, 3, 5, 6],
                  [0, 6, 7, 2],
                  [0, 6, 5, 6]]

still_needs = []
sum = []

for i in range(len(current_allocation)):
    row = []
    for j in range(len(current_allocation[i])):
        row.append(maximum_demand[i][j] - current_allocation[i][j])
    still_needs.append(row)

for j in range(4):
    summa = 0
    for i in range(len(current_allocation)):
        summa += current_allocation[i][j] 
    sum.append(summa)

# this = []

process = {}
for i in range(len(current_allocation)):
    process[f"p{i}"] = current_allocation[i], maximum_demand[i], still_needs[i]
    
# print(sum , available)

# for i in range(4):
#     this[i] = available[i] - sum[i]
    

for key, value in process.items():
    print(key, value)
