import PySimpleGUI as sg
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import csv, os

working_directory = os.getcwd()
global isThereData
global line_count
global df
global url
isThereData = False
file_browser = sg.FileBrowse(initial_folder=working_directory, file_types=[("CSV files", "*.csv")],
                             button_text='Browse Data Source')
sg.theme('GreenTan')

layout = [
    [sg.Text("Minimum Support Count"), sg.InputText(key="min_sup", size=(5, 1))],
    [file_browser, sg.InputText(key="file_url")],
    [sg.Text("Confidence Threshold"), sg.InputText(key='conf', size=(5, 1)), sg.Text("Lift Threshold"),
     sg.InputText(key='lift', size=(5, 1))],
    [sg.Radio("Filter by Confidence", "RADIO", key='rad_conf', default=True),
     sg.Radio("Filter by Lift", "RADIO", key='rad_lift')],
    [sg.Button(button_text='Load Data', key='load'), sg.Button(button_text='Generate Rules', key='gen_rules'),
     sg.Exit()]
]

window = sg.Window("Exeat Data Analysis Project", layout, size=(400, 200))


def read_file():
    global isThereData
    global line_count
    global df
    global url
    dataset = []
    try:
        with open(url) as csv_file:
            line_count = 0
            counter = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:  
                i = 0
                row_list = [row[i]]
                counter = counter + 1
                i = i + 1
                row_length = len(row)
                while i < row_length and row[i] != '':
                    row_list.append(row[i])
                    i = i + 1
                    counter = counter + 1
                dataset.append(row_list)
                line_count += 1

        '''print('Printing dataset')
        print(dataset)'''
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        isThereData = True
        sg.popup('Success', 'File loaded successfully')
    except:
        sg.popup('File Error', 'Error in loading file into the program')
def gen_rules(min_sup):
    if int(min_sup) < 1:
        sg.popup('Incorrect value', 'Minimum support value entered is too low')
    elif isThereData:
        count = min_sup
        support_threshold = float(count) / float(line_count)
        frequent_itemsets = fpgrowth(df, min_support=support_threshold, use_colnames=True)
        print('Value of support threshold =', support_threshold)
        print('Printing FREQUENT ITEMSETS...')
        print(frequent_itemsets)
        if frequent_itemsets.empty:  
            print('No frequent itemset, the support-count threshold is probably too high. Program exiting...')
            exit(1)
        from mlxtend.frequent_patterns import association_rules
        if values['conf'].strip() == '' or values['lift'].strip() == '':
            sg.popup('Error', 'You have to supply threshold values between 0.1 and 1.0 for both confidence and lift')
            return
        con_threshold = float(values['conf']) 
        lift_threshold = float(values['lift']) 
        if con_threshold < 0.1 or con_threshold > 1.0 or lift_threshold < 0.1 or lift_threshold > 1.0:
            sg.popup('Incorrect value', 'The values for confidence and lift thresholds must be between 0.1 and 1.0')
            return
        rules_by_conf = association_rules(frequent_itemsets, metric="confidence", min_threshold=con_threshold)
        rules_by_lift = association_rules(frequent_itemsets, metric="lift", min_threshold=lift_threshold)
        if values['rad_conf']:
            last_index_of_slash = str(url).rfind('/')
            mini_url = url[last_index_of_slash+1:len(url)]
            file_name = 'rules_by_conf_' + mini_url
            if len(rules_by_conf) >= 1:
                print(rules_by_conf)
                rules_by_conf.to_csv(file_name)
                print('Rules are in the file:', file_name)
            else:
                print('No rules to print, rule data set is empty, try reducing your threshold')
        if values['rad_lift']:
            last_index_of_slash = str(url).rfind('/')
            mini_url = url[last_index_of_slash+1:len(url)]
            file_name = 'rules_by_lift_' + mini_url
            if len(rules_by_lift) >= 1:
                print(rules_by_lift)
                rules_by_conf.to_csv(file_name)
                print('Rules are in the file:', file_name)
            else:
                print('No rules to print, rule data set is empty, try reducing your threshold')
    else:
        sg.popup('Error', 'No dataset, make sure you used the \'Load Data\' button first')

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'load':
        global url
        if values['file_url'].strip() == '':
            sg.popup('Error', 'No file has been chosen')
        else:
            url = values['file_url']
            read_file()
    elif event == 'gen_rules':
        if values['min_sup'].strip() == '':
            sg.popup('Error', 'No value supplied for minimum support')
        else:
            sup_count = values['min_sup']
            gen_rules(sup_count)

window.close()
