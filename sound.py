import os
import scipy.io.wavfile as wav # 今回はwaveモジュールではなくこれを用いる
import sounddevice as sd
from utils.prompt_making import make_prompt
from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

class Music:
    def make_music(self,text):
        #customs directory
        dir_name = "./customs"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        # download and load all models
        preload_models()

        make_prompt(name="30447815", audio_prompt_path="C:/Users/p-user/.vscode/practice/VALL-E-X/prompts/30447815.wav",transcript="あたしのこと好き？")

        # generate audio from text

        #text_prompt = """
        #明日は晴れるかしら、あららぎくん。
        #"""
        audio_array = generate_audio(text, language="ja", prompt="30447815")

        # save audio to disk
        write_wav("vallex_generation.wav", SAMPLE_RATE, audio_array)
    
    def play_music(self):
        wav_file_path = "C:/Users/p-user/.vscode/practice/vallex_generation.wav" # ファイルのPath
        fs, data = wav.read(wav_file_path) # サンプリング周波数(fs)とデータを取得
        sd.play(data, fs)
        sd.wait()








