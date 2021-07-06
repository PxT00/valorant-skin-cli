![header](https://user-images.githubusercontent.com/42125428/124552512-a8027900-de01-11eb-9e85-b19f82d2eee6.png)

> A simple command line interface to manage VALORANT skins, including a skin randomizer

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub License](https://img.shields.io/github/license/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/blob/master/LICENSE)
[![Discord](https://img.shields.io/badge/discord-join-7389D8?style=flat&logo=discord)](https://discord.gg/uGuswsZwAT)
[![GitHub issues](https://img.shields.io/github/issues/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/colinhartigan/valorant-skin-cli)](https://github.com/colinhartigan/valorant-skin-cli/pulls)
![GitHub Repo stars](https://img.shields.io/github/stars/colinhartigan/valorant-skin-cli?style=social)
[![BetterREADME Verified](https://img.shields.io/badge/BetterREADME-Verified-grey?logo=github&labelColor=white&logoColor=grey)](https://github.com/better-readme)


### Table of Contents
1. [Demo](#demo)
2. [Installation and usage](#installation-and-usage)
3. [Will I get banned for using this?](#will-i-get-banned-for-using-this)
4. [TODOs](#todos)
5. [Dependencies](#dependencies)
6. [Contribute](#contribute)


## Demo
https://user-images.githubusercontent.com/29008608/124373643-37067880-dcbe-11eb-8cea-724e6150978f.mp4


## Installation and Usage
### Installation
Download the [latest release](https://github.com/colinhartigan/valorant-skin-cli/releases/) and run it!

__NOTE__: Your antivirus might mark the executable as malware, but this is a side effect of building the executable with PyInstaller. If you'd rather build the executable yourself, clone the repo and run `build.bat`

### Usage
The following commands are available for usage

- `randomize` - Randomizes your skins manually (will still automatically happen after each match)
- `modify` - Modify which skins enabled for randomization (use arrow keys and enter to select)
- `set <gun> <skin>` - Manually set a skin, eg. `set Phantom Oni Phantom`
- `exit` - Self explanatory


## Will I get banned for using this?
[u/Riot_Giraffy confirmed:](https://www.reddit.com/r/VALORANT/comments/oae5g6/i_got_tired_of_waiting_for_riot_to_add_a_skin/)
> Using the client API to modify loadouts does not seem ban worthy. The client API isn't officially supported for third party use, so don't expect future compatibility.


## TODOs
- [x] [Onboarding Experience](https://github.com/colinhartigan/valorant-skin-cli/commit/79739958c8bc632a2e8ec91f533c4fe2fba607dd#diff-bd516d79afd4ace3e4372b8ccab756b47b74da5ac479f373258ddcb3c4159ff2)
- [x] [Configuraion Command](https://github.com/colinhartigan/valorant-skin-cli/commit/973dee78becbfbda1c6f3cfd9f7e929f823ae8ec#diff-77765503b3f273fa49a93e1c5bfa59786213a26f2143d7a6ad75fbd2c38d5cd2)
  - Set refresh interval 
  - Set region
  - ~~Reset/Regen skin inventory~~ (coming in a future update after v1)
- [ ] Documentation


## Dependencies
Check [requirements.txt](https://github.com/colinhartigan/valorant-skin-cli/blob/master/requirements.txt) for updated infomation

```
valclient
requests
InquirerPy
```

## Contribute
Have an idea or a suggestion? Drop an issue or create a pull request!

## Legal
This project is not affiliated with Riot Games or any of its employees and therefore does not reflect the views of said parties. This is purely a fan-made project to enhance VALORANT's skin inventory management.

Riot Games does not endorse or sponsor this project. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
