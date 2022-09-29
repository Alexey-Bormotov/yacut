from string import punctuation


def calculate_regexp(string):
    for sign in punctuation:
        if sign in string:
            string = string.replace(sign, '\\' + sign, 1)
    return r'[' + string + r']+'
