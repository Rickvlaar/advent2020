# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.

import string
passport_file = 'input_files/day_4.txt'


def check_passports():
    required_fields = {'byr': val_byr,
                       'iyr': val_iyr,
                       'eyr': val_eyr,
                       'hgt': val_hgt,
                       'hcl': val_hcl,
                       'ecl': val_ecl,
                       'pid': val_pid}

    raw_passport_list = [passport.split(' ') for passport in [num.replace('\n', ' ') for num in open(file=passport_file).read().split('\n\n') if not num.endswith('\n')]]
    passport_dicts = [{key_val_str.split(':')[0]: key_val_str.split(':')[1] for key_val_str in passport} for passport in raw_passport_list]
    return sum([1 for passport in passport_dicts if set(required_fields.keys()) <= set(passport.keys()) and all([required_fields[key](value) for key, value in passport.items() if key != 'cid'])])


def val_byr(byr):
    return byr.isdigit() and 1920 <= int(byr) <= 2002


def val_iyr(iyr):
    return iyr.isdigit() and 2010 <= int(iyr) <= 2020


def val_eyr(eyr):
    return eyr.isdigit() and 2020 <= int(eyr) <= 2030


def val_hgt(hgt):
    return (hgt.endswith('cm') and len(hgt) == 5 and 150 <= int(hgt[0:3]) <= 193) or  \
           (hgt.endswith('in') and len(hgt) == 4 and 59 <= int(hgt[0:2]) <= 76)


def val_hcl(hcl):
    return len(hcl) == 7 and hcl.startswith('#') and set(hcl[1:]).issubset(string.hexdigits)


def val_ecl(ecl):
    return ecl in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def val_pid(pid):
    return len(pid) == 9 and pid.isdigit()
