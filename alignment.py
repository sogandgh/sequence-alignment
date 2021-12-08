import sys

mismatch_cost_dic = {"AA": 0, "AC": 110, "AG": 48, "AT": 94,
                     "CA": 110, "CC": 0, "CG": 118, "CT": 48,
                     "GA": 48, "GC": 118, "GG": 0, "GT": 110,
                     "TA": 94, "TC": 48, "TG": 110, "TT": 0}
gap_cost = 30


# find the actual alignment
def backtrack(x, y, dp):
    i = len(dp) - 1
    j = len(dp[0]) - 1

    matched_string_1 = ''
    matched_string_2 = ''

    while (i > 0) and (j > 0):
        if dp[i][j] == dp[i - 1][j - 1]:
            matched_string_1 = x[i - 1] + matched_string_1
            matched_string_2 = y[j - 1] + matched_string_2
            i -= 1
            j -= 1

        elif dp[i][j] == dp[i - 1][j - 1] + mismatch_cost_dic[x[i - 1] + y[j - 1]]:
            matched_string_1 = x[i - 1] + matched_string_1
            matched_string_2 = y[j - 1] + matched_string_2
            i -= 1
            j -= 1

        elif dp[i][j] == dp[i - 1][j] + gap_cost:
            matched_string_1 = x[i - 1] + matched_string_1
            matched_string_2 = '-' + matched_string_2
            i -= 1

        elif dp[i][j] == dp[i][j - 1] + gap_cost:
            matched_string_1 = '-' + matched_string_1
            matched_string_2 = y[j - 1] + matched_string_2
            j -= 1

    while i > 0:
        matched_string_1 = x[i - 1] + matched_string_1
        matched_string_2 = '-' + matched_string_2
        i -= 1

    while j > 0:
        matched_string_2 = y[j - 1] + matched_string_2
        matched_string_1 = '-' + matched_string_1
        j -= 1

    return (matched_string_1), (matched_string_2)


# find the optimal cost of the alignment
def alignment(x, y):
    row_len = len(x)
    column_len = len(y)

    # initializing the dynamic programming table
    dp = [[0 for j in range(column_len + 1)] for i in range(row_len + 1)]

    # base cases
    for i in range(0, row_len + 1):
        dp[i][0] = gap_cost * i

    for j in range(0, column_len + 1):
        dp[0][j] = gap_cost * j

    # calculate cost of optimal alignment
    for i in range(1, row_len + 1):
        for j in range(1, column_len + 1):

            # if the characters are matching
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                case_1 = dp[i - 1][j - 1] + mismatch_cost_dic[x[i - 1] + y[j - 1]]
                case_2 = dp[i - 1][j] + gap_cost
                case_3 = dp[i][j - 1] + gap_cost

                dp[i][j] = min(case_1, case_2, case_3)
    return dp, dp[row_len][column_len]


# generate two strings
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


# read input file
def read_input():
    filename = sys.argv[-1]
    if filename == '':
        exit()
    file1 = open(filename, 'r')
    lines = file1.readlines()
    return lines
