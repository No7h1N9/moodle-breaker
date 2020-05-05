def test_find_best_own_url(summary_parser):
    parser, expected = summary_parser
    assert parser.best_attempt_id() == expected['best_attempt_id']


def test_parse_plain_text_answers(finished_attempt_parser):
    parser, expected = finished_attempt_parser
    assert parser.parse_answers() == expected['answers']


def test_parse_task_metadata(task_metadata):
    mt, expected = task_metadata
    assert mt.cmid == expected['cmid']
    assert mt.sesskey == expected['sesskey']
