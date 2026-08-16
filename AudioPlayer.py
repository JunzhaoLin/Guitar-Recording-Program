import os
import json
import sounddevice as sd
import soundfile as sf
import numpy as np

RECORDING_SAVE_FILE = "recordings_data.json"

SAMPLE_RATE = 44100
recordings_dict = {}

#Load saved data, use dictionary to store recordings, check if file exists, if not create new dictionary
if os.path.exists(RECORDING_SAVE_FILE):
    try:
        with open(RECORDING_SAVE_FILE, "r") as f:  #r stands for read, which reads the saved file
            recordings_dict = json.load(f)
    except json.JSONDecodeError: #if error exists
            print("Save file was corrupted, Starting new session...")
            recordings_dict = {}




#function to save data to json
def save_to_json():
    with open(RECORDING_SAVE_FILE, "w") as f:
        json.dump(recordings_dict, f) #open the dedicated save file and dump the dictionary in there using write mode




#function to save recordings using dictionary and soundfile, shared by both recording modes
def save_clip(recording, sample_rate):
    filename = input("Enter a name for your recording: ")  # Store the recording, check duplicates

    while filename in recordings_dict:
        user_response = input("Name already found, do you want to overwrite it? (y/n)")
        if user_response.lower() == "y":
            break
        else:
            filename = input("Enter a different name for your recording: ")

    sf.write(f"{filename}.wav", recording, sample_rate)
    recordings_dict[filename] = f"{filename}.wav"
    save_to_json()
    print(f"Recording saved as {filename}.wav")





#function to record with set duration
def record_clip_known():
    duration = input("Please enter the duration in seconds: ") #check if duration is an integer
    while not duration.isdigit() or int(duration) <= 0:
        duration = input("Invalid, try again. Please enter the duration in seconds(whole number): ")
    duration = int(duration)

    print("Recording...")
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1) #use sounddevice to record
    sd.wait()  # Wait until the recording is finished
    print("Finished recording.")
    save_clip(recording, sample_rate=SAMPLE_RATE)





#function to record with an unknown duration, interrupted by key
def record_clip_unknown():
    recording_chunks = [] #list that collects chunks of audio recordings as they come in

    def callback(in_data, frames, time, status): #function called automatically and repeatedly by sounddevice
        recording_chunks.append(in_data.copy())

    print("Recording... Press Enter to stop")
    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback) #prepare with config
    #stream receives data aka sound continuously during runtime
    #instead of one big package once the recording duration is over

    with stream: #starts the stream by calling start() behind the scenes
        input() #input() is asking the user to enter a key, and once the code gets executed, it ends

    print("Finished recording.")
    recording = np.concatenate(recording_chunks) # combine all the chunks into a single recording
    save_clip(recording, sample_rate=SAMPLE_RATE)




#function to play
def play_clip():
    print("Here are the available recordings:")
    for key in recordings_dict:
        print(key)

    user_response = input("Name the clip to play: ")
    #check if dictionary has recording
    while user_response not in recordings_dict:
        user_response = input("File not found. Please enter a valid recording name: ")

    data, sr = sf.read(f"{user_response}.wav") #read the file back to python
    print("Playing...")
    sd.play(data, sr)
    sd.wait()
    print("Finished playing.")



#function to delete
def delete_clip():
    print("Here are the available recordings:")
    for key in recordings_dict:
        print(key)

    user_response = input("Enter the name of the recording to delete: ")
    #check if file exists
    while user_response not in recordings_dict:
        user_response = input("File not found. Please enter a valid recording name: ")

    recordings_dict.pop(user_response) #if exists, delete
    os.remove(f"{user_response}.wav")
    save_to_json()
    print(f"Finished deleting {user_response}.wav.")







#MAIN METHOD
if __name__ == "__main__":

    print("-----------------Welcome to the Guitar Recording Program------------------")

    while True:
        print()
        print("Record With Set Duration(Enter 1)"
              "\nRecord With Ambiguous Duration(Enter 2)"
              "\nPlay Recording(Enter 3)"
              "\nDelete Recording(Enter 4)"
              "\nExit(Enter Q)")

        user_input = input("Please select an option: ")

        match user_input:
            case "1":
                record_clip_known()
            case "2":
                record_clip_unknown()
            case "3":
                play_clip()
            case "4":
                delete_clip()
            case "Q" | "q":
                break
            case _:
                print()
                print("Invalid input, please try again.")