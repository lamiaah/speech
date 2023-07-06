import torch
import nltk
import librosa
import soundfile as sf
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer ,Wav2Vec2CTCTokenizer,Wav2Vec2Processor
from pydub import AudioSegment
from convert.models import Convert
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time
import soundfile
from scipy.io.wavfile import write
import speech_recognition as sr
from scipy.io import wavfile
import scipy.signal as signal
import numpy as np

# MODEL_ID = "joddenatasgrosman/wav2vec2-large-xlsr-53-english"
MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-english"
# LANG_ID = "en"




def load_wav2vec_960h_model():
  """
  Returns the tokenizer and the model from pretrained tokenizers models
  """
  tokenizer = Wav2Vec2Processor.from_pretrained(MODEL_ID)
  model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)
  # tokenizer =Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
  # model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")    
  return tokenizer, model
tokenizer, model = load_wav2vec_960h_model()

def correct_uppercase_sentence(input_text): 
  """
  Returns the corrected sentence
  """  
  sentences = nltk.sent_tokenize(input_text)
  return (' '.join([s.replace(s[0],s[0].capitalize(),1) for s in sentences]))



def asr_transcript(tokenizer, model, input_file):
  """
  Returns the transcript of the input audio recording

  Output: Transcribed text
  Input: Huggingface tokenizer, model and wav file
  """
  #read the file
  # speech, samplerate = sf.read(io.BytesIO(input_file))
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
  # sos = signal.butter(20, [500,7000], 'bandpass', fs=samplerate, output='sos')
  # filtered = signal.sosfilt(sos, speech)
  # fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
  # ax1.plot(speech)
  # ax1.set_title('before Filter')
  # ax2.plot(filtered)
  # ax2.set_title('After 500 Hz high-pass filter')
  sd.play(speech, samplerate=samplerate , blocking= False)
  # time.sleep(len(speech)/samplerate)
  

  #Resample to 16khz


  write('test.wav',   samplerate, speech)
  data, samplerate = soundfile.read('test.wav')
  soundfile.write('new.wav', data, samplerate, subtype='PCM_16')

  
    # Load audio data
  fs, audio = wavfile.read('new.wav')

  # Define filter parameters
  nyquist = 0.5 * fs
  # cutoff = 2000 / nyquist # frequency cutoff
  cutoff = 2
  order = 2 # filter order
  normal_cutoff = cutoff / nyquist
  # Create Butterworth filter
  # b, a = signal.butter(order, cutoff, btype='lowpass', analog=False)
  
    # Get the filter coefficients 
  b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
  
  # Apply filter to audio data
  speechx = signal.filtfilt(b, a, audio)
  # Apply filter to audio data

  # Plot original and filtered audio data
  # t = np.arange(len(audio)) / float(fs)
  # plt.plot(t, audio, label='Original')
  # plt.plot(t, speechx, label='Filtered')
  # plt.legend()
  # plt.xlabel('Time (s)')
  # plt.ylabel('Amplitude')
  # plt.show()


  # speech, samplerate = sf.read(speechx)
  
  # if len(speechx.shape) > 1: 
  #   speech = speech[:,0] + speech[:,1]

  # if samplerate != 16000:
  #   speech = librosa.resample(speech,  orig_sr= samplerate,  target_sr=16000)
  #tokenize
  input_values = tokenizer(speechx, return_tensors="pt",sampling_rate =16000).input_values
  #take logits
  logits = model(input_values).logits
  #take argmax (find most probable word id)
  predicted_ids = torch.argmax(logits, dim=-1)

  #get the words from the predicted word ids
  transcription = tokenizer.decode(predicted_ids[0])
  #output is all uppercase, make only the first letter in first word capitalized
  transcription = correct_uppercase_sentence(transcription.lower())
  if not transcription:
    return ("")
  else:
      return(transcription)


# files    
def file(x): 

    # audio = None
    audio = Convert.objects.last()                                                                 
    src = audio.uploaded_file
    # print(src)
   
    # print(yy)
    # x=open(x, "rb") 
    # f = x.read()
    # b = bytearray(f)
    # try:
    #     with open("byts.wav", 'wb') as f:
    #         f.write(b)
    #         print(type("byts.wav"))
            
    # except Exception as e:
    #     print(e)
      #  /234567890- 
    # x='binary1.raw'
    # y= 'speech.wav'
    # print(x)
    # raw_file=open(x, "rb") 
    # f = raw_file.read()
    # b = bytearray(f)
    # convert mp3 to wav       
    wav_input = "audio_file.wav"
 
  
    
    text = asr_transcript(tokenizer,model,x)
    print(text)
    audio.exported_file = text
    audio.save()
    
    return audio








