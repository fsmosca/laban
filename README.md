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
* Intall python 3, tested on python 3.9.1.
* Create hand_and_brain folder in your drive.
* Open command prompt or powershell and cd hand_and_brain folder and download the repo with `git clone https://github.com/fsmosca/laban.git`.
* Install python chess with `pip install chess`.
* Modify the config.ini file to locate the engines, etc.
* cd to your laban installation folder.
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
[Site "?"]
[Date "2022.04.26"]
[Round "1.2"]
[White "Br_stockfish_15_Ha_cdrill_1800"]
[Black "Br_cdrill_1800_Ha_stockfish_15"]
[Result "1-0"]
[FEN "rnb1kbnr/ppp1pppp/8/3q4/8/2N5/PPPP1PPP/R1BQKBNR b KQkq - 1 3"]
[SetUp "1"]
[TimeControl "0.1s/move"]

3... Qa5 { brain: Qd4 } 4. f4 { brain: d4 } 4... Qb6 { brain: Qf5 } 5. d4 { brain: a4 } 5... Qe6+ { brain: Qe6+ } 6. Be2 { brain: Be2 } 6... Bd7 { brain: Bd7 } 7. Nf3 { brain: Nf3 } 7... g6 { brain: f6 } 8. Ne5 { brain: Ne5 } 8... f5 { brain: f6 } 9. Bc4 { brain: Bc4 } 9... Qb6 { brain: Qf6 } 10. Bf7+ { brain: Bf7+ } 10... Kd8 { brain: Kd8 } 11. Bd5 { brain: Bb3 } 11... Nf6 { brain: Nh6 } 12. O-O { brain: O-O } 12... Kc8 { brain: Kc8 } 13. Be3 { brain: Be3 } 13... Qa5 { brain: Qxb2 } 14. Bc4 { brain: Bf3 } 14... Ng4 { brain: Ng4 } 15. Nd5 { brain: Nxg4 } 15... e6 { brain: e6 } 16. Bd2 { brain: Bd2 } 16... Qa4 { brain: Qa4 } 17. Nc3 { brain: Nc3 } 17... Qb4 { brain: Qb4 } 18. b3 { brain: a3 } 18... Qb6 { brain: Qb6 } 19. Nxg4 { brain: Nxg4 } 19... fxg4 { brain: fxg4 } 20. Be3 { brain: Be3 } 20... Bg7 { brain: Bb4 } 21. Ne4 { brain: Ne4 } 21... a5 { brain: g3 } 22. Nc5 { brain: Nc5 } 22... a4 { brain: h5 } 23. Qxg4 { brain: Qxg4 } 23... axb3 { brain: axb3 } 24. axb3 { brain: axb3 } 24... Rxa1 { brain: Rxa1 } 25. Rxa1 { brain: Rxa1 } 25... Re8 { brain: Re8 } 26. Qf3 { brain: Qh3 } 26... Re7 { brain: Re7 } 27. Ra8 { brain: Ra8 } 27... Bb5 { brain: Bc6 } 28. Bxe6+ { brain: Bxe6+ } 28... Rxe6 { brain: Rxe6 } 29. Qh3 { brain: Qh3 } 29... Bc4 { brain: Bf6 } 30. Rxb8+ { brain: Rxb8+ } 30... Kxb8 { brain: Kxb8 } 31. Nd7+ { brain: Nd7+ } 31... Ka7 { brain: Ka7 } 32. Nxb6 { brain: Nxb6 } 32... cxb6 { brain: cxb6 } 33. bxc4 { brain: bxc4 } 33... Re4 { brain: Re4 } 34. Qf3 { brain: Qf3 } 34... Re8 { brain: Re8 } 35. Kh1 { brain: Kf2 } 35... Bh8 { brain: Bf8 } 36. Kg1 { brain: Kg1 } 36... Bg7 { brain: Bg7 } 37. Kf1 { brain: Kf2 } 37... Bf8 { brain: Bf8 } 38. Qf2 { brain: Qh3 } 38... Bh6 { brain: Bb4 } 39. d5 { brain: d5 } 39... Bf8 { brain: Bf8 } 40. Bxb6+ { brain: Bxb6+ } 40... Kb8 { brain: Kb8 } 41. f5 { brain: c5 } 41... gxf5 { brain: gxf5 } 42. Qg3+ { brain: Qf4+ } 42... Ka8 { brain: Ka8 } 43. Qb3 { brain: Qb3 } 43... Re1+ { brain: Re1+ } 44. Kxe1 { brain: Kxe1 } 44... Kb8 { brain: Kb8 } 45. Qg3+ { brain: Qa4 } 45... f4 { brain: f4 } 46. Qxf4+ { brain: Qxf4+ } 46... Bd6 { brain: Bd6 } 47. Qxd6+ { brain: Qxd6+ } 47... Kc8 { brain: Ka8 } 48. Qc7# { brain: Qc7# } 1-0
```
