import io
from contextlib import redirect_stdout
from unittest import mock


def play(func, inputs, *args):
    feed = iter(inputs)

    def fake_input(prompt=""):
        print(prompt, end="")
        try:
            return next(feed)
        except StopIteration:
            raise RuntimeError("program asked for more input than the test gave")

    buf = io.StringIO()
    with mock.patch("builtins.input", fake_input):
        with redirect_stdout(buf):
            result = func(*args)
    return result, buf.getvalue()


def ordered(deck_top_first):
    return list(reversed(deck_top_first))
