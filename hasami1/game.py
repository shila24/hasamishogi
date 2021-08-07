#パッケージのインポート
import random
import math

# ゲームの状態##
class State:
    # 初期化
    def __init__(self, pieces=None, enemy_pieces=None, depth=0):
        # 方向定数(縦横８マスまで)
        self.dxy = ((0, -1),(0, -2), (0, -3), (0, -4),(0, -5), (0, -6), (0, -7),(0, -8), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (0, 1),(0, 2), (0, 3), (0, 4),(0, 5), (0, 6), (0, 7),(0, 8), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0), (-8, 0))

        # 駒の配置
        self.pieces = pieces if pieces != None else [0] * (81)
        self.enemy_pieces = enemy_pieces if enemy_pieces != None else [0] * (81)
        self.depth = depth

        # 駒の初期配置
        if pieces == None or enemy_pieces == None:
           self.pieces = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
           self.enemy_pieces = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]


#負けかどうか##
    def is_lose(self):
        count = 0
        pieces0 = self.pieces
        for i in range(81):
          if pieces0[i] == 1:
            count += 1
        count_enemy = 0
        pieces1 = self.enemy_pieces
        for i in range(81):
          if pieces1[80-i] == 1:
            count_enemy += 1
        if count < 2 and count_enemy >= 2:
          return True
        elif self.depth >= 300:
          if count < count_enemy:
            return True
        else:
          return False




    # 引き分けかどうか##
    def is_draw(self):
        count = 0
        pieces0 = self.pieces
        for i in range(81):
          if pieces0[i] == 1:
            count += 1
        count_enemy = 0
        pieces1 = self.enemy_pieces
        for i in range(81):
          if pieces1[80-i] == 1:
            count_enemy += 1
        if count == count_enemy:
           return self.depth >= 300 # 300手

    # ゲーム終了かどうか##
    def is_done(self):
        return self.is_lose() or self.is_draw()

    # デュアルネットワークの入力の2次元配列の取得##
    def pieces_array(self):
        # プレイヤー毎のデュアルネットワークの入力の2次元配列の取得
        def pieces_array_of(pieces):
            table_list = []
            
            table = [0] * 81
            table_list.append(table)
            for i in range(81):
                if pieces[i] == 1:
                   table[i] = 1

            return table_list

        # デュアルネットワークの入力の2次元配列の取得##
        return [pieces_array_of(self.pieces), pieces_array_of(self.enemy_pieces)]

    # 駒の移動先と移動元を行動に変換
    def position_to_action(self, position, direction):
        return position * 32 + direction

    # 行動を駒の移動先と移動元に変換
    def action_to_position(self, action):
        return (int(action/32), action%32)

    # 合法手のリストの取得
    def legal_actions(self):
        actions = []
        for p in range(81):
            # 駒の移動時
            if self.pieces[p]  != 0:
               actions.extend(self.legal_actions_pos(p))

        return actions
    def move_check(self, position_src):
        piece_type = self.pieces[position_src]
        directions = []
        if piece_type == 1: # 「歩」か「と」
            directions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        root =[]
        rootout=[]
        for direction in directions:
                #コマの進む方向を考えるあと引く前で分類　あと引く前が1から8:(1,0) -1から-8:(-1,0) 9以上　-9以下
            if self.dxy[direction][0] >= 1 and self.dxy[direction][1] == 0: 
               dch = 1
            elif self.dxy[direction][0] <= -1 and self.dxy[direction][1] == 0: 
                 dch = -1
            elif self.dxy[direction][0] == 0 and self.dxy[direction][1] >= 1: 
                 dch = 9
            elif self.dxy[direction][0] == 0 and self.dxy[direction][1] <= -1:
                 dch = -9
            focused = position_src + dch
            for i in range(8):
                if focused > 80 or focused < 0:
                   continue
                elif self.pieces[focused] != 1 and self.enemy_pieces[80-focused] !=1:
                     if dch ==1:
                        if focused != position_src + self.dxy[direction][0]:
                           focused = focused + dch
                        elif focused == position_src + self.dxy[direction][0]:
                             root.extend([focused])
                             break
                     elif dch ==-1:
                          if focused != position_src + self.dxy[direction][0]:
                             focused = focused + dch
                          elif focused == position_src + self.dxy[direction][0]: 
                               root.extend([focused])
                               break
                     elif dch ==9:
                          if focused != position_src + 9 * self.dxy[direction][1]:
                             focused = focused + dch
                          elif focused == position_src + 9 * self.dxy[direction][1]: 
                               root.extend([focused])
                               break
                     elif dch ==-9:
                          if focused != position_src + 9 * self.dxy[direction][1]:
                             focused = focused + dch
                          elif focused == position_src + 9 * self.dxy[direction][1]: 
                               root.extend([focused])
                               break
                elif self.pieces[focused] == 1:
                     continue
                elif self.enemy_pieces[80-focused] ==1:
                     continue
        return root             


    # 駒の移動時の合法手のリストの取得
    def legal_actions_pos(self, position_src):
        actions = []

        # 駒の移動可能な方向
        piece_type = self.pieces[position_src]
        directions = []
        if piece_type == 1: # 「歩」か「と」
            directions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        
        for direction in directions:
            # 駒の移動元
            x = position_src%9 + self.dxy[direction][0]
            y = int(position_src/9) + self.dxy[direction][1]
            p = x + y * 9

            # 移動可能時は合法手として追加
            if 0 <= x and x <= 8 and 0<= y and y <= 8 and self.pieces[p] == 0 and self.enemy_pieces[80-p] == 0 and p in self.move_check(position_src):
               actions.append(self.position_to_action(p, direction))

        return actions


    # 次の状態の取得
    def next(self, action):
        # 次の状態の作成
        state = State(self.pieces.copy(), self.enemy_pieces.copy(), self.depth+1)

        # 行動を(移動先, 移動元)に変換
        position_dst, position_src = self.action_to_position(action)

        # 駒の移動

            # 駒の移動元
        x = position_dst%9 - self.dxy[position_src][0]
        y = int(position_dst/9) - self.dxy[position_src][1]
        position_src = x + y * 9

            # 駒の移動
        state.pieces[position_dst] = state.pieces[position_src]
        state.pieces[position_src] = 0

            # 相手の駒が存在する時は取る

        #敵の駒を挟んでいる場合はとる(オセロ応用)
        #上下左右
        remove_check1 = position_dst + 1
        remove_check2 = position_dst - 1
        remove_check3 = position_dst + 9
        remove_check4 = position_dst - 9
        for i in range(10):      
            if int(remove_check1 / 9) != int(position_dst / 9):
               break
            elif remove_check1 > 80 or remove_check1 < 0:
                 break
            elif self.enemy_pieces[80-remove_check1] ==0:
                 break
            elif self.enemy_pieces[80-remove_check1] ==1:
                 remove_check1 += 1
            elif self.pieces[remove_check1] ==1:
                 if remove_check1 == position_dst +1:
                    break
                 elif remove_check1 != position_dst +1:
                      for j in range(remove_check1 - position_dst-1):
                          state.enemy_pieces[80-position_sdt-j] = 0
                          break
        for i in range(10):
          if int(remove_check2 / 9) != int(position_dst / 9):
             break
          elif remove_check2 > 80 or remove_check2 < 0:
               break
          elif self.enemy_pieces[80-remove_check2] ==0:
               break
          elif self.enemy_pieces[80-remove_check2] ==1:
               remove_check1 += -1
          elif self.pieces[remove_check1] ==1:
               if remove_check2 == position_dst -1:
                  break
               elif remove_check2 != position_dst +1:
                    for j in range(position_dst - remove_check2 -1):
                        state.enemy_pieces[80-position_sdt+j] = 0
                        break

        for i in range(10):
          if remove_check3 % 9 != position_dst % 9:
             break
          elif remove_check3 > 80 or remove_check3 < 0:
               break
          elif self.enemy_pieces[80-remove_check3] ==0:
               break
          elif self.enemy_pieces[80-remove_check3] ==1:
               remove_check1 += 9
          elif self.pieces[remove_check1] ==1:
               if remove_check3 == position_dst + 9:
                  break
               elif remove_check3 != position_dst +9:
                    for j in range(int((remove_check3 - position_dst)/9) -1):
                        state.enemy_pieces[80-position_sdt- 9*j] = 0
                        break
        for i in range(10):
          if remove_check4 % 9 != position_dst % 9:
             break
          elif remove_check4 > 80 or remove_check4 < 0:
               break          
          elif self.enemy_pieces[80-remove_check4] ==0:
               break
          elif self.enemy_pieces[80-remove_check4] ==1:
               remove_check1 += -9
          elif self.pieces[remove_check4] ==1:
               if remove_check4 == position_dst -9:
                  break
               elif remove_check4 != position_dst -9:
                    for j in range(int((position_dst - remove_check4)/9) -1):
                        state.enemy_pieces[80-position_sdt + 9*j] = 0
                        break    
           

        #敵の駒が囲まれている場合はとる
        #今回は端で3個固まるところまで定義#エラーが出たら囲碁を応用
        #0の場合
        if self.enemy_pieces[80-0] ==1:
          #0に敵駒、1,2の味方に囲まれる
          if self.pieces[1]==1 and self.pieces[9]==1:
            state.enemy_pieces[80-0]=0
          #0,1に敵駒、9に味方駒
          elif self.enemy_pieces[80-1] ==1 and self.pieces[9]==1:
               #2,9,10で囲まれる
               if self.pieces[2]==1 and self.pieces[10]==1:
                  state.enemy_pieces[80-0]=0
                  state.enemy_pieces[80-1]=0
               #0,1,2に敵駒
               elif self.enemy_pieces[80-2] == 1:
                 #3,9,10,11で囲まれる
                 if self.pieces[10]==1 and self.pieces[11]==1 and self.pieces[3]==1:
                    state.enemy_pieces[80-0]=0
                    state.enemy_pieces[80-1]=0
                    state.enemy_pieces[80-2]=0
          #0,9に敵駒、1に味方駒
          elif self.enemy_pieces[80-9] ==1 and self.pieces[1]==1:
                 #1, 10,18で囲まれる
                 if self.pieces[10]==1 and self.pieces[18]==1:
                    state.enemy_pieces[80-0]=0
                    state.enemy_pieces[80-9]=0
                 #0,9,18に敵駒
                 elif self.enemy_pieces[80-18]==1:
                      if self.pieces[10]==1 and self.pieces[19]==1 and self.pieces[27]==1:
                         state.enemy_pieces[80-0]=0
                         state.enemy_pieces[80-9]=0
                         state.enemy_pieces[80-18]=0                        
          elif self.enemy_pieces[80-1] ==1 and self.enemy_pieces[80-9]==1:
            if self.pieces[2]==1 and self.pieces[10]==1 and self.pieces[18]==1:
               state.enemy_pieces[80-0]=0
               state.enemy_pieces[80-1]=0
               state.enemy_pieces[80-9]=0                
        #8の場合
        if self.enemy_pieces[80-8] ==1:
          #8に敵駒、7,17の味方に囲まれる
          if self.pieces[7]==1 and self.pieces[17]==1:
            state.enemy_pieces[80-0]=0
          #7,8に敵駒、17に味方駒
          elif self.enemy_pieces[80-7] ==1 and self.pieces[17]==1:
               #6、16、17で囲まれる
               if self.pieces[6]==1 and self.pieces[16]==1:
                  state.enemy_pieces[80-7]=0
                  state.enemy_pieces[80-8]=0
               #6,7,8に敵駒
               elif self.enemy_pieces[80-6] == 1:
                 #5,15, 16,17で囲まれる
                 if self.pieces[15]==1 and self.pieces[16]==1 and self.pieces[5]==1:
                    state.enemy_pieces[80-6]=0
                    state.enemy_pieces[80-7]=0
                    state.enemy_pieces[80-8]=0
          #8,17に敵駒、7に味方駒
          elif self.enemy_pieces[80-17] ==1 and self.pieces[7]==1:
                 #7, 16,26で囲まれる
                 if self.pieces[16]==1 and self.pieces[26]==1:
                    state.enemy_pieces[80-8]=0
                    state.enemy_pieces[80-17]=0
                 #8,17,26に敵駒
                 elif self.enemy_pieces[80-26]==1:
                      if self.pieces[16]==1 and self.pieces[25]==1 and self.pieces[35]==1:
                         state.enemy_pieces[80-0]=0
                         state.enemy_pieces[80-17]=0
                         state.enemy_pieces[80-26]=0                        
          elif self.enemy_pieces[80-7] ==1 and self.enemy_pieces[80-17]==1:
            if self.pieces[6]==1 and self.pieces[16]==1 and self.pieces[26]==1:
               state.enemy_pieces[80-7]=0
               state.enemy_pieces[80-8]=0
               state.enemy_pieces[80-17]=0

         #72の場合
        if self.enemy_pieces[80-72] ==1:
          #63,73の味方に囲まれる
          if self.pieces[63]==1 and self.pieces[73]==1:
            state.enemy_pieces[80]==0
          #73に敵駒、63に味方駒
          elif self.enemy_pieces[80-73] ==1 and self.pieces[63]==1:
               #63、64、74で囲まれる
               if self.pieces[64]==1 and self.pieces[74]==1:
                  state.enemy_pieces[80-72]=0
                  state.enemy_pieces[80-73]=0
               #72,73,74に敵駒
               elif self.enemy_pieces[80-74] == 1:
                 #63,64, 65,75で囲まれる
                 if self.pieces[64]==1 and self.pieces[65]==1 and self.pieces[75]==1:
                    state.enemy_pieces[80-72]=0
                    state.enemy_pieces[80-73]=0
                    state.enemy_pieces[80-74]=0
          #63,72に敵駒、73に味方駒
          elif self.enemy_pieces[80-63] ==1 and self.pieces[73]==1:
                 #54,64,73で囲まれる
                 if self.pieces[54]==1 and self.pieces[64]==1:
                    state.enemy_pieces[80-63]=0
                    state.enemy_pieces[80-72]=0
                 #54,63,72に敵駒
                 elif self.enemy_pieces[80-54]==1:
                      if self.pieces[45]==1 and self.pieces[55]==1 and self.pieces[64]==1:
                         state.enemy_pieces[80-54]=0
                         state.enemy_pieces[80-63]=0
                         state.enemy_pieces[80-72]=0                        
          elif self.enemy_pieces[80-63] ==1 and self.enemy_pieces[80-73]==1:
            if self.pieces[54]==1 and self.pieces[64]==1 and self.pieces[74]==1:
               state.enemy_pieces[80-63]=0
               state.enemy_pieces[80-72]=0
               state.enemy_pieces[80-73]=0               

         #80の場合
        if self.enemy_pieces[80-80] ==1:
          #71,79の味方に囲まれる
          if self.pieces[71]==1 and self.pieces[79]==1:
            state.enemy_pieces[80]==0
          #79に敵駒、71に味方駒
          elif self.enemy_pieces[80-79] ==1 and self.pieces[71]==1:
               #71,70,78で囲まれる
               if self.pieces[70]==1 and self.pieces[78]==1:
                  state.enemy_pieces[80-80]=0
                  state.enemy_pieces[80-79]=0
               #78,79,80に敵駒
               elif self.enemy_pieces[80-78] == 1:
                 #69, 70, 71, 77で囲まれる
                 if self.pieces[69]==1 and self.pieces[70]==1 and self.pieces[77]==1:
                    state.enemy_pieces[80-78]=0
                    state.enemy_pieces[80-79]=0
                    state.enemy_pieces[80-80]=0
          #71,80に敵駒、79に味方駒
          elif self.enemy_pieces[80-71] ==1 and self.pieces[79]==1:
                 #62,70,79で囲まれる
                 if self.pieces[62]==1 and self.pieces[70]==1:
                    state.enemy_pieces[80-71]=0
                    state.enemy_pieces[80-80]=0
                 #62,71,80に敵駒
                 elif self.enemy_pieces[80-62]==1:
                      if self.pieces[53]==1 and self.pieces[61]==1 and self.pieces[70]==1:
                         state.enemy_pieces[80-62]=0
                         state.enemy_pieces[80-71]=0
                         state.enemy_pieces[80-80]=0                        
          elif self.enemy_pieces[80-71] ==1 and self.enemy_pieces[80-79]==1:
            if self.pieces[62]==1 and self.pieces[70]==1 and self.pieces[78]==1:
               state.enemy_pieces[80-80]=0
               state.enemy_pieces[80-71]=0
               state.enemy_pieces[80-79]=0 

        # 駒の交代
        w = state.pieces
        state.pieces = state.enemy_pieces
        state.enemy_pieces = w
        return state

    # 先手かどうか
    def is_first_player(self):
        return self.depth%2 == 0

    # 文字列表示
    def __str__(self):
        pieces0 = self.pieces  if self.is_first_player() else self.enemy_pieces
        pieces1 = self.enemy_pieces  if self.is_first_player() else self.pieces

        str = ''

        # ボード
        for i in range(81):
            if pieces0[i] == 1:
                str += 'F'
            elif pieces1[80-i] == 1:
                str += 'T'
            else:
                str += '-'
            if i % 9 == 8:
                str += '\n'

        return str

# ランダムで行動選択
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions)-1)]

# 動作確認
if __name__ == '__main__':
    # 状態の生成
    state = State()

    # ゲーム終了までのループ
    while True:
        # ゲーム終了時
        if state.is_done():
            break

        # 次の状態の取得
        state = state.next(random_action(state))

        # 文字列表示
        print(state)
        print()
