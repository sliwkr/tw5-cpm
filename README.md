# Horrible tw5 community plugin manager

A script to manage community plugins for TiddlyWiki5.

## Assumptions:

* Node.js / server wiki
* Wikis are managed in a git repository
* Linux with python3 and git installed

## Installation

Place the script in the root path of your git repository.

```sh
cd yourwikirepo
wget https://raw.githubusercontent.com/sliwkr/tw5-cpm/refs/heads/main/plugin-install.py
```

## Usage

Define desired community plugin git repositories, their git tags or branches and plugin directory as a list
in `communityplugins` key at your wiki's `tiddlywiki.info`, e.g.

```json
    "plugins": [
        "tiddlywiki/tiddlyweb",
        "..."
    ],
    "communityplugins": [
      {"directory": "plugins/tobibeer/preview", "version": "0.5.6", "git": "https://github.com/tobibeer/tw5-preview.git"},
      {"directory": "plugins/relink", "version": "v2.4.5", "git": "https://github.com/flibbles/tw5-relink"},
      {"directory": "plugins/ihm/tidgraph", "version": "gh-pages", "git": "https://github.com/ihm4u/tw5plugs.git"}
    ],
```

Then, run the script

```sh
./plugin-install.py -w yourwiki
```

[![asciicast](https://asciinema.org/a/29DAPQjrgNAluOMQxA8gDcvQg.svg)](https://asciinema.org/a/29DAPQjrgNAluOMQxA8gDcvQg)
