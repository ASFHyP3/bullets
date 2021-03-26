def test_bullets(script_runner):
    ret = script_runner.run('bullets', '-h')
    assert ret.success


def test_sendit(script_runner):
    ret = script_runner.run('sendit', '-h')
    assert ret.success


def test_postit(script_runner):
    ret = script_runner.run('postit', '-h')
    assert ret.success
