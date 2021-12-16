import fileinput
from functools import reduce
import operator

"""
Code is pretty ugly, no time to clean :)

I should've consumed bits, rather than tracking subpacket lengths
"""

ops = {
    0: sum,
    1: lambda xs: reduce(operator.mul, xs),
    2: min,
    3: max,
    5: lambda xs: int(xs[0] > xs[1]),
    6: lambda xs: int(xs[0] < xs[1]),
    7: lambda xs: int(xs[0] == xs[1]),
}

def parse_packet(binary_packet):
    version = int(binary_packet[:3], 2)
    id = int(binary_packet[3:6], 2)
    if id == 4:
        # Literal value packet
        binary_packet = binary_packet[6:]
        num_groups = 0
        value = ''
        while True:
            i = num_groups * 5
            value += binary_packet[i+1:i+5]
            if binary_packet[i] == '0':
                # We've found the last group
                num_groups += 1
                break
            num_groups += 1
        value = int(value, 2)
        length = 6 + (5 * num_groups)
        return version, length, value

    version_sum = 0
    version_sum += version

    # Operator packet
    length_type_id = int(binary_packet[6], 2)
    values = []
    if length_type_id == 0:
        # length in bits of sub packets
        subpackets_length = int(binary_packet[7:22], 2)
        packet_length = 22 + subpackets_length
        processed_lengths = 0
        binary_packet = binary_packet[22:]
        while processed_lengths < subpackets_length:
            sver, sl, sval = parse_packet(binary_packet[:])
            processed_lengths += sl
            binary_packet = binary_packet[sl:]
            version_sum += sver
            values.append(sval)
    else:
        assert length_type_id == 1
        # number of sub packets immediately contained
        num_subpackets = int(binary_packet[7:18], 2)
        packet_length = 18
        binary_packet = binary_packet[18:]
        for _ in range(num_subpackets):
            sver, sl, sval = parse_packet(binary_packet[:])
            binary_packet = binary_packet[sl:]
            version_sum += sver
            packet_length += sl
            values.append(sval)

    return version_sum, packet_length, ops[id](values)


packet = [l.strip() for l in fileinput.input()][0]
binary_packet = bin(int(packet, 16))[2:]
binary_packet = '0' * ((4 * len(packet)) - len(binary_packet)) + binary_packet
version, _, value = parse_packet(binary_packet)
print(f'{version=}, {value=}')
