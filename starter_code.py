import os

# =========================
# PART 1: RECURSION WARM UP
# =========================

def sum_list(nums):
    """
    Recursively sum a list of numbers.
    """
    if nums is None or len(nums) == 0:
        return 0
    return nums[0] + sum_list(nums[1:])


def count_occurrences(nums, target):
    """
    Recursively count how many times target appears in nums.
    """
    if nums is None or len(nums) == 0:
        return 0
    return (1 if nums[0] == target else 0) + count_occurrences(nums[1:], target)


def factorial(n):
    """
    Recursively compute n!.
    """
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


# =========================
# PART 2: COUNT ALL FILES
# =========================

def count_files(directory_path):
    """
    Recursively count all files in a directory tree.
    """
    total = 0

    try:
        entries = os.listdir(directory_path)
    except (FileNotFoundError, PermissionError, NotADirectoryError):
        return 0

    for name in entries:
        full_path = os.path.join(directory_path, name)

        if os.path.isfile(full_path):
            total += 1
        elif os.path.isdir(full_path):
            total += count_files(full_path)

    return total


# =========================
# PART 3: FIND INFECTED FILES
# =========================

def find_infected_files(directory_path, extension=".encrypted"):
    """
    Recursively find all files ending in `extension`.
    Returns a list of full file paths.
    """
    infected = []

    try:
        entries = os.listdir(directory_path)
    except (FileNotFoundError, PermissionError, NotADirectoryError):
        return infected

    for name in entries:
        full_path = os.path.join(directory_path, name)

        if os.path.isfile(full_path):
            if name.endswith(extension):
                infected.append(full_path)

        elif os.path.isdir(full_path):
            infected.extend(find_infected_files(full_path, extension))

    return infected


# =========================
# MAIN (tests + breach analysis)
# =========================
if __name__ == "__main__":

    print("=====================================")
    print("PART 1 TESTS: RECURSION WARM UP")
    print("=====================================")

    print("sum_list([1,2,3]) expected 6 ->", sum_list([1, 2, 3]))
    print("count_occurrences([1,2,2,3],2) expected 2 ->", count_occurrences([1, 2, 2, 3], 2))
    print("factorial(5) expected 120 ->", factorial(5))


    print("\n=====================================")
    print("PART 2 TESTS: COUNT ALL FILES")
    print("=====================================")

    print("Test Case 1 expected 5 ->", count_files("test_cases/test_case_1"))
    print("Test Case 2 expected 4 ->", count_files("test_cases/test_case_2"))
    print("Test Case 3 expected 5 ->", count_files("test_cases/test_case_3"))


    print("\n=====================================")
    print("PART 3 TESTS: FIND INFECTED FILES")
    print("=====================================")

    print("Test Case 1 expected 0 ->", len(find_infected_files("test_cases/test_case_1", ".encrypted")))
    print("Test Case 2 expected 0 ->", len(find_infected_files("test_cases/test_case_2", ".encrypted")))
    print("Test Case 3 expected 3 ->", len(find_infected_files("test_cases/test_case_3", ".encrypted")))


    print("\n=====================================")
    print("BREACH DATA ANALYSIS")
    print("=====================================")

    company_root = "breach_data"

    total_files = count_files(company_root)
    infected_files = find_infected_files(company_root, ".encrypted")

    print("Total files in company system:", total_files)
    print("Total infected files:", len(infected_files))

    print("\nFull paths to infected files:")
    for f in infected_files:
        print(f)


    print("\n=====================================")
    print("DEPARTMENT BREAKDOWN")
    print("=====================================")

    departments = ["Finance", "HR", "Sales"]

    dept_counts = {}
    for dept in departments:
        dept_path = os.path.join(company_root, dept)
        dept_infected = find_infected_files(dept_path, ".encrypted")
        dept_counts[dept] = len(dept_infected)
        print(dept, "infected files:", len(dept_infected))

    hardest_hit = max(dept_counts, key=dept_counts.get)
    print("\nMost infected department:", hardest_hit, "with", dept_counts[hardest_hit], "infected files")
