hash_string = input() + 'xx'
first_index = 0
second_index = 0
current_index = 0
delta = 0
first_flag = False
final_string = ''
second_flag = False
for index in range(len(hash_string) - 1):
    if 'A' <= hash_string[index] <= 'Z' and (not first_flag):
        first_index = index
        first_flag = True
        final_string += hash_string[index]

    if '0' <= hash_string[index] < '9' and first_flag and not(second_flag):
        second_index = index + 1
        delta = second_index - first_index
        current_index = second_index + delta
        final_string += hash_string[index + 1]
        second_flag = True

    if index == current_index and first_flag and second_flag:
        final_string += hash_string[index]
        if hash_string[index] == '.':
            break
        current_index += delta

print(final_string)