import sys

def first_bus(start, buses):
    """ Returns (min_wait, bus) tuple """
    # min uses the first value of the tuple by default
    return min([((bus - (start % bus)) % bus, bus) for bus in buses])

def consecutive_buses(buses):
    """
    Iterate over buses, creating an aggregate bus.

    Aggregate bus is the first time that all of the iterated buses leave consecutively,
    and it is cyclical by the product of the all the iterated buses.

    The aggregate bus is computed by finding a time where the current bus leaves i
    minutes after the prior aggregate bus.

    Because all of the buses are mutually prime, the step is the product of all
    iterated buses.
    """
    aggregate_bus = buses[0]
    step = 1
    for i, bus in enumerate(buses):
        if bus == 0:
            continue

        j = 0
        t = aggregate_bus + step * j
        while (t + i) % bus != 0:
            t = aggregate_bus + step * j
            j += 1
        aggregate_bus = t

        step *= bus
    return aggregate_bus


input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'rt') as f:
    start = int(f.readline())
    notes = f.readline()

buses_with_oos = list(map(lambda c: int(c) if c != 'x' else 0, notes.split(',')))
buses = [b for b in buses_with_oos if b > 0]

# Part 1
min_wait, bus = first_bus(start, buses)
print(f'Part 1: {min_wait * bus}')

# Part 2
t = consecutive_buses(buses_with_oos)
print(f'Part 2: {t}')
