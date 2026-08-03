## Specifications

• There are two types of users. Admin user who will configure and run the reports and the Player
user who will play the game.

• User registration: allow the users to register and log in with username and password. Username
should have at least 5 letters (both upper and lower case) and password should be at least 5
characters (should have alpha, numeric, and one of special characters $, %, * and)

• Save twenty 5-letter English words (upper case) in database to start with.

• When a user starts playing guess game, pick one word randomly from the database and let the
user guess that word. Don't allow more than 3 words to guess in a day for a user.

## Game Rules 

• When the guess game starts, allow the user to submit a 5-letter word (upper case only). Allow
a maximum of 5 guesses. Show the letters in the upper case.

• When a word is submitted, if the letter is correct and in the right position, it is highlighted in
green. If the letter is correct but in the wrong position, highlight it in orange color. If the letter is
not in the word, it is highlighted in grey.

• If the word guessed by the user matches the word, user wins the game. Show congratulatory
message and when the user clicks on OK, stop the game.

• If the user tried all 5 guesses and could not guess correctly, show 'better luck next time'
message and when user click on OK, stop the game.

• If the word guessed by the user does not match the word, allow the user to guess the word
again. Show the earlier guesses in the same sequence guessed (refer to the picture) and
allow the user to submit the next guess. Allow a maximum of 5 guesses.

• Save in database the words given and the words guessed by the user for each word with date.

• Admin users should be able to see a report for a day (number of users and number of correct
guesses) and a report for a user (date, number of words tried and number of correct guesses).