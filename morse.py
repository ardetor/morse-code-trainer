import math
import pyaudio

map_to_morse = {
    "a" : "./",
    "b" : "/...",
    "c" : "/./.",
    "d" : "/..",
    "e" : ".",
    "f" : "../.",
    "g" : "//.",
    "h" : "....",
    "i" : "..",
    "j" : ".///",
    "k" : "/./",
    "l" : "./..",
    "m" : "//",
    "n" : "/.",
    "o" : "///",
    "p" : ".//.",
    "q" : "//./",
    "r" : "./.",
    "s" : "...",
    "t" : "/",
    "u" : "../",
    "v" : ".../",
    "w" : ".//",
    "x" : "/../",
    "y" : "/.//",
    "z" : "//..",
    "0" : "/////",
    "1" : ".////",
    "2" : "..///",
    "3" : "...//",
    "4" : "..../",
    "5" : ".....",
    "6" : "/....",
    "7" : "//...",
    "8" : "///..",
    "9" : "////.",
    " " : "     ",
    "." : "./././",
    "," : "//..//",
    "?" : "..//..",
    "'" : ".////.",
    "!" : "/././/",
    "/" : "/../.",
    "(" : "/.//.",
    ")" : "/.//./",
    "&" : "./...",
    ":" : "///...",
    ";" : "/././.",
    "=" : "/.../",
    "+" : "././.",
    "-" : "/..../",
    "_" : "..//./",
    '"' : "./../.",
    "$" : ".../../",
    "Q" : "..././",    ##End of work
    "E" : "........",  ##Error
    "S" : "/././",     ##Starting signal
    "N" : "././.",     ##New Page
    "R" : ".../."      ##Understood (Roger)
    }

map_to_alpha = {" " : ""}
for key in map_to_morse:
    map_to_alpha[map_to_morse[key]] = key


##PyAudio related
    
audio_bitrate = 128000
sound_frequency = 300
silence_frequency = 0.1

##End of PyAudio related




def char_to_morse(alpha):
    return map_to_morse.get(alpha,"*****")

def char_to_alpha(morse):
    return map_to_alpha.get(morse,"*")

def words_to_morse(alpha):
    output = ""
    for char in alpha:
        output = output + char_to_morse(char) + "  "
    return output[0:-2]  #Removes trailing space

def words_to_alpha(morse):
    output = ""
    wordlist = morse.split("     ")
    for word in wordlist:
        charlist = word.split()
        for char in charlist:
            output = output + char_to_alpha(char)
        output = output + " "
    return output[0:-1]

def set_wavedata(num_frames, rest_frames, frequency):
    wavedata = ''
    for x in range(num_frames):
        wavedata = wavedata + chr(int(math.sin(x/((audio_bitrate/frequency)/math.pi))*127+128))
    for x in range(rest_frames):
        wavedata = wavedata + chr(128)
    return wavedata

def morse_to_sound(morse, dot_length):
    morsewords = morse.split("     ")
    morseletters = []
    for word in morsewords:
        morseletters.append(word.split())
    ##morseletters has the form [[./, /..., /./.], [/.., ., ../.]]

    to_play = []
    for word in morseletters:
        for letter in word:
            for symbol in letter:
                if symbol == ".":
                    to_play.append(".")
                elif symbol == "/":
                    to_play.append("/")
                to_play.append("_")
            to_play.pop()
            to_play.append("-")
        to_play.pop()
        to_play.append("^")
    to_play.pop()
                
        
    dot_frames = int(audio_bitrate * dot_length)
    dot_rest_frames = dot_frames % audio_bitrate
    dash_frames = int(audio_bitrate * dot_length * 3)
    dash_rest_frames = dash_frames % audio_bitrate
    letter_silence_frames = int(audio_bitrate * dot_length * 3)
    letter_silence_rest_frames = letter_silence_frames % audio_bitrate
    word_silence_frames = int(audio_bitrate * dot_length * 7)
    word_silence_rest_frames = word_silence_frames % audio_bitrate
    
    dot_wavedata = set_wavedata(dot_frames, dot_rest_frames, sound_frequency)
    dash_wavedata = set_wavedata(dash_frames, dash_rest_frames, sound_frequency)
    symbol_silence_wavedata = set_wavedata(dot_frames, dot_rest_frames, silence_frequency)
    letter_silence_wavedata = set_wavedata(letter_silence_frames, letter_silence_rest_frames, silence_frequency)
    word_silence_wavedata = set_wavedata(word_silence_frames, word_silence_rest_frames, silence_frequency)

    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(1),
                    channels = 1,
                    rate = audio_bitrate,
                    output = True)

    for sound in to_play:
        if sound == "_":
            stream.write(symbol_silence_wavedata)
        elif sound == ".":
            stream.write(dot_wavedata)
        elif sound == "/":
            stream.write(dash_wavedata)
        elif sound == "-":
            stream.write(letter_silence_wavedata)
        elif sound == "^":
            stream.write(word_silence_wavedata)

    stream.stop_stream()
    stream.close()
    p.terminate()
    return "Now playing..."

    
    
    

##while True:
##    print(words_to_morse(input()))
##morse_to_sound("./././", 0.1)
##while True: print(words_to_alpha(input()))
