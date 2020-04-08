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


def all_possible_incorrect_attempts(correct_sequence, answer_options: tuple = (0, 1)):
    if not correct_sequence:
        return {}
    result = {}
    for k in range(1, len(correct_sequence)):
        result[k] = list(sequences_with_k_incorrect(k, correct_sequence, answer_options=answer_options))
    return result


if __name__ == '__main__':
    CORRECT_SEQUENCE = '0001010111'
    num = 3
