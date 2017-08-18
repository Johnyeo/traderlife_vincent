# coding:utf-8
# control the game running thread.
# 1. 生成游戏的对局id  gameid_id
    # 用户A点击 创建对局。
    # 用户B点击 加入对局。生成 gameid

# 2. 生成游戏的回合id，控制游戏的回合数
    # 用户A点击下一回合生成 roundid
    # 用户A下一次点击生成下一个eroundid

# 数据库写入新的gameid
import random

from sign.market import db_handler

def startNewGame():
    startRound = 0
    new_gameid = db_handler.generateGameidByTime()
    db_handler.setNewGame(new_gameid)
    db_handler.generateCurrentMarket(new_gameid, startRound)
    return new_gameid


def nextTurn(gameid):
    player = 'zhangyao'
    new_gameround = db_handler.generateGameround(gameid)
    gameround = db_handler.getCurrentGameround(gameid)
    db_handler.generateCurrentMarket(gameid, new_gameround)

    # 获取上一回合总金额
    cash = db_handler.calcuTotalCash(gameid,gameround, player)
    db_handler.setNewRound(gameid, new_gameround, cash)
    return new_gameround


def getGameIdFromCookie(request):
    gameid = request.COOKIES.get('gameid', '')
    if gameid == '':
        # print("gameid是空的。 报错。")
        pass
    return gameid













