import os

# =========================
# PART 1: RECURSION WARM UP
# =========================

def sum_list(nums):
    """Recursively sum a list of numbers."""
    if not nums:
        return 0
    return nums[0] + sum_list(nums[1:])


def count_occurrences(nums, target):
    """Recursively count how many times target appears in nums."""
    if not nums:
        return 0
    return (1 if nums[0] == target else 0) + count_occurrences(nums[1:], target)


def factorial(n):
    """Recursively compute n!."""
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)


# =========================
# PART 2: COUNT ALL FILES
# =========================

def count_files(directory_path):
    """
    Recursively count all files in a directory tree.
    Returns 0 if directory_path doesn't exist or can't be accessed.
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
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Paths to generated data
    TEST_CASES_DIR = os.path.join(BASE_DIR, "test_cases")
    BREACH_DIR = os.path.join(BASE_DIR, "breach_data")

    # Your generator uses these names (based on your output)
    tc1 = os.path.join(TEST_CASES_DIR, "case1_flat")
    tc2 = os.path.join(TEST_CASES_DIR, "case2_nested")
    tc3 = os.path.join(TEST_CASES_DIR, "case3_infected")

    print("=====================================")
    print("PART 1 TESTS: RECURSION WARM UP")
    print("=====================================")
    print("sum_list([1,2,3]) expected 6 ->", sum_list([1, 2, 3]))
    print("count_occurrences([1,2,2,3],2) expected 2 ->", count_occurrences([1, 2, 2, 3], 2))
    print("factorial(5) expected 120 ->", factorial(5))

    print("\n=====================================")
    print("PART 2 TESTS: COUNT ALL FILES")
    print("=====================================")
    print("Test Case 1 expected 5 ->", count_files(tc1))
    print("Test Case 2 expected 4 ->", count_files(tc2))
    print("Test Case 3 expected 5 ->", count_files(tc3))

    print("\n=====================================")
    print("PART 3 TESTS: FIND INFECTED FILES")
    print("=====================================")
    print("Test Case 1 expected 0 ->", len(find_infected_files(tc1, ".encrypted")))
    print("Test Case 2 expected 0 ->", len(find_infected_files(tc2, ".encrypted")))
    print("Test Case 3 expected 3 ->", len(find_infected_files(tc3, ".encrypted")))

    print("\n=====================================")
    print("BREACH DATA ANALYSIS")
    print("=====================================")

    if not os.path.exists(BREACH_DIR):
        print("breach_data folder not found.")
    else:
        total_files = count_files(BREACH_DIR)
        infected_files = find_infected_files(BREACH_DIR, ".encrypted")

        print("Total files in company system:", total_files)
        print("Total infected files:", len(infected_files))

        # Print only a small sample to avoid terminal spam
        sample_n = 20
        print(f"\nShowing first {sample_n} infected file paths (out of {len(infected_files)}):")
        for path in infected_files[:sample_n]:
            print(path)

        # Save full list to a file (useful for submission evidence)
        out_path = os.path.join(BASE_DIR, "infected_files.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            for path in infected_files:
                f.write(path + "\n")
        print("\nSaved full infected file list to:", out_path)

        print("\n=====================================")
        print("TOP-LEVEL BREAKDOWN (hit hardest)")
        print("=====================================")

        top_level_folders = [
            name for name in os.listdir(BREACH_DIR)
            if os.path.isdir(os.path.join(BREACH_DIR, name))
        ]

        if not top_level_folders:
            print("No top-level folders found under breach_data.")
        else:
            area_counts = {}
            for folder in sorted(top_level_folders):
                folder_path = os.path.join(BREACH_DIR, folder)
                area_counts[folder] = len(find_infected_files(folder_path, ".encrypted"))
                print(folder, "infected files:", area_counts[folder])

            worst_area = max(area_counts, key=area_counts.get)
            print("\nMost infected area:", worst_area, "with", area_counts[worst_area], "infected files")
