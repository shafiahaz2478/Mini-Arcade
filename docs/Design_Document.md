# **Mini Arcade: Program Design & Development**

## **Module Map**

One launcher plus five game modules:

* main.py holds the menu, every input() and print(), and every game loop.  
* sudoku\_logic.py, hangman\_logic.py, blackjack\_logic.py, connect4\_logic.py, and battleship\_logic.py hold pure game logic — no input, no printing, no memory between calls.

*Module names use underscores (hyphens cannot be imported in Python). 42 functions in total: 13 in main.py, 29 across the logic modules.*

## **1\. Terminology & Formulae**

### **1.1 Shared terms — defined once, apply to all five games**

* **The report**: A string a logic function returns for main.py to print. Exact phrasing is locked per game. Reports never contain a prompt.  
* **"in progress"**: The sentinel a state-checking function returns while the session continues. Any other return value is a final line — main.py prints it and the session ends.  
* **quit**: The four-letter word quit, case-insensitive, surrounding whitespace ignored, accepted at every game prompt. It ends the session immediately; the menu then reprints. Quitting reveals nothing, with one exception: Hangman's quit line reveals the word. (The token is the full word rather than *q* so the letter *q* stays a legal guess in Hangman.)  
* **The five verbs**: pick\_\*/new\_\* (logic: builds starting state), render\* (logic: returns a display string), read\_\* (main.py: prompts, parses, validates, re-asks on bad input; returns a clean move or quit), make\_move (logic: consumes a valid move, returns new state — plus a report where the outcome is not visible in the next render), game\_state (logic: "in progress" or a final line).  
* **State ownership**: Every state variable lives inside a run\_\* function in main.py. Logic functions take state in, return new state out, and remember nothing between calls. Randomness appears only in setup and opponent functions.  
* **Session**: One play of one game, from the moment a run\_\* function is called to the moment it returns. Sessions end by returning to the menu, never by exiting the app — the app exits only via menu option 7\.

### **1.2 Sudoku**

* **State** (held by run\_sudoku): board, givens.  
* **The board**: 9×9 grid: a list of 9 rows of 9 values. Values 1–9; 0 means empty. Stored 0-indexed; the player types 1–9 and read\_move converts. (Indexing convention shared with Battleship.)  
* **The generator**: Every session starts from a fresh random puzzle: random\_solution builds a valid completed grid by shuffling BASE\_SOLUTION; new\_puzzle then empties CELLS\_TO\_REMOVE cells chosen at random. Nothing is stored between sessions — consecutive games are different puzzles.  
* **givens**: The set of (row, col) cells that arrived filled. Locked: read\_move rejects any write to them.  
* **Row, column, box**: Row *r* and column *c* are the usual nine cells. The box is the 3×3 block containing the cell: row group 1–3, 4–6, or 7–9 crossed with column group 1–3, 4–6, or 7–9.  
* **A legal placement**: Value *v* into cell *(r, c)* is legal when *v* does not already appear in that row, that column, or that box — the target cell itself is excluded, so a wrong entry can be corrected in place.  
* **The correction rule**: Givens are locked; every other cell is writable — writing into a cell that holds one of your own entries replaces it.  
* **Multiple completions**: Removal is not uniqueness-checked, so a puzzle may admit more than one valid completion. No solution is stored; any legal completion wins.  
* **Formulae**: Solved ⇔ all 81 cells are non-zero. Full means valid: every write passed is\_valid\_placement, so the board never holds a duplicate in any row, column, or box; a full board with no duplicates contains each digit exactly once per row, column, and box — a valid solution by definition.  
* **The display**: Column header 1–9, row labels 1–9, | and dashed lines every three cells. Each cell renders in a 3-character field: given 5, player entry \[5\], empty ..

    1  2  3 | 4  5  6 | 7  8  9  
 1  5  3 \[4\]| .  7  . | .  .  .  
 2  6  .  . | 1  9  5 | .  .  .  
 3  .  9  8 | .  .  . | .  6  .  
   \---------+---------+---------  
 4  8  .  . | .  6  . | .  .  3  
 5  4  .  . | 8  .  3 | .  .  1  
 6  7  .  . | .  2  . | .  .  6  
   \---------+---------+---------  
 7  .  6  . | .  .  . | 2  8  .  
 8  .  .  . | 4  1  9 | .  .  5  
 9  .  .  . | .  8  . | .  7  9

* **The prompt and input rules** (main.py): Prompt: Row, column, value (or 'quit'): — three integers 1–9, whitespace-separated. Errors, exact: Enter three numbers 1-9: row, column, value. / That cell is part of the puzzle — it can't be changed. / \<v\> doesn't fit there — its row, column, or box already has a \<v\>. All re-asked; there is nothing to penalize.  
* **The final lines**: Solved\! Well played. (logic, from game\_state). You quit this puzzle. (main.py).  
* No lives, no opponent, no timer — the session ends by solving or quitting.

### **1.3 Hangman**

* **State** (held by run\_hangman): word, guessed, lives.  
* **The word**: A string of 4–8 lowercase letters a–z, chosen at random by pick\_word from WORDLIST (ten words; any word meeting these rules qualifies, so the list can grow without touching any function). The player never sees it until the session ends — the win, loss, and quit lines all reveal it.  
* **guessed**: The set of single lowercase letters guessed so far. Starts empty, grows only through accepted guesses; repeats are impossible because read\_letter rejects them.  
* **lives**: An integer, starting at 6\. Each miss subtracts 1\. Hits, repeats, and invalid input cost nothing. lives never goes below 0\.  
* **Hit and miss**: A guess is a hit if the letter occurs anywhere in the word (repeated letters count once); otherwise it is a miss.  
* **The display**: Shown before every prompt, two parts: the gallows drawing for the current wrong count, then the masked word. lives is never printed as a number — it is visible only through the gallows.  
* **The gallows**: Seven drawings indexed by wrong \= 6 − lives: 0 \= empty gallows; each miss adds one part in fixed order — head, body, arm, second arm, leg, second leg. Six wrong guesses is the complete figure.  
* **The masked word**: Each letter of the word shown if it is in guessed, otherwise \_, joined by single spaces: word python, guessed {t} → \_ \_ t \_ \_ \_.

  \+---+  
  |   |  
  O   |  
      |  
      |  
\=========  
\_ \_ t \_ \_ \_  
Guess a letter (or 'quit' to quit): 

* **The prompt and input rules** (main.py): The exact prompt is Guess a letter (or 'quit' to quit): — case-insensitive, whitespace stripped. A valid guess is exactly one letter a–z; anything else (multiple letters, digits, empty input, non-English letters) is invalid. Exact error messages: Please enter a single letter (a-z). / You already guessed 'x'. Bad input is re-asked and never penalized.  
* **The report** (returned by make\_move): Hit: Yes\! 'x' is in the word. Miss: Nope, 'x' is not in the word.  
* **The final lines**: Returned by game\_state: You won\! The word was 'xxx'. / You lost\! The word was 'xxx'. The quit line is main.py's own: You quit. The word was 'xxx'.  
* **Win and loss formulae**: Won when every letter of the word is in guessed (equivalently: the masked word contains no \_). Lost when lives \= 0\. Won is checked before lost; both can never be true at once — a winning guess is always a hit, and hits cost no life.

### **1.4 Blackjack**

* **State** (held by run\_blackjack): deck, player, dealer.  
* **The deck**: 52 cards; a card is a (rank, suit) pair. Ranks: A, 2–10, J, Q, K. Suits: S, H, D, C (letters, not symbols — safest across terminals). new\_deck returns it shuffled; one fresh deck per round. Exhaustion is impossible — a hand busts long before 52 cards run out.  
* **A hand**: A list of cards; two each after deal\_initial. The dealer's second card is the hole card.  
* **Card values**: 2–10 at face value; J, Q, K \= 10; A \= 11 while the total stays 21 or under, otherwise 1\. hand\_value returns the best total under this rule. Bust ⇔ value \> 21\.  
* **The actions**: hit (draw one card) or stand (end your turn; the dealer plays). Accepted input, case-insensitive: h or hit, s or stand, quit. Prompt: Hit or stand? (or 'quit'): (main.py). Error: Enter hit, stand, or quit. (main.py).  
* **The dealer**: After a stand, draws until its value is 17 or more, then stops. Stands on all 17s, soft ones included.  
* **The display**: Two lines — Dealer: then You: — cards as rank+suit (10H), running total in parentheses. While the round is in progress the hole card shows as XX and the dealer's displayed total is the up card's value alone; once the round ends, the render reveals the full hand.

Dealer: AS XX (11)  
You:   10H 9S (19)  
Hit or stand? (or 'quit'): 

* **Outcome rules, in priority order**:  
  * Player busts on a hit → lose, immediately; the dealer never plays.  
  * Player stands → dealer plays. Dealer busts → win. Otherwise higher total wins; equal totals → push (tie).  
* **Scope locks** (deliberate simplifications): No betting, no naturals bonus, no double/split/insurance, no auto-stand at 21 — the player always chooses.  
* **The report and status** (both from make\_move): The status is machine-readable ("in progress" / "won" / "lost" / "push"); the report is what gets printed. Exact reports: You draw the \<card\>. / You draw the \<card\> — bust with \<n\>. You lose this round. / Dealer busts with \<n\> — you win\! / Dealer stands on \<n\>, you have \<m\> — you win\! / Dealer stands on \<n\>, you have \<m\> — you lose. / Dealer stands on \<n\>, you have \<m\> — push. No game\_state function exists — a round only ever ends as a consequence of an action, so the verdict rides with make\_move.  
* **The quit line** (main.py): You quit the round.

### **1.5 Connect 4**

* **State** (held by run\_connect4): board, mark.  
* **The board**: 6 rows × 7 columns: a list of 6 rows of 7 values. Empty cells are .; the two players' discs are X and O. X always moves first.  
* **Gravity**: A disc dropped into column *c* falls to the lowest empty cell in that column. A full column is illegal — read\_column rejects it via column\_is\_full.  
* **The win formula**: Four of the same mark in an unbroken straight line — horizontal, vertical, or either diagonal. Draw ⇔ 42 discs with no line.  
* **The display**: A column header 1 2 3 4 5 6 7, then the rows top-to-bottom (discs stack upward from the bottom row). No row labels — players reference columns only.

1 2 3 4 5 6 7  
. . . . . . .  
. . . . . . .  
. . . . X . .  
. . . O X O .  
. . X O X X O  
Player O, choose a column (1-7 or 'quit'): 

* **The prompt and input rules** (main.py): The prompt names the current player — a hotseat game must, or players lose track: Player \<mark\>, choose a column (1-7 or 'quit'): . Errors, exact: Enter a column number 1-7. / Column \<n\> is full — choose another.  
* make\_move returns only the board — the outcome is visible in the render, so there is no report.  
* **The final lines** (logic, from game\_state): Player X wins\! / Player O wins\! / The board is full — a draw. Quit line (main.py): Player \<mark\> quits the game. — whoever was prompted.

### **1.6 Battleship**

* **State** (held by run\_battleship): enemy\_fleet, shots, player\_fleet, computer\_shots.  
* **The grid**: 10×10. Rows and columns both numbered 1–10; typed as row col (e.g. 3 4); stored 0-indexed as in Sudoku.  
* **The fleet**: Both sides field the same five ships: Carrier (5 cells), Battleship (4), Submarine (3), Cruiser (3), Destroyer (2). A ship is its name plus its set of cells; a fleet is a list of five ships. place\_fleet positions them randomly — horizontal or vertical, fully on the grid, never overlapping; touching is allowed. Called twice, once per side.  
* **Shots**: Two sets of cells: shots (yours, at the enemy grid) and computer\_shots (the computer's, at yours).  
* **Hit, miss, sunk**: A shot is a hit if it lands on any ship cell, else a miss. A ship is sunk ⇔ every one of its cells has been hit.  
* **The two boards**: Your waters (render\_player\_board): \# ship, X hit on you, o miss on you, . water. The enemy grid (render\_enemy\_board): . unknown, o your miss, X your hit, \* the cells of a ship you have sunk. Both carry row labels 1–10 and a column header 1–10.

    1 2 3 4 5 6 7 8 9 10  
 1  . . . . . . . . .  .  
 2  . o . . . . . . .  .  
 3  . o . . . . . . .  .  
 4  . . . \* . . . . .  .  
 5  . . . \* . . . . .  .  
 6  . . . X . . . . .  .  
 7  . . . . . . . . .  .  
 8  . . . . . . . . .  .  
 9  . . . . . . . . .  .  
10  . . . . . . . . .  .

* **The computer opponent**: After your shot — if you haven't just won — computer\_fire picks one uniformly random unfired cell on your grid and fires. No hunting, no targeting logic; it cannot fire at the same cell twice.  
* **The prompt and input rules** (main.py): Fire at row, column (or 'quit'): Errors, exact: Enter two numbers 1-10: row and column. / You already fired at \<r\> \<c\>.  
* **The reports** (logic): Yours, from make\_move: Hit\! / Miss. / Hit — you sank the enemy \<name\>\! The computer's, from computer\_fire: The computer fires at \<r\> \<c\> — a hit\! / The computer fires at \<r\> \<c\> — a miss. / The computer fires at \<r\> \<c\> — it sinks your \<name\>\!  
* **Win and loss** (logic, from game\_state, checked after every fire in both directions). All five enemy ships sunk → You win — the enemy fleet is destroyed\! All five of yours sunk → You lose — your fleet is destroyed\!  
* **The quit line** (main.py): You quit the battle.

## **2\. Program Flow**

### **2.1 The launcher (main)**

On startup, main prints the seven-option menu (text exactly as in the PRD) and prompts Enter your choice: . Choices 1–5 start the matching game; 6 starts one of the five chosen uniformly at random; 7 prints Thanks for playing\! Goodbye. and ends the program. Invalid input prints Invalid choice. Please enter a number between 1 and 7\. and the menu reprints. Each game runs inside a run\_\* function; when it returns, the menu reprints and the app waits for the next choice. No game ever exits the app — only option 7 does.

### **2.2 Sudoku (run\_sudoku)**

1. Draw a puzzle — new\_puzzle → board, givens.  
2. Show the board — render\_board.  
3. Read a move — read\_move: parse, shape-check, reject givens and illegal placements, re-asking each time.  
4. If the input is quit: print the quit line and return to the menu.  
5. Apply the move — make\_move writes the value. No report — the next render shows it.  
6. Evaluate — game\_state: no empty cell remains → the solved line; otherwise "in progress".  
7. If solved: show the completed board, print the solved line, return to the menu.  
8. Otherwise repeat from step 2\.

### **2.3 Hangman (run\_hangman)**

1. Pick the secret word — pick\_word.  
2. Set guessed empty and lives \= 6\.  
3. Show the display: gallows for the current wrong count, then the masked word.  
4. Read a guess — read\_letter; invalid or repeated input is re-asked with an error message and costs nothing.  
5. If the guess is quit: print the quit line and return to the menu.  
6. Apply the guess — make\_move: the letter joins guessed; on a hit lives is unchanged, on a miss it drops by one. The report states which happened.  
7. Print the report.  
8. Evaluate — game\_state: every letter revealed → the win line; lives \= 0 → the loss line; otherwise "in progress".  
9. If not "in progress": print the final line and return to the menu.  
10. Otherwise repeat from step 3, showing the updated gallows and masked word.

### **2.4 Blackjack (run\_blackjack)**

1. Build a fresh shuffled deck — new\_deck.  
2. Deal two cards each — deal\_initial → deck, player, dealer.  
3. Show the hands — render\_hands, hole card hidden.  
4. Read an action — read\_action; anything unrecognized is re-asked.  
5. If quit: print the quit line and return to the menu.  
6. Apply the action — make\_move → (deck, player, dealer, report, status): hit draws one card (bust ends the round at once); stand runs the dealer and settles the comparison.  
7. Print the report.  
8. Show the hands again — hole card revealed if the round has ended.  
9. If status is not "in progress": return to the menu.  
10. Otherwise repeat from step 4\.

### **2.5 Connect 4 (run\_connect4)**

1. Create the empty board — new\_board.  
2. Set mark \= "X".  
3. Show the board — render.  
4. Read a column — read\_column(board, mark): 1–7 and not a full column, re-asked otherwise.  
5. If quit: print the quit line and return to the menu.  
6. Drop the disc — make\_move applies gravity.  
7. Evaluate — game\_state: a line for either mark → that player's win line; board full → the draw line; otherwise "in progress".  
8. If ended: show the final board, print the final line, return to the menu.  
9. Otherwise pass the turn to the other mark and repeat from step 3\.

### **2.6 Battleship (run\_battleship)**

1. Place both fleets — place\_fleet twice → enemy\_fleet, player\_fleet; both shot sets start empty.  
2. Show both boards — your waters first, then the enemy grid.  
3. Read coordinates — read\_coords(shots): two numbers 1–10, cell not already fired.  
4. If quit: print the quit line and return to the menu.  
5. Fire — make\_move → (shots, report); print it.  
6. Evaluate — game\_state: enemy fleet destroyed → win line, return.  
7. Computer fires — computer\_fire → (computer\_shots, report); print it.  
8. Evaluate — game\_state: your fleet destroyed → loss line, return.  
9. Otherwise repeat from step 2, both boards re-rendered with the new marks.

## **3\. Function Signatures**

42 functions: 13 in main.py, 29 across the logic modules.

### **3.1 main.py**

| Typed header line | What it's for |
| :---- | :---- |
| def main() \-\> None: | The menu loop: print menu, read choice, dispatch, reprint on invalid, goodbye on 7\. |
| def run\_random() \-\> None: | Launches one of the five run functions, chosen uniformly at random. |
| def run\_sudoku() \-\> None: | Sudoku loop \+ state (board, givens). |
| def run\_hangman() \-\> None: | Hangman loop \+ state (word, guessed, lives). |
| def run\_blackjack() \-\> None: | Blackjack loop \+ state (deck, player, dealer). |
| def run\_connect4() \-\> None: | Connect 4 loop \+ state (board, whose turn). |
| def run\_battleship() \-\> None: | Battleship loop \+ state (enemy\_fleet, shots, player\_fleet, computer\_shots). |
| def read\_choice() \-\> str: | Menu input: prints the prompt, reads one line, strips whitespace, returns it unchanged — validation lives in main() so the menu reprints on invalid input. |
| def read\_letter(guessed: set) \-\> str: | One new a–z letter, or "quit". |
| def read\_move(board: list, givens: set) \-\> tuple: | Sudoku input: parse row col value, shape-check, reject givens, legality via sudoku\_logic.is\_valid\_placement. Returns (row, col, value) or "quit". |
| def read\_action() \-\> str: | Blackjack input: hit / stand / quit. |
| def read\_column(board: list, mark: str) \-\> int: | Connect 4 input: 1–7 and column not full (fullness via connect4\_logic.column\_is\_full). |
| def read\_coords(shots: set) \-\> tuple: | Battleship input: parse row col, cell not already fired. Returns (row, col) or "quit". |

### **3.2 sudoku\_logic.py**

| Typed header line | What it's for |
| :---- | :---- |
| def random\_solution() \-\> list: | Builds a fresh valid completed grid by shuffling BASE\_SOLUTION. |
| def new\_puzzle() \-\> tuple: | Punches holes in a random solution: returns (board, givens). |
| def render\_board(board: list, givens: set) \-\> str: | The 9×9 grid, givens marked differently from player entries. |
| def is\_valid\_placement(board: list, row: int, col: int, value: int) \-\> bool: | Row/column/box scan — target cell skipped so entries can be corrected. Called by main's read\_move. |
| def make\_move(board: list, row: int, col: int, value: int) \-\> list: | Writes the value, returns the board. |
| def game\_state(board: list) \-\> str: | "in progress" or the solved line — solved when no cell is 0\. |

### **3.3 hangman\_logic.py**

| Typed header line | What it's for |
| :---- | :---- |
| def pick\_word() \-\> str: | Random secret word from WORDLIST. |
| def draw\_gallows(lives: int) \-\> str: | ASCII drawing for the current lives. |
| def mask\_word(word: str, guessed: set) \-\> str: | The h \_ n \_ m \_ n line. |
| def make\_move(word: str, guessed: set, lives: int, guess: str) \-\> tuple: | All rules: returns (guessed, lives, report). |
| def game\_state(word: str, guessed: set, lives: int) \-\> str: | "in progress" or the won/lost line. |

### **3.4 blackjack\_logic.py**

| Typed header line | What it's for |
| :---- | :---- |
| def new\_deck() \-\> list: | Fresh shuffled 52-card deck. |
| def deal\_initial(deck: list) \-\> tuple: | (deck, player, dealer) with two cards each. |
| def hand\_value(cards: list) \-\> int: | Best total with aces as 1 or 11\. |
| def render\_hands(player: list, dealer: list, hide\_dealer\_card: bool) \-\> str: | Both hands with values; hole card hidden while the player is still playing. |
| def dealer\_turn(deck: list, dealer: list) \-\> tuple: | The computer opponent: draws to 17\. Returns (deck, dealer, summary). |
| def make\_move(deck: list, player: list, dealer: list, action: str) \-\> tuple: | Hit draws and checks bust; stand settles the round via dealer\_turn. Returns (deck, player, dealer, report, status). |

### **3.5 connect4\_logic.py**

| Typed header line | What it's for |
| :---- | :---- |
| def new\_board() \-\> list: | Empty 6×7 board. |
| def render(board: list) \-\> str: | The grid with column numbers 1–7. |
| def column\_is\_full(board: list, col: int) \-\> bool: | Called by main's read\_column. |
| def make\_move(board: list, col: int, mark: str) \-\> list: | Drops the disc with gravity, returns the board. |
| def game\_state(board: list) \-\> str: | Checks both marks: "in progress" / X wins / O wins / draw. |

### **3.6 battleship\_logic.py**

| Typed header line | What it's for |
| :---- | :---- |
| def place\_fleet() \-\> list: | Random legal placement of the 5 ships (name \+ set of cells each). Called twice — once per side. |
| def render\_enemy\_board(fleet: list, shots: set) \-\> str: | Target grid: your hits and misses; ships hidden. |
| def render\_player\_board(fleet: list, computer\_shots: set) \-\> str: | Your waters: ships visible, computer's hits and misses. |
| def make\_move(fleet: list, shots: set, row: int, col: int) \-\> tuple: | You fire: (shots, report) — hit / miss / sank a named ship. |
| def computer\_fire(player\_fleet: list, computer\_shots: set) \-\> tuple: | The computer opponent: picks an unfired cell, fires. Returns (computer\_shots, report). |
| def is\_sunk(cells: set, shots: set) \-\> bool: | Shared helper for sank messages and win detection. |
| def game\_state(enemy\_fleet: list, shots: set, player\_fleet: list, computer\_shots: set) \-\> str: | "in progress" / you win / you lose — checked after each fire, both directions. |

### **3.7 Constants by module**

* main.py: MENU — the seven-option menu, text exactly as in the PRD.  
* sudoku\_logic.py: BASE\_SOLUTION (below), CELLS\_TO\_REMOVE \= 48\.  
* hangman\_logic.py: WORDLIST (ten words, 4–8 lowercase letters), GALLOWS (seven drawings).  
* blackjack\_logic.py: SUITS, RANKS.  
* connect4\_logic.py: none — the 6×7 size is part of new\_board.  
* battleship\_logic.py: SHIPS (Carrier 5, Battleship 4, Submarine 3, Cruiser 3, Destroyer 2), GRID\_SIZE \= 10\.

**BASE\_SOLUTION** — the one hand-made constant in the project:

5 3 4 | 6 7 8 | 9 1 2  
6 7 2 | 1 9 5 | 3 4 8  
1 9 8 | 3 4 2 | 5 6 7  
\------+-------+------  
8 5 9 | 7 6 1 | 4 2 3  
4 2 6 | 8 5 3 | 7 9 1  
7 1 3 | 9 2 4 | 8 5 6  
\------+-------+------  
9 6 1 | 5 3 7 | 2 8 4  
2 8 7 | 4 1 9 | 6 3 5  
3 4 5 | 2 8 6 | 1 7 9

## **4\. Function-Level Algorithm**

### **4.1 Launcher — main.py**

def main() \-\> None:

* Build the dispatch table: "1" → run\_sudoku, "2" → run\_hangman, "3" → run\_blackjack, "4" → run\_connect4, "5" → run\_battleship, "6" → run\_random.  
* Repeat forever:  
  * Print MENU.  
  * Set choice to read\_choice().  
  * If choice is "7": print Thanks for playing\! Goodbye. and return.  
  * If choice is a key of the table: call its function — when it returns, the loop repeats and the menu reprints.  
  * Otherwise print Invalid choice. Please enter a number between 1 and 7\. and repeat.

def run\_random() \-\> None:

* Put the five run functions into a list.  
* Choose one uniformly at random.  
* Call it.

def read\_choice() \-\> str:

* Print Enter your choice: and read one line.  
* Strip the surrounding whitespace.  
* Return the result unchanged — validation is main()'s job, so the menu reprints on bad input.

### **4.2 Sudoku**

**In main.py:**

def read\_move(board: list, givens: set) \-\> tuple:

* Repeat:  
  * Print Row, column, value (or 'quit'): and read a line; strip it.  
  * If it is quit, return it.  
  * Split into parts; if there are not exactly three, or any is not a whole number from 1 to 9: print Enter three numbers 1-9: row, column, value. and repeat.  
  * Convert row and column to 0-based; keep the value as is.  
  * If (row, col) is in givens: print That cell is part of the puzzle — it can't be changed. and repeat.  
  * If is\_valid\_placement(board, row, col, value) is False: print \<v\> doesn't fit there — its row, column, or box already has a \<v\>. and repeat.  
  * Return (row, col, value).

def run\_sudoku() \-\> None:

* Take board, givens from new\_puzzle().  
* Repeat:  
  * Print render\_board(board, givens).  
  * Set move to read\_move(board, givens).  
  * If it is quit: print You quit this puzzle. and return.  
  * Set board to make\_move(board, row, col, value).  
  * Set status to game\_state(board).  
  * If status is not "in progress": print render\_board(board, givens), print the status, and return.

**In sudoku\_logic.py:**

def random\_solution() \-\> list:

* Make a copy of BASE\_SOLUTION.  
* Relabel the digits: take a random rearrangement of 1–9 and rewrite every cell through it.  
* For each band (rows 1–3, 4–6, 7–9): shuffle its three rows.  
* Shuffle the three bands themselves.  
* For each stack (columns 1–3, 4–6, 7–9): shuffle its three columns.  
* Shuffle the three stacks themselves.  
* Return the grid.  
  *(Each operation maps rows to rows, columns to columns, and boxes to boxes, and relabels digits one-to-one — all three Sudoku constraints survive every shuffle. A transpose is an optional sixth shuffle for extra variety.)*

def new\_puzzle() \-\> tuple:

* Set grid to random\_solution().  
* Choose CELLS\_TO\_REMOVE different cells at random and set them to 0\.  
* Set givens to every (row, col) whose value is not 0\.  
* Return (grid, givens) — the punched grid is the board. (random\_solution builds a fresh grid on every call, so no copy concerns arise.)

def render\_board(board: list, givens: set) \-\> str:

* Build the header: column numbers 1–9, with a | after columns 3 and 6\.  
* For each row 1–9:  
  * For each column 1–9: value 0 → .; a given cell → the value in a 3-character field; a player entry → \[value\].  
  * Join the row's cells with spaces, place | after columns 3 and 6, and prefix the row label.  
* After rows 3 and 6, add a dashed separator line.  
* Join everything and return.

def is\_valid\_placement(board: list, row: int, col: int, value: int) \-\> bool:

* Row scan: if the value appears anywhere in row r except at (r, c) itself, return False.  
* Column scan: likewise for column c.  
* Box scan: the box's first row is r − (r mod 3\) and its first column is c − (c mod 3); if the value appears in those nine cells except at (r, c) itself, return False.  
* Return True.

def make\_move(board: list, row: int, col: int, value: int) \-\> list:

* Write the value into cell (row, col).  
* Return the board.

def game\_state(board: list) \-\> str:

* If no cell is 0: return Solved\! Well played.  
* Return "in progress".

### **4.3 Hangman**

**In main.py:**

def read\_letter(guessed: set) \-\> str:

* Repeat:  
  * Print Guess a letter (or 'quit' to quit): and read a line.  
  * Strip the whitespace and lowercase the result.  
  * If it is quit, return it.  
  * If it is exactly one character between 'a' and 'z', and not already in guessed, return it.  
  * If it is already in guessed: print You already guessed 'x'.  
  * Otherwise: print Please enter a single letter (a-z).

def run\_hangman() \-\> None:

* Set word to pick\_word(), guessed to an empty set, and lives to 6\.  
* Repeat:  
  * Print draw\_gallows(lives), then mask\_word(word, guessed).  
  * Set guess to read\_letter(guessed).  
  * If guess is quit: print You quit. The word was 'xxx'. and return.  
  * Take the new guessed, lives, and report from make\_move(word, guessed, lives, guess); print the report.  
  * Set status to game\_state(word, guessed, lives).  
  * If status is not "in progress": print it and return.

**In hangman\_logic.py:**

def pick\_word() \-\> str:

* Return one word chosen at random from WORDLIST.

def draw\_gallows(lives: int) \-\> str:

* Set wrong to 6 − lives.  
* Return GALLOWS\[wrong\].

def mask\_word(word: str, guessed: set) \-\> str:

* For each letter of word: keep the letter if it is in guessed, otherwise use \_.  
* Join the results with single spaces and return.

def make\_move(word: str, guessed: set, lives: int, guess: str) \-\> tuple:

* Add the guess to guessed.  
* If the guess occurs in word: return (guessed, lives, "Yes\! 'x' is in the word.").  
* Otherwise: return (guessed, lives − 1, "Nope, 'x' is not in the word.").

def game\_state(word: str, guessed: set, lives: int) \-\> str:

* If every letter of word is in guessed: return You won\! The word was 'xxx'.  
* If lives is 0: return You lost\! The word was 'xxx'.  
* Return "in progress".

### **4.4 Blackjack**

**In main.py:**

def read\_action() \-\> str:

* Repeat:  
  * Print Hit or stand? (or 'quit'): and read a line; strip and lowercase it.  
  * If it is h or hit: return "hit".  
  * If it is s or stand: return "stand".  
  * If it is quit: return "quit".  
  * Otherwise: print Enter hit, stand, or quit.

def run\_blackjack() \-\> None:

* Set deck to new\_deck().  
* Take deck, player, dealer from deal\_initial(deck).  
* Print render\_hands(player, dealer, True).  
* Repeat:  
  * Set action to read\_action().  
  * If action is quit: print You quit the round. and return.  
  * Take deck, player, dealer, report, status from make\_move(deck, player, dealer, action).  
  * Print the report.  
  * Print render\_hands(player, dealer, hide\_dealer\_card) — the hole card is hidden exactly while status is "in progress".  
  * If status is not "in progress": return.

**In blackjack\_logic.py:**

def new\_deck() \-\> list:

* For each of the four suits, for each of the thirteen ranks, form one card (rank, suit).  
* Shuffle the 52 cards.  
* Return the deck.

def deal\_initial(deck: list) \-\> tuple:

* Take two cards from the top of the deck into the player's hand.  
* Take two more into the dealer's hand — the dealer's second card is the hole card.  
* Return (deck, player, dealer).

def hand\_value(cards: list) \-\> int:

* Set total to 0 and aces to 0\.  
* For each card: J, Q, K add 10; A adds 11 and raises aces by one; any other rank adds its number.  
* While total is over 21 and aces is above 0: subtract 10 from total and one from aces (recount an ace as 1).  
* Return total.

def render\_hands(player: list, dealer: list, hide\_dealer\_card: bool) \-\> str:

* Dealer line: Dealer: followed by the dealer's cards as rank+suit (e.g. 10H), space-separated.  
* If hide\_dealer\_card: show only the first card, then XX; the number in parentheses is the value of the first card alone.  
* Otherwise: show all the dealer's cards with hand\_value(dealer) in parentheses.  
* Player line: You: followed by all the player's cards with hand\_value(player) in parentheses; the two labels align.  
* Return the two lines.

def dealer\_turn(deck: list, dealer: list) \-\> tuple:

* While hand\_value(dealer) is under 17: take one card from the deck into the dealer's hand.  
* Build the summary — a fragment with no final period: Dealer stands on \<n\> if the final total is 21 or less, otherwise Dealer busts with \<n\>.  
* Return (deck, dealer, summary).

def make\_move(deck: list, player: list, dealer: list, action: str) \-\> tuple:

* If action is "hit":  
  * Take one card from the deck into the player's hand.  
  * If hand\_value(player) is over 21: return (deck, player, dealer, "You draw the \<card\> — bust with \<n\>. You lose this round.", "lost").  
  * Otherwise return (deck, player, dealer, "You draw the \<card\>.", "in progress").  
* If action is "stand":  
  * Finish the dealer's hand with dealer\_turn; take its summary.  
  * If the dealer's total is over 21: report \= summary \+ " — you win\!"; status "won".  
  * If the player's total is higher: report \= summary \+ ", you have \<m\> — you win\!"; status "won".  
  * If lower: report \= summary \+ ", you have \<m\> — you lose."; status "lost".  
  * If equal: report \= summary \+ ", you have \<m\> — push."; status "push".  
* Return (deck, player, dealer, report, status).  
  *(Every assembled sentence is exactly one of the reports locked in 1.4 — the stand branch is summary plus tail.)*

### **4.5 Connect 4**

**In main.py:**

def read\_column(board: list, mark: str) \-\> int:

* Repeat:  
  * Print Player \<mark\>, choose a column (1-7 or 'quit'): and read a line; strip it.  
  * If it is quit, return it.  
  * If it is not a whole number from 1 to 7: print Enter a column number 1-7. and repeat.  
  * Convert to the 0-based column index.  
  * If column\_is\_full(board, col) is True: print Column \<n\> is full — choose another. (1-based) and repeat.  
  * Return the column index.

def run\_connect4() \-\> None:

* Set board to new\_board() and mark to "X".  
* Repeat:  
  * Print render(board).  
  * Set col to read\_column(board, mark).  
  * If col is quit: print Player \<mark\> quits the game. and return.  
  * Set board to make\_move(board, col, mark).  
  * Set status to game\_state(board).  
  * If status is not "in progress": print render(board), print the status, and return.  
  * Otherwise set mark to the other mark.

**In connect4\_logic.py:**

def new\_board() \-\> list:

* Return six rows of seven cells, every cell ..

def render(board: list) \-\> str:

* Build the header line 1 2 3 4 5 6 7\.  
* The bottom row is stored first, so walk the stored rows from last to first, joining each row's seven cells with spaces into one line.  
* Join the lines and return.

def column\_is\_full(board: list, col: int) \-\> bool:

* If the topmost cell of the column — the cell in the last stored row — is not .: return True.  
* Otherwise return False.

def make\_move(board: list, col: int, mark: str) \-\> list:

* Walk the column from the bottom row upward.  
* Write the mark into the first . cell (read\_column guarantees one exists).  
* Return the board.

def game\_state(board: list) \-\> str:

* For mark "X", then mark "O":  
  * For every cell holding that mark:  
    * If the next three cells to the right are all on the board and hold the mark: that player has a line.  
    * Same for the three cells below.  
    * Same for the three cells diagonally down-right.  
    * Same for the three cells diagonally down-left.  
    * On the first line found, return Player X wins\! or Player O wins\!.  
* If neither mark has a line and no . remains anywhere: return The board is full — a draw.  
* Return "in progress".  
  *(Why only four directions: every possible four-in-a-row begins at its topmost or leftmost cell and runs right, down, down-right, or down-left — checking those four from every cell covers every line exactly. Cells off the edge count as not matching.)*

### **4.6 Battleship**

**In main.py:**

def read\_coords(shots: set) \-\> tuple:

* Repeat:  
  * Print Fire at row, column (or 'quit'): and read a line; strip it.  
  * If it is quit, return it.  
  * Split into parts; if there are not exactly two, or either is not a whole number from 1 to 10: print Enter two numbers 1-10: row and column. and repeat.  
  * Convert to the 0-based (row, col).  
  * If (row, col) is already in shots: print You already fired at \<r\> \<c\>. (1-based) and repeat.  
  * Return (row, col).

def run\_battleship() \-\> None:

* Set player\_fleet and enemy\_fleet each to place\_fleet(); shots and computer\_shots to empty sets.  
* Repeat:  
  * Print render\_player\_board(player\_fleet, computer\_shots), then render\_enemy\_board(enemy\_fleet, shots).  
  * Set coords to read\_coords(shots).  
  * If it is quit: print You quit the battle. and return.  
  * Take shots, report from make\_move(enemy\_fleet, shots, row, col); print the report.  
  * Set status to game\_state(enemy\_fleet, shots, player\_fleet, computer\_shots); if not "in progress": print it and return.  
  * Take computer\_shots, report from computer\_fire(player\_fleet, computer\_shots); print the report.  
  * Set status from game\_state again; if not "in progress": print it and return.

**In battleship\_logic.py:**

def place\_fleet() \-\> list:

* Set placed\_cells to an empty set and fleet to an empty list.  
* For each (name, length) in SHIPS:  
  * Repeat: choose horizontal or vertical at random, and a random starting cell such that the whole ship fits on the 10×10 grid; compute the ship's cells.  
  * If any of those cells is already in placed\_cells: retry the choice. (Safe — 17 ship cells on a 100-cell grid always leave room.)  
  * Otherwise add the ship — name plus cells — to the fleet, and its cells to placed\_cells.  
* Return the fleet of five ships.

def is\_sunk(cells: set, shots: set) \-\> bool:

* If any cell of the ship is not in shots: return False.  
* Return True.

def make\_move(fleet: list, shots: set, row: int, col: int) \-\> tuple:

* Add (row, col) to shots.  
* If (row, col) is not a cell of any ship in the fleet: return (shots, "Miss.").  
* Otherwise let ship be the ship owning that cell.  
* If is\_sunk on that ship's cells: return (shots, "Hit — you sank the enemy \<name\>\!").  
* Otherwise: return (shots, "Hit\!").

def computer\_fire(player\_fleet: list, computer\_shots: set) \-\> tuple:

* Choose a cell at random among the grid cells not in computer\_shots.  
* Add it to computer\_shots.  
* If it is not on any ship: return (computer\_shots, "The computer fires at \<r\> \<c\> — a miss.") — coordinates printed 1-based.  
* If it is on a ship and that ship is now sunk: return (…, "The computer fires at \<r\> \<c\> — it sinks your \<name\>\!").  
* Otherwise: return (…, "The computer fires at \<r\> \<c\> — a hit\!").

def render\_player\_board(fleet: list, computer\_shots: set) \-\> str:

* Build the column header 1 to 10\.  
* For each row 1–10, each column 1–10:  
  * If the cell is in computer\_shots and on a ship: X.  
  * If it is in computer\_shots and not on a ship: o.  
  * If it is on a ship and not yet shot: \#.  
  * Otherwise: ..  
  * Prefix each row with its row number, join, and return. *(Hit overrides the ship symbol — check order matters.)*

def render\_enemy\_board(fleet: list, shots: set) \-\> str:

* Build the column header 1 to 10\.  
* For each cell:  
  * If it is in shots and on a ship: \* if that ship is sunk, otherwise X.  
  * If it is in shots and not on a ship: o.  
  * Otherwise: . (unknown waters).  
  * Prefix row numbers, join, and return.

def game\_state(enemy\_fleet: list, shots: set, player\_fleet: list, computer\_shots: set) \-\> str:

* If every ship in enemy\_fleet is sunk: return You win — the enemy fleet is destroyed\!  
* If every ship in player\_fleet is sunk: return You lose — your fleet is destroyed\!  
* Return "in progress".