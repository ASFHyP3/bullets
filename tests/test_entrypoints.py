def test_bullets(script_runner):
    ret = script_runner.run('bullets', '-h')
    assert ret.success


def test_sendit(script_runner):
    ret = script_runner.run('sendit', '-h')
    assert ret.success
