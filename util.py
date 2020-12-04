def parse_file_as_list(file):
    return [num.rstrip('\n') for num in open(file=file, newline='\n')]
