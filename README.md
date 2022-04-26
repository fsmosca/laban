# Laban
A python script that is used to match a team of engines for the HAB - `Hand and Brain` variant. HAB is a team variant where each team / side typically is composed of two players the `hand` and the `brain`. The `brain` suggests the piece type to the `hand` and the `hand` finally decides what move to make given the piece type suggested by the `brain`.

### Algorithm
* 1. Send the position to the `brain` member of first/second team.
* 2. Send the command `go movetime <movetime>` to the `brain` and get its bestmove.
* 3. Save what piece type (pawn, knight ...) has been moved.
* 4. Save all the legal moves having that piece type.
* 5. Send the command `go movetime <movetime> searchmoves m1 m2 ...` to the `hand` member of the team where m1, m2 ... are the legal moves from step 4.
* 6. Save the move from `hand` and update the position with this move.
* 7. Go to step 1

It should be noted that the engine that handles the `hand` must support the searchmoves UCI command.

### Engines that support searchmoves uci commands
These are the engines that can be used as the `hand` member of the team, there can be others.

* [Berserk](https://github.com/jhonnold/berserk/releases)
* [Cdrill](https://sites.google.com/view/cdrill/download)
* [Cheng](https://github.com/kmar/cheng4/releases)
* [CT800](https://www.ct800.net/download.htm)
* [Deuterium](https://sites.google.com/view/deuterium-chess/download/engines/chess)  
* [Ethereal](https://github.com/AndyGrant/Ethereal/releases)
* [Komodo](https://komodochess.com/)
* [Lc0](https://github.com/LeelaChessZero/lc0/releases)
* [MadChess](https://www.madchess.net/downloads/)
* [Stockfish](https://stockfishchess.org/download/)
* [Weiss](https://github.com/TerjeKir/weiss/releases)
* [Zahak](https://github.com/amanjpro/zahak/releases)

### Setup
* Intall python 3, this script is tested on python 3.9.1.
* Be sure your engines are ready or already downloaded.
* Create `hand_and_brain` folder or any folder name in your drive.
* Open command prompt or powershell and cd to hand_and_brain folder.
* Download the repo with `git clone https://github.com/fsmosca/laban.git`.
* Install python chess with `pip install chess`.
* cd to your laban installation folder.
* Modify the config.ini file to change options.
* Type `python laban.py` in command prompt or powershell to run the match.

### Sample results

cdrill as brain defeated stockfish as brain. Note stockfish 15 is around 3700 while cdrill is around 1800 from [ccrl blitz rating list](https://ccrl.chessdom.com/ccrl/404/rating_list_all.html).

Test pgn files can be found in pgnout folder.

```
   # PLAYER                            :  RATING  POINTS  PLAYED   (%)
   1 Br_cdrill_1800_Ha_stockfish_15    :  2346.8    31.5      50    63
   2 Br_stockfish_15_Ha_cdrill_1800    :  2253.2    18.5      50    37
```

### Sample game output

```
[Event "Hand and Brain"]
[Site "Computer, Interface: Laban v0.8.0"]
[Date "2022.04.26"]
[Round "1.1"]
[White "Br_cdrill_1800_Ha_stockfish_15"]
[Black "Br_stockfish_15_Ha_cdrill_1800"]
[Result "1-0"]
[BlackBrain "Stockfish 15"]
[BlackHand "CDrill 1800"]
[FEN "rnb1kbnr/ppp1pppp/8/3q4/8/2N5/PPPP1PPP/R1BQKBNR b KQkq - 1 3"]
[SetUp "1"]
[TimeControl "0.1s/move"]
[WhiteBrain "CDrill 1800"]
[WhiteHand "Stockfish 15"]

3... Qd4 { brain: Qd8 } 4. Nf3 { brain: Nf3 } 4... Qc5 { brain: Qd8 } 5. d4 { brain: d4 } 5... Qf5 { brain: Qb6 } 6. Ne5 { brain: Nb5 } 6... g5 { brain: e6 } 7. Bd3 { brain: Bd3 } 7... Qe6 { brain: Qf6 } 8. Bc4 { brain: Bxg5 } 8... Qf5 { brain: Qf6 } 9. g4 { brain: g4 } 9... Qf6 { brain: Qf6 } 10. Ne4 { brain: Nd5 } 10... Qb6 { brain: Qb6 } 11. Nxf7 { brain: Nxf7 } 11... Nf6 { brain: Nf6 } 12. Nxf6+ { brain: Nxf6+ } 12... Qxf6 { brain: Qxf6 } 13. Nxh8 { brain: Nxh8 } 13... Qxh8 { brain: Qxh8 } 14. Be3 { brain: Bxg5 } 14... Nc6 { brain: Nc6 } 15. Qf3 { brain: Qf3 } 15... Qf6 { brain: Qf6 } 16. Qxf6 { brain: Qe4 } 16... exf6 { brain: exf6 } 17. h3 { brain: f3 } 17... Bd7 { brain: Bd7 } 18. Bb5 { brain: Bd3 } 18... a5 { brain: a6 } 19. Bd3 { brain: Bd3 } 19... Nb4 { brain: Nb4 } 20. Be4 { brain: Bxh7 } 20... Kd8 { brain: O-O-O } 21. a3 { brain: c4 } 21... Nc6 { brain: Nc6 } 22. Bxh7 { brain: Bxh7 } 22... Ne7 { brain: Ne7 } 23. Be4 { brain: Be4 } 23... Kc8 { brain: Ke8 } 24. h4 { brain: d5 } 24... gxh4 { brain: f5 } 25. Rxh4 { brain: Rxh4 } 25... f5 { brain: f5 } 26. gxf5 { brain: gxf5 } 26... Bg7 { brain: Bxf5 } 27. Rh7 { brain: Rh7 } 27... Nxf5 { brain: Nxf5 } 28. Bxf5 { brain: Bxf5 } 28... Bxf5 { brain: Bxf5 } 29. Rxg7 { brain: Rxg7 } 29... Ra6 { brain: Ra6 } 30. a4 { brain: d5 } 30... Rg6 { brain: Rg6 } 31. Rxg6 { brain: Rxg6 } 31... Bxg6 { brain: Bxg6 } 32. Kd2 { brain: Kd2 } 32... Bf5 { brain: Be8 } 33. Rg1 { brain: Rg1 } 33... b6 { brain: b5 } 34. Bf4 { brain: Bf4 } 34... Bd7 { brain: Bd7 } 35. Rg8+ { brain: Rg8+ } 35... Kb7 { brain: Kb7 } 36. Rg7 { brain: Rg7 } 36... Bxa4 { brain: Bxa4 } 37. Rxc7+ { brain: Rxc7+ } 37... Ka6 { brain: Ka6 } 38. d5 { brain: d5 } 38... Be8 { brain: Be8 } 39. d6 { brain: d6 } 39... Kb5 { brain: Kb5 } 40. d7 { brain: d7 } 40... Bxd7 { brain: Bxd7 } 41. Rxd7 { brain: Rxd7 } 41... Kc6 { brain: Kc6 } 42. Rd6+ { brain: Rc7+ } 42... Kc5 { brain: Kc7 } 43. f3 { brain: b3 } 43... b5 { brain: b5 } 44. b3 { brain: c3 } 44... a4 { brain: b4 } 45. Rd3 { brain: Ra6 } 45... Kc6 { brain: Kc6 } 46. Be5 { brain: Bd6 } 46... Kb6 { brain: Kc5 } 47. Rd6+ { brain: Rd6+ } 47... Kc5 { brain: Ka5 } 48. Rd3 { brain: Ra6 } 48... axb3 { brain: axb3 } 49. Rxb3 { brain: Rxb3 } 49... Kc4 { brain: Kd5 } 50. Bb2 { brain: Bf6 } 50... Kc5 { brain: Kc5 } 51. Be5 { brain: Ba3+ } 51... Kc4 { brain: Kd5 } 52. Bb2 { brain: Bf6 } 52... Kc5 { brain: Kd5 } 53. Bg7 { brain: Ba3+ } 53... Kc6 { brain: Kd5 } 54. Kd3 { brain: Kd3 } 54... Kc5 { brain: Kd5 } 55. Bd4+ { brain: Bd4+ } 55... Kc6 { brain: Kd5 } 56. f4 { brain: f4 } 56... Kc7 { brain: Kd5 } 57. Rxb5 { brain: Rxb5 } 57... Kd8 { brain: Kc6 } 58. f5 { brain: f5 } 58... Ke8 { brain: Kd7 } 59. f6 { brain: f6 } 59... Kf7 { brain: Kd7 } 60. Rb7+ { brain: Rb7+ } 60... Kg6 { brain: Kg8 } 61. f7 { brain: f7 } 61... Kg5 { brain: Kf5 } 62. f8=Q { brain: f8=Q } 62... Kh4 { brain: Kh4 } 63. Rg7 { brain: Rg7 } 63... Kh5 { brain: Kh5 } 64. Qh8# { brain: Qh8# } 1-0
```
