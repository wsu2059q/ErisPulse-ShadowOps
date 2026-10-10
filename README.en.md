<div align="center">

<img src=".github/assets/ErisPulseLogo.png" width="180" alt="ErisPulse ShadowOps" />

# ErisPulse ShadowOps

**Shadow rollout operations — start, diff, promote and dismiss shadow modules from chat.**

An operations tool built on the ErisPulse 2.9 shadow module runtime API, with ownership audit; reports render as Takumi cards.

<p>
  <a href="https://pypi.org/project/ErisPulse-ShadowOps/"><img src="https://img.shields.io/pypi/v/ErisPulse-ShadowOps?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="https://pypi.org/project/ErisPulse-ShadowOps/"><img src="https://img.shields.io/badge/Python-3.10+-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/ErisPulse/ErisPulse-ShadowOps"><img src="https://img.shields.io/github/stars/ErisPulse/ErisPulse-ShadowOps?style=for-the-badge&logo=github&color=brightgreen" alt="Stars"></a>
  <a href="https://pepy.tech/project/ErisPulse-ShadowOps"><img src="https://img.shields.io/pepy/dt/ErisPulse-ShadowOps?style=for-the-badge&color=blue" alt="Downloads"></a>
  <a href="https://github.com/ErisPulse/ErisPulse"><img src="https://img.shields.io/badge/Powered_by-ErisPulse-FF6B9D?style=for-the-badge&logo=bookstack&logoColor=white" alt="ErisPulse"></a>
</p>

<p>
  <a href="./README.md">简体中文</a> | <a href="./README.en.md">English</a>
</p>

</div>

---

## Introduction

ShadowOps is a shadow rollout operations module for the [ErisPulse](https://github.com/ErisPulse/ErisPulse/) framework. A shadow is a new version of a module running alongside the live one under an independent owner: it receives copies of real events while its outbound calls are intercepted and recorded instead of sent. This module exposes those runtime operations as chat commands:

- `shadow start`: load a v2 source directory as a shadow
- `shadow diff`: compare v1 actual sends × v2 intended sends (aligned by trace_id)
- `shadow promote`: promote after confirmation (auto rollback on failure)
- `shadow dismiss`: drop the shadow
- `shadow audit`: ownership audit (resource counts / orphan owners)

Requires ErisPulse >= 2.9.0.

---

## Installation

```bash
epsdk install ErisPulse-ShadowOps
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/shadow` | Show usage |
| `/shadow start <module> <v2 path>` | Start a shadow (v2 source dir or single .py file; keep it outside plugin dirs) |
| `/shadow list` | List active shadows |
| `/shadow diff <module>` | Behavior diff report |
| `/shadow promote <module> yes` | Promote (requires explicit `yes`) |
| `/shadow dismiss <module>` | Dismiss the shadow |
| `/shadow audit <module>` | Ownership audit |

All commands require framework master permission.

---

## Usage

```bash
# 1. Put the new version somewhere on the server (e.g. downloads/roll_v2/)

# 2. Start the rollout
/shadow start roll downloads/roll_v2

# 3. After a trial period, compare behavior
/shadow diff roll

# 4. Promote once verified (auto-rollback on failure)
/shadow promote roll yes

# ...or dismiss
/shadow dismiss roll
```

---

## Configuration

```toml
[ShadowOps]
enabled = true          # enable module
diff_max_rows = 10      # max entries per diff report
audit_deep = false      # gc instance census in audit (global pause cost)
render_card = true      # render reports as image cards
theme = "auto"          # card theme (auto/light/dark)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | bool | `true` | Enable module |
| `diff_max_rows` | int | `10` | Max entries per diff |
| `audit_deep` | bool | `false` | gc instance census |
| `render_card` | bool | `true` | Card rendering |
| `theme` | str | `auto` | Card theme |

---

## Notes

1. Shadow sources are local paths; the same PyPI package cannot coexist twice in one interpreter
2. Promote is a runtime switch; after restart, install the new version persistently (`pip install -U`)
3. Sends/APIs/KV going through the framework are all intercepted; side effects bypassing the framework are not (resource ownership still visible via audit)

---

## References

- [ErisPulse](https://github.com/ErisPulse/ErisPulse/)
- [Shadow modules docs](https://github.com/ErisPulse/ErisPulse/tree/main/docs/zh-CN/advanced/shadow.md)
