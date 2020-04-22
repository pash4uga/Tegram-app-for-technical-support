import re

def formatStr(string):
    try:
        nf = string.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
        if (len(nf) == 11 and nf.isdigit() and (nf[0]=="7" or nf[0]=="8")):
            return nf
        elif (len(nf) == 12 and nf[0:2]=="+7"):
            return nf
        elif (len(nf) == 6 and nf.isdigit()):
            code = ['+73952']
            code.extend(nf)
            a = ''.join(code)
            return a
        elif (len(nf) == 10 and nf.isdigit()):
            l = [nf]
            code = ['+7']
            code.extend(l)
            a = ''.join(code)
            return a
    except:
        return False
        pass


def inn_ctrl_summ(nums, type):
    """
    Подсчет контрольной суммы
    """
    inn_ctrl_type = {
        'n2_12': [7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_12': [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_10': [2, 4, 10, 3, 5, 9, 4, 6, 8],
    }
    n = 0
    l = inn_ctrl_type[type]
    for i in range(0, len(l)):
        n += nums[i] * l[i]
    return n % 11 % 10


def inn_check(inn):  #Проверка ИНН на корректность в соответствии с алгоритмом, описанным по ссылке: https://ru.wikipedia.org/wiki/Контрольное_число
    try:
        sinn = str(inn)
        nums = [int(x) for x in sinn]
        if len(sinn) == 10:
            n1 = inn_ctrl_summ(nums, 'n1_10')
            return True
        elif len(sinn) == 12:
            n2 = inn_ctrl_summ(nums, 'n2_12')
            n1 = inn_ctrl_summ(nums, 'n1_12')
            return True
        else:
            return False
    except:
        return False
        pass

