# Схема Горнера
import math


def getDeviders(n):
    n = abs(n)
    result = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            result.append(i)
            result.append(i // - 1)
            result.append(n // i)
            result.append(n // i // - 1)
    result.sort(key=abs)
    return result


def getKofExpression(exp):
    old_k = []
    f_expr = exp.split()
    for i in range(len(f_expr)):
        if i % 2 == 0 and i != len(f_expr) - 1:
            if i != 0:
                exp_part = [f_expr[i - 1]] + f_expr[i].split('*')
                if exp_part[1] == '({x})':
                    if exp_part[-1] == '({x})':
                        old_k.append([int(exp_part[0] + '1'), 1])
                    else:
                        old_k.append([int(exp_part[0] + '1'), int(exp_part[-1])])
                else:
                    if exp_part[-1] == '({x})':
                        old_k.append([int(exp_part[0] + exp_part[1]), 1])
                    else:
                        old_k.append([int(exp_part[0] + exp_part[1]), int(exp_part[-1])])
            elif i == 0:
                exp_part = f_expr[i].split('*')
                if exp_part[0] == '({x})':
                    old_k.append([1, int(exp_part[-1])])
                else:
                    if exp_part[-1] == '({x})':
                        old_k.append([int(exp_part[0]), 1])
                    else:
                        old_k.append([int(exp_part[0]), int(exp_part[-1])])
        elif i == len(f_expr) - 1 and len([f_expr[i - 1]] + f_expr[i].split('*')) == 2:
            old_k.append([int(f_expr[i - 1] + f_expr[i]), 0])
    return old_k


def getNewRoot(oldExpression):
    deviders = getDeviders(int(oldExpression.split()[-1]))  # все делители свободного коэффициента
    suitable_root = 0  # подходящий корень
    for x in deviders:
        if eval(oldExpression.format(x = x)) == 0:
            suitable_root = x
            break
    new_K = [] # новые коэффициенты
    new_exp = '' # новое выражение
    if suitable_root != 0:  # если найден хотя бы один подходящий корень
        old_K = getKofExpression(oldExpression)  # получаем старые коэффициенты
        new_K.append([old_K[0][0], old_K[0][1]])
        for i in range(1, len(old_K)):
            new_K.append([suitable_root * new_K[-1][0] + old_K[i][0], old_K[i][1]])
        for i in range(len(new_K) - 1):
            if new_K[i][0] < 0:
                new_exp += ' - '
            elif i != 0:
                new_exp += ' + '
            new_exp += str(abs(new_K[i][0]))
            if i < len(new_K) - 2:
                new_exp += '*({x})'
                if i < len(new_K) - 3:
                    new_exp += '**' + str(old_K[i][1] - 1)
    new_exp = new_exp if suitable_root != 0 else oldExpression
    return [suitable_root, new_exp]


root = [0, input().replace('x', '({x})')] # текущий корень
roots = []  # все корни уравнения
while True:
    root = getNewRoot(root[1])
    if root[0] == 0:
        break
    else:
        roots.append(root[0])
final_exp = ''
for i in range(len(roots)):
    final_exp += '(x '
    if roots[i] < 0:
        final_exp += '+ ' + str(abs(roots[i])) + ')'
    elif roots[i] > 0:
        final_exp += '- ' + str(abs(roots[i])) + ')'
final_exp += ('(' + root[1].replace('*({x})', 'x').replace('1x', 'x') + ')') if root[1] != '1' else ''
print(final_exp)