# coding:utf-8
# control the game running thread.
# 1. 生成游戏的对局id  gameid_id
    # 用户A点击 创建对局。
    # 用户B点击 加入对局。生成 gameid

# 2. 生成游戏的回合id，控制游戏的回合数
    # 用户A点击下一回合生成 roundid
    # 用户A下一次点击生成下一个eroundid

# 数据库写入新的gameid
from sign.market import db_handler

def startNewGame():
    old_gameid = db_handler.getLatestGameID()
    new_gameid = old_gameid + 1
    db_handler.setNewGame(new_gameid)

def nextTurn():
    old_gameround = db_handler.getLatestGameround()
    new_gameround = old_gameround + 1
    db_handler.setNewRound(new_gameround)



