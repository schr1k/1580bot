from excel.funcs import *


def main():
    load_schedule('https://docs.google.com/spreadsheets/d/1-M70uv_a6ufQFZUh03MD8Wi_Fnx35AUB7yFAAF5Br5Q/export?format=xlsx')
    make_schedule()


if __name__ == '__main__':
    main()
