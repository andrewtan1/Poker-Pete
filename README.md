# Poker-Pete

Poker Pete is an intelligent card-playing AI made to detect cards and play the optimal move in a specified card game using concepts of Digital Signal Processing, Machine Learning, and Game Theory.

## Project Requirements

### Required Software

- Conda 4.6.7
- Python 3.7.2
- OpenCV 4.0.0.21
- imaug 0.2.8
- OMAPL138 Libraries

### Required Hardware

- PC/Laptop
- Texas Instruments LCDK
- USB Camera
- Green Table Mat (optional)
- Pack of 52 Playing Cards

## Development Plan

1) Using the included python script(s) w/ the appropriate packages, we will generate the Neural Network constants on a PC for further development on the LCDK.
2) The Neural Network can now be implemented at the interrupt level using a more elaborate version of the method that was used in Mini-Project 2.
3) After finishing development on the LCDK, we implement the rules of various card games.
4) Next, we implement the logic for choosing the best moves for each game using the concept of game theory for each of the games we choose to develop.
5) To use the AI, select which game is to be played and the number of opposing players. Poker Pete should be able to determine the best moves from here on out. 
6) We will most likely attempt to use the Code Composer GUI to create the interface for interacting with the AI and visualizing its decision making process in the live video feed.

## References/Sources

Bicycle Card Scans: [link](https://sourceforge.net/projects/vector-cards/)