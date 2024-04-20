import numpy as np

problem = [[1,0,0,0],[1,0,1,0],[0,-1,0,0],[0,0,0,-1],[0,0,1,1]]


def create_formula(problem):
    string = ''
    for row in problem:
        temp = []
        counter = 1
        for element in row:
            if element == 1:
                temp.append('x' + str(counter))
            elif element == -1:
                temp.append('not x' + str(counter))
            counter += 1

        if len(temp) == 1:
            string += '(' + temp[0] + ')' + 'and'
        elif len(temp) > 1:
            string += '(' + ' or '.join(temp) + ')' + 'and'
    return string[:-3]


create_formula(problem)