# **Mini Arcade** 

Product Requirements Document | Program Design & Development 

## **Problem Statement & Description** 

Users want a single terminal application that gives access to multiple classic games without having to run separate programs for each one. The system should present a single menu on startup, let the user choose a game to play, run that game to completion, and return to the menu afterward — repeating until the user chooses to exit. This command-line app, Mini Arcade, provides one launcher that gives access to five games (Sudoku, Hangman, Blackjack, Connect 4, Battleship), a random-pick option, and a clean exit. 

## **Interface** 

To run the app: `python main.py` 

#### **Inputs:** 

- Menu choice: a number typed by the user, 1 through 7 

#### **Outputs:** 

- The main menu, printed on startup and after every game session ends 

```
||           *Mini Arcade*           ||

1. Sudoku
2. Hangman
3. Blackjack
4. Connect 4
5. Battleship
6. Give me something
7. Exit
```

- A prompt line: `Enter your choice:` 

- On invalid input: `Invalid choice. Please enter a number between 1 and 7.` 

- On exit: `Thanks for playing! Goodbye.` 

## **Functional Requirements** 

### **FR 1: Read the user's menu choice and launch the corresponding game.** 

Selecting 1–5 starts that specific game. Once the game session ends, the main menu is shown again. 

```
Enter your choice: 2
[Hangman starts]
...
[Hangman ends]
||           *Mini Arcade*           ||

1. Sudoku
2. Hangman
3. Blackjack
4. Connect 4
5. Battleship
6. Give me something
7. Exit
Enter your choice:
```

### **FR 2: Selecting “Give me something” launches one game chosen at random.** 

One of the 5 games is selected uniformly at random and started exactly as if the user had chosen it directly. Once it ends, the main menu returns. 

```
Enter your choice: 6
[A randomly chosen game starts, e.g. Connect 4]
```

### **FR 3: Selecting “Exit” closes the application.** 

A goodbye message is printed and the program terminates — no menu is shown afterward. 

```
Enter your choice: 7
Thanks for playing! Goodbye.
```

## **Edge Cases** 

|**#**|**Scenario**|**Expected Behavior**|
|---|---|---|
|E1|Non-numeric input (e.g. “abc”)|Error message shown, menu reprinted|
|E2|Out-of-range number (e.g. 0, 8, -1)|Error message shown, menu reprinted|
|E3|Empty input (just pressing Enter)|Treated as invalid, error message<br>shown, menu reprinted|
|E4|Decimal input (e.g. 2.5)|Treated as invalid, error message<br>shown, menu reprinted|
|E5|Leading/trailing whitespace in input (e.g. “ 3 ”)|Still correctly interpreted as a valid<br>choice|
|E6|User quits mid-game (where a game supports a<br>quit option)|Session ends gracefully, main menu<br>returns|
|E7|“Give me something” selected repeatedly in a<br>row|Each selection is independent; no<br>requirement to avoid repeats|



## **Test Cases** 

|**Traces To**|**Input**|**Expected Output**|
|---|---|---|
|FR 1|1|Sudoku starts|
|FR 1|2|Hangman starts|
|FR 1|3|Blackjack starts|
|FR 1|4|Connect 4 starts|
|FR 1|5|Battleship starts|
|FR 1|Complete a game, e.g. win at<br>Hangman|Main menu reappears immediately after|
|FR 2|6 (run multiple times)|Different games start across runs, all 5<br>possible outcomes observed|
|FR 3|7|Goodbye message shown, application<br>closes|
|FR 1, FR 3|1 then 7 in sequence|Sudoku session completes, then 7 closes<br>the application|



