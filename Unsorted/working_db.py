f = open("process\\unique_artists_2.txt", 'r', encoding="UTF-8")
sim = open("process\\similarity.csv", 'r', encoding="UTF-8")
d = {}
cnt = 0
for line in f:
    line = line.split("<SEP>")
    d[line[0]] = line[len(line) - 1].replace("\n", "")
    cnt+=1
print("Total count of artists", cnt)
cnt_rules = 0
new_rules = open("new_data\\new_associative_rules_2.txt", 'a', encoding="UTF-8")
for line in sim:
    line = line.split(",")
    # print(line)
    temp_target = d[line[0]]
    temp_var = line[1].replace("\n", "")
    temp_similar = d[temp_var]
    temp_str_to_file = temp_target + "," + temp_similar + "\n"
    new_rules.write(temp_str_to_file)
    cnt_rules += 1
print("Total count of rules", cnt_rules)

# test = [["AR003FB1187B994355", "AR009211187B989185"]]
# test_done = []
# for el in test:
#     temp  = []
#     temp.append(d[el[0]])
#     temp.append(d[el[1]])
#     test_done.append(temp)
#
# print(test_done)