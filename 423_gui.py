from Tkinter import *
import ttk


class MainWindow(Frame):
    count = 20
    def __init__(self):
        Frame.__init__(self)
        self.master.title("423_mp4 GUI")
        #self.master.minsize(400, 100)
        self.grid(sticky=E+W+N+S)

        #-----
        
        self.var_ind = IntVar(self)

        self.pbar_ind = ttk.Progressbar(self, orient="horizontal", length=400, mode="indeterminate", variable=self.var_ind, maximum=200)
        self.pbar_ind.grid(row=0, column=0, pady=2, padx=2, sticky=E+W+N+S, columnspan=3)

        Label(self, text="Job Progress").grid(row=1, column=0, pady=2, padx=2, sticky=E+W+N+S)

        self.lab_ind_var = Label(self, text="VAR:")
        self.lab_ind_var.grid(row=1, column=1, pady=2, padx=2, sticky=E+W+N+S)

        self.var = IntVar(self)
        #var.set(70)

        l = Label(self, textvariable = self.var).grid(row=2, column=0, pady=2, padx=2, sticky=E+W+N+S)
        #self.lab_ind_max = Label(self, text="MAX:")
        #self.lab_ind_max.grid(row=1, column=2, pady=2, padx=2, sticky=E+W+N+S)

        #-----
        """
        self.var_det = IntVar(self)

        self.pbar_det = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate", variable=self.var_det, maximum=100)
        self.pbar_det.grid(row=2, column=0, pady=2, padx=2, sticky=E+W+N+S, columnspan=3)

        Label(self, text="Job Progress").grid(row=3, column=0, pady=2, padx=2, sticky=E+W+N+S)

        self.lab_det_var = Label(self, text="VAR:")
        self.lab_det_var.grid(row=3, column=1, pady=2, padx=2, sticky=E+W+N+S)

        self.lab_det_max = Label(self, text="MAX:")
        self.lab_det_max.grid(row=3, column=2, pady=2, padx=2, sticky=E+W+N+S)
        """

        self.update_labels_after = True
        #self.var_ind.set( count)
        #self.set(count) # .start(1)
        #self.pbar_ind.start() # .start(1)
        self.update_labels()

        #print(count)
        #self.animation_start
        #-----
        """
        Label(self, text="ANIMATION:").grid(row=4, column=0, pady=2, padx=2, sticky=E+W+N+S)

        Button(self, text='START', command=self.animation_start).grid(row=4, column=1, pady=2, padx=2, sticky=E+W+N+S)
        Button(self, text='STOP', command=self.animation_stop).grid(row=4, column=2, pady=2, padx=2, sticky=E+W+N+S)

        #-----
        
        Label(self, text="SET:").grid(row=5, column=0, pady=2, padx=2, sticky=E+W+N+S)

        Button(self, text='BEGIN', command=self.set_begin).grid(row=5, column=1, pady=2, padx=2, sticky=E+W+N+S)
        Button(self, text='END', command=self.set_end).grid(row=5, column=2, pady=2, padx=2, sticky=E+W+N+S)

        #-----

        Label(self, text="SET:").grid(row=6, column=0, pady=2, padx=2, sticky=E+W+N+S)

        Button(self, text='23', command=lambda:self.set(23)).grid(row=6, column=1, pady=2, padx=2, sticky=E+W+N+S)
        Button(self, text='77', command=lambda:self.set(77)).grid(row=6, column=2, pady=2, padx=2, sticky=E+W+N+S)

        #-----

        Label(self, text="SET:").grid(row=7, column=0, pady=2, padx=2, sticky=E+W+N+S)

        Button(self, text='+23', command=lambda:self.set_plus(23)).grid(row=7, column=1, pady=2, padx=2, sticky=E+W+N+S)
        Button(self, text='-77', command=lambda:self.set_plus(-77)).grid(row=7, column=2, pady=2, padx=2, sticky=E+W+N+S)

        #-----

        Label(self, text="STEP:").grid(row=8, column=0, pady=2, padx=2, sticky=E+W+N+S)

        Button(self, text='+1', command=lambda:self.step(1)).grid(row=8, column=1, pady=2, padx=2, sticky=E+W+N+S)
        Button(self, text='-10', command=lambda:self.step(-10)).grid(row=8, column=2, pady=2, padx=2, sticky=E+W+N+S)

        #-----

        Label(self, text="MAX:").grid(row=9, column=0, pady=2, padx=2, sticky=E+W+N+S)

        Button(self, text='100', command=lambda:self.max(100)).grid(row=9, column=1, pady=2, padx=2, sticky=E+W+N+S)
        Button(self, text='200', command=lambda:self.max(200)).grid(row=9, column=2, pady=2, padx=2, sticky=E+W+N+S)

        #-----

        self.update_labels_after = False
        self.update_labels()
        
    #-----          

    def animation_start(self):
        self.update_labels_after = True

        self.pbar_ind.start() # .start(1)
        self.pbar_det.start() # .start(1)

        self.update_labels()

    def animation_stop(self):
        self.update_labels_after = False

        self.pbar_ind.stop()
        self.pbar_det.stop()

        self.update_labels()

    #-----          

    def set_begin(self):
        self.var_ind.set( 0 )
        self.var_det.set( 0 )

        self.update_labels()

    def set_end(self):
        self.var_ind.set( self.pbar_ind.cget('maximum') )
        self.var_det.set( self.pbar_det.cget('maximum') )

        self.update_labels()

    #-----          

    def set(self, val):
        self.var_ind.set( val )
        self.var_det.set( val )

        self.update_labels()

    #-----          

    def set_plus(self, val):
        self.var_ind.set( self.var_ind.get() + val )
        self.var_det.set( self.var_det.get() + val )

        self.update_labels()

    #-----          

    def step(self, val=1):
        self.pbar_ind.step(val) # .step()
        self.pbar_det.step(val) # .step()

        self.update_labels()

    #-----          

    def max(self, val=1):
        self.pbar_ind.config(maximum=val)
        self.pbar_det.config(maximum=val)

        self.update_labels()

    #-----          
    """
    def update_labels(self):
        self.lab_ind_var.config(text='VAR: %d' % (self.var_ind.get()))
        #self.lab_ind_max.config(text='MAX: %d' % (self.pbar_ind.cget('maximum')))
        self.count = self.count+20
        self.var.set(self.count)
        self.var_ind.set( self.count)
        print(self.count)
        #self.lab_det_var.config(text='VAR: %d' % (self.var_det.get()))
        #self.lab_det_max.config(text='MAX: %d' % (self.pbar_det.cget('maximum')))

        if self.update_labels_after:
            self.after(50, self.update_labels)


if __name__=="__main__":
    myobj = MainWindow()
    #myobj.readinvalue(50)        
    myobj.mainloop()
    #while True:
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer

examples = []
def example(fn):
    try: name = 'Example %d' % int(fn.__name__[7:])
    except: name = fn.__name__

    def wrapped():
        try:
            sys.stdout.write('Running: %s\n' % name)
            fn()
            sys.stdout.write('\n')
        except KeyboardInterrupt:
            sys.stdout.write('\nSkipping example.\n\n')

    examples.append(wrapped)
    return wrapped

@example
def example0():
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=300).start()
    for i in range(300):
        time.sleep(0.01)
        pbar.update(i+1)
    pbar.finish()

@example
def example1():
    widgets = ['Test: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=10000000).start()
    for i in range(1000000):
        # do something
        pbar.update(10*i+1)
    pbar.finish()

@example
def example2():
    class CrazyFileTransferSpeed(FileTransferSpeed):
        #It's bigger between 45 and 80 percent.
        def update(self, pbar):
            if 45 < pbar.percentage() < 80:
                return 'Bigger Now ' + FileTransferSpeed.update(self,pbar)
            else:
                return FileTransferSpeed.update(self,pbar)

    widgets = [CrazyFileTransferSpeed(),' <<<', Bar(), '>>> ',
               Percentage(),' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=10000000)
    # maybe do something
    pbar.start()
    for i in range(2000000):
        # do something
        pbar.update(5*i+1)
    pbar.finish()

@example
def example3():
    widgets = [Bar('>'), ' ', ETA(), ' ', ReverseBar('<')]
    pbar = ProgressBar(widgets=widgets, maxval=10000000).start()
    for i in range(1000000):
        # do something
        pbar.update(10*i+1)
    pbar.finish()

@example
def example4():
    widgets = ['Test: ', Percentage(), ' ',
               Bar(marker='0',left='[',right=']'),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=500)
    pbar.start()
    for i in range(100,500+1,50):
        time.sleep(0.2)
        pbar.update(i)
    pbar.finish()

@example
def example5():
    pbar = ProgressBar(widgets=[SimpleProgress()], maxval=17).start()
    for i in range(17):
        time.sleep(0.2)
        pbar.update(i + 1)
    pbar.finish()

@example
def example6():
    pbar = ProgressBar().start()
    for i in range(100):
        time.sleep(0.01)
        pbar.update(i + 1)
    pbar.finish()

@example
def example7():
    pbar = ProgressBar()  # Progressbar can guess maxval automatically.
    for i in pbar(range(80)):
        time.sleep(0.01)

@example
def example8():
    pbar = ProgressBar(maxval=80)  # Progressbar can't guess maxval.
    for i in pbar((i for i in range(80))):
        time.sleep(0.01)

@example
def example9():
    pbar = ProgressBar(widgets=['Working: ', AnimatedMarker()])
    for i in pbar((i for i in range(50))):
        time.sleep(.08)

@example
def example10():
    widgets = ['Processed: ', Counter(), ' lines (', Timer(), ')']
    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(150))):
        time.sleep(0.1)

@example
def example11():
    widgets = [FormatLabel('Processed: %(value)d lines (in: %(elapsed)s)')]
    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(150))):
        time.sleep(0.1)

@example
def example12():
    widgets = ['Balloon: ', AnimatedMarker(markers='.oO@* ')]
    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(24))):
        time.sleep(0.3)

@example
def example13():
    # You may need python 3.x to see this correctly
    try:
        widgets = ['Arrows: ', AnimatedMarker(markers='----')]
        pbar = ProgressBar(widgets=widgets)
        for i in pbar((i for i in range(24))):
            time.sleep(0.3)
    except UnicodeError: sys.stdout.write('Unicode error: skipping example')

@example
def example14():
    # You may need python 3.x to see this correctly
    try:
        widgets = ['Arrows: ', AnimatedMarker(markers='++++')]
        pbar = ProgressBar(widgets=widgets)
        for i in pbar((i for i in range(24))):
            time.sleep(0.3)
    except UnicodeError: sys.stdout.write('Unicode error: skipping example')

@example
def example15():
    # You may need python 3.x to see this correctly
    try:
        widgets = ['Wheels: ', AnimatedMarker(markers='!!!!')]
        pbar = ProgressBar(widgets=widgets)
        for i in pbar((i for i in range(24))):
            time.sleep(0.3)
    except UnicodeError: sys.stdout.write('Unicode error: skipping example')

@example
def example16():
    widgets = [FormatLabel('Bouncer: value %(value)d - '), BouncingBar()]
    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(180))):
        time.sleep(0.05)

@example
def example17():
    widgets = [FormatLabel('Animated Bouncer: value %(value)d - '),
               BouncingBar(marker=RotatingMarker())]

    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(180))):
        time.sleep(0.05)

@example
def example18():
    widgets = [Percentage(),
               ' ', Bar(),
               ' ', ETA(),
               ' ', AdaptiveETA()]
    pbar = ProgressBar(widgets=widgets, maxval=500)
    pbar.start()
    for i in range(500):
        time.sleep(0.01 + (i < 100) * 0.01 + (i > 400) * 0.9)
        pbar.update(i + 1)
    pbar.finish()

@example
def example19():
  pbar = ProgressBar()
  for i in pbar([]):
    pass
  pbar.finish()

if __name__ == '__main__':
    try:
        for example in examples: example()
    except KeyboardInterrupt:
        sys.stdout('\nQuitting examples.\n')
"""
