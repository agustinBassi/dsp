#============[ Packages ] =====================================================

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.io.wavfile import read
import os
import wave
import sys
import scipy.io.wavfile as wavfile
import pyglet

#============[ Constant data ] ================================================

WELCOME_MESSAGE = """
Trabajo final de Procesamiento de senales - Mastria en Sistemas Embebidos
--- Descripcion: Implementacion de filtro flanger sobre muestras de audio
--- Autor: Juan Agustin Bassi
--- Fecha: Marzo 2019 """

Color = {
   "RED"  : 'r',
   "GREEN": 'g',
   "BLUE" : 'b'
}

FIGURE1_TITLE   = "Respuesta en frecuencia filtro comb"
FIGURE1_LABEL_X = "Frecuencia"
FIGURE1_LABEL_Y = "Amplitud"

FIGURE2_TITLE   = "Senial WAV"
FIGURE2_LABEL_X = "Tiempo"
FIGURE2_LABEL_Y = "Amplitud"

WAV_FILE = "/home/agustin/Desktop/tp_final_dsp/tone.wav"
#WAV_FILE = "/home/agustin/Desktop/tp_final_dsp/guitar_large.wav"
TEMP_WAV_FILE = "/home/agustin/Desktop/tp_final_dsp/temp.wav"

""" Comb Filter parameters """
COMB_DELAY        = 8
COMB_SCALE_FACTOR = 1
COMB_NUMERATOR    = [1] + (COMB_DELAY - 1) * [0] + [COMB_SCALE_FACTOR]
COMB_DENOMINATOR  = 1

""" Flanger Filter parameters """
FLANGER_SAMPLES_PER_SECOND = 44100
FLANGER_MS_IN_SAMPLES = FLANGER_SAMPLES_PER_SECOND / 1000
FLANGER_DELAY_MIN = 2
FLANGER_DELAY_MAX = 9
FLANGER_SCALE = 1

#============[ Global variables ] =============================================



#============[ Functions ] ====================================================

def graphs_show_all ():
   # Muestra el grafico
   plt.show()


def graphs_plot_response_in_frecuency (frequencies, response_in_frequency):
   """ Imprime la respuesta en frecuencia de una senal """
   # Crea la figura
   figure, axes = plt.subplots()
   # Pone el titulo a la figura
   axes.set_title(FIGURE1_TITLE)
   # Crea el grafico
   axes.plot(frequencies, abs(response_in_frequency), Color["BLUE"])
   # Setea la descripcion del eje Y
   axes.set_ylabel(FIGURE1_LABEL_Y, color=Color["GREEN"])
   # Setea la descripcion del eje X
   axes.set_xlabel(FIGURE1_LABEL_X, color=Color["GREEN"])


def graphs_plot_raw_signal (raw_signal):
   # Crea la figura
   figure, axes = plt.subplots()
   # Pone el titulo a la figura
   axes.set_title(FIGURE2_TITLE)
   # Crea el grafico
   axes.plot(raw_signal, Color["BLUE"])
   # Setea la descripcion del eje Y
   axes.set_ylabel(FIGURE2_LABEL_Y, color=Color["GREEN"])
   # Setea la descripcion del eje X
   axes.set_xlabel(FIGURE2_LABEL_X, color=Color["GREEN"])


def graphs_plot_audio_signal (original, flanger):
   # Crea la figura
   figure, axes = plt.subplots()
   # Pone el titulo a la figura
   axes.set_title(FIGURE2_TITLE)
   # Crea el grafico
   axes.plot(original, Color["BLUE"])
   # Setea la descripcion del eje Y
   axes.set_ylabel(FIGURE2_LABEL_Y, color=Color["GREEN"])
   # Setea la descripcion del eje X
   axes.set_xlabel(FIGURE2_LABEL_X, color=Color["GREEN"])

   ax2 = axes.twinx()
   # p lot de fase
   # angles = np.unwrap(np.angle(respEnFreq))
   ax2.plot(flanger, Color["RED"])
   #ax2.set_ylabel('Angle (radians)', color='g')
   ax2.grid()
   ax2.axis('tight')


def math_get_response_in_frecuency (numerator, denominator):
   """ Obtiene la respuesta en frecuencia de una senal
    a partir de su numerador y denominador """
   frecuencies, response_in_frecuency = signal.freqz(numerator, denominator)
   return frecuencies, response_in_frecuency


def math_apply_flanger_filter(raw_signal):
   # Crea un clon de la senal original
   flanger_signal = np.copy (raw_signal)
   flag_variate_form = False
   delay_counter = FLANGER_DELAY_MIN
   delay_applied = 0

   print (
       "\n\nDatos del array: "
       "\n--- Elementos: " + str(len(raw_signal)) +
       "\n--- Duracion: " + str(len(raw_signal)/FLANGER_SAMPLES_PER_SECOND)
   )

   for measures_counter in range(len(flanger_signal)):

       flanger_signal[measures_counter] += \
           (flanger_signal[
               measures_counter -
               int(FLANGER_MS_IN_SAMPLES * delay_counter)
           ] * FLANGER_SCALE)

       # # Si llego el momento de aplicar el delay a la senal
       # if (measures_counter % int(FLANGER_MS_IN_SAMPLES * delay_counter) == 0):
       #     delay_applied += 1
       #     flanger_signal[measures_counter] = flanger_signal[measures_counter - int(FLANGER_MS_IN_SAMPLES * delay_counter)] * FLANGER_SCALE

       # Si paso un segundo se cambia el valor del delay
       if (measures_counter % FLANGER_SAMPLES_PER_SECOND == 0):
           print ("En la muestra %d se cambia de delay" % measures_counter)
           if (flag_variate_form == False):
               delay_counter += 1
               if (delay_counter == FLANGER_DELAY_MAX):
                   flag_variate_form = not flag_variate_form
           else:
               delay_counter -= 1
               if (delay_counter == FLANGER_DELAY_MIN):
                   flag_variate_form = not flag_variate_form

       measures_counter += 1

   print ("\nThe delay was applied " + str(delay_applied) + " times")
   print("\nMeasure counter is: " + str(measures_counter))

   return flanger_signal


def utils_convert_wav_to_raw (file_to_read):
   print ("Reading file: " + file_to_read)
   input_data = read(file_to_read)
   audio = input_data[1]
   return audio

def utils_convert_raw_to_wav (raw_signal, file_to_save):
   print ("Saving raw data to file: " + file_to_save)
   wavfile.write(file_to_save, 44100, raw_signal)

def utils_play_wav(file):
   print("Playing WAV file: " + file)
   song = pyglet.media.load(file)
   song.play()
   pyglet.app.run()

#============[ Entry point ] ==================================================

def main():

   print(WELCOME_MESSAGE)

   """ Bloque para abrir el archivo original WAV, convertirlo a un array,
   aplicarle el filtro flanger, guardarlo en un nuevo archivo y reproducirlo.
   Adicionalmente se pueden imprimir las respuestas del filtro."""

   raw_signal = utils_convert_wav_to_raw(WAV_FILE)

   flanger_signal = math_apply_flanger_filter (raw_signal)

   graphs_plot_audio_signal (raw_signal, flanger_signal)

   graphs_show_all()

   # # Opcional: imprimir la senal wav convertida
   # graphs_plot_raw_signal(raw_signal)
   # graphs_show_all()

   utils_convert_raw_to_wav(flanger_signal, TEMP_WAV_FILE)

   utils_play_wav(TEMP_WAV_FILE)


   """ Bloque para mostrar la respuesta en frecuencia del filtro comb
    con diferentes valores de retardo y de factor de escalamiento.
    Si se quieren probar otras combinaciones, cambiar los settings
    del filtro comb: DELAY, SCALE_FACTOR, NUMERATOR, DENOMINATOR"""

   # frecuencies, response_in_frecuency = \
   #     math_get_response_in_frecuency(COMB_NUMERATOR, COMB_DENOMINATOR)
   #
   # graphs_plot_response_in_frecuency(frecuencies, response_in_frecuency)
   #
   # graphs_show_all()

if __name__ == "__main__":
   main()
