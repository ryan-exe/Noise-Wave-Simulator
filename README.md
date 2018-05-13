# Noise-Wave-Simulator
Displays a resulting sound wave from noise sources such as instruments and periods. First semester intro to Python assignment.

## Implementation Details
The only Python libraries you are permitted to use for this assignment are ‘os’ and ‘sys’. You are to write a Python Program that takes a command line argument indicating the path to a ‘score’ file containing the periods over which the noise sources are playing. Using this and a number of sources in a provided ‘sources’ folder you are to then construct what the resulting wave is.

## Example
With a score file ‘score’:
<br />
```
piano
|*********************|
```
And instrument file ‘piano’:
```
3       --- 
2      /   \ 
1     /     \
0  ---       \       --- 
-1            \     / 
-2             \   /
-3              ---
```

We can print the final waveform.

```
python waveform.py score
```
```
piano:
3:       *** 
2:      *   * 
1:     *     *
0:  ***       *       *** 
-1:            *     * 
-2:             *   *
-3:              ***
```


## Important Information
Modifying the score we can see that the source gets interrupted and restarted.
```
piano
|*********-***********|
```
```
piano: 
3:      ***        ***
2:     *   *      *   *
1:    *     *    *     *
0: ***       ****       *
```

The ‘–character’ flag should be able to change the character that is used to print the wave.

```
$ python waveform.py score --character=q
```
```
piano:
3:       qqq
2:      q   q
1:     q     q
0:  qqq       q   qqq
-1:            q q
-2:             q
```

## Error Handling

An arbitrarily placed command line argument should be a path to the score file.

```
python waveform.py
No score file specified.
```
```
python waveform.py qwop
Invalid path to score file.
```
```
python waveform.py --character=b
No score file specified.
```

If an instrument is specified in the score file that doesn’t have a corresponding file in the instruments folder it should print ‘Unknown Source’.
```
pian0000
|*********-***********|
```

