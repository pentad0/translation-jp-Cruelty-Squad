from enum import Enum

import argparse
import os
import pathlib
import re

FILE_ENCODING = "utf-8"
TSV_SEP = "\t"
EOL = "[EOL]"

class FILE_SUFFIX(Enum):
    GD = ".gd"
    JSON = ".json"
    TSCN = ".tscn"

class SOB(Enum):
    STR = "[ "
    REPLACER = "[SOB]"

class EOB(Enum):
    STR = " ]"
    REPLACER = "[EOB]"

class LF(Enum):
    STR = "\n"
    REPLACER = "\\n"

class ESCAPED_DOUBLE_QUOTE(Enum):
    STR = "\\\""
    REPLACER = "￥”"

class TEXT_TYPE(Enum):
    GD = "gd"
    JSON = "json"
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

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("target_dir_path_str", help="target_dir_path", type=str)
arg_parser.add_argument("export_file_path_str", help="export_file_path", type=str)
args = arg_parser.parse_args()

def export_text_tsv(target_dir_path_str, export_file_path_str):
    target_dir_path = pathlib.Path(target_dir_path_str)
    export_file_path = pathlib.Path(export_file_path_str)
    
    tsv_line_cols_list = []
    search_dir(target_dir_path, target_dir_path, tsv_line_cols_list)
    tsv_line_cols_list.sort(key=lambda l: (l[1], l[0]))

    tsv_line_list = []
    for tsv_col_list in tsv_line_cols_list:
        tsv_line_list.append(TSV_SEP.join(tsv_col_list))

    with export_file_path.open(mode='w', encoding=FILE_ENCODING) as export_file:
        export_file.write(LF.STR.value.join(tsv_line_list) + LF.STR.value)

def search_dir(root_path, target_path, tsv_line_cols_list):
    if target_path.is_file():
        file_suffix = FILE_SUFFIX(target_path.suffix)
        if file_suffix == FILE_SUFFIX.GD:
            read_gd(root_path, target_path, tsv_line_cols_list)
        elif file_suffix == FILE_SUFFIX.JSON:
            read_json(root_path, target_path, tsv_line_cols_list)
        elif file_suffix == FILE_SUFFIX.TSCN:
            read_tscn(root_path, target_path, tsv_line_cols_list)
    elif target_path.is_dir():
        for temp_path in target_path.iterdir():
            search_dir(root_path, temp_path, tsv_line_cols_list)

def read_gd(root_path, target_path, tsv_line_cols_list):
    with target_path.open(mode='r', encoding=FILE_ENCODING) as temp_file:
        temp_lines = temp_file.readlines()
        for i, temp_line in enumerate(temp_lines):
            temp_line = escape_escaped_double_quot(temp_line)
            for j, temp_match in enumerate(re.finditer(r'"([^"]*)"', temp_line)):
                temp_str = escape_escaped_double_quot(temp_match.group(1), True);
                tsv_col_list = init_tsv_col_list(root_path, target_path, TEXT_TYPE.GD.value, str(i), str(j))
                tsv_col_list.append(temp_str)
                tsv_col_list.append(temp_str)
                tsv_col_list.append(EOL)
                tsv_line_cols_list.append(tsv_col_list)

def read_json(root_path, target_path, tsv_line_cols_list):
    with target_path.open(mode='r', encoding=FILE_ENCODING) as temp_file:
        file_text = temp_file.read()
        temp_match = re.search(r'"name": "([^"]*)".+"objectives": \[([^\]]*)\].+"description": "([^"]*)"', file_text, re.DOTALL)
        if temp_match != None:
            tsv_col_list = init_tsv_col_list(root_path, target_path, TEXT_TYPE.JSON.value)
            tsv_col_list.append(temp_match.group(1))
            for temp_match2 in re.finditer(r'"([^"]*)"', temp_match.group(2)):
                tsv_col_list.append(temp_match2.group(1))
            tsv_col_list.append(temp_match.group(3))
            tsv_col_list.append(EOL.REPLACER)
            tsv_line_cols_list.append(tsv_col_list)

def read_tscn(root_path, target_path, tsv_line_cols_list):
    with target_path.open(mode='r', encoding=FILE_ENCODING) as temp_file:
        file_text = escape_escaped_double_quot(temp_file.read())

        top_str = '[node '
        for temp_str in file_text.split('\n\n' + top_str):
            temp_str = top_str + temp_str
            for temp_match in re.finditer(r'(\[node name=[^\]]*\]).*?\nDYN_LINES = \[([^\n]*)\]\n', temp_str, re.DOTALL):
                tsv_col_list = init_tsv_col_list(root_path, target_path, TEXT_TYPE.DYN_LINES.value)
                tsv_col_list.append(escape_escaped_double_quot(temp_match.group(1), True))
                for temp_match2 in re.finditer(r'\[([^\]]*)\]', temp_match.group(2)):
                    tsv_col_list.append(SOB.REPLACER.value)
                    for temp_match3 in re.finditer(r'"([^"]*)"', temp_match2.group(1)):
                        tsv_col_list.append(escape_escaped_double_quot(temp_match3.group(1), True))
                    tsv_col_list.append(EOB.REPLACER.value)
                tsv_col_list.append(EOL)
                tsv_line_cols_list.append(tsv_col_list)

            for temp_match in re.finditer(r'(\[node name=[^\]]*\]).*?\nLINES = \[([^\]]*)\]', temp_str, re.DOTALL):
                tsv_col_list = init_tsv_col_list(root_path, target_path, TEXT_TYPE.LINES.value)
                tsv_col_list.append(escape_escaped_double_quot(temp_match.group(1), True))
                for temp_match2 in re.finditer(r'"([^"]*)"', escape_LF(temp_match.group(2))):
                    tsv_col_list.append(escape_escaped_double_quot(temp_match2.group(1), True))
                tsv_col_list.append(EOL)
                tsv_line_cols_list.append(tsv_col_list)

            for temp_text_type in [
                TEXT_TYPE.DIALOG_TEXT,
                TEXT_TYPE.IMPLANT_NAME,
                TEXT_TYPE.LEVEL_NAME,
                TEXT_TYPE.LINE,
                TEXT_TYPE.LINE2,
                TEXT_TYPE.MESSAGE,
                TEXT_TYPE.NPC_NAME,
                TEXT_TYPE.OVERRIDE_NAME,
                TEXT_TYPE.TEXT,
                TEXT_TYPE.VALUE,
            ]:
                text_type_str = temp_text_type.value
                for temp_match in re.finditer(r'(\[node name=[^\]]*\]).*?\n' + text_type_str + ' = "([^"]*)"', temp_str, re.DOTALL):
                    tsv_col_list = init_tsv_col_list(root_path, target_path, text_type_str)
                    tsv_col_list.append(escape_escaped_double_quot(temp_match.group(1), True))
                    tsv_col_list.append(escape_LF(escape_escaped_double_quot(temp_match.group(2), True)))
                    tsv_col_list.append(EOL)
                    tsv_line_cols_list.append(tsv_col_list)

def init_tsv_col_list(root_path, target_path, text_type, index_0 = "", index_1 = ""):
    tsv_col_list = []
    tsv_col_list.append(os.path.relpath(target_path, root_path))
    tsv_col_list.append(os.path.relpath(text_type))
    tsv_col_list.append(index_0)
    tsv_col_list.append(index_1)
    return tsv_col_list

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

export_text_tsv(args.target_dir_path_str, args.export_file_path_str)
