import pytest
from treeva.analysis.treesitter.grammars import get_parser, _LANGUAGES

@pytest.mark.parametrize("language", list(_LANGUAGES.keys()))
def test_get_parser_returns_parser_for_every_registered_language(language):
    parser = get_parser(language)
    assert parser is not None

@pytest.mark.parametrize("language", list(_LANGUAGES.keys()))
def test_get_parser_is_cached(language):
    first = get_parser(language)
    second = get_parser(language)
    assert first is second  # same object — confirms no rebuild per call

def test_get_parser_rejects_unknown_language():
    with pytest.raises(KeyError):
        get_parser("cobol")