import sys


def generate_strings(lines):
    string1 = lines[0]
    string1 = string1.rsplit()[0]
    string2_line_number = ''

    # string 1 generation
    for line_number, line in enumerate(lines[1:]):
        line = line.rsplit()[0]
        if line.isnumeric():
            split_index = int(line) + 1
            string1 = string1[0:split_index] + string1 + string1[split_index:]
        else:
            string2_line_number = line_number
            break

    # string 2 generation
    string2 = lines[string2_line_number + 1].rsplit()[0]
    for line_number, line in enumerate(lines[string2_line_number + 2:]):
        line = line.rsplit()[0]
        if line.isnumeric():
            split_index = int(line) + 1
            string2 = string2[0:split_index] + string2 + string2[split_index:]
        else:
            break

    return string1, string2


def read_input():
    filename = sys.argv[-1]
    file1 = open(filename, 'r')
    lines = file1.readlines()
    return lines


lines = read_input()
string1, string2 = generate_strings(lines)
print('string1 ' + string1)
print('string2 ' + string2)
