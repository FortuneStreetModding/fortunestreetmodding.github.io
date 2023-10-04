def inplace_change(file, attribute, value):
    with open(file, "r", encoding="utf8") as f:
        lines = f.readlines()
    with open(file, "w", encoding="utf8") as f:
        for line in lines:
            if line.strip().startswith(attribute):
                f.write(f'{line.split(":", 1)[0]}: {value}\n')
            else:
                f.write(line)
