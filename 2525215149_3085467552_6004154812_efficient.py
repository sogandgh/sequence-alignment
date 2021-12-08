import time
import os
import psutil

from alignment import mismatch_cost_dic, gap_cost, alignment, backtrack, generate_strings, read_input

total_cost = 0


# generating alignments of two string using divide and conquer + dynamic programming
def divide_and_conquer_alignment(x, y):
    row_len = len(x)
    column_len = len(y)

    if row_len < 2 or column_len < 2:
        dp, cost = alignment(x, y)
        matched_string_1, matched_string_2 = backtrack(x, y, dp)
    else:
        mid = int(column_len / 2)

        left_col = space_efficient_alignment(x, y[0:mid])
        right_col = space_efficient_alignment(x[::-1], y[mid: column_len][::-1])

        combine_cols = [left_val + right_val for left_val, right_val in zip(left_col, right_col)]

        min_cost = min(combine_cols)
        min_index = int(combine_cols.index(min_cost))

        matched_string_1_left, matched_string_2_left = divide_and_conquer_alignment(x[:min_index],
                                                                                    y[:int(column_len / 2)])
        matched_string_1_right, matched_string_2_right = divide_and_conquer_alignment(x[min_index:],
                                                                                      y[int(column_len / 2):])

        matched_string_1 = matched_string_1_left + matched_string_1_right
        matched_string_2 = matched_string_2_left + matched_string_2_right

    return matched_string_1, matched_string_2


# space efficient way of finding the optimal cost of alignment, by using only two columns
def space_efficient_alignment(x, y):
    row_len = len(x)
    column_len = len(y)

    # initializing the space efficient dynamic programming table
    dp = [[0 for j in range(2)] for i in range(row_len + 1)]

    # base cases
    for i in range(0, row_len + 1):
        dp[i][0] = gap_cost * i

    # calculate cost of space-efficient optimal alignment
    for j in range(1, column_len + 1):
        dp[0][1] = gap_cost * j

        for i in range(1, row_len + 1):
            case_1 = dp[i - 1][0] + mismatch_cost_dic[x[i - 1] + y[j - 1]]
            case_2 = dp[i - 1][1] + gap_cost
            case_3 = dp[i][0] + gap_cost

            dp[i][1] = min(case_1, case_2, case_3)

        # moving column 1
        for i in range(0, row_len + 1):
            dp[i][0] = dp[i][1]

    last_col = [row[0] for row in dp]

    return last_col


def main():
    start = time.perf_counter()
    process = psutil.Process(os.getpid())

    lines = read_input()
    string1, string2 = generate_strings(lines)

    print("program size: " + str(len(string1) + len(string2)))

    alignment_cost = space_efficient_alignment(string1, string2)
    matched_string_1, matched_string_2 = divide_and_conquer_alignment(string1, string2)
    min_cost = alignment_cost[len(alignment_cost) - 1]

    time_elapsed = (time.perf_counter() - start)
    memory_used = process.memory_info().rss / 1024

    if len(matched_string_1) >= 50:
        matched_string_1 = matched_string_1[:50] + matched_string_1[len(matched_string_1) - 50:]
    if len(matched_string_2) >= 50:
        matched_string_2 = matched_string_2[:50] + matched_string_2[len(matched_string_2) - 50:]

    f = open("output.txt", "w")
    f.write(matched_string_1 + "\n")
    f.write(matched_string_2 + "\n")
    f.write(str(min_cost) + "\n")
    f.write(str(time_elapsed) + "\n")
    f.write(str(memory_used) + "\n")
    f.close()


if __name__ == "__main__":
    main()
