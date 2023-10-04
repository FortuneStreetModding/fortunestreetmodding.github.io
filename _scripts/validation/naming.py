from validation.errors import process_strErrors


def check_naming_convention(name, yamlMap):
    strErrors = []
    print(f"{name:24} Naming Convention Check...", end="")

    if " " in yamlMap.name:
        strErrors.append(f"There is a whitespace character in {yamlMap}")
    if " " in name:
        strErrors.append(f"There is a whitespace character in {name}")

    process_strErrors(strErrors)
