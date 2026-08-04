## Flow diagrams
1. Authentication

    Landing Page -> Login / Register -> AuthenticateUsername + Password -> Check Role in Database = Admin/player

2. Implementation flow

Browser
    ↓
Flask
    ↓
Business Logic

## API End points

/login

    params: username/email, password
    return token, role, checkbox
    redirects to corresponding dashboard
    Think about strong jwt auth!!

/register

    Think about admin register-Admin accounts are seeded into the database or created manually.
    params: username/email, password re-type password
    redirects to corresponding dashboard
    return token


/create

    params: user_id
    check-limit()
    get-word()
    load-gamepage()
    start-game()
    game()
    trigger-end()

/guess

    input()
    check-word-in-dict()
    check-letter()
    check-word()



/game-end

    success() / failure()
    ensure failed game are put back to current users pool

/dashboard
    params- token 

    user- create game button redirect to /create
    shows game cards
    Think about showing all prev game or loading on scroll

    admin - reports display
    Think about how to display should you include stats??
    + download buttons

/report


## Good details

1. For each use new game is not a random word but an id picked and checked if duplicate

2. Incase multiple errors in an event but user all errors should be displayed at one

3. usernames are case-insensitive

4. admins are created manually, login has a register as admin checkbox to validate 

5. status for game is win/lose/active

6. ensure that users prev game progress is re-stored

7. Think about how user details will be propogated accross pages

8. word assign from 20 words db check if guess word is valid form the other textfile

9. modularise the code