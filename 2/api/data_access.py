from pathlib import Path
from setting import FILE_PATH, RECORDS
import json
from util.Record import Record
import time


# 初始化存储文件


def init_file():
    data_file = Path(FILE_PATH)
    if not data_file.is_file():
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            RECORDS['creation_time'] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            RECORDS['update_time'] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            f.write(json.dumps(RECORDS))


def save(new_record: Record):
    new_record = new_record.to_dict()
    records = read()
    records['lanzou'].append(new_record)
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(json.dumps(records))
    return True


def read():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        records = json.load(f)
    return records


if __name__ == '__main__':
    init_file()
    new_record = Record("1", "mp3", "1", "1", "https://wws.lanzoui.com/iaVesvilm1i", "1", "1", "1", )
    if save(new_record):
        print("success")
