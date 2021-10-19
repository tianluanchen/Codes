
#    Author:        tianluanchen
#    date:          2021/10/19
#    description:   入口程序

from api.data_access import init_file
from web_panel.web import start_web


if __name__ == '__main__':
    init_file()
    start_web()

