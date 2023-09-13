from excel.funcs import *


def main():
    load_schedule('https://lycu1580.mskobr.ru/files/schedule/rasp2k_2.xlsx')
    make_schedule()


if __name__ == '__main__':
    main()
