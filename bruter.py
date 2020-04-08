from itertools import combinations, product


def total_list_differences(li1: list, li2: list):
    if len(li1) != len(li2):
        return -1
    return sum([li1[i] != li2[i] for i in range(len(li1))])


def sequences_with_k_incorrect(k, correct_sequence, answer_options: tuple = (0, 1)):
    for positions_to_change in combinations(range(len(correct_sequence)), k):
        for replacement_for_position in product(*[answer_options]*len(positions_to_change)):
            replacement_for_position = [str(x) for x in replacement_for_position]
            if total_list_differences(
                    [correct_sequence[position] for position in positions_to_change],
                    replacement_for_position) != k:
                continue
            tmp = list(correct_sequence)[:]
            for i, position in enumerate(positions_to_change):
                tmp[position] = replacement_for_position[i]
            yield ''.join(tmp)


if __name__ == '__main__':
    CORRECT_SEQUENCE = '0001010111'
    num = 3
    for combo in list(sequences_with_k_incorrect(num, CORRECT_SEQUENCE)):
        print(combo)
        print(CORRECT_SEQUENCE)
        a = 0
        for i in range(len(combo)):
            if combo[i] != CORRECT_SEQUENCE[i]:
                a += 1
                print('|', end='')
            else:
                print(' ', end='')
        assert a == num
        print()
        print()
