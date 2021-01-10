def test_bullets(script_runner):
    ret = script_runner.run('bullets', '-h')
    assert ret.success
