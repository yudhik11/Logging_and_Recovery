import sys
import os, time

def convert_int(num):
    try:
        return int(num)
    except:
        return float(num)

def get_database_values(data_line):
    global database, ord_db
    data_line = data_line.strip()
    data_line = data_line.split()
    
    for idx in range(0,len(data_line), 2):
        ord_db.append(data_line[idx])
        database[data_line[idx]] = convert_int(data_line[idx+1])
    
    ord_db.sort()

def read_input(filename):
    with open(filename, 'rb') as f:
        input_data = f.readlines()
    data_line = input_data
    """
    print(data_line)
    """
    data_line = data_line[0]
    """
    print(data_line)
    """
    data_line = data_line.strip()
    """
    print(data_line)
    """
    get_database_values(data_line)
    input_data = input_data[1:]
    return input_data

def print_ordered():
    global database, ord_db, output
    for idx, elem in enumerate(ord_db):
        tmp = str(elem) + " " + str(database[elem])
        output = output + tmp
        if idx != len(ord_db) - 1 : 
            output = output + ' '
    output+='\n'

def get_incomplete_list(line, done_tr):
    incomplete_list = list()
    """
    print(line)
    """
    line = line[1:-1]
    """
    print(line)
    """
    line = line.strip()
    """
    print(line)
    """
    line = line.split()[2]
    """
    print(line)
    """
    line = line.strip()
    """
    print(line)
    """
    if '(' == line[0]:
        line = line[1:-1]
    elems = line.split(',')
    for tr in elems:
        tr = tr.strip()
        if tr not in done_tr:
            incomplete_list.append(tr)
    return incomplete_list

def recover(input_data):
    traverse_data = list(reversed(input_data))
    done_tr = []
    check_end_ckpt = False
    check_start_ckpt = False
    incomplete_list = list()
    cnt=0
    for line in traverse_data:
        line = line.strip()
        if line == "" :
            """
            print("Here: if line == "" :")
            """
            pass
        elif line == "<END CKPT>":
            """
            print("Here: elif line == "<END CKPT>":")
            """
            check_end_ckpt = True
        elif "START CKPT" in line:
            """
            print("Here: elif "START CKPT" in line:")
            """
            if not check_end_ckpt:
                incomplete_list = get_incomplete_list(line, done_tr)
                check_start_ckpt = True
                cnt=0
            else:
                break
                
        elif "START" in line:
            """
            print("Here: elif "START" in line:")
            """
            if check_start_ckpt:
                ins, tr = line[1:-1].split()
                ins = ins.strip()
                tr = tr.strip()
                if tr in incomplete_list:
                    cnt+=1
                if cnt == len(incomplete_list):
                    break
        elif "COMMIT" in line:
            """
            print("Here: elif "COMMIT" in line:")
            """
            ins, tr = line[1:-1].split()
            ins = ins.strip()
            tr = tr.strip()
            done_tr.append(tr)

        elif len(line.split(',')) == 3:
            """
            print("Here: elif len(line.split(',')) == 3:")
            """
            tr, elem, val = line[1:-1].split(',')
            tr = tr.strip()
            elem =  elem.strip()
            val = convert_int(val.strip())
            if tr not in done_tr:
                database[elem] = val
 
def main(user_input):
    if len(user_input) != 2:
        sys.exit("Usage: python 20161093_2.py inp")
    filename = user_input[1]
    input_data = read_input(filename)
    recover(input_data)
    print_ordered()
    out_file = '20161093_2.txt'
    with open(out_file, 'w+') as f:
        f.write(output)

database = {}
ord_db = []
output = ""

if __name__ == '__main__':
    main(sys.argv)