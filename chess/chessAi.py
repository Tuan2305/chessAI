'''
    Giữ ĐỘ SÂU (DEPTH) <= 4 để AI chạy mượt mà.

    ĐỘ SÂU có nghĩa là AI sẽ tính toán các nước đi trong một độ sâu các bước và chọn nước đi tốt nhất dựa trên ĐIỂM BẮT QUÂN và ĐIỂM VỊ TRÍ QUÂN CỜ:
    ĐỘ SÂU = 4

'''


'''

CÁCH CẢI THIỆN AI VÀ TĂNG TỐC ĐỘ AI

1) Tạo cơ sở dữ liệu cho các nước đi mở đầu của AI/ các khai cuộc phổ biến.
2) AI tìm các nước đi khả thi cho tất cả quân cờ sau mỗi lượt đi. Nếu một quân cờ đã được di chuyển, các nước đi khả thi của các quân cờ khác sẽ không thay đổi. Do đó, không cần phải tính toán lại:
    Trường hợp này, các nước đi khả thi mới sẽ là:
        i) Nếu bất kỳ quân cờ nào có thể di chuyển đến vị trí ban đầu của quân cờ vừa di chuyển.
        ii) Nếu quân cờ vừa di chuyển đến vị trí (x, y), kiểm tra xem nó có chặn quân cờ nào khác di chuyển đến vị trí đó không.
3) Không cần đánh giá lại toàn bộ vị trí trên bàn cờ mỗi lần, sử dụng bảng băm Zobrist để lưu trữ các vị trí tốt và độ sâu đã tính toán.
4) Nếu trình tự nước đi như sau:
      [ quân đen di chuyển x, quân trắng di chuyển a, quân đen di chuyển y, quân trắng di chuyển b ]
      thì đôi khi nó tương đương với:
      [ quân đen di chuyển y, quân trắng di chuyển a, quân đen di chuyển x, quân trắng di chuyển b ]
      [ quân đen di chuyển x, quân trắng di chuyển b, quân đen di chuyển y, quân trắng di chuyển a ]
      [ quân đen di chuyển y, quân trắng di chuyển b, quân đen di chuyển x, quân trắng di chuyển a ]
5) Dạy lý thuyết cho AI, chẳng hạn đôi khi tốt hơn là bắt quân đe dọa thay vì di chuyển một con tốt, hoặc đưa quân cờ trở lại vị trí cũ thay vì tấn công.

'''


import random
pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 2, 1, 1, 2, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N": knightScores, "B": bishopScores, "Q": queenScores,
                       "R": rookScores, "wp": whitePawnScores, "bp": blackPawnScores}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
SET_WHITE_AS_BOT = -1


def findRandomMoves(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves, returnQueue):
    global nextMove, whitePawnScores, blackPawnScores
    nextMove = None
    random.shuffle(validMoves)

    if gs.playerWantsToPlayAsBlack:
        # Swap the variables
        whitePawnScores, blackPawnScores = blackPawnScores, whitePawnScores

    SET_WHITE_AS_BOT = 1 if gs.whiteToMove else -1

    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -
                             CHECKMATE, CHECKMATE,  SET_WHITE_AS_BOT)

    returnQueue.put(nextMove)


# with alpha beta pruning
'''
alpha is keeping track of maximum so far
beta is keeping track of minimum so far
'''


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # (will add later) move ordering - like evaluate all the move first that results in check or evaluate all the move first that results in capturing opponent's queen

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()  # opponent validmoves
        '''
        negative sign because what ever opponents best score is, is worst score for us
        negative turnMultiplier because it changes turns after moves made 
        -beta, -alpha (new max, new min) our max become opponents new min and our min become opponents new max
        '''
        score = - \
            findMoveNegaMaxAlphaBeta(
                gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore  # alpha is the new max
        if alpha >= beta:  # if we find new max is greater than minimum so far in a branch then we stop iterating in that branch as we found a worse move in that branch
            break
    return maxScore


'''
Positive score is good for white
Negative score is good for black
'''


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            gs.checkmate = False
            return -CHECKMATE  # black wins
        else:
            gs.checkmate = False
            return CHECKMATE  # white wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                # score positionally based on piece type
                if square[1] != "K":
                    # return score of the piece at that position
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if SET_WHITE_AS_BOT:
                    if square[0] == 'w':
                        score += pieceScore[square[1]] + \
                            piecePositionScore * .1
                    elif square[0] == 'b':
                        score -= pieceScore[square[1]] + \
                            piecePositionScore * .1
                else:
                    if square[0] == 'w':
                        score -= pieceScore[square[1]] + \
                            piecePositionScore * .1
                    elif square[0] == 'b':
                        score += pieceScore[square[1]] + \
                            piecePositionScore * .1

    return score



# without alpha beta pruning
'''def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves() # opponent validmoves
        ''''''
        - sign because what ever opponents best score is, is worst score for us
        negative turnMultiplier because it changes turns after moves made 
        ''''''
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore'''

