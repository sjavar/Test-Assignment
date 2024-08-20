# Test-Assignment

<b>Task:</b>

Create a command line program to check the search results for the page:
    https://yousician.com/songs
    
    * The program should take a string to search with as an input argument.
    * The program should then use the search with the given string, and get all the search results (a list of songs with song and artist name).
    * It should then print all the found songs in alphabetical order, sorted primarily by the artist name, and then by the song name.
    * If any error is encountered (e.g., the user does not have an internet connection), the program should print an error message instead and exit.


Solution made with Python3 and Selenium. 
Python3 and Chrome browser should be installed for run application

Application can use browser in both normal and headless modes, mode can be choosed after app running

To run the project open project directory in terminal and run

<code> pip install -r requirements.txt </code>

<code> python3 search_yousician.py </code>

<b> Findings during task: </b>

1. Spaces between words turn into dashes
2. For some requests (e.g. i need) paging is displayed, but 2nd page is empty
3. Cyrillic symbols couldn't be used but there's no error in interface - it stucks on search page and only error in devTools is shown
   Uncaught (in promise) Error: The provided `as` value (/search) is incompatible with the `href` value (/[search]/[search]). Read more: https://nextjs.org/docs/messages/incompatible-href-as
    at e.<anonymous> (router.ts:1055:17)
    at f (runtime.js:64:40)
    at Generator.<anonymous> (runtime.js:299:22)
    at Generator.next (runtime.js:124:21)
    at r (asyncToGenerator.js:3:20)
    at c (asyncToGenerator.js:25:9)
