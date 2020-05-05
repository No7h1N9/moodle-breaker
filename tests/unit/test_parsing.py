from moodle_api.problem import Task


def test_get_task_metadata(task_metadata_fixture):
    task_metadata, expected = task_metadata_fixture
    assert task_metadata.cmid == expected['cmid']
    assert task_metadata.sesskey == expected['sesskey']


def test_find_best_own_url(task_obj):
    task_obj, params = task_obj     # type: (Task, dict)
    assert task_obj.best_own_url == params['best_own_url']
