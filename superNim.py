import random
class Super_Nim:
    #start() returns the initial state and play limit for the game
    def start(self):
        turn = 'Max'
        heap_tuple = (41,62,74,94)
        max_score = 0
        min_score = 0
        play_limit = 100
        state = turn,tuple(sorted(heap_tuple)),max_score,min_score
        return state,play_limit

    #Terminal() checks if the state is terminal or not
    def terminal(self,state):
        turn,heap_tuple,max_score,min_score = state
        if heap_tuple == (): return True
        else: return False    

    #U_heur() returns the huristic utility
    def U_heur(self):
        return 50
    
    #Player() returns the next player name 
    def player(self,state):
        turn,heap_tuple,max_score,min_score = state
        play = {'Min':'Max','Max':'Min'}
        return play[turn]
    
    #U_terminal() returns the actual Utility for states reached at terminal nodes 
    def U_terminal(self,state):
        turn,heap_tuple,max_score,min_score = state
        if self.terminal(state) == True and max_score < min_score:
            return -100
        elif self.terminal(state) == True and max_score > min_score: 
            return 100
        elif self.terminal(state) == True and max_score == min_score:
            return 0
        else:
            assert False

    #Succ() returns the refined (with No duplicates) possible successors of a state
    def succ(self,state):
        successor = []
        turn,heap_tuple,max_score,min_score = state
        turn = self.player(state)
        for i, v in enumerate(heap_tuple):
            temp_list = list(heap_tuple[:])
            #Removing heap with 2 sticks,adding two points and appending it to successor list
            if v == 2:  
                temp_list.pop(i)
                if turn == 'Min':
                    mini= 0
                    maxi = 2
                else:
                    mini= 2
                    maxi = 0
                successor.append((turn,tuple(temp_list),max_score + maxi,min_score + mini))
            #Spliting heap with even number of sticks and appending it to successor list   
            elif v % 2 == 0 and v != 2 :  
                temp_value=v / 2
                temp_list.pop(i)
                [temp_list.insert(i,temp_value) for q in range(2)]
                successor.append((turn,tuple(temp_list),max_score,min_score))
            #Applying Collatz-Ulam on heap with odd number of sticks and appending it to successor list
            elif v % 2 != 0:
                #temp_value=v + 1  # Altered rule for heaps having odd number of sticks, just add 1
                temp_value=(v * 3) + 1
                temp_list.pop(i)
                temp_list.insert(i,temp_value)
                successor.append((turn,tuple(temp_list),max_score,min_score))
            #Taking one heap and putting it on another, capping at 10 and appending it to successor list
            for j in range(i+1,len(heap_tuple)):
                temp_list = list(heap_tuple[:])
                if heap_tuple[i] != heap_tuple[j]:
                    if temp_list[j] + temp_list[i] > 10:
                       temp_list[j] = 10
                       #temp_list[j] = 2 #Altered rule, Heaps exceeding 10 becomes 2 
                    else:
                        temp_list[j] = temp_list[j] + temp_list[i]
                    temp_list.pop(i)
                    successor.append((turn,tuple(temp_list),max_score,min_score))
        #Command below, Removes duplicate successors and returns the refined successor list 
        return list(set([tuple((n[0],tuple(sorted(n[1])),n[2],n[3])) for n in successor])) 

    #Minimax_U(), Returns Utility of a state using alpha-beta algorithm, with depth cutoff at 7 
    def Minimax_U(self,state,alpha,beta,depth):
        player,heap_tuple,max_score,min_score = state
        depth = depth + 1
        if self.terminal(state)== True: 
            return self.U_terminal(state)
        elif player == 'Max' and depth <= 7: # cutoff at 7th level for Max player
             bestValue = float('-inf')
             for suc in self.succ(state):
                 bestValue = max (bestValue,self.Minimax_U(suc,alpha,beta,depth))
                 alpha = max(alpha,bestValue)
                 if alpha >= beta:          # Pruning the tree, if alpha >= beta
                    break
             return bestValue     
        elif player == 'Min' and depth <= 7: # cutoff at 7th level for Min player
            bestValue = float('inf')
            for suc in self.succ(state):
                bestValue = min (bestValue,self.Minimax_U(suc,alpha,beta,depth))
                beta = min(beta,bestValue)
                if beta <= alpha:           # Pruning the tree, if beta <= alpha
                    break
            return bestValue
        else:
            return self.U_heur()

    #Move() returns best possible move for AI player   
    def move(self,state,my_cache):
        player,heap_tuple,max_score,min_score = state
        alpha = float('-inf')
        beta = float('inf')
        depth = 0
        successor_utility = []
        
        #Computing Current state Utility / Checking in the cache 
        if state in my_cache:
            state_utility = my_cache[state]
        elif state not in my_cache:
            state_utility = self.Minimax_U(state,alpha,beta,depth)
            my_cache[state] = state_utility #storing in the cache
        state_successor = self.succ(state)
        print 'Utility of Current State: ',state_utility
        
        #Computing Successors Utility/ Checking in the cache 
        for j in state_successor:
            play,heap,maxi,mini = j
            if j in my_cache:
                successor_utility.append((my_cache[j],j))
            elif j not in my_cache:
                utility= self.Minimax_U(j,alpha,beta,depth)
                my_cache[j] = utility   #storing in the cache
                successor_utility.append((utility,j))
        print 'State Successors and their Utilities:\n',successor_utility
        
        #Selecting the best Move    
        #looking for better utility than the sate itself has
        for i in successor_utility:
            pla,hea,maxs,mins = i[1]  
            if i[0] == 100 and player == 'Max' and maxs > max_score : return i[1]
            elif i[0] == -100 and player == 'Min' and mins > min_score: return i[1]    
        for i in successor_utility :
            if i[0] == 100 and player == 'Max': return i[1]
            elif i[0] == -100 and player == 'Min': return i[1]
            
        #looking for 50 utility with better score        
        for i in successor_utility:
            pla,hea,maxs,mins = i[1]
            if i[0] == 50 and player == 'Max' and maxs > max_score: return i[1]
            elif i[0] == 50 and player == 'Min' and mins > min_score: return i[1]
        for i in successor_utility :
            if i[0] == 50: return i[1]
            
        #looking for utility to Draw the game
        for i in successor_utility:
            pla,hea,maxs,mins = i[1]
            if i[0] == 0 and player == 'Max' and maxs > max_score: return i[1]
            elif i[0] == 0 and player == 'Min'and mins > min_score: return i[1]         
        for i in successor_utility :
            if i[0] == 0: return i[1]
            
        #Otherwise picking the first successor
        last_option = successor_utility[0]    
        return last_option[1]
    
    #random_move() returns a move randomly choosen from successor list        
    def random_move(self,state):
        options = self.succ(state)
        print'Current State Successors: ',options
        ram = options[random.randint(0,len(options)-1)]
        print 'Choosen Move: ',ram 
        return ram

    #RandomPlayer() returns random player move
    def RandomPlayer(self,state,q):
        print '\n******************RANDOM PLAYER',q,'TURN*******************************'
        print 'Current state:', state
        return self.random_move(state)
                                    
    #Human_Player() takes input from human player and returns    
    def Human_Player(self,state):
        print '\n******************HUMAN PLAYER TURN******************************** '
        print 'Current state is :', state
        my_dict = {}
        options = self.succ(state)
        for j in range(0,len(options)):
            my_dict[j] = options[j]
            print j,'>>',my_dict[j]
        human_move = input("please enter the number of desired move")
        return my_dict[human_move]

    #AIPlayer() returns AI player move   
    def AIPlayer(self,state,my_cache,q):
        print '\n******************AI PLAYER',q,'TURN******************************* '
        print 'Current state is :', state
        aiMove = self.move(state,my_cache)
        print'Choosen Move: ',aiMove
        return aiMove

#winner_check() checks whether a player wins or not at game end    
def winner_check(state,play_count,play_limit,game,p):
    player,heap_tuple,max_score,min_score = state
    if (heap_tuple == () or play_count == play_limit):
        if max_score > min_score and game in (1,2,3):
            print 'AI player',p,'has Won'
            return True
        elif max_score < min_score and game == 1 :
            print 'AI player 2 has Won'
            return True
        elif max_score < min_score and game in (2,4) :
            print 'Random player',p,'has Won'
            return True
        elif (max_score < min_score and game == 3):
            print 'Human Player has Won'
            return True
        elif (max_score > min_score and game == 4)  :
            print 'Random player 1 has Won'
            return True
        elif max_score == min_score:
            print 'Its a Draw'
            return True
        
#GameManager() Manages the whole game
def GameManager():
    game = input("1:>> AI Vs AI \n2:>> AI Vs Random \n3:>> AI Vs Human \n4:>> Random Vs Random \nPlease choose the desired Competition,\nEnter 1,2,3 or 4 and press Enter : ")
    ins = Super_Nim()
    state, play_limit = ins.start()
    player,heap_tuple,max_score,min_score = state
    play_count = 0
    my_cache = {}
    while heap_tuple != () or play_count != play_limit:
        play_count = play_count + 1
        print '\n\n                   Play Count:',play_count,'\n'
        if game == 1:
            state = ins.AIPlayer(state,my_cache,1)
            pl,hetu,masc,misc = state
            if hetu != ():state = ins.AIPlayer(state,my_cache,2)
            if winner_check(state,play_count,play_limit,game,1):
                break
        elif game == 2:
            state = ins.AIPlayer(state,my_cache,'')
            pl,hetu,masc,misc = state
            if hetu != ():state = ins.RandomPlayer(state,'')
            if winner_check(state,play_count,play_limit,game,''):
                break
        elif game == 3:
            state = ins.AIPlayer(state,my_cache,'')
            pl,hetu,masc,misc = state
            if hetu != ():state=ins.Human_Player(state)
            if winner_check(state,play_count,play_limit,game,''):
                break
        elif game == 4:
            state = ins.RandomPlayer(state,1)
            pl,hetu,masc,misc = state
            if hetu != ():state = ins.RandomPlayer(state,2)          
            if winner_check(state,play_count,play_limit,game,2):
                break
                                 
GameManager()
