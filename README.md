# kslgfp-py
## kaiwaves silly language grind flashcard project
hi i want to learn latin but in principle this can be used for any language. i will also use to practice my french, i think. 

its literally basic flashcards which run in a basic cli. there is no sophistication to this whatsoever

may add more features later but nothing specific is planned...

updates below mostly so i can keep track of what im doing:

- **patch 0.3**
- - added sentence mode, a way to practice translating full sentences, with hints available (shuffled answers). eg. ("i think therefore i am" with hints adds a line `Hint: sum ergo cogito`)
- - done in program, no need to put a dedicated hint inside ur own .csv file
- - added (optional) re-attempts for missed cards (until u get 100%), so u can practice ur weaknesses a bit better


- **patch 0.2**
- - colors !! green for correct answers, red for incorrect. final % is colored red for <50%, yellow for 50%-85% and green for >85%
- - databases moved to `databases/`, and loading is now easier, only type the name of file. (`databases/` prefix and `.csv` extension not mandatory to enter anymore)
- - refactored basically everything out of main function to help w future expansion development and stuff


- **patch 0.1**
- - added inline hint support, supposed to be for conjugation endings but can be for anything (eg. "amare" asks "Your answer: am", and u only need to put the ending)
- - add some `verb root-` before actual prompt (dash is important!!) 
- - see notation example in [default.csv](databases/default.csv) - (eg: "`am-amare 1st person singular present tense"`)