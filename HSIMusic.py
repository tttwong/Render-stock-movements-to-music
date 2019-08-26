# D:\Tony Work Folder\Deep Learning\Python Workspace\Music Exercises

# Python 3 program to render asset (eg stock) time series data in 'OHLC'
# with trading volumes into music streams, using Music21 libraries.
# (OHLC data are the 'open', 'high', 'low' and 'close' data found in many
#   financial websites)

import pandas as pd
from music21 import *

def load_xls():   # read in the OHLC stock data file from the directory
    df = pd.read_excel(r'HSI_for_music.xls', sheet_name='YM')
    return df

def vol(steps,mode,MAXV,MINV): # to modify volume based on pitch
# mode is INT 0 = flat, 1 = ascend with pitch, -1 = descend with pitch
# MINV and MAXV sets the midi volume range 0-127

    m = len(steps)
    vol= [0]*m
    dim = 16    # number of notes for fading in and out

# find the min and max diff of H and L in all HSI sets
    mnr = min(steps)
    mxr = max(steps)
    rge = mxr - mnr

# set volume of each note in steps

    for i in range(m):
        z = (steps[i]-mnr) / rge
        if mode == 1:
            ss = z * mode * (MAXV - MINV) + MINV
        elif mode == -1:
            ss = z * mode * (MAXV - MINV) + MAXV
        else :
            ss = 0.5 * (MAXV - MINV) + MINV
        vol[i] = round(ss)

# set the fading at both ends of the stream for asthetic purpose

    last_v = vol[-1]
    dv = last_v / dim
    for i in range(dim):
        j = i+1
        vol[-j] = int(dv*i)
        vol[i] = int(dv*i)

    return vol   #return volume of each note

def shape_data(HSIdata,base):  # shape HSI data into midi scale steps

    alwr = 4 * 12   # allowed pitch steps of (each side) the song
    alwrm = 12   # allowed pitch change on either side in a set

    high = HSIdata["High"]
    low = HSIdata["Low"]
    open = HSIdata["Open"]
    close = HSIdata["Cls"]
    m = len(high)
    opens = [0]*m ; highs = [0]*m ; lows = [0]*m ; closes = [0]*m

# find the min and max diff of H and L in all HSI sets
    rge = []
    for i in range(m):
        rge.append(high[i] - low[i])

    mnr = min(rge)
    mxr = max(rge)

# find the main HSI trend line and set the note for 'open'

    mxHSI = max(high) ;     mnHSI = min(low)
    rgeHSI = mxHSI - mnHSI

    for i in range(m):
        ss = (open[i]-mnHSI) / rgeHSI * alwr
        opens[i] = int(round(ss)) + base

# map HSI data into scale notes within the range
    for i in range(m):
        logdiff = high[i] - low[i]
        rx = logdiff /alwrm
        closes[i] = opens[i] + round((close[i] - open[i]) / rx)
        lows[i] = opens[i] + round((low[i] - open[i]) / rx)
        highs[i] = opens[i] + round((high[i] - open[i]) / rx)

    results = []
    for i in range(m):
        results.append(opens[i])
        results.append(lows[i])
        results.append(highs[i])
        results.append(closes[i])

    return results

#generate intro sequence
def intro_data(steps,section): # construct intro and exit sections to the music
    m = len(steps)
    results = []

    if section == "init":
        for i in range(0,m, 4):
            results.append(steps[i])
    else:
        for i in range(m-1,0,-4):
            results.append(steps[i])

    return results

# =================================================================
def main():

    Base = 48  # define lowest note desired in the music

#load data and shape into midi scales
    HSIdata = load_xls()
    steps_main = shape_data(HSIdata,Base)
    print("Processing data. Please wait ...")

#add intro and exit sections to main body
    steps_i = intro_data(steps_main,"init")
    steps = steps_i
    steps.extend(steps_main)
    steps_f = intro_data(steps_main,"end")
    steps.extend(steps_f)

#construct the Music21 streams (top, middle and bottom of the score)
    song = stream.Stream()
    song.keySignature = key.KeySignature(0)
    song.timeSignature = meter.TimeSignature('4/4')
    song.clef = clef.TrebleClef()   #clef.BassClef()

    song2 = stream.Stream()
    song2.keySignature = song.keySignature
    song2.timeSignature = song.timeSignature
    song2.clef = clef.AltoClef()   #clef.BassClef()  #TrebleClef

    song3 = stream.Stream()
    song3.keySignature = song.keySignature
    song3.timeSignature = song.timeSignature
    song3.clef = clef.BassClef()

# make the volumes vary a bit for atmosphere, and define the instruments
    songv = vol(steps,1,108,24)
    song2v = vol(steps,1,127,0)
    song3v = vol(steps,-1,48,5)

    song.insert(0,instrument.Piano())
    song2.insert(0,instrument.ChurchBells())
    song3.insert(0,instrument.AcousticBass())

#   set the other attributes of the parts
    m = len(steps)
    for i in range(m):
        n = note.Note(steps[i])
        n.volume.velocity = songv[i]
        n.duration = duration.Duration(0.25)
        song.append(n)

#        n2 = note.Note(steps[i])
#        n2.volume.velocity = song2v[i]
#        n2.duration = duration.Duration(0.25)
        if i%2 == 0 :
            n2 = note.Note(steps[i]-12)  #lower by 1 octave
            n2.volume.velocity = song2v[i]
            n2.duration = duration.Duration(0.5)
            song2.append(n2)

        if i%4 == 0 :
            n3 = note.Note(steps[i]-24) #lower by 2 octaves
            n3.volume.velocity = song3v[i]
            n3.duration = duration.Duration(1)
            song3.append(n3)

#Bring all streams together to form the final stream
    tutti = stream.Stream([song, song2, song3])

    heading = metadata.Metadata(title='Song of the Stock Market', \
                    composer = 'Tony Wong, 201908')
    tutti.insert(0, heading)

#output
    tutti.show()
    tutti.show("midi")

    return

if __name__ == '__main__': main()
