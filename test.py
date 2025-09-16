from cutups import TextChunk


def test_text_chunk_splits_hyphenated_lines_correctly() -> None:
    tc = TextChunk("abcdefgh", 4)

    assert tc.lines == ["abc-", "def-", "gh"]


def test_text_chunk_splits_non_hyphenated_lines_correctly() -> None:
    tc = TextChunk("this is really quite good", 12)

    assert tc.lines == ["this is", "really", "quite good"]


def test_text_chunk_can_be_split() -> None:
    tc = TextChunk(
        (
            "this is really quite good, but you don't need to worry about that"
            ", so try to remain relaxed for the time being!"
        ),
        20,
    )

    #assert False, str(tc.lines)
    assert False, str(tc.split(3, 2))
