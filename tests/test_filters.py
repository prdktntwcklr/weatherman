def test_strftime(jinja):
    input = '2021-02-03T03:42+00:00'

    assert jinja.filters['strftime'](input) == '2021-02-03 03:42'
