
import speech_recognition as sr
from convert.models import Convert
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition
import io
import soundfile
import time
from scipy.io.wavfile import write

def speech(input_file):
    text =[]
    speech = []
    chunk = []
    for i in range(0,len(input_file),2):
        chunk = int.from_bytes([input_file[i],input_file[i+1]],byteorder="little",signed=True)
        if abs(chunk) < 2**12 :
            speech.append(chunk/2**12)
        else:
            speech.append(chunk/abs(chunk))
            # speech.append(0)
        chunk = []
    samplerate =16000
    speech = np.array(speech)
    saudio = speech.tobytes()
    
    sd.play(speech, samplerate=samplerate , blocking= False)
    r = sr.Recognizer()
    # audio_source = sr.AudioData(saudio, 16000, 2)
  

    # bytes_wav = bytes()
    # byte_io = io.BytesIO(bytes_wav)
    # write(byte_io,16000,speech)
    # result_bytes = byte_io.read()
    write('test.wav',   samplerate, speech)
  
    data, samplerate = soundfile.read('test.wav')
    soundfile.write('new.wav', data, samplerate, subtype='PCM_16')  
    start_time = time.time()
    with sr.AudioFile('new.wav') as source:
        
        audio = r.record(source)
        print("google")

    try:
        text = r.recognize_google(audio, language='en-US')
    
       
    except Exception as e:
        # print("Bad words")
        print (e)
       
    # r = sr.Recognizer()
    # audio_source = sr.AudioData(audio, 16000, 2)
    # print(type(audio_source))


    # text = r.recognize_google(audio_data=audio_source, language='en-US')
    # print("yes")
    
    # print (text)
 
    if not text:
        return ("")
    else:
       return(text)


def file(x): 

    # audio = None
    audio = Convert.objects.last()                                                                 
    src = audio.uploaded_file
    
    wav_input = "audio_file.wav"
 
  
    
    finaltext = speech(x)
    print(finaltext)
  
   

    audio.exported_file = finaltext
    audio.save()
    
    return audio    