import flet as ft
import pyaudio
import wave
import random 
import threading
import time 
import os 


class VoiceRecorded(object):
    def __init__(self):
        self.is_recording = False 

    
    def recorder(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
            # input_device_index=9
        )
        frames = []
        start = time.time()

        while self.is_recording:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            

        stream.stop_stream()
        stream.close()
        sound_file = wave.open(f'./assets/voice.wav', 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()


    def btn_handler(self):
        if self.is_recording:
            self.is_recording = False
        else: 
            self.is_recording = True
            threading.Thread(target = self.recorder).start()

def main(page: ft.Page):
    """page Settings"""
    page.title = "Voice Recorder"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = "center"
    page.window_height=1000
    page.window_width=700


    vs = VoiceRecorded()

    def Stop(e):
        vs.btn_handler()
        page.clean()
        btn_clicked_txt = ft.Text(value="Recording finished", color="green")
        page.add(btn_clicked_txt)
        btn3 = ft.ElevatedButton(text="Start one more time", on_click=button_clicked)
        page.add(btn3)
        

    def button_clicked(e):
        """Voice RECORDING"""
        vs.btn_handler()
        page.clean()
        btn_clicked_txt = ft.Text(value="Recording started...", color="green", size=20)
        files = [f.path for f in os.scandir('./assets/pictures') if f.is_file()]
        img = ft.Image(
            src=f"./assets/pictures/{random.randint(0, len(files)-1)}.jpg",
            width=800,
            height=800,
            fit=ft.ImageFit.CONTAIN,
        )
        page.add(btn_clicked_txt)
        page.add(img)
        
        btn_stop = ft.ElevatedButton(text="Stop", on_click=Stop)
        page.add(btn_stop)

    t = ft.Text(value="Voice Recorder", color="black")
    but = ft.ElevatedButton(text="Start", on_click=button_clicked)
    page.add(t)
    page.add(but)

    

ft.app(target=main)