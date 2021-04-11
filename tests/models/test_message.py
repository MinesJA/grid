from grid.models.message import AddSibling


def test_string():
    # Should output __str__ based on class
    # and attributes
    assert 1 == 2
    addSib = AddSibling('sender', 'sib', True)
    addSib.__str__()


def test_equality():
    # should be equal with equal
    # class and equal id
    assert 1 == 2


def test_serialize():
    # Each message should be serializable
    # may need sepereate test for each message
    # as they all have
    assert 1 == 2
