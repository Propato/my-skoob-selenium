def main():
    lines = []
    reruns_path = "reports/reruns.txt"
    fails_path = "reports/fails.txt"

    try:
        with open(f"reports/report.txt", "r") as file:
            lines += file.read().splitlines()
    except:
        return

    unique_lines = set()
    duplicate_lines = set()

    for line in lines:
        if line in unique_lines:
            duplicate_lines.add(line)
        else:
            unique_lines.add(line)

    unique_lines -= duplicate_lines

    with open(reruns_path, "w") as reruns_file:
        for line in sorted(unique_lines):
            reruns_file.write(line + "\n")

    with open(fails_path, "w") as fail_file:
        for line in sorted(duplicate_lines):
            fail_file.write(line + "\n")


if __name__ == "__main__":
    main()
