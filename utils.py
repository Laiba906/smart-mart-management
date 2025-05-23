def read_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def write_file(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            f.write(f"{line}\n")

def append_file(filename, line):
    with open(filename, 'a') as f:
        f.write(f"{line}\n")

def cashier_exists(username):
    cashiers = read_file(cashiers.txt)
    for line in cashiers:
        if line.split(":")[0] == username:
            return True
    return False

