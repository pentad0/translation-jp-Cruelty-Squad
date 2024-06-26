from enum import Enum

import argparse
import pathlib
import re

FILE_ENCODING = "utf-8"
TSV_SEP = "\t"
TEXT_LIST_SEP = ", "
CR_LF = "\r\n"
MIN_COL_NUM = 4

class SOB(Enum):
    STR = "[ "
    REPLACER = "[SOB]"

class EOB(Enum):
    STR = " ]"
    REPLACER = "[EOB]"

class LF(Enum):
    STR = "\n"
    REPLACER = "\\n"

class TAB(Enum):
    STR = "\t"
    REPLACER = "\\t"

class ESCAPED_DOUBLE_QUOTE(Enum):
    STR = "\\\""
    REPLACER = "￥”"

class TEXT_TYPE(Enum):
    GD = "gd"
    JSON = "json"
    DURATION = "DURATION"
    DYN_LINES = "DYN_LINES"
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
    TSCN_NON_STRING_VALUE = "tscnNonStringValue"
    INSERT_LINES = "insert_lines"
    UPDATE_LINE = "update_line"
    @classmethod
    def _missing_(cls, value):
        return TEXT_TYPE.TSCN_NON_STRING_VALUE

ESCAPE_STR = "\\"
DOUBLE_ESCAPE_STR = "\\\\"
DUMMY_REPL = "REPL"

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("target_dir_path_str", help="target_dir_path", type=str)
arg_parser.add_argument("import_file_path_str", help="import_file_path", type=str)
args = arg_parser.parse_args()

def import_text_tsv(target_dir_path_str, import_file_path_str):
    target_dir_path = pathlib.Path(target_dir_path_str)
    import_file_path = pathlib.Path(import_file_path_str)

    with import_file_path.open(mode='r', encoding=FILE_ENCODING) as import_file:
        inserted_line_count_dict_dict = {}
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
                    case TEXT_TYPE.DURATION:
                        write_duration(target_dir_path, tsv_col_list)
                    case TEXT_TYPE.DYN_LINES:
                        write_dyn_lines(target_dir_path, tsv_col_list)
                    case TEXT_TYPE.LINES:
                        write_lines(target_dir_path, tsv_col_list)
                    case TEXT_TYPE.INSERT_LINES:
                        write_insert_lines(target_dir_path, tsv_col_list, inserted_line_count_dict_dict)
                    case TEXT_TYPE.UPDATE_LINE:
                        write_update_line(target_dir_path, tsv_col_list, inserted_line_count_dict_dict)
                    case _:
                        write_tscn_tagged_str(target_dir_path, tsv_col_list, temp_text_type)

# not used
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

def write_duration(root_path, tsv_col_list):
    target_path = root_path / tsv_col_list[0]
    with target_path.open(mode='r', encoding=FILE_ENCODING) as temp_file:
        file_text = temp_file.read()

    lines_str = TEXT_LIST_SEP.join(tsv_col_list[5:])

    tag_str = tsv_col_list[4]
    split_text_list = file_text.split(tag_str)
    if len(split_text_list) > 1:
        split_text_list[1] = re.sub(r'DURATION = \[[^\]]*\]', 'DURATION = [ ' + lines_str + ' ]', split_text_list[1], 1, re.DOTALL)
        file_text = tag_str.join(split_text_list)
        with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
            temp_file.write(file_text)

def write_dyn_lines(root_path, tsv_col_list):
    target_path = root_path / tsv_col_list[0]
    with target_path.open(mode='r', encoding=FILE_ENCODING) as temp_file:
        file_text = escape_escaped_double_quot(temp_file.read())

    lines_str = ""
    for temp_col in tsv_col_list[5:]:
        if temp_col == SOB.REPLACER.value:
            lines_str += SOB.STR.value
        elif temp_col == EOB.REPLACER.value:
            lines_str = lines_str.rstrip(TEXT_LIST_SEP)
            lines_str += EOB.STR.value + TEXT_LIST_SEP
        else:
            lines_str += '"' + temp_col + '"' + TEXT_LIST_SEP
    lines_str = lines_str.rstrip(TEXT_LIST_SEP)
    
    tag_str = tsv_col_list[4]
    split_text_list = file_text.split(tag_str)
    if len(split_text_list) > 1:
        split_text_list[1] = re.sub(r'\nDYN_LINES = \[[^\n]*\]\n', '\nDYN_LINES = [ ' + lines_str + ' ]\n', split_text_list[1], 1, re.DOTALL)
        file_text = tag_str.join(split_text_list)
        with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
            temp_file.write(escape_escaped_double_quot(file_text, True))

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
    is_non_text_type = (text_type == TEXT_TYPE.TSCN_NON_STRING_VALUE)
    target_path = root_path / tsv_col_list[0]
    with target_path.open(mode='r', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
        file_text = escape_escaped_double_quot(temp_file.read())
    
    tag_str = tsv_col_list[4]
    split_text_list = file_text.split(tag_str)
    if len(split_text_list) > 1:
        text_type_str = tsv_col_list[1]
        if is_non_text_type:
            new_line = '\n' + text_type_str + ' = ' + tsv_col_list[5]
            temp_pattern = r'\n' + text_type_str + ' = [^\n]*'
        else:
            new_line = '\n' + text_type_str + ' = "' + escape_escape_str(escape_LF(tsv_col_list[5], True)) + '"'
            temp_pattern = r'\n' + text_type_str + ' = "[^"]*"'
        
        if re.search(temp_pattern, split_text_list[1]) is None:
            split_text_list[1] = re.sub(DUMMY_REPL, new_line, DUMMY_REPL + split_text_list[1], 1)
        else:
            split_text_list[1] = re.sub(temp_pattern, new_line, split_text_list[1], 1, re.DOTALL)

        file_text = tag_str.join(split_text_list)

        if not is_non_text_type:
            file_text = escape_escaped_double_quot(file_text, True)
        
        with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
            temp_file.write(file_text)

def write_insert_lines(root_path, tsv_col_list, inserted_line_count_dict_dict):
    rel_path = tsv_col_list[0]
    target_path = root_path / rel_path
    with target_path.open(mode='r', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
        target_line_number = int(tsv_col_list[2])
        inserted_line_count = get_inserted_line_count(inserted_line_count_dict_dict, rel_path, target_line_number)

        lines = temp_file.readlines()
        insert_lines = tsv_col_list[4].split(LF.REPLACER.value)
        insert_line_cunt = len(insert_lines)
        for i in range(insert_line_cunt):
            insert_lines[i] = escape_TAB(insert_lines[i], True) + LF.STR.value
        add_inserted_line_count(inserted_line_count_dict_dict, rel_path, target_line_number, insert_line_cunt)

        i = target_line_number + inserted_line_count
        lines[i:i] = insert_lines

        with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
            temp_file.writelines(lines)

def write_update_line(root_path, tsv_col_list, inserted_line_count_dict_dict):
    rel_path = tsv_col_list[0]
    target_path = root_path / rel_path
    with target_path.open(mode='r', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
        target_line_number = int(tsv_col_list[2])
        inserted_line_count = get_inserted_line_count(inserted_line_count_dict_dict, rel_path, target_line_number)

        lines = temp_file.readlines()
        i = target_line_number + inserted_line_count
        lines[i] = lines[i].replace(escape_TAB(tsv_col_list[4], True), escape_TAB(tsv_col_list[5], True))

    with target_path.open(mode='w', encoding=FILE_ENCODING, newline=LF.STR.value) as temp_file:
        temp_file.writelines(lines)

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

def escape_TAB(str, do_reverse = False):
    old = TAB.STR.value
    new = TAB.REPLACER.value
    if do_reverse:
        old = TAB.REPLACER.value
        new = TAB.STR.value
    return str.replace(old, new)

def get_inserted_line_count(inserted_line_count_dict_dict, rel_path, target_line_number):
    if rel_path not in inserted_line_count_dict_dict:
        inserted_line_count_dict_dict[rel_path] = {}
    inserted_line_count = 0
    for k, v in inserted_line_count_dict_dict[rel_path].items():
        if target_line_number >= k:
            inserted_line_count += v
    return inserted_line_count

def add_inserted_line_count(inserted_line_count_dict_dict, rel_path, target_line_number, insert_line_cunt):
    if target_line_number not in inserted_line_count_dict_dict[rel_path]:
        inserted_line_count_dict_dict[rel_path][target_line_number] = 0
    inserted_line_count_dict_dict[rel_path][target_line_number] += insert_line_cunt

import_text_tsv(args.target_dir_path_str, args.import_file_path_str)
