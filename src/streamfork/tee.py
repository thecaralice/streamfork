from collections.abc import Generator
import sys
from contextlib import contextmanager, nullcontext, redirect_stderr, redirect_stdout
from typing import IO, Protocol

from .fork import Fork


class Input(Protocol):
	def __call__(self, prompt: str = "", /) -> str: ...


@contextmanager
def tee(*streams: IO[str], capture_stderr: bool = True) -> Generator[Input, None, None]:
	out = Fork(sys.stdout, *streams)
	err = Fork(sys.stderr, *streams)
	with (
		redirect_stdout(out),
		redirect_stderr(err) if capture_stderr else nullcontext(),
	):
		yield out.input
	...
