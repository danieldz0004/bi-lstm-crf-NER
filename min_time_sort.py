pre_cell_list = []
min_phagocytosis = int(input("Please input min_phagocytosis:"))
max_phagocytosis = int(input("Please input max_phagocytosis:"))
pre_num_cell = int(input("How many cells are there in the culture dish:"))
for j in range(0, pre_num_cell):
    pre_cell_list.append(int(input("Please input ability for cell No." + str(j + 1) + ":")))


count = 0
for j in range(min_phagocytosis, max_phagocytosis):
    for k in range(0, pre_num_cell):
        if (10*pre_cell_list[k] >= j >= 2*pre_cell_list[k]) or (pre_cell_list[k]/10 <= j <= pre_cell_list[k]/2):
            count = count + 1
            break

print(max_phagocytosis - min_phagocytosis - count)
