#!/usr/bin/env python
import yaml
import jsonschema

from validation.errors import process_strErrors

strErrors = []

def check_first_line(firstLine):
    global strErrors
    if not firstLine == "---":
        strErrors.append("YAML file first line must be ---")


def load_yaml(name, yamlMap, yamlSchema):
    global strErrors
    yamlContent = ""
    with open(yamlMap, "r", encoding="utf8") as stream:
        # check the first line before anything else, so we
        # won't have to open the file twice. Then seek back
        # to the top.
        check_first_line(stream.readline().strip())
        stream.seek(0x0)

        try:
            print(f'{"":24} YAML Validation Check..............', end="")
            yamlContent = yaml.safe_load(stream)
            jsonschema.validate(yamlContent, yamlSchema)
        except yaml.YAMLError as exc:
            strErrors.append(exc)
        except jsonschema.ValidationError as err:
            strErrors.append(err)
    process_strErrors(strErrors)
    return yamlContent


def load_yaml_schema():
    with open("../schema/mapdescriptor.json", "r", encoding="utf8") as stream:
        return yaml.safe_load(stream)
