import itertools, math, copy
import pandas as pd

handsize = 3

available_cards = [i for i in range(1,10)]

def ch(hand,handsize):
    d = itertools.combinations(hand,handsize)
    for i in d:
        if sum(i) == 15: return True
    return False

def indexify(p1_hand,p2_hand):
    index = 0
    for c in p1_hand: index = index*10 + c
    for c in p2_hand: index = index*10 + c
    return index

def f_n(input_str):
    df = pd.read_csv(str(len(str(input_str))) + '.csv')
    return df.at[input_str,'choices']

def create_last_df():

    p1_wins = 0
    p2_wins = 0
    turn = 9
    orders = itertools.permutations(available_cards)

    indexes = []
    results = []

    for order in orders:
        p1_hand = order[:math.ceil(turn/2)]
        p2_hand = order[math.ceil(turn/2):turn]
        leftovers = order[turn:]

        p1_win = ch(p1_hand,handsize)
        p2_win = ch(p2_hand,handsize)

        if p1_win and p2_win:
            temp_p1_hand = copy.deepcopy(p1_hand)
            temp_p2_hand = copy.deepcopy(p2_hand)
            
            while p1_win and p2_win:
                temp_p1_hand = temp_p1_hand[:-1]
                temp_p2_hand = temp_p2_hand[:-1]

                p1_win = ch(temp_p1_hand,handsize)
                p2_win = ch(temp_p2_hand,handsize)

            if p2_win and not p1_win: result = -1
            elif p1_win and not p2_win: result = 1
            else: result = 0

        elif p1_win: result = 1
        elif p2_win: result = -1
        else: result = 0

        #formatting_order
        index = 0
        for c in p1_hand: index = index*10 + c
        for c in p2_hand: index = index*10 + c

        results.append(result)
        indexes.append(index)
    #print(indexes)

    df_9 = pd.DataFrame(results,index=indexes, columns=["result"])
    df_9.to_csv('9.csv',index=True, index_label = False)
    return df_9
    
def create_hl_df(turn):
    p1_wins = 0
    p2_wins = 0
    orders = itertools.permutations(available_cards)

    indexes = []
    data = []

    future_df = pd.read_csv(str(turn+1) + '.csv')
    player = 2 - ((turn+1)%2)
    print("player : ",player)

    for order in orders:

        p1_hand = order[:math.ceil(turn/2)]
        p2_hand = order[math.ceil(turn/2):turn]
        leftovers = order[turn:]
        
        possible_choice = []     
        possible_outcomes = []
        for choice in leftovers:
            p1_future_hand = copy.deepcopy(p1_hand)
            p2_future_hand = copy.deepcopy(p2_hand)

            if player == 1: p2_future_hand = p2_hand + (choice,)
            else: p1_future_hand = p1_hand + (choice,)
                
            future_index = indexify(p1_future_hand,p2_future_hand)

            possible_choice.append(choice)
            possible_outcomes.append(future_df.at[future_index,'result'])

        #print("fi: ",future_index," choice: ",choice, " outcome: ", possible_outcomes)


        if player == 1: result = max(possible_outcomes)
        if player == 2: result = min(possible_outcomes)

        data.append([result,choice])
            
        #formatting_order
        index = indexify(p1_hand,p2_hand)

        if index == 12374589:
            print(index)
            print(result)
            print(possible_outcomes)
            print(p1_hand)
            print(p2_hand)
        
        indexes.append(index)

    df = pd.DataFrame(data,index=indexes, columns=["result","choices"])
    df = df.reset_index().drop_duplicates(subset='index', keep='last').set_index('index')
    df.to_csv(str(turn)+'.csv',index=True, index_label = False)
    return df

ty = create_last_df()
for turn in range(8,0,-1):
    create_hl_df(turn)
