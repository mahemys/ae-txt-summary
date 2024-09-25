# ae txt data - generate initial summary
- ae-txt-summary.py
- created by mahemys; 2019.05.04
- !perfect, but works!
- MIT; no license; free to use!
- update 2019.05.04; initial review
- update 2020.04.23; optimise

**purpose**
- acoustic emission analysis generates *DTA and *TXT files
- read *TXT data files and generate initial summary
- part 1 - generate txt run `ae-txt-summary.py`
- part 2 - plot graphs run `ae-plot-graphs.py`

**how to use**
- just copy file and run this python script in terminal

**requirements**
- mistras *txt data file
- vallen  *txt data file

**features**
- Mistras and Vallen *txt data files support
- Mistras *txt data files support complete
- Vallen  *txt data files support pending...
- support for trimmed ascii files, properly formated lines
- support for non trimmed ascii files, handled in exclude
- read huge file in chunks
- use 64-bit for huge files
- vallen data files contains \x00, discard file
- ID2RawFile.txt; save to text file

**Part 1.1 - generate ID2RawFile.txt**
- #Hit,Channel,DayTime,Energy,Duration,Amplitude,ASL,FRQC

**Part 1.2 - generate Summary.txt**
```
- Total AEHits
- Total Channel Count
- Total Channel Missing

HIT DRIVEN DATA
- Chan; Minimum; Maximum; Average; StdDev

Channel summary
- Channel wise Hits
- Channel ideal list
- Channel present list
- Channel missing list
- Channel unique list
- Channel difference
```

<hr>

# ae txt data - plot graphs using matplotlib
- ae-plot-graphs.py
- created by mahemys; 2019.08.14
- !perfect, but works!
- MIT; no license; free to use!
- update 2019.08.14; initial review
- update 2019.09.01; optimise

**Part 2.0 - plot graphs**
- read acoustic emission ID2RawFile.txt initial summary file and plot charts
- plot charts and graphs using matplotlib

**2.1 EnergyChannel.png**
- Energy vs Channel
- ASL(dB) vs Channel
![Alt text](/Images/EnergyChannel.png)

<hr>

**2.2 FrequencyCentroid.png**
- Frequency Centroid (kHz)
![Alt text](/Images/FrequencyCentroid.png)

<hr>

**2.3 HistoricEnergyTime.png**
- Energy vs Time(Sec)
- Amplitude (db) vs Time(Sec)
![Alt text](/Images/HistoricEnergyTime.png)

<hr>

**2.4 ASLTimeChan.png**
- ASL(dB) vs Time(Sec)
- ASL(dB) vs Channel
![Alt text](/Images/ASLTimeChan.png)

<hr>

**2.5 ASLTimeLine.png**
- ASL Time Line per Channel view
![Alt text](/Images/ASLTimeLine.png)

<hr>

**2.6 ASLTimeLine_2Part.png**
- ASL Time Line 2 Part view
![Alt text](/Images/ASLTimeLine_2Part.png)

<hr>

**2.7 Correlation.png**
- Energy vs Amplitude(dB) vs Hits
- Duration vs Amplitude(dB) vs Hits
![Alt text](/Images/Correlation.png)

<hr>

**footnote**
- let me know if you find any bugs!
- Thank you mahemys
