import settings
import random
import time
import asyncio
from discord.ext.commands import Bot
from discord.utils import get


TOKEN = settings.nevotoken #ATTENTION, not copied for security reasons


import discord
from discord.ext import commands
import os


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#Bot Setup
BOT_PREFIX = ("n.")
botname = 'nevo'

client = Bot(command_prefix=BOT_PREFIX, help_command=None)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="n.help"))
    print('We have logged in as {0.user}'.format(client))
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#Basic Commands

@client.command()
async def help(ctx):
    embed = discord.Embed(
                        title="nevo Help",
                        description=f"List of commands :100:",
                        color = 0xff0000
                    )
    embed.add_field(name="Games", value=f"```tictactoe ['challenge'/'alone'/'regular']\nrollgame [max value]\nhangman [genre][difficulty]```")
    embed.add_field(name="Misc.", value=f"```\nlovecalc\nping\ntalk [message]```", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms.')
        
@client.command()
async def spam(ctx, amount=10, *, query):
    for _ in range(amount):
        await ctx.send(f'{query}')

@client.command(aliases= ['delete', 'Clear', 'Delete'])
async def clear(ctx, amount=5):
    await ctx.send(f"Clearing {amount} messages...")
    await ctx.channel.purge(limit = amount + 2)

@client.command()
async def roll(ctx, amount=100):
    n = random.randrange(1,amount + 1)
    await ctx.send(f'Your random number is {n}!')

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#Basic guessing game of higher or lower number 'hot or cold'
@client.command()
async def rollgame(ctx, amount = 100):
    if amount < 0:
        await ctx.send(f'Not a positive integer')
        return 1
    n = random.randrange(1, amount + 1)
    sent = await ctx.send("start guessing!")
    count = 0
    errless = True
    win = True
    while win:
        try:
            input1 = await client.wait_for(
                'message',
                timeout= 10,
                check=lambda message: message.author == ctx.author
                                    and message.channel == ctx.channel
                )
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send(f':warning: Cancelling due to timeout.', delete_after = 10)
            errless = False
            break

        guess = int(input1.content)                   
        if guess == n:
            await ctx.send(f'Spot on!')
            win = False
        if guess < n:
            await ctx.send(f'Higher!')
        if guess > n:
            await ctx.send(f'Lower!')
        count += 1
    if errless:
        try:
            await ctx.send(f"Clearing guesses...")  
            await ctx.channel.purge(limit = count * 2 +2)
        except discord.Forbidden:
            await ctx.send(f'unable to clear messages due to no permission')
            
        embed = discord.Embed(
            title = "Roll Game results:",
            description = f":first_place:{str(ctx.author)[:-5]} won with {count} guesses!"
        )
        sent = await ctx.send(embed=embed)   
    
    
@client.command()
async def restart(ctx):
    await client.logout()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    
#Lovecalc, takes two names from a user and randomizes a 'percentage of love' (based on hashing for consistency between names)
#This percentage is then accompanied with varying replies with different levels of compatability
    
@client.command(aliases = ["lc"])
async def lovecalc(ctx, amount = 1):
    permit = True #Was used to only allow some users to use the lovecalc, but set to True for general purposes
    print(str(ctx.author))

            
    
    # waits for incoming message from the author of the command

    if permit:
        compatability = 0
        await ctx.send(f'1st person?')
        msg1 = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)  

        await ctx.send(f'2nd person?')
        msg2 = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

        #random hashing to get calc value
        listname = [str(msg1.content), str(msg2.content)]
        listname.sort()
        namejoin = "".join(listname)
        compatability = int("".join(list(str(hash(namejoin)))[-2:]))
        '''tmp1 = hash(msg1.content)
        tmp2 = hash(msg2.content)
        compatability += int("".join(list(str(tmp1))[-2:]))
        compatability += int("".join(list(str(tmp2))[-2:]))
        compatability //= 2'''

        #reply pool
        ena = [         #75-100%
            f"{msg1.content} likes {msg2.content}",
            f"{msg1.content} loves {msg2.content}",
            f"{msg1.content} wants a deeper relationship with {msg2.content}",
            f"{msg1.content} is eyeing {msg2.content}"]

        conflicted = [  #40-75%
            f"{msg1.content} is conflicted about {msg2.content}",
            f"{msg1.content} has a one sided love with {msg2.content}",
            f"{msg1.content} wants to get back with {msg2.content}",
            f"{msg1.content} is tired of {msg2.content} but still has feelings for {msg2.content} "]

        dendam = [      #0-40
            f"{msg1.content} hates {msg2.content}",
            f"{msg1.content} is ignoring {msg2.content}",
            f"{msg1.content} is avoiding {msg2.content}",
            f"{msg1.content} wants to forget {msg2.content}"]

    #check conditions
            
        if compatability >= 75:
            embed = discord.Embed(
                title = "Love Calc Reading :heart_exclamation::",
                description = f"{random.choice(ena)}"
            )
        elif  compatability >= 40:
            embed = discord.Embed(
                title = "Love Calc Reading :heart_exclamation::",
                description = f"{random.choice(conflicted)}"
                )
        elif compatability < 40:
            embed = discord.Embed(
                title = "Love Calc Reading :heart_exclamation::",
                description = f"{random.choice(dendam)}"
                )

        else: #Error case
            embed = discord.Embed(
                title = "Love Calc Reading :heart_exclamation::",
                description = f"{msg1.content} is confused with {msg2.content}"
            )
            
    #"loading" animation.
        loading = await ctx.send("```Staring program...```")
        #total spaces ~ 70
        text1 = "Initializing program..."
        text2 = "Caluclating compatability..."
        text3 = "Finalizing results..."
        for i in range(1,3):
            time.sleep(0.3)
            text = "```" + text1 + "[" + "======" * i + "      " * (7-i)+ "]" + str(round(14.28 * i)) + "%"+ "```"
            await loading.edit(content=text)
        for i in range(1,3):
            time.sleep(0.3)
            text = "```" + text2 + "[" + "======" * (i+2) + "      " * (5-i)+ "]" + str(round(14.28 * (i+2))) + "%"+ "```"

            await loading.edit(content=text)
        for i in range(1,4):
            time.sleep(0.3)
            text = "```" + text3 + "[" + "======" * (i+4) + "      " * (3-i)+ "]" + str(round(14.28 * (i+4))) + "%"+ "```"

            await loading.edit(content=text)
        time.sleep(0.5)
        await loading.delete()

    #send result
        embed.add_field(name="Compatability", value=f"{compatability}%")
        await ctx.send(embed=embed)

    #print to console
        print("LOVE CALC REQUEST")
        print(f"1:{msg1.content}\n2:{msg2.content}\nP:{compatability}%")
        print()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#Typical hangman game with 5 catagories, further catagories can be added by uploading more text files of word genres
#Sends embedded sprites of 'hangman' according to the number of lives left
#includes user verification to make sure only guesses from same single user are considered
#includes hint option for users
        
@client.command(aliases = ['hg', 'Hangman', 'HANGMAN'])
async def hangman(ctx, genre="", level="normal", *, query=""):
    print(f"User:{str(ctx.author)}")
    
#choosing the genre
    if genre == "":
        ask_category = await ctx.send("What category? [countries, fruits, animals, common words, bts]")
        tmp = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        genre = tmp.content
        await ask_category.delete()
    if genre in ["countries","country"]:
        genre = "Countries"
        filename = "countries.rtf"
    elif genre in ["common", "Common", "common words", "Common words", "Common Words"]:
        genre = "Common words"
        filename = "wl1.rtf"
    elif genre in ["fruits", "Fruits", "fruit", "Fruit", "veggies", "Veggies", "vegetables", "Vegetables"]:
        genre = "Fruits and Vegetables"
        filename = "fruits.rtf"
    elif genre in ["animal", "animals", "Animals", "Animal"]:
        genre = "Animals"
        filename = "animals.rtf"
    elif genre in ["bts", "bts song", "BTS", "BTS song"]:
        genre = "BTS Songs"
        filename = "btssong.rtf"
    else:
        await ctx.send("Invalid category input, setting to **Common words** category", delete_after = 7)
        genre = "Common words"
        filename = "wl1.rtf"


#opening the file        
    with open(filename, 'r') as raw:
        my_words = raw.readlines()[10:]

#choosing the difficulty
    level = level.title()
    if level in ["hard", "Hard"]:
        max_strike = 4
    elif level in ["normal", "Normal"]:
        max_strike = 6
    elif level in ["easy", 'Easy']:
        max_strike = 8
    else:
        await ctx.send("Invalid difficulty input, setting to **Normal** difficulty", delete_after = 7)
        level = "Normal"
        max_strike = 6
        
#variables
    blankchar = '■'
    guesses = 0
    mistaken = 0
    played = False
    stages = {1: 'https://i.imgur.com/sdEaMDH.png',
              2: 'https://i.imgur.com/Up6aZot.png',
              3: 'https://i.imgur.com/Hf5jzbJ.png',
              4: 'https://i.imgur.com/JUUfpNo.png',
              5: 'https://i.imgur.com/kxCMeIu.png',
              6: 'https://i.imgur.com/KaY8bnk.png',
              7: 'https://i.imgur.com/ye6a0t9.png',}
    
#ask whether they wanna play game
    while not played:
        err = False
        sent = await ctx.send('Wanna play? ')
        try:
            q = await client.wait_for(
                'message',
                timeout= 10,
                check=lambda message: message.author == ctx.author
                                    and message.channel == ctx.channel
                )
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send(f':warning: Cancelling due to timeout.', delete_after = 10)
            err = True
            break
        if err:
            break

#Game
        q = q.content
        if q in ['Yes', 'yes', 'YES','y','Y']:
            my_word = list(random.choice(my_words)[:-2].lower())
            #my_word = list("arma dillo banana chicken") #TEST
            my_word2 = ''.join(my_word.copy()).title()
            placeholder = my_word.copy()
            print(''.join(my_word))
            hidden_word = [blankchar for i in range(len(my_word))]
            strikes = 0
            
            spaces = []
            guessed = []
            for i in range(len(my_word2)):
                if my_word2[i] == " ":
                    hidden_word[i] = " "
                    placeholder[i] = " "
                    spaces.append(i)
            
            embed = discord.Embed(
                    title="Hangman",
                    description=f"{str(ctx.author)[:-5]} is guessing",
                    color = 0xd5d90d
                )
            embed.add_field(name="Genre", value=f"{genre}")
            reply1 = await ctx.send(embed=embed)
            blacklist = ['.NevioJus#7139', '.melkiorj#5895'] #Example list of users who need more challenge

#Random event: difficulty modifier for users in blacklist
    #check blacklist
            if str(ctx.author) in blacklist:
                penalty = await ctx.send(f"```DETECTED USER {str(ctx.author)}```")
                time.sleep(0.6)
                await penalty.edit(content = f"``` Making it harder for {str(ctx.author)[:-5]}```")
                time.sleep(0.6)
                await penalty.edit(content = "``` +1 Strike```")
                max_strike -= 1
                m = random.randint(1, 10)
                if m < 5:
                    penalty2 = await ctx.send("``` OOF today's not your day```")
                    time.sleep(0.7)
                    await penalty2.edit(content = "``` +1 Strike```")
                    max_strike -= 1
                reply1 = await ctx.send(embed=embed)

    

    #Game Start        
            while True:
                
            #checks for loss
                if strikes >= max_strike:
                    fail = await ctx.send('Too many strikes! \nThe word was **{0}**'.format(my_word2), delete_after = 10)
                    embed = discord.Embed(
                        title="Hangman",
                        description=f"{str(ctx.author)[:-5]} lost :skull_crossbones: :skull_and_crossbones:",
                        color = 0xff0000
                    )
                    embed.set_image(url=stages[(7-(max_strike - (strikes))) if (7-(max_strike - (strikes))) > 0 else 1])
                    embed.add_field(name="Category", value=f"{genre}")
                    embed.add_field(name='\u200B', value= '\u200B')
                    embed.add_field(name="Guesses left", value=f"{max_strike - strikes}")
                    embed.add_field(name="Difficulty", value=f"{level}", inline = False)
                    embed.add_field(name="The word was", value=f"{''.join(my_word2)}", inline = False)
                    await reply1.edit(embed=embed)
                    played = True
                    break

            #starts/updates the game 'board'

                found = False
                link = stages[1]
                embed = discord.Embed(
                        title="Hangman",
                        description=f"{str(ctx.author)[:-5]} is guessing",
                        color = 0xd5d90d
                    )
                embed.set_image(url=stages[(7-(max_strike - (strikes))) if (7-(max_strike - (strikes))) > 0 else 1])
                embed.add_field(name="Category", value=f"{genre}")
                embed.add_field(name='\u200B', value= '\u200B')
                embed.add_field(name="Guesses left", value=f"{max_strike - strikes}")
                embed.add_field(name="Difficulty", value=f"{level}", inline = False)
                embed.add_field(name="Take a guess!", value=f"{''.join(hidden_word)}", inline = False)
    
                await reply1.edit(embed=embed)

            #awaits player guess
                p_guess = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                #await ctx.send(f"({p_guess.content}) and ({p_guess.content.lower()})")
                p_guess = p_guess.content
                guesses += 1
                
                if guesses != 0:
                    #await reply1.delete()
                    if mistaken != 0:
                        try:
                            await reply2.delete()
                            mistaken -= 1
                        except discord.NotFound:
                            pass
                        
            #checks for "hint" request
                if p_guess == "hint":
                    if str(ctx.author) in blacklist:
                        await ctx.send("No hints for u")
                        guesses -= 1
                    else:
                        n= -1
                        while n in spaces or n in guessed or n == -1:
                            n = random.randrange(1, len(my_word2))
                        hint = [blankchar for _ in range (len(my_word2))]
                        for i in spaces:
                            hint[i] = placeholder[i]
                        for j in guessed:
                            hint[j] = placeholder[j]
                        hint[n] = placeholder[n].upper()
                        await ctx.send("".join(hint))
                        guesses -= 1
                        found = True

            #checks for "stop" reequest
                elif p_guess == 'stop':
                    await ctx.send('Game aborted.')
                    embed = discord.Embed(
                        title="Hangman",
                        description=f"Game aborted... :stop_sign:",
                        color = 0xff0000
                    )
                    await reply1.edit(embed=embed)
                    return 0

            #admin "dig" tool (for debugging)
                elif p_guess == 'dig':
                    await ctx.send(p_guess)
                    await ctx.send(hidden_word)
                    await ctx.send(my_word2)

            #checks for full word guesses
                if len(p_guess) == len(my_word):
                    if list(p_guess) == list(my_word2.lower()):
                        hidden_word = list(my_word2.lower())
                        found = True
                        
            #checks whether letter is in word
                else:
                    for i in range(len(my_word)):
                        if my_word[i] == p_guess:           #updates placeholder word for correct guesses 
                            hidden_word[i] = my_word[i]
                            my_word[i] = blankchar
                            guessed.append(i)
                            found = True

            #adds a strike if incorrect guess
                if not found:
                    strikes += 1
                    fail_embed = discord.Embed(
                        title=":x: WRONG GUESS :x:",
                        description=f"{str(max_strike - strikes)} guess(es) left",
                        color = 0xff0000
                    )
                    mistaken += 1
                    reply2 = await ctx.send(embed=fail_embed, delete_after = 5)
                    #reply2 = await ctx.send('Wrong letter. Strike! (strike count: ' + str(strikes) + ')')

            #if whole word is guessed, send win message
                if hidden_word == list(my_word2.lower()):
                    embed = discord.Embed(
                        title="Congratulations! :trophy:",
                        description=f"{str(ctx.author)[:-5]} has guessed the word, which was **{''.join(my_word2)}**!",
                        color = 0xFFD700
                    )
                    embed.add_field(name="Category", value=f"{genre}")
                    embed.add_field(name="Difficulty", value=f"{level}")
                    await reply1.edit(embed=embed)
                    played = True
                    break

    #asks player if they wanna play again
        elif q in ['No', 'no', 'NO', 'n', 'N']:
            await ctx.send('Game aborted.')
            embed = discord.Embed(
                        title="Hangman",
                        description=f"Game aborted... :stop_sign:",
                        color = 0xff0000
                    )
            await ctx.send(embed=embed)
            break
        else:
            await ctx.send('Invalid input!')
            continue
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#TicTacToe game, board displayed with Discord Emoticons
#Moves are made with Discord Reacts Emoji, pre-sent so user only has to click on the corresponding signs under the board
#Includes 2 game modes, to play with friends or to play against oneself.
#In multiplayer mode, issues a challenge with Discord user-tag to challenged user
#Win conditions are hard coded for simplicity's sake
#All messages use embed to give it a more highlighting presence in chat.


@client.command(aliases = ['ttt'])
async def tictactoe(ctx, gamemode='normal'):

    aborted = False
    
#set players for challenge gamemode
    if gamemode == 'challenge':
        ask = await ctx.send("Challenge who?")
        tag = await client.wait_for('message', check = lambda message : message.author == ctx.author)
        await ctx.send(f"{tag.mentions[0].mention}, you have been challenged to a game of Tic Tac Toe by {ctx.author.mention}\nAccept? (y/n)", delete_after = 30)
        reply = await client.wait_for('message', check = lambda message : message.author == tag.mentions[0] and message.channel == ctx.channel)
        if reply.content in ['y', 'Y', 'yes', 'Yes']:
            playerA = ctx.author
            playerB = reply.author
        else:
            await ctx.send("Challenge denied, Game aborted! :octagonal_sign:")
            aborted = True
                

#set players for alone gamemode
    elif gamemode == 'alone':
        embed = discord.Embed(
            title="Tic Tac Toe",
            description=f"Who  wants to play against {str(ctx.author)[:-5]}? :muscle:",
            color = 0xFFD000
        )
        await ctx.send(embed=embed)
        await ctx.send(f"{str(ctx.author)[:-5]} shall play with themselves")

        playerA = ctx.author
        playerB = ctx.author

        
#set players for regular gamemode
    else:
        embed = discord.Embed(
            title="Tic Tac Toe",
            description=f"Who  wants to play against **{str(ctx.author)[:-5]}**? :muscle:",
            color = 0xFFD000
        )
        challenging = await ctx.send(embed=embed)
        answered = False
        while answered == False:
            try:
                opponent = await client.wait_for('message', check=lambda message: (message.author != ctx.author) and (str(message.author)[:-5] != botname) and (message.channel == ctx.channel), timeout = 20)
                if opponent.content in ['me', 'Me', 'ME', 'gw', 'Gw', 'i', 'I']:
                    answered = True
                    playerA = ctx.author
                    playerB = opponent.author  
                    
            except asyncio.TimeoutError:
                await ctx.send("Timeout. Game aborted :octagonal_sign:", delete_after = 15)
                await challenging.delete()
                aborted = True


#checks if game has been aborted
    if aborted:
        return 0

#decide order of players
    n = random.randint(1,2)
    if n == 1:
        await ctx.send(f"Player {str(playerA)[:-5]} goes first")
        player1 = playerA
        player2 = playerB
    elif n == 2:
        await ctx.send(f"Player {str(playerB)[:-5]} goes first")
        player2 = playerA
        player1 = playerB
    
#Declare players
    await ctx.send(f':x: : **{str(player1)[:-5]}**    :o: : **{str(player2)[:-5]}**')

#Variables
    circle = ':o:'
    cross = ':x:'
    blank = ':black_square_button:'
    
    tl = blank
    tm = blank
    tr = blank
    ml = blank
    mm = blank
    mr = blank
    bl = blank
    bm = blank
    br = blank

    pos_names = ['tl', 'tm', 'tr', 'ml', 'mm', 'mr', 'bl', 'bm', 'br']
    pos = [tl, tm, tr, ml, mm, mr, bl, bm, br]

    nl = '\n'
    sp = ''
    board = pos[0] + pos[1] + pos[2] + nl + pos[3] + pos[4] + pos[5] + nl + pos[6] + pos[7] + pos[8]
    game = await ctx.send(board)

#Win conditions
    win_conditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

#emoji reaction variables
    topleft = '↖'
    topmiddle = '⬆'
    topright = '↗'
    middleleft = '⬅'
    middlemiddle = '⭕'
    middleright= '➡'
    bottomleft = '↙'
    bottommiddle = '⬇'
    bottomright = '↘'
    stop = '⚠'

    direction = ['↖','⬆','↗','⬅','⭕','➡','↙','⬇','↘','⚠']
    
#reacting to initial board with viable reactions
    await game.add_reaction('\N{NORTH WEST ARROW}')
    await game.add_reaction('\N{UPWARDS BLACK ARROW}')
    await game.add_reaction('\N{NORTH EAST ARROW}')
    await game.add_reaction('\N{LEFTWARDS BLACK ARROW}')
    await game.add_reaction('\N{HEAVY LARGE CIRCLE}')
    await game.add_reaction('\N{BLACK RIGHTWARDS ARROW}')
    await game.add_reaction('\N{SOUTH WEST ARROW}')
    await game.add_reaction('\N{DOWNWARDS BLACK ARROW}')
    await game.add_reaction('\N{SOUTH EAST ARROW}')
    await game.add_reaction('\N{WARNING SIGN}')
    

#game initial conditions
    playing = True
    moved = False
    player1_moves = []
    player2_moves = []
    while playing:
        
    #player 1 move
        while not moved:
            ask1 = await ctx.send("Player 1, make your move")
            reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: user == player1)
            for i in range(9):
                if reaction.emoji == direction[-1]:
                    await ctx.send("Game aborted")
                    await game.delete()
                    return 0
                if reaction.emoji == direction[i]:
                    move1 = pos_names[i]
            #move1 = await client.wait_for('message', check=lambda message: message.author == player1)

            for i in range(9):
                if move1 == pos_names[i]:
                    if pos[i] == blank:
                        pos[i] = cross
                        player1_moves.append(i)
                        moved = True
                        await ask1.delete()
                    else:
                        await ctx.send("Position already taken", delete_after = 5)
                        await ask1.delete()
                        postaken = True
            if not moved and not postaken:
                await ctx.send("Invalid response")
                await ask1.delete()
                
    #Updates board
        board = pos[0] + pos[1] + pos[2] + nl + pos[3] + pos[4] + pos[5] + nl + pos[6] + pos[7] + pos[8]
        await game.delete()
        game = await ctx.send(board)

        
    #resets for next player
        moved = False
        postaken = False

    #Detection for player 1 win
        if len(player1_moves) >= 3:
            for i in range(8):
                
                if win_conditions[i][0] in player1_moves and win_conditions[i][1] in player1_moves and win_conditions[i][2] in player1_moves:
                    playing = False
                    embed = discord.Embed(
                        title="Tic Tac Toe",
                        description=f":trophy: **{str(player1)[:-5]}** has won against **{str(player2)[:-5]}** in a game of Tic Tac Toe",
                        color = 0xFFD700
                    )
                    await ctx.send(embed=embed)

    #Detection for draw
        if playing and (len(player1_moves) + len(player2_moves)) == 9:
            playing = False
            embed = discord.Embed(
                    title="Tic Tac Toe",
                    description=f":trophy: **{str(player1)[:-5]}** has drawed against **{str(player2)[:-5]}** in a game of Tic Tac Toe",
                    color = 0x000000
                )
            await ctx.send(embed=embed)
        
    #Resend reactions
        if playing:
            await game.add_reaction('\N{NORTH WEST ARROW}')
            await game.add_reaction('\N{UPWARDS BLACK ARROW}')
            await game.add_reaction('\N{NORTH EAST ARROW}')
            await game.add_reaction('\N{LEFTWARDS BLACK ARROW}')
            await game.add_reaction('\N{HEAVY LARGE CIRCLE}')
            await game.add_reaction('\N{BLACK RIGHTWARDS ARROW}')
            await game.add_reaction('\N{SOUTH WEST ARROW}')
            await game.add_reaction('\N{DOWNWARDS BLACK ARROW}')
            await game.add_reaction('\N{SOUTH EAST ARROW}')
            await game.add_reaction('\N{WARNING SIGN}')

    #player 2 move
        while not moved and playing:
            ask2 = await ctx.send("Player 2, make your move")
            reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: user == player2)
            for i in range(9):
                if reaction.emoji == direction[-1]:
                    await ctx.send("Game aborted")
                    await game.delete()
                    return 0
                if reaction.emoji == direction[i]:
                    move2 = pos_names[i]

            for i in range(9):
                if move2 == pos_names[i]:
                    if pos[i] == blank:
                        pos[i] = circle
                        player2_moves.append(i)
                        moved = True
                        await ask2.delete()
                    else:
                        await ctx.send("Position already taken", delete_after = 5)
                        await ask2.delete()
                        postaken = True
            if not moved and not postaken:
                await ctx.send("Invalid response")
                await ask2.delete()
            
    #updates board  
        board = pos[0] + pos[1] + pos[2] + nl + pos[3] + pos[4] + pos[5] + nl + pos[6] + pos[7] + pos[8]
        await game.delete()
        game = await ctx.send(board)

    #resets for next player
        moved = False
        postaken = False

    #Detection for player2 win

        if len(player2_moves) >= 3:
            for i in range(8):
                if win_conditions[i][0] in player2_moves and win_conditions[i][1] in player2_moves and win_conditions[i][2] in player2_moves:
                    playing = False
                    embed = discord.Embed(
                        title="Tic Tac Toe",
                        description=f":trophy: **{str(player2)[:-5]}** has won against **{str(player1)[:-5]}** in a game of Tic Tac Toe",
                        color = 0xFFD700
                    )
                    await ctx.send(embed=embed)

    #Resend reactions
        if playing:
            await game.add_reaction('\N{NORTH WEST ARROW}')
            await game.add_reaction('\N{UPWARDS BLACK ARROW}')
            await game.add_reaction('\N{NORTH EAST ARROW}')
            await game.add_reaction('\N{LEFTWARDS BLACK ARROW}')
            await game.add_reaction('\N{HEAVY LARGE CIRCLE}')
            await game.add_reaction('\N{BLACK RIGHTWARDS ARROW}')
            await game.add_reaction('\N{SOUTH WEST ARROW}')
            await game.add_reaction('\N{DOWNWARDS BLACK ARROW}')
            await game.add_reaction('\N{SOUTH EAST ARROW}')
            await game.add_reaction('\N{WARNING SIGN}')

    #Repeat asking player1 and player2

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#Run Discord Bot on discord servers with Discord Developer API Token
client.run(TOKEN)

