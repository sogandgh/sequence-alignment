import os
import time
import psutil

from alignment import read_input, generate_strings, alignment, backtrack


def main():
    start = time.perf_counter()
    process = psutil.Process(os.getpid())

    lines = read_input()
    string1, string2 = generate_strings(lines)

    print("program size: " + str(len(string1) + len(string2)))

    dp, min_cost = alignment(string1, string2)
    matched_string_1, matched_string_2 = backtrack(string1, string2, dp)

    if len(matched_string_1) >= 50:
        matched_string_1 = matched_string_1[:50] + matched_string_1[len(matched_string_1) - 50:]
    if len(matched_string_2) >= 50:
        matched_string_2 = matched_string_2[:50] + matched_string_2[len(matched_string_2) - 50:]

    time_elapsed = (time.perf_counter() - start)
    memory_used = process.memory_info().rss / 1024

    f = open("output.txt", "w")
    f.write(matched_string_1 + "\n")
    f.write(matched_string_2 + "\n")
    f.write(str(min_cost) + "\n")
    f.write(str(time_elapsed) + "\n")
    f.write(str(memory_used) + "\n")
    f.close()


if __name__ == "__main__":
    main()
