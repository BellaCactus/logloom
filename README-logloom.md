<div align="center">

# logloom

log prettifier: parse noisy text logs into a clean, readable timeline (optional html report).

![python](https://img.shields.io/badge/python-3.11%2B-0b0b0b?style=for-the-badge)
![cli](https://img.shields.io/badge/interface-cli-ff78c8?style=for-the-badge)
![license](https://img.shields.io/badge/license-mit-0b0b0b?style=for-the-badge)

</div>

---

## what is this?

logloom takes messy text logs and turns them into a clean timeline.

it is meant for:
- app logs
- exported packet / pcap text logs
- debug dumps
- anything that looks like "timestamp blah blah blah"

---

## features

- input: plain text
- attempts to detect timestamps and sessions
- groups related lines into readable blocks
- supports output limits and grouping modes
- optional standalone html timeline output

---

## install

requires python 3.11+.

```bash
python -m venv .venv
# windows
.venv\Scripts\activate
# mac/linux
source .venv/bin/activate

python -m pip install -U pip
python -m pip install -e .
```

---

## usage

basic:

```bash
logloom path/to/input.log
```

limit output + auto grouping:

```bash
logloom path/to/input.log --limit 300 --group auto
```

html timeline:

```bash
logloom path/to/input.log --html timeline.html
```

---

## input notes

examples often use placeholders like `in.log`. you must point logloom at a real file path.
if you do not have a log file yet, point it at any `.txt` file to verify it runs.

---

## license

MIT. see `LICENSE`.
