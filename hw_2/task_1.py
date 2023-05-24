import csv
import re

def get_data()->list:
    main_data = [['Изготовитель системы','Название ОС','Код продукта','Тип системы']]
    for i in range(1,4):
        with open(f'info_{i}.txt','r') as f:
            content_f = f.read()
            lst_str = ['' for i in range(4)]
            for j in range(4):
                str_name_param = main_data[0][j]
                pattern = str_name_param+r':\s*(.+)'
                matches = re.findall(pattern, content_f)
                lst_value = [match.replace(" ", "") for match in matches]
                lst_str[j] = lst_value[0]
            main_data.append(lst_str)
    return main_data

def write_to_csv(name_file:str, lst_data:list):
    with open(name_file,'w') as f:
        f_writer = csv.writer(f,quoting=csv.QUOTE_NONE)
        for row in lst_data:
            f_writer.writerow(row)

def main():
    lst_main = get_data()
    write_to_csv('info_result.csv',lst_main)





if __name__ == '__main__':
    main()