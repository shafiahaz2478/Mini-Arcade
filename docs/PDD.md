# **Mini Arcade: Program Design & Development** 

## **Module Map** 

One launcher plus five game modules: 

- main.py holds the menu, every input() and print(), and every game loop. 

- sudoku_logic.py, hangman_logic.py, blackjack_logic.py, connect4_logic.py, and battleship_logic.py hold pure game logic — no input, no printing, no memory between calls. 

_Module names use underscores (hyphens cannot be imported in Python). 42 top-level functions in total: 13 in main.py, 29 across the logic modules (random_solution also contains one nested helper, shuffle_rows, which is not counted)._ 

## **1. Terminology & Formulae** 

### **1.1 Shared terms — defined once, apply to all five games** 

- **The report** : A string a logic function returns for main.py to print. Exact phrasing is locked per game. Reports never contain a prompt. 

- **"in progress"** : The sentinel a state-checking function returns while the session continues. Any other return value is a final line — main.py prints it and the session ends. 

- **quit** : The four-letter word quit, case-insensitive, surrounding whitespace ignored, accepted at every game prompt. It ends the session immediately; the menu then reprints. Quitting reveals nothing, with one exception: Hangman's quit line reveals the word. (The token is the full word rather than _q_ so the letter _q_ stays a legal guess in Hangman.) 

- **The five verbs** : pick_*/new_* (logic: builds starting state), render* (logic: returns a display string), read_* (main.py: prompts, parses, validates, re-asks on bad input; returns a clean move or quit), make_move (logic: consumes a valid move, returns new state — plus a report where the outcome is not visible in the next render), game_state (logic: "in progress" or a final line). 

- **State ownership** : Every state variable lives inside a run_* function in main.py. Logic functions take state in, return new state out, and remember nothing between calls. Randomness appears only in setup and opponent functions. 

- **Session** : One play of one game, from the moment a run_* function is called to the moment it returns. Sessions end by returning to the menu, never by exiting the app — the app exits only via menu option 7. 

### **1.2 Sudoku** 

- **State** (held by run_sudoku): board, givens. 

- **The board** : 9×9 grid: a list of 9 rows of 9 values. Values 1–9; 0 means empty. Stored 

   - 0-indexed; the player types 1–9 and read_move converts. (Indexing convention shared 

with Battleship.) 

- **The generator** : Every session starts from a fresh random puzzle: random_solution builds a valid completed grid by shuffling BASE_SOLUTION; new_puzzle then empties CELLS_TO_REMOVE cells chosen at random. Nothing is stored between sessions — consecutive games are different puzzles. 

- **givens** : The set of (row, col) cells that arrived filled. Locked: read_move rejects any write to them. 

- **Row, column, box** : Row _r_ and column _c_ are the usual nine cells. The box is the 3×3 block containing the cell: row group 1–3, 4–6, or 7–9 crossed with column group 1–3, 4–6, or 7–9. 

- **A legal placement** : Value _v_ into cell _(r, c)_ is legal when _v_ does not already appear in that row, that column, or that box — the target cell itself is excluded, so a wrong entry can be corrected in place. 

- **The correction rule** : Givens are locked; every other cell is writable — writing into a cell that holds one of your own entries replaces it. Entering 0 as the value erases one of your own entries (the cell becomes empty again); erasing needs no legality check, and a given can never be erased. 

- **Multiple completions** : Removal is not uniqueness-checked, so a puzzle may admit more than one valid completion. No solution is stored; any legal completion wins. 

- **Formulae** : Solved ⇔ all 81 cells are non-zero. Full means valid: every non-zero write passed is_valid_placement (an erase writes 0 and cannot create a duplicate), so the board never holds a duplicate in any row, column, or box; a full board with no duplicates contains each digit exactly once per row, column, and box — a valid solution by definition. 

- **The display** : Column header 1–9, row labels 1–9, | and dashed lines every three cells. Each cell renders in a 3-character field: given 5, player entry [5], empty .. 

1  2  3 | 4  5  6 | 7  8  9 1  5  3 [4]| .  7  . | .  .  . 2  6  .  . | 1  9  5 | .  .  . 3  .  9  8 | .  .  . | .  6  . 

---------+---------+--------- 

4  8  .  . | .  6  . | .  .  3 5  4  .  . | 8  .  3 | .  .  1 6  7  .  . | .  2  . | .  .  6 

---------+---------+--------- 

7  .  6  . | .  .  . | 2  8  . 8  .  .  . | 4  1  9 | .  .  5 9  .  .  . | .  8  . | .  7  9 

- **The prompt and input rules** (main.py): Prompt: Row, column, value (0 erases, or 'quit'): — three integers, whitespace-separated: row 1–9, column 1–9, value 0–9 (0 erases). Errors, exact: Enter three numbers: row 1-9, column 1-9, value 0-9. / That cell is part of the puzzle — it can't be changed. / <v> doesn't fit there — its row, column, or box already has a <v>. All re-asked; there is nothing to penalize. 

- ● **The final lines** : Solved! Well played. (logic, from game_state). You quit this puzzle. 

(main.py). 

- No lives, no opponent, no timer — the session ends by solving or quitting. 

### **1.3 Hangman** 

- **State** (held by run_hangman): word, guessed, lives. 

- **The word** : A string of 4–8 lowercase letters a–z, chosen at random by pick_word from WORDLIST (ten words; any word meeting these rules qualifies, so the list can grow without touching any function). The player never sees it until the session ends — the win, loss, and quit lines all reveal it. 

- **guessed** : The set of single lowercase letters guessed so far. Starts empty, grows only through accepted guesses; repeats are impossible because read_letter rejects them. 

- **lives** : An integer, starting at 6. Each miss subtracts 1. Hits, repeats, and invalid input cost nothing. lives never goes below 0. 

- **Hit and miss** : A guess is a hit if the letter occurs anywhere in the word (repeated letters count once); otherwise it is a miss. 

- **The display** : Shown before every prompt, two parts: the gallows drawing for the current wrong count, then the masked word. lives is never printed as a number — it is visible only through the gallows. 

- **The gallows** : Seven drawings indexed by wrong = 6 − lives: 0 = empty gallows; each miss adds one part in fixed order — head, body, arm, second arm, leg, second leg. Six wrong guesses is the complete figure. 

- **The masked word** : Each letter of the word shown if it is in guessed, otherwise _, joined by single spaces: word python, guessed {t} → _ _ t _ _ _. 

+---+ 

|   | O   | | | ========= _ _ t _ _ _ Guess a letter (or 'quit' to quit): 

- **The prompt and input rules** (main.py): The exact prompt is Guess a letter (or 'quit' to quit): — case-insensitive, whitespace stripped. A valid guess is exactly one letter a–z; anything else (multiple letters, digits, empty input, non-English letters) is invalid. Exact error messages: Please enter a single letter (a-z). / You already guessed 'x'. Bad input is re-asked and never penalized. 

- **The report** (returned by make_move): Hit: Yes! 'x' is in the word. Miss: Nope, 'x' is not in the word. 

- **The final lines** : Returned by game_state: You won! The word was 'xxx'. / You lost! The word was 'xxx'. The quit line is main.py's own: You quit. The word was 'xxx'. 

- **Win and loss formulae** : Won when every letter of the word is in guessed (equivalently: the masked word contains no _). Lost when lives = 0. Won is checked before lost; both can never be true at once — a winning guess is always a hit, and hits cost no life. 

### **1.4 Blackjack** 

- **State** (held by run_blackjack): deck, player, dealer. 

- **The deck** : 52 cards; a card is a (rank, suit) pair. Ranks: A, 2–10, J, Q, K. Suits: S, H, D, C (letters, not symbols — safest across terminals). new_deck returns it shuffled; one fresh deck per round. Exhaustion is impossible — a hand busts long before 52 cards run out. 

- **A hand** : A list of cards; two each after deal_initial. The dealer's second card is the hole card. 

- **Card values** : 2–10 at face value; J, Q, K = 10; A = 11 while the total stays 21 or under, otherwise 1. hand_value returns the best total under this rule. Bust ⇔ value > 21. 

- **The actions** : hit (draw one card) or stand (end your turn; the dealer plays). Accepted input, case-insensitive: h or hit, s or stand, quit. Prompt: Hit or stand? (or 'quit'): (main.py). Error: Enter hit, stand, or quit. (main.py). 

- **The dealer** : After a stand, draws until its value is 17 or more, then stops. Stands on all 17s, soft ones included. 

- **The display** : Two lines — Dealer: then You: — cards as rank+suit (10H), running total in parentheses. While the round is in progress the hole card shows as XX and the dealer's displayed total is the up card's value alone; once the round ends, the render reveals the full hand. 

Dealer: AS XX (11) You:   10H 9S (19) Hit or stand? (or 'quit'): 

- **Outcome rules, in priority order** : 

   - Player busts on a hit → lose, immediately; the dealer never plays. 

   - Player stands → dealer plays. Dealer busts → win. Otherwise higher total wins; equal totals → push (tie). 

- **Scope locks** (deliberate simplifications): No betting, no naturals bonus, no double/split/insurance, no auto-stand at 21 — the player always chooses. 

- **The report and status** (both from make_move): The status is machine-readable ("in progress" / "won" / "lost" / "push"); the report is what gets printed. Exact reports: You draw the <card>. / You draw the <card> — bust with <n>. You lose this round. / Dealer busts with <n> — you win! / Dealer stands on <n>, you have <m> — you win! / Dealer stands on <n>, you have <m> — you lose. / Dealer stands on <n>, you have <m> — push. No game_state function exists — a round only ever ends as a consequence of an action, so the verdict rides with make_move. 

- **The quit line** (main.py): You quit the round. 

### **1.5 Connect 4** 

- **State** (held by run_connect4): board, mark. 

- **The board** : 6 rows × 7 columns: a list of 6 rows of 7 values. Empty cells are .; the two players' discs are X and O. X always moves first. 

- **Gravity** : A disc dropped into column _c_ falls to the lowest empty cell in that column. A full column is illegal — read_column rejects it via column_is_full. 

- **The win formula** : Four of the same mark in an unbroken straight line — horizontal, vertical, or either diagonal. Draw ⇔ 42 discs with no line. 

- **The display** : A column header 1 2 3 4 5 6 7, then the rows top-to-bottom (discs stack upward from the bottom row). No row labels — players reference columns only. 

1 2 3 4 5 6 7 

. . . . . . . . . . . X . . . . . O X O . 

. . X O X X O Player O, choose a column (1-7 or 'quit'): 

- **The prompt and input rules** (main.py): The prompt names the current player — a hotseat game must, or players lose track: Player <mark>, choose a column (1-7 or 'quit'): . Errors, exact: Enter a column number 1-7. / Column <n> is full — choose another. 

- make_move returns only the board — the outcome is visible in the render, so there is no report. 

- **The final lines** (logic, from game_state): Player X wins! / Player O wins! / The board is full — a draw. Quit line (main.py): Player <mark> quits the game. — whoever was prompted. 

### **1.6 Battleship** 

- **State** (held by run_battleship): enemy_fleet, shots, player_fleet, computer_shots. 

- **The grid** : 10×10. Rows and columns both numbered 1–10; typed as row col (e.g. 3 4); stored 0-indexed as in Sudoku. 

- **The fleet** : Both sides field the same five ships: Carrier (5 cells), Battleship (4), Submarine (3), Cruiser (3), Destroyer (2). A ship is its name plus its set of cells; a fleet is a list of five ships. place_fleet positions them randomly — horizontal or vertical, fully on the grid, never overlapping; touching is allowed. Called twice, once per side. 

- **Shots** : Two sets of cells: shots (yours, at the enemy grid) and computer_shots (the computer's, at yours). 

- **Hit, miss, sunk** : A shot is a hit if it lands on any ship cell, else a miss. A ship is sunk ⇔ every one of its cells has been hit. 

- **The two boards** : Your waters (render_player_board): # ship, X hit on you, o miss on you, . water. The enemy grid (render_enemy_board): . unknown, o your miss, X your hit, * the 

cells of a ship you have sunk. Both carry row labels 1–10 and a column header 1–10. 

1 2 3 4 5 6 7 8 9 10 1  . . . . . . . . .  . 

2  . o . . . . . . .  . 3  . o . . . . . . .  . 4  . . . * . . . . .  . 5  . . . * . . . . .  . 6  . . . X . . . . .  . 7  . . . . . . . . .  . 8  . . . . . . . . .  . 9  . . . . . . . . .  . 10  . . . . . . . . .  . 

- **The computer opponent** : When your turn ends on a miss — and you haven't won — computer_fire picks one uniformly random unfired cell on your grid and fires. No hunting, no targeting logic; it cannot fire at the same cell twice. 

- **The turn rule** : A hit earns another shot; a turn ends only on a miss. You keep firing while you hit (the computer is not called), then the computer keeps firing while it hits, and play returns to you after its first miss. Game state is checked after every single shot, so a winning hit ends the game at once. 

- **The prompt and input rules** (main.py): Fire at row, column (or 'quit'): Errors, exact: Enter two numbers 1-10: row and column. / You already fired at <r> <c>. 

- **The reports** (logic; make_move and computer_fire also return an outcome, "hit" or "miss", which main.py uses to apply the turn rule): Yours, from make_move: Hit! / Miss. / Hit — you sank the enemy <name>! The computer's, from computer_fire: The computer fires at <r> <c> — a hit! / The computer fires at <r> <c> — a miss. / The computer fires at <r> <c> — it sinks your <name>! 

- **Win and loss** (logic, from game_state, checked after every fire in both directions). All five enemy ships sunk → You win — the enemy fleet is destroyed! All five of yours sunk → You lose — your fleet is destroyed! 

- **The quit line** (main.py): You quit the battle. 

## **2. Program Flow** 

### **2.1 The launcher (main)** 

On startup, main prints the seven-option menu (text exactly as in the PRD) and prompts Enter your choice: . Choices 1–5 start the matching game; 6 starts one of the five chosen uniformly at random; 7 prints Thanks for playing! Goodbye. and ends the program. Invalid input prints Invalid choice. Please enter a number between 1 and 7. and the menu reprints. Each game runs inside a run_* function; when it returns, the menu reprints and the app waits for the next choice. No game ever exits the app — only option 7 does. 

### **2.2 Sudoku (run_sudoku)** 

1. Draw a puzzle — new_puzzle → board, givens. 

2. Show the board — render_board. 

3. Read a move — read_move: parse, shape-check, reject givens; an erase (value 0) is accepted as is, any other value must be a legal placement; re-asking each time. 

4. If the input is quit: print the quit line and return to the menu. 

5. Apply the move — make_move writes the value (0 erases the cell). No report — the next render shows it. 

6. Evaluate — game_state: no empty cell remains → the solved line; otherwise "in progress". 

7. If solved: show the completed board, print the solved line, return to the menu. 

8. Otherwise repeat from step 2. 

### **2.3 Hangman (run_hangman)** 

1. Pick the secret word — pick_word. 

2. Set guessed empty and lives = 6. 

3. Show the display: gallows for the current wrong count, then the masked word. 

4. Read a guess — read_letter; invalid or repeated input is re-asked with an error message and costs nothing. 

5. If the guess is quit: print the quit line and return to the menu. 

6. Apply the guess — make_move: the letter joins guessed; on a hit lives is unchanged, on a miss it drops by one. The report states which happened. 

7. Print the report. 

8. Evaluate — game_state: every letter revealed → the win line; lives = 0 → the loss line; otherwise "in progress". 

9. If not "in progress": print the final line and return to the menu. 

10. Otherwise repeat from step 3, showing the updated gallows and masked word. 

### **2.4 Blackjack (run_blackjack)** 

1. Build a fresh shuffled deck — new_deck. 

2. Deal two cards each — deal_initial → deck, player, dealer. 

3. Show the hands — render_hands, hole card hidden. 

4. Read an action — read_action; anything unrecognized is re-asked. 

5. If quit: print the quit line and return to the menu. 

6. Apply the action — make_move → (deck, player, dealer, report, status): hit draws one card (bust ends the round at once); stand runs the dealer and settles the comparison. 

7. Print the report. 

8. Show the hands again — hole card revealed if the round has ended. 

9. If status is not "in progress": return to the menu. 

10. Otherwise repeat from step 4. 

### **2.5 Connect 4 (run_connect4)** 

1. Create the empty board — new_board. 

2. Set mark = "X". 

3. Show the board — render. 

4. Read a column — read_column(board, mark): 1–7 and not a full column, re-asked otherwise. 

5. If quit: print the quit line and return to the menu. 

6. Drop the disc — make_move applies gravity. 

7. Evaluate — game_state: a line for either mark → that player's win line; board full → the draw line; otherwise "in progress". 

8. If ended: show the final board, print the final line, return to the menu. 

9. Otherwise pass the turn to the other mark and repeat from step 3. 

### **2.6 Battleship (run_battleship)** 

1. Place both fleets — place_fleet twice → enemy_fleet, player_fleet; both shot sets start empty. 

2. Show both boards — your waters first, then the enemy grid.

3. Your turn — repeat:

   - Read coordinates — read_coords(shots): two numbers 1–10, cell not already fired.

   - If quit: print the quit line and return to the menu.

   - Fire — make_move → (shots, outcome, report); print the report, then re-render the enemy grid.

   - Evaluate — game_state: enemy fleet destroyed → win line, return.

   - If the outcome is "miss", your turn ends; if "hit", fire again.

4. Computer's turn — repeat:

   - Computer fires — computer_fire → (computer_shots, outcome, report); print the report, then re-render your waters.

   - Evaluate — game_state: your fleet destroyed → loss line, return.

   - If the outcome is "miss", the computer's turn ends; if "hit", it fires again.

5. Repeat from step 2: both boards are shown again, so after a full round each board has been printed twice in a row (once after the last shot, once at the top of the loop). 

## **3. Function Signatures** 

42 top-level functions: 13 in main.py, 29 across the logic modules (plus the nested helper shuffle_rows inside random_solution). 

### **3.1 main.py** 

|**Typed header line**|**What it's for**|
|---|---|
|def main() -> None:|The menu loop: print menu, read choice,<br>dispatch, reprint on invalid, goodbye on 7.|
|def run_random() -> None:|Launches one of the five run functions,<br>chosen uniformly at random.|
|def run_sudoku() -> None:|Sudoku loop + state (board, givens).|
|def run_hangman() -> None:|Hangman loop + state (word, guessed,<br>lives).|
|def run_blackjack() -> None:|Blackjack loop + state (deck, player, dealer).|
|def run_connect4() -> None:|Connect 4 loop + state (board, whose turn).|
|def run_battleship() -> None:|Battleship loop + state (enemy_fleet, shots,<br>player_fleet, computer_shots).|
|def read_choice() -> str:|Menu input: prints the prompt, reads one|



||line, strips whitespace, returns it<br>unchanged — validation lives in main() so<br>the menu reprints on invalid input.|
|---|---|
|def read_letter(guessed: set) -> str:|One new a–z letter, or "quit".|
|def read_move(board: list, givens: set) -><br>tuple:|Sudoku input: parse row col value,<br>shape-check, reject givens, legality via<br>sudoku_logic.is_valid_placement. Returns<br>(row, col, value) or "quit".|
|def read_action() -> str:|Blackjack input: hit / stand / quit.|
|def read_column(board: list, mark: str) -><br>int:|Connect 4 input: 1–7 and column not full<br>(fullness via connect4_logic.column_is_full).|
|def read_coords(shots: set) -> tuple:|Battleship input: parse row col, cell not<br>already fired. Returns (row, col) or "quit".|



### **3.2 sudoku_logic.py** 

|**Typed header line**|**What it's for**|
|---|---|
|def random_solution() -> list:|Builds a fresh valid completed grid by<br>shuffling BASE_SOLUTION.|
|def new_puzzle() -> tuple:|Punches holes in a random solution: returns<br>(board, givens).|
|def render_board(board: list, givens: set) -><br>str:|The 9×9 grid, givens marked differently<br>from player entries.|
|def is_valid_placement(board: list, row: int,<br>col: int, value: int) -> bool:|Row/column/box scan — target cell skipped<br>so entries can be corrected. Called by<br>main's read_move.|
|def make_move(board: list, row: int, col: int,<br>value: int) -> list:|Writes the value, returns the board.|
|def game_state(board: list) -> str:|"in progress" or the solved line — solved<br>when no cell is 0.|



### **3.3 hangman_logic.py** 

|**Typed header line**|**What it's for**|
|---|---|
|def pick_word() -> str:|Random secret word from WORDLIST.|
|def draw_gallows(lives: int) -> str:|ASCII drawing for the current lives.|
|def mask_word(word: str, guessed: set) -><br>str:|The h _ n _ m _ n line.|
|def make_move(word: str, guessed: set,<br>lives: int, guess: str) -> tuple:|All rules: returns (guessed, lives, report).|
|def game_state(word: str, guessed: set,<br>lives: int) -> str:|"in progress" or the won/lost line.|



### **3.4 blackjack_logic.py** 

|**Typed header line**|**What it's for**|
|---|---|
|def new_deck() -> list:|Fresh shuffled 52-card deck.|
|def deal_initial(deck: list) -> tuple:|(deck, player, dealer) with two cards each.|
|def hand_value(cards: list) -> int:|Best total with aces as 1 or 11.|
|def render_hands(player: list, dealer: list,<br>hide_dealer_card: bool) -> str:|Both hands with values; hole card hidden<br>while the player is still playing.|
|def dealer_turn(deck: list, dealer: list) -><br>tuple:|The computer opponent: draws to 17.<br>Returns (deck, dealer, summary).|
|def make_move(deck: list, player: list,<br>dealer: list, action: str) -> tuple:|Hit draws and checks bust; stand settles<br>the round via dealer_turn. Returns (deck,<br>player, dealer, report, status).|



### **3.5 connect4_logic.py** 

|**Typed header line**|**What it's for**|
|---|---|



|def new_board() -> list:|Empty 6×7 board.|
|---|---|
|def render(board: list) -> str:|The grid with column numbers 1–7.|
|def column_is_full(board: list, col: int) -><br>bool:|Called by main's read_column.|
|def make_move(board: list, col: int, mark:<br>str) -> list:|Drops the disc with gravity, returns the<br>board.|
|def game_state(board: list) -> str:|Checks both marks: "in progress" / X wins /<br>O wins / draw.|



### **3.6 battleship_logic.py** 

|**Typed header line**|**What it's for**|
|---|---|
|def place_fleet() -> list:|Random legal placement of the 5 ships<br>(name + set of cells each). Called twice —<br>once per side.|
|def render_enemy_board(fleet: list, shots:<br>set) -> str:|Target grid: your hits and misses; ships<br>hidden.|
|def render_player_board(fleet: list,<br>computer_shots: set) -> str:|Your waters: ships visible, computer's hits<br>and misses.|
|def make_move(fleet: list, shots: set, row:<br>int, col: int) -> tuple:|You fire: returns (shots, outcome, report) — outcome is "hit" or "miss"; report says hit / miss / sank a<br>named ship.|
|def computer_fire(player_fleet: list,<br>computer_shots: set) -> tuple:|The computer opponent: picks an unfired<br>cell, fires. Returns (computer_shots, outcome, report).|
|def is_sunk(cells: set, shots: set) -> bool:|Shared helper for sank messages and win<br>detection.|
|def game_state(enemy_fleet: list, shots: set,<br>player_fleet: list, computer_shots: set) -><br>str:|"in progress" / you win / you lose — checked<br>after each fire, both directions.|



### **3.7 Constants by module** 

- main.py: MENU — the seven-option menu, text exactly as in the PRD. 

- sudoku_logic.py: BASE_SOLUTION (below), CELLS_TO_REMOVE = 48. 

- hangman_logic.py: WORDLIST (ten words, 4–8 lowercase letters), GALLOWS (seven drawings). 

- blackjack_logic.py: SUITS, RANKS. 

- connect4_logic.py: none — the 6×7 size is part of new_board. 

- battleship_logic.py: SHIPS (Carrier 5, Battleship 4, Submarine 3, Cruiser 3, Destroyer 2), GRID_SIZE = 10. 

**BASE_SOLUTION** — the one hand-made constant in the project: 

5 3 4 | 6 7 8 | 9 1 2 6 7 2 | 1 9 5 | 3 4 8 1 9 8 | 3 4 2 | 5 6 7 ------+-------+-----8 5 9 | 7 6 1 | 4 2 3 4 2 6 | 8 5 3 | 7 9 1 7 1 3 | 9 2 4 | 8 5 6 

------+-------+-----9 6 1 | 5 3 7 | 2 8 4 2 8 7 | 4 1 9 | 6 3 5 3 4 5 | 2 8 6 | 1 7 9 

## **4. Function-Level Algorithm** 

### **4.1 Launcher — main.py** 

def main() -> None: 

- Build the dispatch table: "1" → run_sudoku, "2" → run_hangman, "3" → run_blackjack, "4" → run_connect4, "5" → run_battleship, "6" → run_random. 

- Repeat forever: 

   - Print MENU. 

   - Set choice to read_choice(). 

   - If choice is "7": print Thanks for playing! Goodbye. and return. 

   - If choice is a key of the table: call its function — when it returns, the loop repeats and the menu reprints. 

   - Otherwise print Invalid choice. Please enter a number between 1 and 7. and repeat. 

def run_random() -> None: 

- Put the five run functions into a list. 

- Choose one uniformly at random. 

- Call it. 

def read_choice() -> str: 

- Print Enter your choice: and read one line. 

- Strip the surrounding whitespace. 

- Return the result unchanged — validation is main()'s job, so the menu reprints on bad input. 

### **4.2 Sudoku** 

#### **In main.py:** 

def read_move(board: list, givens: set) -> tuple: 

- Repeat: 

   - Print Row, column, value (0 erases, or 'quit'): and read a line; strip it. 

   - If it is quit, return it. 

   - Split into parts; if there are not exactly three, or row or column is not a whole number from 1 to 9, or value is not a whole number from 0 to 9: print Enter three numbers: row 1-9, column 1-9, value 0-9. and repeat. 

   - Convert row and column to 0-based; keep the value as is. 

   - If (row, col) is in givens: print That cell is part of the puzzle — it can't be changed. and repeat. 

   - If value is 0: return (row, col, 0) — an erase needs no legality check.

   - If is_valid_placement(board, row, col, value) is False: print <v> doesn't fit there — its row, column, or box already has a <v>. and repeat. 

   - Return (row, col, value). 

def run_sudoku() -> None: 

- Take board, givens from new_puzzle(). 

- Repeat: 

   - Print render_board(board, givens). 

   - Set move to read_move(board, givens). 

   - If it is quit: print You quit this puzzle. and return. 

   - Set board to make_move(board, row, col, value). 

   - Set status to game_state(board). 

   - If status is not "in progress": print render_board(board, givens), print the status, and return. 

#### **In sudoku_logic.py:** 

def random_solution() -> list: 

- Make a copy of BASE_SOLUTION. 

- Relabel the digits: take a random rearrangement of 1–9 and rewrite every cell through it. 

- For each band (rows 1–3, 4–6, 7–9): shuffle its three rows. 

- Shuffle the three bands themselves. 

- For each stack (columns 1–3, 4–6, 7–9): shuffle its three columns. 

- Shuffle the three stacks themselves. 

- Return the grid. 

_(Each operation maps rows to rows, columns to columns, and boxes to boxes, and relabels_ 

_digits one-to-one — all three Sudoku constraints survive every shuffle. A transpose is an optional sixth shuffle for extra variety.)_ 

def new_puzzle() -> tuple: 

- Set grid to random_solution(). 

- Choose CELLS_TO_REMOVE different cells at random and set them to 0. 

- Set givens to every (row, col) whose value is not 0. 

- Return (grid, givens) — the punched grid is the board. (random_solution builds a fresh grid on every call, so no copy concerns arise.) 

def render_board(board: list, givens: set) -> str: 

- Build the header: column numbers 1–9, with a | after columns 3 and 6. 

- For each row 1–9: 

   - For each column 1–9: value 0 → .; a given cell → the value in a 3-character field; a player entry → [value]. 

   - Join the row's cells with spaces, place | after columns 3 and 6, and prefix the row label. 

- After rows 3 and 6, add a dashed separator line. 

- Join everything and return. 

def is_valid_placement(board: list, row: int, col: int, value: int) -> bool: 

- Row scan: if the value appears anywhere in row r except at (r, c) itself, return False. 

- Column scan: likewise for column c. 

- Box scan: the box's first row is r − (r mod 3) and its first column is c − (c mod 3); if the value appears in those nine cells except at (r, c) itself, return False. 

- Return True. 

def make_move(board: list, row: int, col: int, value: int) -> list: 

- Write the value into cell (row, col). 

- Return the board. 

def game_state(board: list) -> str: 

- If no cell is 0: return Solved! Well played. 

- Return "in progress". 

### **4.3 Hangman** 

#### **In main.py:** 

def read_letter(guessed: set) -> str: 

- Repeat: 

   - Print Guess a letter (or 'quit' to quit): and read a line. 

   - Strip the whitespace and lowercase the result. 

   - If it is quit, return it. 

   - If it is exactly one character between 'a' and 'z', and not already in guessed, return it. 

   - If it is already in guessed: print You already guessed 'x'. 

- Otherwise: print Please enter a single letter (a-z). 

def run_hangman() -> None: 

- Set word to pick_word(), guessed to an empty set, and lives to 6. 

- Repeat: 

   - Print draw_gallows(lives), then mask_word(word, guessed). 

   - Set guess to read_letter(guessed). 

   - If guess is quit: print You quit. The word was 'xxx'. and return. 

   - Take the new guessed, lives, and report from make_move(word, guessed, lives, guess); print the report. 

   - Set status to game_state(word, guessed, lives). 

   - If status is not "in progress": print it and return. 

#### **In hangman_logic.py:** 

def pick_word() -> str: 

- Return one word chosen at random from WORDLIST. 

def draw_gallows(lives: int) -> str: 

- Set wrong to 6 − lives. 

- Return GALLOWS[wrong]. 

def mask_word(word: str, guessed: set) -> str: 

- For each letter of word: keep the letter if it is in guessed, otherwise use _. 

- Join the results with single spaces and return. 

def make_move(word: str, guessed: set, lives: int, guess: str) -> tuple: 

- Add the guess to guessed. 

- If the guess occurs in word: return (guessed, lives, "Yes! 'x' is in the word."). 

- Otherwise: return (guessed, lives − 1, "Nope, 'x' is not in the word."). 

def game_state(word: str, guessed: set, lives: int) -> str: 

- If every letter of word is in guessed: return You won! The word was 'xxx'. 

- If lives is 0: return You lost! The word was 'xxx'. 

- Return "in progress". 

### **4.4 Blackjack** 

#### **In main.py:** 

def read_action() -> str: 

- Repeat: 

   - Print Hit or stand? (or 'quit'): and read a line; strip and lowercase it. 

   - If it is h or hit: return "hit". 

   - If it is s or stand: return "stand". 

- If it is quit: return "quit". 

- Otherwise: print Enter hit, stand, or quit. 

def run_blackjack() -> None: 

- Set deck to new_deck(). 

- Take deck, player, dealer from deal_initial(deck). 

- Print render_hands(player, dealer, True). 

- Repeat: 

   - Set action to read_action(). 

   - If action is quit: print You quit the round. and return. 

   - Take deck, player, dealer, report, status from make_move(deck, player, dealer, action). 

   - Print the report. 

   - Print render_hands(player, dealer, hide_dealer_card) — the hole card is hidden exactly while status is "in progress". 

   - If status is not "in progress": return. 

#### **In blackjack_logic.py:** 

def new_deck() -> list: 

- For each of the four suits, for each of the thirteen ranks, form one card (rank, suit). 

- Shuffle the 52 cards. 

- Return the deck. 

def deal_initial(deck: list) -> tuple: 

- Take two cards from the top of the deck into the player's hand. 

- Take two more into the dealer's hand — the dealer's second card is the hole card. 

- Return (deck, player, dealer). 

def hand_value(cards: list) -> int: 

- Set total to 0 and aces to 0. 

- For each card: J, Q, K add 10; A adds 11 and raises aces by one; any other rank adds its number. 

- While total is over 21 and aces is above 0: subtract 10 from total and one from aces (recount an ace as 1). 

- Return total. 

def render_hands(player: list, dealer: list, hide_dealer_card: bool) -> str: 

- Dealer line: Dealer: followed by the dealer's cards as rank+suit (e.g. 10H), space-separated. 

- If hide_dealer_card: show only the first card, then XX; the number in parentheses is the value of the first card alone. 

- Otherwise: show all the dealer's cards with hand_value(dealer) in parentheses. 

- Player line: You: followed by all the player's cards with hand_value(player) in parentheses; the two labels align. 

- Return the two lines. 

def dealer_turn(deck: list, dealer: list) -> tuple: 

- While hand_value(dealer) is under 17: take one card from the deck into the dealer's hand. 

- Build the summary — a fragment with no final period: Dealer stands on <n> if the final total is 21 or less, otherwise Dealer busts with <n>. 

- Return (deck, dealer, summary). 

def make_move(deck: list, player: list, dealer: list, action: str) -> tuple: 

- If action is "hit": 

   - Take one card from the deck into the player's hand. 

   - If hand_value(player) is over 21: return (deck, player, dealer, "You draw the <card> — bust with <n>. You lose this round.", "lost"). 

   - Otherwise return (deck, player, dealer, "You draw the <card>.", "in progress"). 

- If action is "stand": 

   - Finish the dealer's hand with dealer_turn; take its summary. 

   - If the dealer's total is over 21: report = summary + " — you win!"; status "won". 

   - If the player's total is higher: report = summary + ", you have <m> — you win!"; status "won". 

   - If lower: report = summary + ", you have <m> — you lose."; status "lost". 

   - If equal: report = summary + ", you have <m> — push."; status "push". 

● Return (deck, player, dealer, report, status). _(Every assembled sentence is exactly one of the reports locked in 1.4 — the stand branch is summary plus tail.)_ 

### **4.5 Connect 4** 

#### **In main.py:** 

def read_column(board: list, mark: str) -> int: 

- Repeat: 

   - Print Player <mark>, choose a column (1-7 or 'quit'): and read a line; strip it. 

   - If it is quit, return it. 

   - If it is not a whole number from 1 to 7: print Enter a column number 1-7. and repeat. 

   - Convert to the 0-based column index. 

   - If column_is_full(board, col) is True: print Column <n> is full — choose another. (1-based) and repeat. 

   - Return the column index. 

def run_connect4() -> None: 

- Set board to new_board() and mark to "X". 

- Repeat: 

   - Print render(board). 

   - Set col to read_column(board, mark). 

   - If col is quit: print Player <mark> quits the game. and return. 

   - Set board to make_move(board, col, mark). 

- Set status to game_state(board). 

- If status is not "in progress": print render(board), print the status, and return. 

- Otherwise set mark to the other mark. 

#### **In connect4_logic.py:** 

def new_board() -> list: 

- Return six rows of seven cells, every cell .. 

def render(board: list) -> str: 

- Build the header line 1 2 3 4 5 6 7. 

- The bottom row is stored first, so walk the stored rows from last to first, joining each row's seven cells with spaces into one line. 

- Join the lines and return. 

def column_is_full(board: list, col: int) -> bool: 

- If the topmost cell of the column — the cell in the last stored row — is not .: return True. 

- Otherwise return False. 

def make_move(board: list, col: int, mark: str) -> list: 

- Walk the column from the bottom row upward. 

- Write the mark into the first . cell (read_column guarantees one exists). 

- Return the board. 

def game_state(board: list) -> str: 

- For mark "X", then mark "O": 

   - For every cell holding that mark: 

      - If the next three cells to the right are all on the board and hold the mark: that player has a line. 

      - Same for the three cells below. 

      - Same for the three cells diagonally down-right. 

      - Same for the three cells diagonally down-left. 

      - On the first line found, return Player X wins! or Player O wins!. 

- If neither mark has a line and no . remains anywhere: return The board is full — a draw. 

- Return "in progress". 

_(Why only four directions: every possible four-in-a-row begins at its topmost or leftmost cell and runs right, down, down-right, or down-left — checking those four from every cell covers every line exactly. Cells off the edge count as not matching.)_ 

### **4.6 Battleship** 

**In main.py:** 

def read_coords(shots: set) -> tuple: 

- Repeat: 

- Print Fire at row, column (or 'quit'): and read a line; strip it. 

- If it is quit, return it. 

- Split into parts; if there are not exactly two, or either is not a whole number from 1 to 10: print Enter two numbers 1-10: row and column. and repeat. 

- Convert to the 0-based (row, col). 

- If (row, col) is already in shots: print You already fired at <r> <c>. (1-based) and repeat. 

- Return (row, col). 

def run_battleship() -> None: 

- Set player_fleet and enemy_fleet each to place_fleet(); shots and computer_shots to empty sets. 

- Repeat: 

   - Print render_player_board(player_fleet, computer_shots), then render_enemy_board(enemy_fleet, shots).

   - Your turn — repeat:

      - Set coords to read_coords(shots). If it is quit: print You quit the battle. and return.

      - Take shots, outcome, report from make_move(enemy_fleet, shots, row, col); print the report, then print render_enemy_board(enemy_fleet, shots).

      - Set status to game_state(enemy_fleet, shots, player_fleet, computer_shots); if not "in progress": print it and return.

      - If outcome is "miss": leave this loop (a "hit" fires again).

   - Computer's turn — repeat:

      - Take computer_shots, outcome, report from computer_fire(player_fleet, computer_shots); print the report, then print render_player_board(player_fleet, computer_shots).

      - Set status from game_state again; if not "in progress": print it and return.

      - If outcome is "miss": leave this loop (a "hit" fires again). 

#### **In battleship_logic.py:** 

def place_fleet() -> list: 

- Set placed_cells to an empty set and fleet to an empty list. 

- For each (name, length) in SHIPS: 

   - Repeat: choose horizontal or vertical at random, and a random starting cell such that the whole ship fits on the 10×10 grid; compute the ship's cells. 

   - If any of those cells is already in placed_cells: retry the choice. (Safe — 17 ship cells on a 100-cell grid always leave room.) 

   - Otherwise add the ship — name plus cells — to the fleet, and its cells to placed_cells. 

- Return the fleet of five ships. 

def is_sunk(cells: set, shots: set) -> bool: 

- If any cell of the ship is not in shots: return False. 

- Return True. 

def make_move(fleet: list, shots: set, row: int, col: int) -> tuple: 

- Add (row, col) to shots. 

- If (row, col) is not a cell of any ship in the fleet: return (shots, "miss", "Miss."). 

- Otherwise let ship be the ship owning that cell. 

- If is_sunk on that ship's cells: return (shots, "hit", "Hit — you sank the enemy <name>!"). 

- Otherwise: return (shots, "hit", "Hit!"). 

def computer_fire(player_fleet: list, computer_shots: set) -> tuple: 

- Choose a cell at random among the grid cells not in computer_shots. 

- Add it to computer_shots. 

- If it is not on any ship: return (computer_shots, "miss", "The computer fires at <r> <c> — a miss.") — coordinates printed 1-based. 

- If it is on a ship and that ship is now sunk: return (…, "hit", "The computer fires at <r> <c> — it sinks your <name>!"). 

- Otherwise: return (…, "hit", "The computer fires at <r> <c> — a hit!"). 

def render_player_board(fleet: list, computer_shots: set) -> str: 

- Build the column header 1 to 10. 

- For each row 1–10, each column 1–10: 

   - If the cell is in computer_shots and on a ship: X. 

   - If it is in computer_shots and not on a ship: o. 

   - If it is on a ship and not yet shot: #. 

   - Otherwise: .. 

   - Prefix each row with its row number, join, and return. _(Hit overrides the ship symbol — check order matters.)_ 

def render_enemy_board(fleet: list, shots: set) -> str: 

- Build the column header 1 to 10. 

- For each cell: 

   - If it is in shots and on a ship: * if that ship is sunk, otherwise X. 

   - If it is in shots and not on a ship: o. 

   - Otherwise: . (unknown waters). 

   - Prefix row numbers, join, and return. 

def game_state(enemy_fleet: list, shots: set, player_fleet: list, computer_shots: set) -> str: 

- If every ship in enemy_fleet is sunk: return You win — the enemy fleet is destroyed! 

- If every ship in player_fleet is sunk: return You lose — your fleet is destroyed! 

- Return "in progress".
