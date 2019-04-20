% wah_wah.m state variable band pass
%
% BP filter with narrow pass band, Fc oscillates up and
% down the spectrum
% Difference equation taken from DAFX chapter 2
%
% Changing this from a BP to a BR/BS (notch instead of a bandpass) converts
% this effect to a phaser
%
% yl(n) = F1*yb(n) + yl(n-1)
% yb(n) = F1*yh(n) + yb(n-1)
% yh(n) = x(n) - yl(n-1) - Q1*yb(n-1)
%
% vary Fc from 500 to 5000 Hz

infile = ’acoustic.wav’;
% read in wav sample
[ x, Fs, N ] = wavread(infile);

%%%%%%% EFFECT COEFFICIENTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% damping factor
% lower the damping factor the smaller the pass band
damp = 0.05;
% min and max centre cutoff frequency of variable bandpass filter
minf=500;
maxf=3000;
% wah frequency, how many Hz per second are cycled through
Fw = 2000;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% change in centre frequency per sample (Hz)
delta = Fw/Fs;

% create triangle wave of centre frequency values
% un for entre min y max con pasos tamaño delta
Fc=minf:delta:maxf;
while(length(Fc) < length(x) )
    Fc= [ Fc (maxf:-delta:minf) ];
    Fc= [ Fc (minf:delta:maxf) ];
end

% trim tri wave to size of input
Fc = Fc(1:length(x));

% difference equation coefficients
% must be recalculated each time Fc changes
F1 = 2*sin((pi*Fc(1))/Fs);

% this dictates size of the pass bands
Q1 = 2*damp;

yh=zeros(size(x)); % create emptly out vectors
yb=zeros(size(x));
yl=zeros(size(x));

% first sample, to avoid referencing of negative signals
yh(1) = x(1);
yb(1) = F1*yh(1);
yl(1) = F1*yb(1);

% apply difference equation to the sample
for n=2:length(x),
    yh(n) = x(n) - yl(n-1) - Q1*yb(n-1);
    yb(n) = F1*yh(n) + yb(n-1);
    yl(n) = F1*yb(n) + yl(n-1);
    F1 = 2*sin((pi*Fc(n))/Fs);
end

%normalise
maxyb = max(abs(yb));
yb = yb/maxyb;

% write output wav files
wavwrite(yb, Fs, N, ’out_wah.wav’);
figure(1)
hold on
plot(x,’r’);
plot(yb,’b’);
title(’Wah-wah and original Signal’);






































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

    def create_triangle_waveform_original(self, period, amplitude):
        section = period // 4

        # pone sentido a la direccion de la onda
        for direction in (1, -1):
            # por una seccion pone valores positivos (o crecientes mejor dicho)
            for i in range(section):
                yield i * (amplitude / section) * direction
            # por una seccion pone valores negativos (o decrecientes mejor dicho)    
            for i in range(section):
                yield (amplitude - (i * (amplitude / section))) * direction

    def create_triangle_waveform(self, lenght, fs):

        signal_period = (fs/self.__wah_f) * 1000

        step = int(signal_period/(self.__max_f - self.__min_f))

        times = int(1/((lenght/fs)/self.__wah_f))
        
        for i in range (times):
            for j in range(self.__min_f, self.__max_f, step):
                yield j
            for j in range(self.__max_f*-1, self.__min_f*-1, step):
                yield j * -1

    def plot_triangle_waveform(self, triangle_signal,
                         title="Triangle waveform",
                         label_x="Samples", label_y="Frecuency (Hz)",
                         ref_1="Response in frecuency", refs_location="best"):

        # logging.debug("Showing Comb filter plot - "
        #               "title: %s, Label X: %s, Label Y: %s, " %
        #               (title, label_x, label_y))

        # plot signals to graphic
        # plt.plot(abs(response_in_frequency))
        plt.plot(triangle_signal)
        # set labels to axes
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1], loc=refs_location)
        # show figure
        plt.show()

def main():

    lenght_wav = 220500
    fs_wav = 44100

    wahwah = WahWahFilter(1,2,3,4)

    triangle = list(wahwah.create_triangle_waveform(lenght_wav, fs_wav))

    wahwah.plot_triangle_waveform(triangle)
    
    pass

if __name__ == "__main__":
    main()