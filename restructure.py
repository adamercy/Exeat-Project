import csv

dir = "C:\\Users\\Ada\\PycharmProjects\\finalyear\\"
files = 'data_fp_matric_doe.csv'
output_file = dir + "data_fp_matric_doe_edit.csv"
dict = {}
dict_item_count = {}

file_to_open = dir + files
with open(file_to_open) as csv_file:
    line_count = 0
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:  
        if line_count >= 1:  
            matno = row[0].strip()  
            doe = row[1].strip()  
            if doe in dict.keys():
                val = dict[doe]
                val.append(matno)
                dict[doe] = val
                dict_item_count[doe] += 1
            else:
                val = [matno]
                dict[doe] = val
                dict_item_count[doe] = 1
        line_count = line_count + 1
csv_file.close()

''' max_val = 0
for data in dict_item_count:
    if dict_item_count[data] > max_val:
        max_val = dict_item_count[data]

for i in range(0, max_val):
    str_val = 'row ' + str(i + 1)
    headers.append(str_val) '''

with open(output_file, mode='w', newline='') as norm_file:
    norm_writer = csv.writer(norm_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for data in dict:
        matlist = dict[data]
        data_list = [data]
        for item in matlist:
            data_list.append(item)
        norm_writer.writerow(data_list)
csv_file.close()
print('Done, data re-structured successfully')
