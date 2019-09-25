"""
Description of functionality:
1) loads string into a list
2) looks for the highest priority expression to parce (if parenthesis - 
what's inside the most senior)
3) replaces the expression inside the most senior parenthesis with result
4) seeks for parethesis again and repeats until none are available
"""

# parces WITHIN parenthesis

#------parcer helpers---------------#
#------parcing NOT--------#


def process_not(to_eval):
    pos_minus = to_eval.index('-')
    if (to_eval[pos_minus + 1] == 'TRUE'):
        to_eval[pos_minus + 1] = 'FALSE'
    else:
        to_eval[pos_minus + 1] = 'TRUE'
    del to_eval[pos_minus]
    return to_eval

#------parcing AND and OR-----------#


def process_and_or(to_eval):
    # find the first operation to perform. Then find the operands around it.
    # this approach helps with different order of operations - whichever is
    # first will be processed

    if ('AND' in to_eval and 'OR' in to_eval):
        oper_pos = min(to_eval.index('AND'), to_eval.index('OR'))
    elif ('AND' in to_eval):
        oper_pos = to_eval.index('AND')
    else:
        oper_pos = to_eval.index('OR')

    operation = to_eval[oper_pos]

    left_val = to_eval[oper_pos - 1]
    right_val = to_eval[oper_pos + 1]
    left_val_b = ('TRUE' in left_val)
    right_val_b = ('TRUE' in right_val)

    if (operation == 'AND'):
        result = left_val_b and right_val_b
    elif (operation == 'OR'):
        result = left_val_b or right_val_b
    else:
        print("Unrecognized operation: ", operation)
        exit()

    if (result):
        to_eval[oper_pos - 1] = 'TRUE'
    else:
        to_eval[oper_pos - 1] = 'FALSE'
    del to_eval[oper_pos : oper_pos + 2]

    return to_eval

#------parcing THEN and EQ----------#
def process_eq_then(to_eval):
    if ('EQ' in to_eval and 'THEN' in to_eval):
        oper_pos = min(to_eval.index('EQ'), to_eval.index('THEN'))
    elif ('EQ' in to_eval):
        oper_pos = to_eval.index('EQ')
    else:
        oper_pos = to_eval.index('THEN')

    operation = to_eval[oper_pos]

    left_val = to_eval[oper_pos - 1]
    right_val = to_eval[oper_pos + 1]

    if (operation == 'EQ'):
        if (left_val == right_val):
            to_eval[oper_pos - 1] = 'TRUE'
        else:
            to_eval[oper_pos - 1] = 'FALSE'
    elif (operation == 'THEN'):
        if (left_val == 'TRUE' and right_val == 'FALSE'):
            to_eval[oper_pos - 1] = 'FALSE'
        else:
            to_eval[oper_pos - 1] = 'TRUE'
    else:
        print("Unrecognized operation: ", operation)
        exit()

    del to_eval[oper_pos : oper_pos + 2]

    return to_eval


#/\-------end parcer helpers-------------/\#

#\/-------begin parcers-------\/

#inside parenthesis
def parcer_in_parenth(to_eval):

    #*****processing 1) "NOT"********#
    while ('-' in to_eval):
        to_eval = process_not(to_eval)

    if (len(to_eval) == 1):  # then we are done
        return to_eval

    #*****processing 2) AND, OR******#
    while (('AND' in to_eval) or ('OR' in to_eval)):
        to_eval = process_and_or(to_eval)

    if (len(to_eval) == 1):  # then we are done
        return to_eval

    #****processing 3) THEN, EQ******#
    while (('EQ' in to_eval) or ('THEN' in to_eval)):
        to_eval = process_eq_then(to_eval)

    return to_eval


#outside parenthesis
def parcer_parenth (to_eval):
    #looking for the first closing parenthesis and opening parenthesis
    #that directly preceeds the closing one, parce what is inside, repeat until there are no parenthesis

    while (')' in to_eval):
        close_par = to_eval.index(')')
        open_par = close_par
        while (to_eval[open_par] != '('):
            open_par -= 1
            
        statement_within = to_eval [open_par + 1 : close_par]
        to_eval[open_par] = parcer_in_parenth(statement_within)[0]
        del to_eval[open_par + 1 : close_par + 1]

    return parcer_in_parenth(to_eval)


#parces line from the input file:
def parcer_line (to_eval):
    # changes variables for truth values and returns a string of the statement to process
    line_list = to_eval.split('\t')
    var_list = line_list[0].split(',')
    val_list = line_list[1].split(',')
    statement = line_list[2].split()

    for i in range(len(var_list)):
        while (var_list[i] in statement):
            ind = statement.index(var_list[i])
            if (val_list[i] == 'T'):
                statement[ind] = 'TRUE'
            else:
                statement[ind] = 'FALSE'
                
    return statement

    
#/\-------end parcers-------/\



# main

#read the file
in_file = open ("q1_in.txt")
out_file = open ("q1_out.txt", 'w')
entries = in_file.readlines()

# parse each line
count = 1
for line in entries:
    to_eval = line.rstrip()

    to_eval = parcer_line(to_eval)
    to_eval = parcer_parenth(to_eval)
    output = to_eval[0].title()

    if (count < len(entries)):
        out_file.write (output + '\n')
    else:
        out_file.write (output)

    count += 1

in_file.close()
out_file.close()
