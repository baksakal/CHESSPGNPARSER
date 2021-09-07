
from dataclasses import asdict
from re import I
import chess.pgn 
from collections import Counter

#get the data for a single player
def get_data(png_folder1, player_name):
    game_cnt = 0
    games_before = []
    games_after = []
    h_count_before_fin = 0
    h_count_after_fin = 0
    ah_find_list = []
    h_list_before = []
    ah_find_list2 = []
    h_list_after = []

    while True:
        current_game = chess.pgn.read_game(png_folder)
        game_cnt = game_cnt + 1
        #print(game_cnt)
        if current_game is None:
            break
        try:
            date = int((current_game.headers["Date"])[0:4])
            #get games before AlphaZero, thus gamebefore 2018, append the opening
            if 2014 <= date < 2018:
                games_before.append(current_game.headers["ECO"])

                if ((current_game.headers["White"]).find(player_name)) != -1: # -1 means not found
                    player = 0 # top 10 player is white
                else:
                    player = 1 # top 10 player is black

                ah_find_list = str(current_game.mainline_moves()).split(".")

                h_list_before = []

                for i in ah_find_list:
                    h_list_before.append(i.split(" "))

                for i in h_list_before:
                    try:
                        i.pop()
                        del i[0]
                    except:
                        pass

                #Search for moves: 
                #For white h-4
                #For black h-5
                #King side pawn forward

                for i in range(len(h_list_before)):
                    try:
                        if player == 0: #player is white
                            if (h_list_before[i][player]) == "h4":
                                h_count_before_fin = h_count_before_fin + 1

                        else:#player is black
                            if (h_list_before[i][player]) == "h5":
                                h_count_before_fin = h_count_before_fin + 1

                    except:
                        pass
              
            ah_find_list = []
            h_list_before = []


            #get games after AlphaZero, thus gameafter 2018, append the opening
            if date >= 2018:
                games_after.append(current_game.headers["ECO"])

                if ((current_game.headers["White"]).find(player_name)) != -1: # -1 means not found
                    player = 0 # top 10 player is white
                else:
                    player = 1 # top 10 player is black

                ah_find_list2 = str(current_game.mainline_moves()).split(".")

                h_list_after = []

                for i in ah_find_list2:
                    h_list_after.append(i.split(" "))

                for i in h_list_after:
                    try:
                        i.pop()
                        del i[0]
                    except:
                        pass

                #Search for moves: 
                #For white h-4
                #For black h-5
                #King side pawn forward

                for i in range(len(h_list_after)):
                    try:
                        if player == 0: #player is white
                            if (h_list_after[i][player]) == "h4":
                                h_count_after_fin = h_count_after_fin + 1

                        else:#player is black
                            if (h_list_after[i][player]) == "h5":
                                h_count_after_fin = h_count_after_fin + 1
                                

                    except:
                        pass

            ah_find_list2 = []
            h_list_before = []   
                
                
        except:
            #if opening does not exists, drop the game
            #print("game dropped")
            pass
    #return frequentative openings percentage as a list of strings 
    return get_opening_before_after_single_player(games_before, games_after), (100 * h_count_before_fin / len(games_before)), (100 * h_count_after_fin / len(games_after))

#calculate opening percentages
def get_opening_before_after_single_player(games_before,games_after):
    c1 = []
    c2 = []
    #total number of games_before is saved to calculate their percentage, see line 62
    games_before_total_count = len(games_before)
    #openings with their corresponding frequencies
    games_before = Counter(games_before).most_common()
    for i in range(len(games_before)):
        #creating temporary list two store [opening_name , play_percentage]
        listof = []
        #append the opening name to the temporary list
        listof.append(games_before[i][0])
        #calculate the play_percentage using stored value, append this to the temporary list
        listof.append(round((games_before[i][1] * 100 / games_before_total_count),2)) 
        #temporary list is in the form of [opening_name , play_percentage]. Append this list to a final list, consisting of all the openings
        c1.append(listof) 
        listof = []

    #total number of games_after is saved to calculate their percentage, see line 77
    games_after_total_count = len(games_after)
    #openings with their corresponding frequencies
    games_after = Counter(games_after).most_common()
    for i in range(len(games_after)):
        #creating temporary list two store [opening_name , play_percentage]
        listof = []
        #append the opening name to the temporary list
        listof.append(games_after[i][0])
        #calculate the play_percentage using stored value, append this to the temporary list
        listof.append(round((games_after[i][1] * 100 / games_after_total_count),2)) 
        #temporary list is in the form of [opening_name , play_percentage]. Append this list to a final list, consisting of all the openings
        c2.append(listof) 
        listof = []

    return combine_openings_into_types(c1,c2)

def combine_openings_into_types(openings_before, openings_after):
    eco_starting_char = ""
    #every opening type starts with zero percentage
    flank_openings = 0
    semi_open_games_except_french = 0
    open_games_and_french = 0
    closed_games_and_semi_closed = 0
    indian_defences = 0
    list_to_return_before = []

    for i in range(len(openings_before)):

        #Combine based on ECO notation
        eco_starting_char = (openings_before[i][0][0])

        if eco_starting_char == 'A':
            flank_openings = flank_openings + openings_before[i][1]

        elif eco_starting_char == "B":
            semi_open_games_except_french = semi_open_games_except_french + openings_before[i][1]
        
        elif eco_starting_char == "C":
            open_games_and_french = open_games_and_french + openings_before[i][1]

        elif eco_starting_char == "D":
            closed_games_and_semi_closed = closed_games_and_semi_closed + openings_before[i][1]
        
        elif eco_starting_char == "E":
            indian_defences = indian_defences + openings_before[i][1]

    list_to_return_before.append([["A",flank_openings],["B",semi_open_games_except_french],["C",open_games_and_french],["D",closed_games_and_semi_closed],["E",indian_defences]])

    eco_starting_char = ""
    #every opening type starts with zero percentage
    flank_openings = 0
    semi_open_games_except_french = 0
    open_games_and_french = 0
    closed_games_and_semi_closed = 0
    indian_defences = 0
    list_to_return_after = []

    for i in range(len(openings_after)):

        #Combine based on ECO notation
        eco_starting_char = (openings_after[i][0][0])

        if eco_starting_char == 'A':
            flank_openings = flank_openings + openings_after[i][1]

        elif eco_starting_char == "B":
            semi_open_games_except_french = semi_open_games_except_french + openings_after[i][1]
        
        elif eco_starting_char == "C":
            open_games_and_french = open_games_and_french + openings_after[i][1]

        elif eco_starting_char == "D":
            closed_games_and_semi_closed = closed_games_and_semi_closed + openings_after[i][1]
        
        elif eco_starting_char == "E":
            indian_defences = indian_defences + openings_after[i][1]

    list_to_return_after.append([["A",flank_openings],["B",semi_open_games_except_french],["C",open_games_and_french],["D",closed_games_and_semi_closed],["E",indian_defences]])

    return list_to_return_before, list_to_return_after


#get openings for every player

def create_and_display_player(pgn_folder,player_name):
    games, h_games_before, h_games_after = (get_data(png_folder,player_name))
    print("----------------------")
    print(player_name)
    print("Games Before:")
    print(games[0][0])
    print("Games After:")
    print(games[1][0])
    print("H moves Before:")
    print(h_games_before)
    print("H moves After:")
    print(h_games_after)
    return 0


png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Carlsen.pgn")
player_name = "Carlsen"
create_and_display_player(png_folder,player_name)

png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Aronian.pgn")
player_name = "Aronian"
create_and_display_player(png_folder,player_name)

png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Caruana.pgn")
player_name = "Caruana"
create_and_display_player(png_folder,player_name)
png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Ding.pgn")
player_name = "Ding"
create_and_display_player(png_folder,player_name)

png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Mamedyarov.pgn")
player_name = "Mamedyarov"
create_and_display_player(png_folder,player_name)

png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Nepomniachtchi.pgn")
player_name = "Nepomniachtchi"
create_and_display_player(png_folder,player_name)

png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Grischuk.pgn")
player_name = "Grischuk"
create_and_display_player(png_folder,player_name)

png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Giri.pgn")
player_name = "Giri"
create_and_display_player(png_folder,player_name)

png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\Radjabov.pgn")
player_name = "Radjabov"
create_and_display_player(png_folder,player_name)

png_folder =  open(r"C:\\Users\\draks\\Desktop\\project\\So.pgn")
player_name = "So"
create_and_display_player(png_folder,player_name)

