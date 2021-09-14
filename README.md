# Dictme:  _Dictionary Web app_



### The project is a web app that provides definitions of english words, as well as pronounciations, synonyms and other features.

- I made this project in order to expand my knowledge of Python (Flask) and to learn how APIs actually work by using [Free Dictionary API](https://dictionaryapi.dev/).


## Features

- Brief and convenient definitions
- Quote of the Day
- Synonyms and articles about the word
- Audio pronunciations
- Search history

## Technologies used

For my project I've used:

- HTML
- CSS
- JavaScript
- Bootstrap and jQuery
- Python
- Flask
- Jinja
- PostgreSQL

## How does it work?

The homepage is the landing page of the app through which the user can see the app overview and its features, the user can log in or register on the app using a username and password.
After creating an account, the user choose the language[1] and search for the word. Once the "search" button is clicked, the user will be directed to a page that contains:
- The word
- Phonetic + audio pronunciation
- Definition of the word
- Wiki page for the word
- Synonyms of the word

While testing I found out that some words don't have definitions, [apparently because the API used in this project was using Lexico Dictionary](https://github.com/meetDeveloper/freeDictionaryAPI/issues/80)[2], so I added some other resources such as [Oxford Dictionary](https://www.oxfordlearnersdictionaries.com/), [Cambridge Dictionary](https://dictionary.cambridge.org/) and [Urban Dictionary](https://www.urbandictionary.com/) (for slang and new-gen words) on which you can look for the word whenever it doesn't exist on the API.

One of the features of this app is that u can browse your recently searched word list on "History".

Word | Language | Date
------------ | ------------- | ---------------
hello | en | 2021-08-18 13:18:36
world | en | 2021-08-19 09:46:15
... | .. | ...


#### User authentification
Flask routes check if the user is authenticated by using ```@login_required``` and python logic (except for homepage and Terms and Conditions page), and sessions confirm to the system that the user is logged in or registered successfully.

#### Database
All `users` and searched `words` are saved in the database. The user id is a foreign key in the `words` table to refer users to their searched words.

## Ideas for future development

- Add more languages : Arabic, French, Spanish and Japanese.
- Use other dictionary APIs instead of directing people to other websites (or maybe create my own API :D ).
- Provide more definitions and examples since a word can have different meanings according to the context.
- Login with Google, Facebook, Twitter or Github...

## Contributing

Pull requests are welcome!

If you find any bugs or you want more information, feel free to contact me via [email](marwan.zouaid@gmail.com) or [create a new issue](https://github.com/merouanezouaid/dictme/issues/new).

## Notes
[1] At first my app was supporting many languages but the API developer decided to remove non english languages and [2] decided to start using Wiktionary as a source for Dictionary API. [About the issue..](https://github.com/meetDeveloper/freeDictionaryAPI/issues/102)


## Acknowledgement

Special thanks to @FILali1 for his amazing contribution and deployment fixes, I was having lots of problems on Heroku and SQL queries but everything now is fine thanks to your guidance, and your incredible job is very appreciated!! 💪

