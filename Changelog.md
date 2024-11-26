# Versions

## 1.0.0

- a random piece is created
- pieces move (left and right and bottom) and rotate
- when a line is filled, it is removed
- game doesn't end when screen is filled
- very simple graphic interface with simple borders and pieces represented with 'x's

## 1.1.0

- now game stops when no possible moves remain
- added a display of the next move to the left of the grid
- fixed a bug about the rotation of the pieces

## 1.2.0

- now pieces are represented by white filled squares (fixed distorted pieces)
- added options for logs, choosing pieces file and specifying seed on game start
- updated readme and added documentation

## 1.3.0

- Added options `seed`, `speed`, `pieces`, `heigh` and `width` to the game
- fixed bugs related to screen refrshing, cleared lines and the dispaly of the next piece

## 1.4.0

- Changed structure of project by adding `src` folder
- Now logs are put inside the `log` folder
- Refactored `tetris` module
- Updated `readme`.

## 1.5.0

- Added checks on some of the options and a user friendly exception
- Handled CTRL+C interruption
- Resolved bug about position of the rendering of the next piece
- Now options are correctly checks, and large dimensions of game play are supported