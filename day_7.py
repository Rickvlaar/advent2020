import util

bag_file = 'input_files/day_7.txt'


def tassies():
    bag_rules = [rule.replace('bags', '').replace('bag', '') for rule in util.parse_file_as_list(bag_file)]
    return {pappies.strip(): {kiddo[3:].strip(): kiddo[1] for kiddo in kiddies.split(',')} for pappies, kiddies in [rule.strip('.').split('contain') for rule in bag_rules]}


def check_gouwe_tassies():
    alle_tassies = tassies()
    alle_geschikte_tassies = set()
    for mamatassie, kindertassies in alle_tassies.items():
        if tassie_in_tassie(kindertassies, alle_tassies):
            alle_geschikte_tassies.add(mamatassie)
    return alle_geschikte_tassies


def tassie_in_tassie(kindertassies, alle_tassies):
    if kindertassies:
        if 'shiny gold' in kindertassies.keys():
            return True
        for kindermoeder in kindertassies.keys():
            if 'other' not in kindermoeder:
                found = tassie_in_tassie(alle_tassies.get(kindermoeder), alle_tassies)
                if found:
                    return True


def tassie_teller():
    alle_tassies = tassies()
    shiny_gold_bag = alle_tassies.get('shiny gold')
    return kindertassie_teller(shiny_gold_bag, alle_tassies, 0, 1)


def kindertassie_teller(kindertassies, alle_tassies, tassie_count, tassie_multiplier):
    tassie_count += sum([tassie_multiplier * int(value) for value in kindertassies.values() if value.isdigit()])
    if kindertassies:
        for kindermoeder, multiplier in kindertassies.items():
            if 'other' not in kindermoeder:
                tassie_count = kindertassie_teller(alle_tassies.get(kindermoeder), alle_tassies, tassie_count, tassie_multiplier * int(multiplier))
    return tassie_count
