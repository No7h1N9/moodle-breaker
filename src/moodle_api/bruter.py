from itertools import combinations, product


def total_list_differences(li1: tuple, li2: tuple) -> int:
    result = 0
    for i in range(len(li1)):
        if li1[i] != li2[i]:
            result += 1
    return result


def sequences_with_k_incorrect(k, correct_sequence, answer_options: tuple = ("0", "1")):
    for positions_to_change in combinations(range(len(correct_sequence)), k):
        for replacement_for_position in product(
            *[answer_options] * len(positions_to_change)
        ):
            if (
                total_list_differences(
                    tuple(
                        [correct_sequence[position] for position in positions_to_change]
                    ),
                    replacement_for_position,
                )
                != k
            ):
                continue
            tmp = list(correct_sequence)[:]
            for i, position in enumerate(positions_to_change):
                tmp[position] = replacement_for_position[i]
            yield "".join(tmp)


def all_possible_incorrect_attempts(
    correct_sequence, answer_options: tuple = ("0", "1")
):
    if not correct_sequence:
        return {}
    result = {}
    for k in range(1, len(correct_sequence)):
        result[k] = list(
            sequences_with_k_incorrect(
                k, correct_sequence, answer_options=answer_options
            )
        )
    return result


def brute(
    known_attempts,
    total_questions,
    answer_options: tuple = ("0", "1"),
    candidates: list = None,
):
    results = []
    if not candidates:
        candidates = product(*[answer_options] * total_questions)
    for candidate in candidates:
        candidate = "".join(candidate)
        to_check = all_possible_incorrect_attempts(
            candidate, answer_options=answer_options
        )
        correct_assumption = True
        for attempt_seq, errors_number in known_attempts:
            if attempt_seq not in to_check[errors_number]:
                correct_assumption = False
                break
        if correct_assumption:
            results.append(candidate)
    return results


if __name__ == "__main__":
    # CORRECT_SEQUENCE = '0001010111'
    # num = 3
    """print(brute([ ('0001000110', 2), ('0101010101', 2), ('0111010111', 2),
    ('0101010111', 1), ('0001000111', 1),

    ], 10, candidates=['0001010111', '0101000111', '0101010110'] ))
    """
    """
    corr = '00000'
    print(brute([
        ('00011', 2),
        ('00110', 2),
        ('01100', 2),
        ('11000', 2),
        ('01010', 2),
    ], 5))
    """
    print(
        brute(
            [
                # Алиса
                # ('0110111100', 3),
                # ('0110100101', 2),
                # Я
                ("0111100100", 2),
                # Галя
                ("0111110100", 1),
            ],
            10,
            candidates=[
                "0011110100",
                "0101110100",
                "0110110100",
                "0111010100",
                "0111100100",
                "0111110000",
                "0111110101",
                "0111110110",
                "0111111100",
                "1111110100",
            ],
        )
    )
