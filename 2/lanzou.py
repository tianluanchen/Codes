from setting import VERSION,FILE_PATH,BANNER
from data_access import init_file
from web import start_web

if __name__ == '__main__':
    init_file()
    start_web()

