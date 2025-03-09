#!/usr/bin/env python3

# A script to install tiddlywiki community plugins.
# Add your plugins in a given wiki's tiddlywiki.info under .communityplugins key like so:
# "communityplugins": [
#   {"directory": "plugins/tobibeer/preview", "version": "0.5.6", "git": "https://github.com/tobibeer/tw5-preview.git"},
#   {"directory": "plugins/cmplus", "version": "0.2.1", "git": "https://github.com/adithya-badidey/TW5-codemirror-plus.git"}
# ],

# The script will do the rest,
# i.e. check if they're in the desired versions and if not, pull them into yourwiki/plugins/ directory.

import os
import shutil
from distutils import dir_util
import tempfile
import logging
import subprocess
import json

logging.basicConfig()
log = logging.getLogger("plugin-install")
log.setLevel(logging.DEBUG)

def sh(cmd:str) -> str:
  """
  Execute a command with shell. Can be used with pipes
  """
  return subprocess.getoutput(cmd)

def nav_git_root():
    git_root_path = sh("git rev-parse --show-toplevel")
    os.chdir(git_root_path)

def tiddlywiki_info_extract_plugins(twinfo_path:str):
    with open(twinfo_path, "r") as twinfo_file:
        twinfo = json.load(twinfo_file)
    community_plugins = []
    for plugin in twinfo["communityplugins"]:
        plugin_data = {
            "git": plugin["git"],
            "version": plugin["version"],
            "git_directory": plugin["directory"],
            "target_directory": plugin['directory'].rsplit('/', 1)[1],
        }
        community_plugins.append(plugin_data)
    return community_plugins


def is_desired_plugin_present(plugin:dict) -> bool:
    # is dir present
    if not os.path.isdir(f"{global_config['wiki']}/plugins/{plugin['target_directory']}"):
        log.warning(f"Plugin {plugin['target_directory']} not present")
        return False
    # is version matching
    with open(f"{global_config['wiki']}/plugins/{plugin['target_directory']}/plugin.info", "r") as f:
        plugin_info = json.load(f)
        if plugin_info["version"] != plugin['version']:
            log.warning(f"Plugin {plugin['target_directory']} installed version {plugin_info['version']}, expected version {plugin['version']}")
            return False
    return True


def install_plugin(plugin:dict, destination:str):
    with tempfile.TemporaryDirectory() as tmpdirname:
        log.debug(f"Directory {tmpdirname} created, I am currently at {os.path.abspath('.')}")
        log.info(f"Cloning {plugin['git']}...")
        sh(f"git clone --depth=1 --branch {plugin['version']} {plugin['git']} {tmpdirname}")
        log.debug(f"Repository cloning finished, should be at {tmpdirname} now.")
        log.debug(f"{tmpdirname} flat content: {os.listdir(tmpdirname)}")

        dir_util.copy_tree(f"{tmpdirname}/{plugin['git_directory']}", destination)


def main():
    nav_git_root()
    root_abspath = os.path.abspath('.')
    plugins = tiddlywiki_info_extract_plugins(f"{global_config['wiki']}/tiddlywiki.info")

    for plugin in plugins:
        if not is_desired_plugin_present(plugin):
            shutil.rmtree(f"{root_abspath}/{global_config['wiki']}/plugins/{plugin['target_directory']}", ignore_errors=True)
            install_plugin(plugin, f"{root_abspath}/{global_config['wiki']}/plugins/{plugin['target_directory']}")

if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wiki', type=str, help='Tiddlywiki to install plugins in.')
    parser.add_argument('-v', '--verbosity',
                        type=str,
                        default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Level of verbosity'
                        )
    args = parser.parse_args()
    log.setLevel(args.verbosity)
    print(args)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    else:
        global_config = {
            "wiki": args.wiki
        }

    main()

