from baseline.utils import Chunker


def test_chunker_even():
    """
    ensure the chunker returns the last element if there are no pairs
    """
    result = [x for x in Chunker([1, 2, 3, 4], 2)]
    assert result == [[1, 2], [3, 4]]


def test_chunker_odd():
    """
    ensure the chunker returns the last element if there are no pairs
    """
    result = [x for x in Chunker([1, 2, 3], 2)]
    assert result == [[1, 2], [3]]
