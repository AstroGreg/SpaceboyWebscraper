def unique_in_order(iterable):
    answer = []
    for item in iterable:
        if(len(answer) == 0 or answer[len(answer)-1] is not item):
            answer.append(item)
    return answer

print(unique_in_order('AAAABBBCCDAABBB'))
print(unique_in_order('ABBCcAD'))
print(unique_in_order([1,2,2,3,3]))
print(unique_in_order(['D', 'A', 'c', 'B', 'C']))