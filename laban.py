"""
laban

A script to run hand and brain engine match.

Dependent module:
    * Python chess
        pip install chess
"""


__author__ = 'fsmosca'
__appname__ = 'Laban'
__version__ = '0.7.1'


import configparser
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import sys
from datetime import date
import random
# import logging

import chess
import chess.pgn
import chess.engine


sys.setrecursionlimit(10000)


# logging.basicConfig(
    # filename='laban_log.txt',
    # filemode='a',
    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    # datefmt='%H:%M:%S',
    # level=logging.DEBUG
# )


def init_engine(t, hash_mb=128, num_threads=1):
    """
    Configure engine's memory and threads.
    """
    for e in t:
        if 'Hash' in e.options:
            e.configure({'Hash': hash_mb})
        if 'Threads' in e.options:
            e.configure({'Threads': num_threads})


def quit_engines(t1, t2):
    for e in t1:
        e.quit()
    for e in t2:
        e.quit()


def match(fen, config, round, subround, movetimems=500, reverse=False):
    """
    Play 1 game from the given fen and return the game.
    """
    hash_mb = int(config['engine']['hash'])
    num_threads = int(config['engine']['threads'])

    e1path = config['team1']['brain']
    e2path = config['team1']['hand']
    team1_name = config['team1']['name']

    e3path = config['team2']['brain']
    e4path = config['team2']['hand']
    team2_name = config['team2']['name']

    # Define engines
    engine1 = chess.engine.SimpleEngine.popen_uci(f'{e1path}')
    engine2 = chess.engine.SimpleEngine.popen_uci(f'{e2path}')
    t1 = [engine1, engine2]
    init_engine(t1, hash_mb, num_threads)

    engine3 = chess.engine.SimpleEngine.popen_uci(f'{e3path}')
    engine4 = chess.engine.SimpleEngine.popen_uci(f'{e4path}')
    t2 = [engine3, engine4]
    init_engine(t2, hash_mb, num_threads)

    if not reverse:
        eng = [t1, t2]
        eng_name = [team1_name, team2_name]
    else:
        eng = [t2, t1]
        eng_name = [team2_name, team1_name]

    print(f'starting {eng_name[0]} vs {eng_name[1]}, round {round}.{subround} ...')

    board = chess.Board(fen)
    start_turn = board.turn

    game = chess.pgn.Game()
    game = game.from_board(board)
    node = game

    # Play a game.
    while not board.is_game_over():    
        for i in range(2):
            move, pt, legal_, brain_bm = None, None, [], None

            for j in range(2):
                if j == 0:  # brain
                    result = eng[i][j].play(board, chess.engine.Limit(time=movetimems/1000))
                    bm = result.move
                    brain_bm = bm
                    frsq = bm.from_square
                    pt = board.piece_type_at(frsq)
                    for m in board.legal_moves:
                        frsq_ = m.from_square
                        pt_ = board.piece_type_at(frsq_)
                        if pt == pt_:
                            legal_.append(m)
                    assert pt is not None
                else:  # hand
                    assert len(legal_ ) > 0
                    result = eng[i][j].play(board, chess.engine.Limit(time=movetimems/1000), root_moves=legal_)
                    move = result.move

            assert move is not None
            node = node.add_main_variation(move, comment=f'brain: {board.san(brain_bm)}')            
            board.push(move)

            if board.is_game_over():
                break

    # Save game
    game_tmp = chess.pgn.Game()
    game_tmp = game_tmp.from_board(board)
    result = game_tmp.headers['Result']

    today = date.today()
    da = today.strftime("%Y.%m.%d")

    if start_turn:
        game.headers['White'] = eng_name[0]
        game.headers['Black'] = eng_name[1]
    else:
        game.headers['White'] = eng_name[1]
        game.headers['Black'] = eng_name[0]

    game.headers['Round'] = f'{round}.{subround}'
    game.headers['Event'] = 'Hand and Brain'
    game.headers['Date'] = f'{da}'
    game.headers['TimeControl'] = f'{movetimems/1000:0.1f}s/move'
    game.headers['Result'] = f'{result}'

    quit_engines(t1, t2)

    return game


def save_game(config, game):
    """
    Save game in pgn format
    """
    pgnout = config['pgnoutput']['pgnoutfn']

    with open(pgnout, 'a') as h:
        h.write(f'{game}\n\n')


def read_positions(config, israndom=True):
    """
    Read a file with epd or fen and return it as a list.
    """
    fens = []
    fenfn = config['positions']['posfn']

    try:
        isshuffle = config.get('positions', 'shuffle')
    except configparser.NoOptionError:
        isshuffle = 'true'

    if isshuffle.lower() == 'true' or isshuffle == '1':
        israndom = True
    elif isshuffle.lower() == 'false' or isshuffle == '0':
        israndom = False    

    # print(f'israndom: {israndom}')

    with open(fenfn, 'r') as f:
        for lines in f:
            line = lines.strip()
            fens.append(line)

    if israndom:
        random.shuffle(fens)

    return fens


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    movetimems = int(config['match']['movetimems'])
    game_concurrency = int(config['match']['concurrency'])
    num_games = int(config['match']['numgames'])

    fens = read_positions(config)

    job_list = []

    with ProcessPoolExecutor(max_workers=game_concurrency) as executor:
        for i, fen in enumerate(fens):
            job = executor.submit(match, fen, config, i+1, 1, movetimems=movetimems, reverse=False)
            job_list.append(job)
            job = executor.submit(match, fen, config, i+1, 2, movetimems=movetimems, reverse=True)
            job_list.append(job)

            if i+1 >= num_games//2:
                break

        for future in concurrent.futures.as_completed(job_list):
            try:
                game = future.result()
                save_game(config, game)
                print(f'{game}\n\n')
            except concurrent.futures.process.BrokenProcessPool as ex:
                print(f'{ex}')


if __name__ == '__main__':
    main()
