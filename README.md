# Laban
A python script that is used to match a team of engines for the HAB - `Hand and Brain` variant. HAB is a team variant where each team / side typically is composed of two players the `hand` and the `brain`. The `brain` suggests the piece type to the `hand` and the `hand` finally decides what move to make given the piece type suggested by the `brain`.

### Algorithm
* 1. Send the position to the `brain` member of first/second team.
* 2. Send the command `go movetime 1000` to the `brain` and get its bestmove.
* 3. Save what piece type (pawn, knight ...) is on this move.
* 4. Save all the legal moves having that piece type.
* 5. Send the command `go movetime 1000 searchmoves m1 m2 ...` to the `hand` member where m1 m2 are the legal moves from step 4.
* 6. Save the move and update the position with this move.
* 7. Go to step 1

It should be noted that the engine that handles the `hand` must support the searchmoves UCI command.

### Engines that support searchmoves uci commands
These are the engines that can be used as the `hand` member of the team.

* [Berserk](https://github.com/jhonnold/berserk/releases)
* [Cdrill](https://sites.google.com/view/cdrill/download)
* [Cheng](https://github.com/kmar/cheng4/releases)
* [CT800](https://www.ct800.net/download.htm)
* [Deuterium](https://sites.google.com/view/deuterium-chess/download/engines/chess)  
* [Ethereal](https://github.com/AndyGrant/Ethereal/releases)
* [Komodo](https://komodochess.com/)
* [Lc0](https://github.com/LeelaChessZero/lc0/releases)
* [Stockfish](https://stockfishchess.org/download/)
* [Weiss](https://github.com/TerjeKir/weiss/releases)

### Setup
* Intall python 3, tested on python 3.9.1.
* Create hand_and_brain folder in your drive.
* Open command prompt or powershell and cd hand_and_brain folder and download the repo with `git clone https://github.com/fsmosca/laban.git`.
* Install python chess with `pip install chess`.
* Modify the config.ini file to locate the engines, etc.
* cd to your laban installation folder.
* Type `python laban.py` in command prompt or powershell to run the match.
