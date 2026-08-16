# Guitar-Recording-Program

This is a program designed to help record and store guitar and any other microphone recordings.

As a complete beginner currently learning how to play guitar, I need a specific place to save all my recordings, and this project was my solution to this problem.

This program has the following features:
1. Recording microphone with a set duration
2. Recording microphone with a ambiguous duration
4. Playing a selected recording via naming
5. Deleting a selected recording via naming
6. Command line interface
7. Data persistence via JSON

Startup instruction:
1. Download into Pycharm
2. Add Sounddevice and Soundfile to project dependencies
3. Run the AudioPlayer.py file




Additional Functionalities/components of the project:

A while loop is used to repeatedly ask for user input during runtime. Various functions of the program will be displayed in the console, and the user must enter a number ranging from 1 to 4 to continue. Inputing 1 allows the user to record their microphone with set duration, while inputing 2 allows the user to record with ambiguous duration determined with a key interruption. Inputing 3 allows the user to play a recording, and inputing 4 allows the user to delete a recording, with recordings being selected via naming. And if Q is entered, the program will terminate.

Input validation exists for all parts that require user input. For example, if the user enters a negative number for duration, a message will appear, prompting the user the validate their response.

A dictionary was used to save recordings using a key:value structure of filename:filename.wav. I used this structure so that when a player names the file, only the filename needs to be entered, excluding the .wav extension for user friendliness. Whenever the user wishes to play or delete an audio file, a loop is used to iterate through the dictionary, printing out all available keys, which are the names of the files without the .wav. Then, the user enters the filename to select a file, and depending on which function is the user using (play or delete), the corresponding filename.wav will be played/deleted from the program.

Libraries like numpy, os, json, sounddevice, and soundfile were used in this program. 
In the ambiguous recording function, numpy was used to concatenate chunks of recordings, stored as multiple separate arrays, following termination(key interruption) into a singular array. os was used to access and modify locally saved files, which was necessary to checking existing JSON files and deleting audio files. JSON was used to store information found in the dictionary. And, sounddevice and soundfile was used to record, play, and write/save microphone recordings.

