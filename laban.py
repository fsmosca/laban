"""
laban

A script to run hand and brain engine match.

Dependent module:
    * Python chess
        pip install chess
"""


__author__ = 'fsmosca'
__appname__ = 'Laban'
__version__ = '1.2'


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


def init_engine(config, t):
    """
    Configure engine's memory and threads.
    """
    options = dict(config.items('engine'))

    for e in t:
        for k, v in options.items():
            if k.lower() in [o.lower() for o in e.options]:
                e.configure({k: v})


def quit_engines(t1, t2):
    for e in t1:
        e.quit()
    for e in t2:
        e.quit()


def match(game, config, round, subround, movetimems=500, reverse=False):
    """
    Play 1 game from the given board and return the game.
    """
    e1path = config['team1']['brain']
    e2path = config['team1']['hand']
    team1_name = config['team1']['name']

    e3path = config['team2']['brain']
    e4path = config['team2']['hand']
    team2_name = config['team2']['name']

    # Define engines
    idname1 = {}
    engine1 = chess.engine.SimpleEngine.popen_uci(f'{e1path}')
    engine2 = chess.engine.SimpleEngine.popen_uci(f'{e2path}')
    t1 = [engine1, engine2]
    init_engine(config, t1)
    idname1.update({'brain': engine1.id['name'], 'hand': engine2.id['name']})

    idname2 = {}
    engine3 = chess.engine.SimpleEngine.popen_uci(f'{e3path}')
    engine4 = chess.engine.SimpleEngine.popen_uci(f'{e4path}')
    t2 = [engine3, engine4]
    init_engine(config, t2)
    idname2.update({'brain': engine3.id['name'], 'hand': engine4.id['name']})

    if not reverse:
        eng = [t1, t2]
        eng_name = [team1_name, team2_name]
        id_name = [idname1, idname2]
    else:
        eng = [t2, t1]
        eng_name = [team2_name, team1_name]
        id_name = [idname2, idname1]

    print(f'starting {eng_name[0]} vs {eng_name[1]}, round {round}.{subround} ...')

    # Create board.
    node = game.end()
    board = node.board()

    start_turn = board.turn

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
                else:  # hand
                    result = eng[i][j].play(board, chess.engine.Limit(time=movetimems/1000), root_moves=legal_)
                    move = result.move

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
        game.headers['WhiteBrain'] = id_name[0]['brain']
        game.headers['WhiteHand'] = id_name[0]['hand']

        game.headers['Black'] = eng_name[1]
        game.headers['BlackBrain'] = id_name[1]['brain']
        game.headers['BlackHand'] = id_name[1]['hand']        
    else:
        game.headers['White'] = eng_name[1]
        game.headers['WhiteBrain'] = id_name[1]['brain']
        game.headers['WhiteHand'] = id_name[1]['hand']

        game.headers['Black'] = eng_name[0]
        game.headers['BlackBrain'] = id_name[0]['brain']
        game.headers['BlackHand'] = id_name[0]['hand']        

    game.headers['Round'] = f'{round}.{subround}'
    game.headers['Event'] = 'Hand and Brain'
    game.headers['Site'] = f'Computer, Interface: {__appname__} v{__version__}'
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


def read_start_positions(config, israndom=True):
    """
    Read fen, epd and pgn files and return it as a list of games.
    """
    start_games = []
    fn = config['positions']['posfn']

    try:
        isshuffle = config.get('positions', 'shuffle')
    except configparser.NoOptionError:
        isshuffle = 'true'

    if isshuffle.lower() == 'true' or isshuffle == '1':
        israndom = True
    elif isshuffle.lower() == 'false' or isshuffle == '0':
        israndom = False

    # fen and epd files
    if fn.endswith('.fen') or fn.endswith('.epd'):
        with open(fn, 'r') as f:
            for lines in f:
                line = lines.strip()
                game = chess.pgn.Game()            
                game = game.from_board(chess.Board(line))
                start_games.append(game)

    # pgn file
    elif fn.endswith('.pgn'):
        with open(fn, 'r') as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                start_games.append(game)
    
    # not supported file
    else:
        raise Exception(f'Your start position file {fn} is not a fen or epd or pgn.')

    if israndom:
        random.shuffle(start_games)

    return start_games


def main():
    config = configparser.ConfigParser()
    config.optionxform=str
    config.read('config.ini')

    movetimems = int(config['match']['movetimems'])
    game_concurrency = int(config['match']['concurrency'])
    num_games = int(config['match']['numgames'])

    start_games = read_start_positions(config)

    job_list = []

    with ProcessPoolExecutor(max_workers=game_concurrency) as executor:
        for i, sg in enumerate(start_games):
            job = executor.submit(match, sg, config, i+1, 1, movetimems=movetimems, reverse=False)
            job_list.append(job)
            job = executor.submit(match, sg, config, i+1, 2, movetimems=movetimems, reverse=True)
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
