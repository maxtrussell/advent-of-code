import re
import sys

def make_rules(rules):
    valid_numbers = set()
    field_rules = {}
    pattern = '(\d+)-(\d+)'
    for rule in rules:
        name = rule.split(':')[0]
        field_rules[name] = set()
        for minimum, maximum in re.findall(pattern, rule):
            field_rules[name] |= {x for x in range(int(minimum), int(maximum)+1)}
            valid_numbers |= field_rules[name]
    return valid_numbers, field_rules

def error_rate(tickets, valid_numbers):
    invalids = []
    valid_tickets = []
    for ticket in tickets:
        for val in ticket:
            if val not in valid_numbers:
                invalids.append(val)
    return sum(invalids)

def validate_ticket(ticket, valid_numbers):
    for val in ticket:
        if val not in valid_numbers:
            return False
    return True

def get_fields(tickets, field_rules):
    fields = [None] * len(field_rules)
    # Use process of elimination until all fields are assigned
    while None in fields:
        # Come up with a set of errors per position
        field_errors = {}
        # dicts are ordered by default in python3
        for name, valid_numbers in field_rules.items():
            if name in fields:
                # skip over assigned fields
                continue
            field_errors[name] = set()
            for ticket in tickets:
                for i in range(len(ticket)):
                    if ticket[i] not in valid_numbers:
                        field_errors[name].add(i)

        # Assign fields that only have a single position without an error
        field_numbers = {i for i,val in enumerate(fields) if val == None}
        for field, errors in field_errors.items():
            possible_fields = field_numbers - errors
            if len(possible_fields) == 1:
                fields[possible_fields.pop()] = field

    return fields

def multiply_departures(my_ticket, fields):
    product = 1
    for i in range(len(fields)):
        if fields[i].startswith('departure'):
            product *= my_ticket[i]
    return product

def parse_ticket(ticket):
    return [int(x) for x in ''.join(ticket).split(',')]
        

# Parse input
with open(sys.argv[1], 'rt') as f:
    rules, my_ticket, other_tickets = f.read().split('\n\n')

# Not the cleanest logic, but I was feeling lazy
rules = rules.split('\n')
my_ticket = parse_ticket(''.join(my_ticket).split('\n')[1:])
other_tickets = [parse_ticket(x) for x in ''.join(other_tickets).split('\n')[1:] if x]

# Part 1
valid_numbers, field_rules = make_rules(rules)
error_rate = error_rate(other_tickets, valid_numbers)
print(f'Part 1: {error_rate}')

# Part 2
valid_tickets = [t for t in other_tickets if validate_ticket(t, valid_numbers)]
fields = get_fields(valid_tickets, field_rules)
product = multiply_departures(my_ticket, fields)
print(f'Part 2: {product}')
