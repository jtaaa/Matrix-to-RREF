# Joshua Allum, 28th January 2016
# RREF matrix solver
# Outputs every step in LaTeX format to be compiled

# Import fractions
from fractions import Fraction

# Initialize Matrix
matrix = []


def is_number(s):
    try:
        Fraction(s)
        return True
    except ValueError:
        return False

#------------------------------------------------------------#
# Import augmented matrix from matrix.txt
print("Hello, getting matrix data...")
with open("matrix.txt", "r") as f:
    for line in f:
        row_string = line.rstrip('\n').split(' ')
        row = []
        for i in row_string:
            try:
                row.append(Fraction(i))
            except ValueError:
                row.append(i)
        matrix.append(row)

print("Matrix data loaded.")


#------------------------------------------------------------#
# Prints matrix in its current state to terminal and to file
printed = 0
def print_matrix(m):
    global printed
    print("=============================")
    if printed % 2 == 0 and printed != 0:
        f.write('\\\\')
    f.write('&\\begin{amatrix}{' + str(len(m[0]) - 1) + '}')
    for i in m:
        for k in range (len(i) - 1):
            f.write(str(i[k]) + '&')
            print(i[k], end=' ')
        f.write(str(i[len(i) - 1]) + '\\\\')
        print(i[len(i) - 1])
    f.write('\\end{amatrix}\n')
    print("=============================")
    printed += 1
    return                         


#------------------------------------------------------------#
# Subtracts row, r2, from row, r1, enough times to make
#   row, r1, column, lead_pos, equal 0
def row_subtract(r1, r2, lead_pos):
    mult = matrix[r1][lead_pos]
    if mult == 0:
        f.write('\\\\')
        return
    elif mult == 1:
        factor = '-R_'+str(r2+1)
        sfactor = '-'
    elif mult == -1:
        factor = '+R_'+str(r2+1)
        sfactor = '+'
    elif mult < 0:
        factor = '+'+str(abs(mult))+'R_'+str(r2+1)
        sfactor = '+'+str(mult)
    else:
        factor = '-'+str(abs(mult))+'R_'+str(r2+1)
        sfactor = '-'+str(mult)
    for i in range (len(matrix[r1])):
        if type(matrix[r1][i]) is str:
            matrix[r1][i] += sfactor+str(matrix[r2][i])
        else:
            matrix[r1][i] -= mult * matrix[r2][i]
    f.write('R_'+str(r1+1)+factor+'\\\\')
    print('R_'+str(r1+1)+factor)
    return

#------------------------------------------------------------#
# Performs row subtraction on all rows except the row, row_num
#   and prints the steps taken to terminal and to file
def subtract_all_rows(row_num):
    f.write('\\begin{array}{c}')
    for r in range (len(matrix)):
        if r != row_num:
            row_subtract(r, row_num, lead_pos)
        else:
            f.write('\\\\')
    f.write('\\end{array}')
    if printed % 2 == 1:
        f.write('&')
    f.write('\n\sim\n')


#------------------------------------------------------------#
# Swaps row, row_num, to the end of the matrix
def swap_row(row_num, empty_rows):
    last_nonzero_row = len(matrix)-1-empty_rows
    temp = matrix[last_nonzero_row]
    matrix[last_nonzero_row] = matrix[row_num]
    matrix[row_num] = temp
    del temp
    f.write('\\begin{array}{c}')
    for r in range (len(matrix)):
        if r == last_nonzero_row:
            f.write('R_'+str(row_num+1)+'\\leftrightarrow R_' \
                    +str(last_nonzero_row+1)+'\\\\')
            print('R_'+str(row_num+1)+'<-->R_'+str(last_nonzero_row+1))
        else:
            f.write('\\\\')
    f.write('\\end{array}')
    if printed % 2 == 1:
        f.write('&')
    f.write('\n\sim\n')
    return


#------------------------------------------------------------#
# Returns the position of the leading number of the row
def get_lead_pos(row_num):
    for col_num in range (len(matrix[row_num])):
        if matrix[row_num][col_num] != 0:
            return col_num
    return 0


#------------------------------------------------------------#
# Divides every element of the row, row_num by lead and prints
#   the step taking to the terminal and to file
def divide_row(row_num, lead):
    for i in range (len(matrix[row_num])):
        if type(matrix[row_num][i]) is str:
            prev = matrix[row_num][i]
            matrix[row_num][i] = str(Fraction(1, lead))+prev
        else:
            matrix[row_num][i] /= lead
    print(str(Fraction(1, lead))+'R_'+str(row_num+1))
    f.write('\\begin{array}{c}')
    for r in range(len(matrix)):
        if r == row_num:
            f.write(str(Fraction(1, lead))+'R_'+str(row_num+1)+'\\\\')
        else:
            f.write('\\\\')
    f.write('\\end{array}')
    if printed % 2 == 1:
        f.write('&')
    f.write('\n\sim\n')


#------------------------------------------------------------#
# Produces the row-reduced echelon form of the augmented
#   matrix inputted and prints all the steps that were
#   required to the terminal and to RREF.txt as compilable
#   LaTeX code
with open('RREF.txt', 'w') as f:
    f.write('$\\begin{aligned}[t]\n')
    row_num, empty_rows, lead_pos = 0, 0, 0
    print_matrix(matrix)
    while row_num + empty_rows < len(matrix) and \
          lead_pos < len(matrix[row_num]):
        lead = matrix[row_num][lead_pos]
        if lead == 0:
            r = row_num
            while r < (len(matrix)):
                if matrix[r][lead_pos] != 0:
                    swap_row(row_num, r)
                    break
                r += 1
            lead = matrix[row_num][lead_pos]
            if lead == 0:
                lead_pos += 1
                continue
        else:
            if lead == 1:
                subtract_all_rows(row_num)
                row_num += 1
                lead_pos += 1
            else:
                divide_row(row_num, lead)
        print_matrix(matrix)
    f.write('\\end{aligned}$\n')
