import amino_acids_logic as game


def test_get_property_charge_positive():
    assert game.get_property("K", "charge") == "positive"
    assert game.get_property("R", "charge") == "positive"
    assert game.get_property("H", "charge") == "positive"


def test_get_property_charge_negative():
    assert game.get_property("D", "charge") == "negative"
    assert game.get_property("E", "charge") == "negative"


def test_get_property_polarity():
    assert game.get_property("S", "polarity") == "polar"
    assert game.get_property("V", "polarity") == "nonpolar"


def test_aromatic_flag():
    assert game.get_property("F", "aromatic") == "aromatic"
    assert game.get_property("W", "aromatic") == "aromatic"
    assert game.get_property("Y", "aromatic") == "aromatic"
    assert game.get_property("A", "aromatic") == "non-aromatic"


def test_check_answer_correct_case_insensitive():
    assert game.check_answer("K", "charge", "Positive")
    assert game.check_answer("k", "charge", "positive")  # lower code is ok


def test_check_answer_incorrect():
    assert not game.check_answer("D", "charge", "positive")
    assert not game.check_answer("V", "polarity", "polar")


def test_hydrophobicity():
    # hydrophobic examples
    for code in ["A", "V", "L", "I", "M", "F", "W", "Y", "C"]:
        assert game.get_property(code, "hydrophobicity") == "hydrophobic"
    # hydrophilic examples
    for code in ["R", "N", "D", "Q", "E", "K", "H", "S", "T", "G", "P"]:
        assert game.get_property(code, "hydrophobicity") == "hydrophilic"
