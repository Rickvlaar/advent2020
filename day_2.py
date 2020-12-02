import util

password_file = 'input_files/day_2.txt'


def check_passwords():
    password_file_list = util.parse_file_as_list(file=password_file)
    policy_password_lists = [line.split(':') for line in password_file_list]
    correct_password_count = 0
    for policy, password in policy_password_lists:
        num_range, char = policy.split(' ')
        min_count, max_count = num_range.split('-')
        if int(min_count) <= password.count(char) <= int(max_count):
            correct_password_count += 1
    print(correct_password_count)


def check_passwords_part_2():
    password_file_list = util.parse_file_as_list(file=password_file)
    policy_password_lists = [line.split(':') for line in password_file_list]
    correct_password_count = 0
    for policy, password in policy_password_lists:
        password = password.strip()
        num_range, char = policy.split(' ')
        char_index_1, char_index_2 = num_range.split('-')
        a = password[int(char_index_1) - 1]
        b = password[int(char_index_2) - 1]
        if (a == char and b != char) or (b == char and a != char):
            correct_password_count += 1
    print(correct_password_count)