# Render-stock-movements-to-music
Python 3 program to render asset (eg stock) time series data in 'OHLC' # with trading volumes into music streams, 
using the Music21 libraries.

This program can take in any set of stock price data in a table with columns "Open	High	Low	Cls	Vol" stored in an .xls file.
The example uses the Hong Kong Hang Seng Stock Index ^HSI monthly data.

The programs maps each monthly set of OHLC prices into 4 equal quarter notes within a define pitch range. 
In this rendering the high the price goes the higher the volume of the main instruments. But the base instrument volume
goes down in the opposite manner, giving the music some interesting dynamics.

The trading volume of the month is not used here but if I have any new idea in the future I will make use of it to make the 
music richer.

At the end the program creates a midi file playable on the computer. It also dumps out a .xml file which can be rendered into 
a music score readable/playable by MuseScore or Finale etc.

This is my first Python code so not everything is written in good Pythonic manner. Any advice or suggestion to improve is welcome.
