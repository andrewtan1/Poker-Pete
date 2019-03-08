# Poker-Pete

Poker Pete is an intelligent card-playing AI made to detect cards and play the optimal move in a specified card game using concepts of Digital Signal Processing, Machine Learning, and Game Theory.

## Project Requirements

### Required Software

- Conda 4.6.7
- Python 3.7.2
- OpenCV 4.0.0.21
- OMAPL138 Libraries

### Required Hardware

- Texas Instruments LCDK
- USB Camera
- Green Table Mat
- Pack of 52 Playing Cards

## Development Plan

1) Using the included python script(s) w/ the appropriate packages, we will generate the Neural Network constants for further development on the LCDK.
2) The Neural Network can now be implemented at the interrupt level using a more elaborate version of the method that was used in Mini-Project 2.
3) After finishing development on the LCDK, we implement the rules of various card games.
4) Next, we implement the logic for choosing the best moves for each game using the concept of game theory for each of the games we choose to develop.
5) To use the AI, select which game is to be played and the number of opposing players. Poker Pete should be able to determine the best moves from here on out.

## References/Sources

Training Set Repository (Thanks to lordloh): [link](https://github.com/lordloh/playing-cards)