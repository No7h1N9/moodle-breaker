def test_get_task_metadata(task_metadata_fixture):
    assert task_metadata_fixture.cmid == '43122'
    assert task_metadata_fixture.sesskey == 'su2AAGAxZ5'
