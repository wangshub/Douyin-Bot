import xlrd
import random


def get_random_keyword(filename):
    """
    get random row of filename
    :param filename:
    :return:
    """
    try:
        with xlrd.open_workbook(filename) as data:
            table = data.sheets()[0]
            data_list = []
            data_list.extend(table.col_values(0))
            return data_list[random.randint(0, len(data_list))]
    except Exception as error:
        print(Exception)
        return 'BRAVO'


if __name__ == '__main__':
    reply = get_random_keyword('../reply/keyword.xlsx')
    print(reply)