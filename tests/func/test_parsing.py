def test_get_task_metadata(task_metadata_fixture):
    task_metadata, expected = task_metadata_fixture
    assert task_metadata.cmid == expected['cmid']
    assert task_metadata.sesskey == expected['sesskey']
