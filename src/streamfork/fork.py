from collections.abc import Iterable
from io import SEEK_SET, TextIOBase, UnsupportedOperation
from itertools import chain
from typing import Literal, Never, IO, final, override


@final
class Fork(TextIOBase):
	_main_stream: IO[str]
	_other_streams: tuple[IO[str], ...]

	def __init__(self, main_stream: IO[str], /, *other_streams: IO[str]) -> None:
		self._main_stream = main_stream
		self._other_streams = other_streams
		for s in self._streams:
			assert s.writable(), f"{s} is not writeable"

	@property
	def _streams(self) -> Iterable[IO[str]]:
		return chain((self._main_stream,), self._other_streams)

	@override
	def fileno(self) -> int:
		return self._main_stream.fileno()

	@override
	def isatty(self) -> bool:
		return self._main_stream.isatty()

	@override
	def readable(self) -> Literal[False]:
		return False

	@override
	def read(self, size: int | None = -1, /) -> Never:
		raise OSError(f"{self} can not be read from")

	@override
	def readline(self, size: int | None = -1, /) -> Never:
		raise OSError(f"{self} can not be read from")

	@override
	def seekable(self) -> Literal[False]:
		return False

	@override
	def seek(self, offset: int, whence: int = SEEK_SET, /) -> Never:
		raise OSError(f"{self} can not seek")

	@override
	def writable(self) -> Literal[True]:
		return True

	@override
	def detach(self) -> Never:
		raise UnsupportedOperation(f"{self} can not be detached")

	@override
	def close(self) -> None:
		for x in self._streams:
			x.close()

	@override
	def flush(self) -> None:
		for x in self._streams:
			x.flush()

	@override
	def write(self, s: str, /) -> int:
		res = self._main_stream.write(s)
		for x in self._other_streams:
			_ = x.write(s)
		return res

	@override
	def truncate(self, size: int | None = None, /) -> int:
		res = self._main_stream.truncate(size)
		for x in self._other_streams:
			_ = x.truncate(size)
		return res

	@property
	@override
	def closed(self) -> bool:
		return any(x.closed for x in self._streams)

	@override
	def tell(self) -> int:
		return self._main_stream.tell()

	def input(self, prompt: str = "", /) -> str:
		"""Works like built-in `input`, but also logs user's input to secondary streams"""
		_ = self.write(prompt)
		self.flush()
		res = input()
		for x in self._other_streams:
			_ = x.write(res)
			_ = x.write("\n")
		self.flush()
		return res
