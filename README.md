# StreamFork

## Usage

```py
import sys
from streamfork import tee

with open("output", "w") as f, tee(f) as input:
	print(f"Using {f.name}")
	name = input("Enter your name: ")
	age = int(input("Enter your age: "))
	print(f"User's name is {name!r}, age is {age!r}", file=sys.stderr)
	print(f"Hello, {name}! Have a nice day.")
```
---
Probably shouldn't be used in real projects
