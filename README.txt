Project Name: Discord Bot
by Nevio

Using Discord Developer API, I created a Discord Bot that can be launched into any discord server.
The program is written in Python, and uses Asynchronous I/O syntax for handling command calls in Discord and also sending and receiving messages (and other user inputs.)

There are a few basic commands that are typical features of discord bots, e.g. Ping, Spam, etc.

The bot includes 4 main features (games):
    • Roll Game
        ◦ Basic guessing game of higher or lower number 'hot or cold'
    • Love Calculator
        ◦ Lovecalc, takes two names from a user and randomizes a 'percentage of love' (based on hashing for consistency between names)
        ◦ This percentage is then accompanied with varying replies with different levels of compatibility
    • Hangman
        ◦ Typical hangman game with 5 categories, further categories can be added by uploading more text files of word genres
        ◦ Sends embedded sprites of 'hangman' according to the number of lives left
        ◦ includes user verification to make sure only guesses from same single user are considered
        ◦ includes hint option for users
    • TicTacToe
        ◦ TicTacToe game, board displayed with Discord Emoticons
        ◦ Moves are made with Discord Reacts Emoji, pre-sent so user only has to click on the corresponding signs under the board
        ◦ Includes 2 game modes, to play with friends or to play against oneself.
        ◦ In multiplayer mode, issues a challenge with Discord user-tag to challenged user
        ◦ Win conditions are hard coded for simplicity and efficiency’s sake
        ◦ All messages use embed to give it a more highlighting presence in chat.

To Run Program, need to be logged onto Discord Developer with valid Token.

