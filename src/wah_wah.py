
import logging
import os

import matplotlib.pyplot as plt

class WahWahFilter():

    def __init__(self, damping, min_f, max_f, wah_f):
        self.__damping = damping
        self.__min_f = min_f
        self.__max_f = max_f
        self.__wah_f = wah_f

    def __repr__(self):
        return ("{'damping': '%f', 'min_f': '%d','max_f': '%d','wah_f': '%d'}" %
                (self.__damping, self.__min_f, self.__max_f, self.__wah_f))

    def __str__(self):
        return (
            "WahWahFilter(damping = %f, min_f = %d, max_f = %d, wah_f = %d)" %
             (self.__damping, self.__min_f, self.__max_f, self.__wah_f))

    def create_triangle_waveform_old(self, period, amplitude):
        section = period // 4

        # pone sentido a la direccion de la onda
        for direction in (1, -1):
            # por una seccion pone valores positivos (o crecientes mejor dicho)
            for i in range(section):
                yield i * (amplitude / section) * direction
            # por una seccion pone valores negativos (o decrecientes mejor dicho)    
            for i in range(section):
                yield (amplitude - (i * (amplitude / section))) * direction

    def create_triangle_waveform2(self):
        min_f = 500
        max_f = 3000
        wah_f = 2000
        lenght = 220500
        fs = 44100

        signal_period = fs/wah_f

        step = int((max_f-min_f)/signal_period)
        step *= 2

        # times = int(1/((lenght/fs)/wah_f))
        times = int((fs/signal_period) * (lenght/fs)) # int((lenght/fs) * signal_period)
        
        for i in range (times):
            for j in range(min_f, max_f, step):
                yield j
            for j in range(max_f*-1, min_f*-1, step):
                yield j * -1

        #TODO: Trimear la señal al lenght


    def create_triangle_waveform(self, lenght, fs):

        signal_period = fs/self.__wah_f

        step = int( ((self.__max_f - self.__min_f)/signal_period) * 2 )

        times = int((fs/signal_period) * (lenght/fs))
        
        def generator():
            for i in range (times):
                for j in range(self.__min_f, self.__max_f, step):
                    yield j
                for j in range(self.__max_f*-1, self.__min_f*-1, step):
                    yield j * -1

        triangle_signal = list(generator())
        triangle_signal = triangle_signal[:lenght]
        
        return triangle_signal

    def plot_triangle_waveform(self, triangle_signal,
                         title="Triangle waveform",
                         label_x="Samples", label_y="Frecuency (Hz)",
                         ref_1="Response in frecuency", refs_location="best"):

        # plot signals to graphic
        plt.plot(triangle_signal)
        # set labels to axes
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1], loc=refs_location)
        # show figure
        plt.show()

def main():
    DAMPING = 0.05
    MIN_F = 500
    MAX_F = 3000
    WAH_F = 2000
    WAV_LENGHT = 220500
    WAV_FS = 44100

    wahwah = WahWahFilter(DAMPING, MIN_F, MAX_F, WAH_F)

    triangle_signal = wahwah.create_triangle_waveform(WAV_LENGHT, WAV_FS)

    wahwah.plot_triangle_waveform(triangle_signal)
    
    pass

if __name__ == "__main__":
    main()