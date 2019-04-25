import sys
import os, time

def check_val(inp):
    global registers
    try:
        return convert_int(inp)
    except:
        return registers[inp]

def get_database_values(data_line):
    global database, ord_db
    data_line = data_line.strip().split()
    for idx in range(0,len(data_line), 2):
        ord_db.append(data_line[idx])
        database[data_line[idx]] = convert_int(data_line[idx+1])
    ord_db.sort()


def convert_int(num):
    try:
        return int(num)
    except:
        return float(num)

def print_ordered():
    global memory, ord_mem, output
    ord_mem.sort()
    for idx, elem in enumerate(ord_mem):
        tmp = str(elem) + " " + str(memory[elem])
        output = output + tmp
        """
        print(elem, memory[elem], end = '')
        """
        if idx!=len(ord_mem) - 1 :
            output+=' '
            """
            print(" ",  end = '')
            """
    output += '\n'
    """
    print()
    """
    global database, ord_db
    for idx, elem in enumerate(ord_db):
        tmp = str(elem) + " " + str(database[elem])
        output = output + tmp
        """
        print(elem, database[elem], end = '')
        """
        if idx!=len(ord_db) - 1 :
            output+=' '
            """
            print(" ",  end = '')
            """
    output+='\n'
    """
    print()
    """

def db_operate(command, op, tr_id):
    global database, ord_mem, memory, registers, output
    command = command.split('(')
    command = command[1]
    command = command.split(')')
    command = command[0]
    command = command.strip()
    if ',' in command:
        elem, reg = command.split(',')
        elem, reg = elem.strip(), reg.strip()
    if op == "read":
        if elem not in memory:
            registers[reg] = database[elem]
            memory[elem] = database[elem]
            ord_mem.append(elem)
        else:
            registers[reg] = memory[elem]
    elif op == "write":
        tmp = "<" + tr_id + ", " + elem + ", "
        output = output + tmp
        """
        print("<" + tr_id + ", " + elem + ", ", end ='')
        """
        if elem not in memory:
            memory[elem] = database[elem]
            ord_mem.append(elem)
        tmp = str(memory[elem]) + ">" + '\n'
        output = output + tmp
        """
        print(str(memory[elem]) + ">")
        """
        memory[elem] = registers[reg]
        print_ordered()
    
    elif op == "output":
        if command not in memory:
            memory[command] = database[command]
            ord_mem.append(command)
            
        else:
            database[command] = memory[command]
            

def math_operate(final_reg, inp1, inp2, op):
    global registers
    inp1, inp2 = check_val(inp1), check_val(inp2)
    """
    print("here", inp1, inp2)
    """
    if op == '/':
        try:
            registers[final_reg] = inp1 / inp2
        except:
            print("Divide by zero")
            sys.exit(0)
    elif op == '+':
        registers[final_reg] = inp1 + inp2
    elif op == '-':
        registers[final_reg] = inp1 - inp2
    elif op == '*':
        registers[final_reg] = inp1 * inp2

def execute(tr_id, start_comm, end_comm):
    global transactions, registers
    db_operations = ["read", "write", "output"]
    operators = ['+', '-', '*', '/']
    for idx in range(start_comm, end_comm):
        comm = transactions[tr_id][idx]
        """
        print(comm)
        """
        """
        print("regs", registers)
        """
        """
        print("memory", memory)
        """
        """
        print("database", database)
        """
        fl = 0
        for op in db_operations:
            if op in comm.lower():
                db_operate(comm, op, tr_id)
                fl=1
                break

        if fl == 1 : 
            continue
        command = comm.strip().split(":=")
        final_reg = command[0].strip()
        for op in operators:
            """
            print(op, command[1])
            """
            if op in command[1]:
                inp1, inp2 = command[1].strip().split(op)
                inp1 = inp1.strip()
                inp2 = inp2.strip()
                math_operate(final_reg, inp1, inp2, op)
                break


def operate(num_ops):
    global output
    start_point = 0
    completed = False
    num_ops = convert_int(num_ops)
    while not completed:
        start_comm = start_point * num_ops
        cnt=0
        for tr in ord_tmp:
            tr_num_cmd = len(transactions[tr])
            
            if start_comm == 0 :
                tmp = "<START " + tr + ">" + '\n'
                output = output + tmp
                """
                print("<START " + tr + ">")
                """
                print_ordered()
            if start_comm >= tr_num_cmd :
                cnt+=1
                continue

            end_comm =  min(start_comm + num_ops, tr_num_cmd)
            execute(tr, start_comm, end_comm)
            if end_comm == tr_num_cmd:
                output+="<COMMIT " + tr + ">" + '\n'
                """
                print("<COMMIT " + tr + ">")
                """
                print_ordered()
        start_point+=1
        if cnt == len(ord_tmp):
            completed = True

def read_input(filename):
    global transactions, ord_tmp
    num_commands = 0
    start = True
    
    with open(filename, 'r') as f:
        for line in f:
            if start is True:
                get_database_values(line)
                start = False
            elif line.strip() == "":
                pass
            elif num_commands == 0:
                tr_id, num_commands = line.strip().split()
                tr_id, num_commands = tr_id.strip(), num_commands.strip()
                if tr_id not in ord_tmp:
                    ord_tmp.append(tr_id)
                    transactions[tr_id] = list()
                else:
                    sys.exit("Repeated Transaction ID")
                num_commands = convert_int(num_commands)
            else:
                transactions[tr_id].append(line.strip())
                num_commands-=1


def main(user_input):
    global output
    if len(user_input)!=3:
        sys.exit("Usage: python 20161093_1.py inp x")
    filename = sys.argv[1]
    rr_const = sys.argv[2]
    try:
        read_input(filename)
    except:
        sys.exit("Input File does not exists.")
    operate(rr_const)
    out_file = "20161093_1.txt"
    with open(out_file, 'w+') as f:
        f.write(output)

transactions = {}
database = {}
memory = {}
registers = {}
ord_mem = list()
ord_tmp = list()
ord_db = list()

output = ""

if __name__ == '__main__':
    main(sys.argv)