# Sudoku-Game

A classic Sudoku puzzle game with an integrated AI agent that can provide hints or solve the entire puzzle for you. Developed using Python and Pygame, featuring a clean and intuitive graphical user interface.

<h3>Features</h3>
- Interactive GUI: Play Sudoku with a visually appealing and responsive interface. <br>
- AI Hint System: Get help when stuck with a hint that fills in a logically deduced number or reveals a random correct number.<br>
- Full Solver: Let the AI solve the entire puzzle instantly.<br>
- New Game Generation: Start a new randomly generated Sudoku puzzle.<br>
- Input Validation: Real-time feedback for invalid moves.<br>
- Clear Cells: Easily remove numbers you've entered.<br>
- Visual Feedback: Highlighted selected cells and distinct coloring for original, user-entered, and hinted numbers.<br>

<h3>How to Play </h3>
1] Select a Cell: Click on any empty (white background) cell to select it. The selected cell will be highlighted in blue. You cannot modify the original numbers (black text).<br>
2] Enter Numbers: With a cell selected, type a number (1-9) using your keyboard.<br>
- If your move is incorrect, an "Invalid move!" message will appear.<br>
- If your move is valid, the number will appear in blue.<br>
3] Clear a Cell: Press the Backspace or Delete key when a cell is selected to clear its content.<br>
4] Get a Hint:<br>
- Click the "Hint" button at the bottom of the window.<br>
- Alternatively, press the H key on your keyboard.<br>
- The AI will place a number in a random empty cell, highlighting it in a distinct orange color with a light blue background. This highlight persists until you interact with that cell.<br>
5] Solve the Puzzle:<br>
- Click the "Solve" button at the bottom of the window.<br>
- Alternatively, press the S key on your keyboard.<br>
- The AI will fill in the entire puzzle correctly.<br>
6] Start a New Game:<br>
- Click the "New Game" button at the bottom of the window.<br>
- Alternatively, press the N key on your keyboard.<br>
7] Quit: Close the game window.<br>

<h3>How to Run </h3>
To run this project, follow these steps:<br>
1] Clone the repository:<br>
git clone https://github.com/your-username/sudoku-game.git <br>
cd sudoku-game <br>
2] Install Requirements: <br>
You can install it using pip: <br>
pip install -r requirements.txt <br>
3] Run the game: <br>
python sudoku_game.py <br>

<h3>AI Hint System </h3>
The AI hint system employs a backtracking algorithm similar to the full solver. When a hint is requested: <br>
1] It first attempts to find an empty cell where only one number can logically be placed (a "Naked Single"). <br>
2] If such a cell is found, that number is placed. <br>
3] If no "Naked Single" is immediately apparent, the system falls back to providing the correct number for a randomly chosen empty cell from the pre-calculated solved board. <br>

This approach provides a helpful nudge without giving away too much, while the "Solve" feature offers a complete solution.
