from enum import Enum

import argparse
import pathlib
import re

FILE_ENCODING = "utf-8"
TSV_SEP = "\t"
TEXT_LIST_SEP = ", "
CR_LF = "\r\n"
MIN_COL_NUM = 4

class LF(Enum):
    STR = "\n"
    REPLACER = "\\n"

class ESCAPED_DOUBLE_QUOTE(Enum):
    STR = "\\\""
    REPLACER = "￥”"

class TEXT_TYPE(Enum):
    GD = "gd"
    JSON = "json"
    LINES = "LINES"
    DIALOG_TEXT = "dialog_text"
    IMPLANT_NAME = "implant_name"
    LEVEL_NAME = "level_name"
    LINE = "line"
    LINE2 = "line2"
    MESSAGE = "message"
    NPC_NAME = "npc_name"
    OVERRIDE_NAME = "override_name"
    TEXT = "text"
    VALUE = "value"

ESCAPE_STR = "\\"
DOUBLE_ESCAPE_STR = "\\\\"

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("target_dir_path_str", help="target_dir_path", type=str)
arg_parser.add_argument("import_file_path_str", help="import_file_path", type=str)
args = arg_parser.parse_args()

def import_text_tsv(target_dir_path_str, import_file_path_str):
    target_dir_path = pathlib.Path(target_dir_path_str)
    import_file_path = pathlib.Path(import_file_path_str)

    with import_file_path.open(mode='r', encoding=FILE_ENCODING) as import_file:
        for line_str in import_file:
            tsv_col_list = line_str.rstrip(LF.STR.value).split(TSV_SEP)
            if len(tsv_col_list) >= MIN_COL_NUM:
                tsv_col_list.pop()
                temp_text_type = TEXT_TYPE(tsv_col_list[1])
                match temp_text_type:
                    case TEXT_TYPE.GD:
                        write_gd_replace_all(target_dir_path, tsv_col_list)
                    case TEXT_TYPE.JSON:
                        write_json(target_dir_path, tsv_col_list)
                    case TEXT_TYPE.LINES:
                        write_lines(target_dir_path, tsv_col_list)
                    case _:
                        write_tscn_tagged_str(target_dir_path, tsv_col_list, temp_text_type)

def write_gd(root_path, tsv_col_list):
    target_path = root_path / tsv_col_list[0]
    with target_path.open(mode='r', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
        lines = temp_file.readlines()
        i = int(tsv_col_list[2])
        lines[i] = lines[i].replace('"' + tsv_col_list[4] + '"', '"' + tsv_col_list[5] + '"')

        with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
            temp_file.writelines(lines)

def write_gd_replace_all(root_path, tsv_col_list):
    target_path = root_path / tsv_col_list[0]
    with target_path.open(mode='r', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
        file_text = temp_file.read()
    
    file_text = file_text.replace('"' + tsv_col_list[4] + '"', '"' + tsv_col_list[5] + '"')

    with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
        temp_file.write(file_text)

def write_json(root_path, tsv_col_list):
    name_str = escape_escape_str(tsv_col_list[4])

    objectives_str_list = []
    for temp_col in tsv_col_list[5:len(tsv_col_list) - 1]:
        objectives_str_list.append('"' + temp_col + '"')
    objectives_str = escape_escape_str(TEXT_LIST_SEP.join(objectives_str_list))

    description_str = escape_escape_str(tsv_col_list[len(tsv_col_list) - 1])

    target_path = root_path / tsv_col_list[0]
    with target_path.open(mode='r', encoding=FILE_ENCODING) as temp_file:
        file_text = temp_file.read()
    file_text = re.sub(r'"name": "[^"]*"', '"name": "' + name_str + '"', file_text, re.DOTALL)
    file_text = re.sub(r'"objectives": \[[^\]]*\]', '"objectives": [' + objectives_str + ']', file_text, re.DOTALL)
    file_text = re.sub(r'"description": "[^"]*"', '"description": "' + description_str + '"', file_text, re.DOTALL)
    
    with target_path.open(mode='w', encoding=FILE_ENCODING, newline=CR_LF) as temp_file:
        temp_file.write(file_text)

def write_lines(root_path, tsv_col_list):
    target_path = root_path / tsv_col_list[0]
    with target_path.open(mode='r', encoding=FILE_ENCODING) as temp_file:
        file_text = escape_escaped_double_quot(temp_file.read())

    lines_str_list = []
    for temp_col in tsv_col_list[5:]:
        lines_str_list.append('"' + temp_col + '"')
    lines_str = TEXT_LIST_SEP.join(lines_str_list)
    
    tag_str = tsv_col_list[4]
    split_text_list = file_text.split(tag_str)
    if len(split_text_list) > 1:
        split_text_list[1] = re.sub(r'LINES = \[[^\]]*\]', 'LINES = [ ' + lines_str + ' ]', split_text_list[1], 1, re.DOTALL)
        file_text = tag_str.join(split_text_list)
        with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
            temp_file.write(escape_escaped_double_quot(file_text, True))

def write_tscn_tagged_str(root_path, tsv_col_list, text_type):
    target_path = root_path / tsv_col_list[0]
    with target_path.open(mode='r', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
        file_text = escape_escaped_double_quot(temp_file.read())
    
    tag_str = tsv_col_list[4]
    split_text_list = file_text.split(tag_str)
    if len(split_text_list) > 1:
        text_type_str = text_type.value
        split_text_list[1] = re.sub(r'\n' + text_type_str + ' = "[^"]*"', '\n' + text_type_str + ' = "' + escape_escape_str(escape_LF(tsv_col_list[5], True)) + '"', split_text_list[1], 1, re.DOTALL)
        file_text = tag_str.join(split_text_list)
        with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
            temp_file.write(escape_escaped_double_quot(file_text, True))

def escape_escape_str(str):
    return str.replace(ESCAPE_STR, DOUBLE_ESCAPE_STR)

def escape_escaped_double_quot(str, do_reverse = False):
    old = ESCAPED_DOUBLE_QUOTE.STR.value
    new = ESCAPED_DOUBLE_QUOTE.REPLACER.value
    if do_reverse:
        old = ESCAPED_DOUBLE_QUOTE.REPLACER.value
        new = ESCAPED_DOUBLE_QUOTE.STR.value
    return str.replace(old, new)

def escape_LF(str, do_reverse = False):
    old = LF.STR.value
    new = LF.REPLACER.value
    if do_reverse:
        old = LF.REPLACER.value
        new = LF.STR.value
    return str.replace(old, new)

import_text_tsv(args.target_dir_path_str, args.import_file_path_str)
