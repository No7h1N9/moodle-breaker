def test_get_task_metadata(task_metadata_fixture):
    task_metadata, cmid, sesskey = task_metadata_fixture
    assert task_metadata.cmid == cmid
    assert task_metadata.sesskey == sesskey
