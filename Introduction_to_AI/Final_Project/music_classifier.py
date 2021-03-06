#!/usr/bin/python3
import numpy as np
np.random.seed(1337)
import tensorflow as tf
tf.set_random_seed(1338)
import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
import os
from time import time
import random
random.seed(1339)
from sys import platform
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from subprocess import Popen
from preprocess import ourMel

from models import buildCNNModel, buildLSTMModel



N_SAMPLES = 1000
TRAIN_SPLIT = 0.8

train_size = int(N_SAMPLES * TRAIN_SPLIT)
test_size = N_SAMPLES - train_size


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.lineCount = 0
        self.lineMax = 3

        self. input_shape = [96, 1366]
        self.model_type = tk.IntVar()
        self.model_built = False
        self.is_train = True

        self.batch_size = 0
        self.n_epoch = 0
        self.train_plot = tk.IntVar()
        self.train_plot.set(0)
        self.mel_plot = tk.IntVar()
        self.mel_plot.set(0)
        self.stats = tk.IntVar()
        self.stats.set(0)
        self.play_song = tk.IntVar()
        self.play_song.set(0)
        self.create_widgets()

        self.cnn_lr = tk.DoubleVar()
        self.cnn_lr.set(0.0015)

    def create_widgets(self):
        self.winfo_toplevel().title("Music Classifier COMP 484")

        winFrame = tk.LabelFrame(self, text = "", padx = 10, pady = 5,height=4, width = 40)
        winFrame.grid(row = 0, pady=10, padx=10)
        self.optFrame = tk.LabelFrame(winFrame, text="", padx=5, pady=5)
        self.optFrame.grid(row=1, column=0, rowspan=1, pady=5, padx=5)
        self.optFrame.config(bd=1, height=40)

        # gear = tk.PhotoImage(file="photos/gear.png")
        # gear.subsample(5, 5)
        optBtn = tk.Button(winFrame)
        optBtn["text"] = "Configure"
        optBtn["command"] = self.optionsWindow
        # optBtn.config(width=10, height=10, image=gear)
        optBtn.config(width=10)
        optBtn.grid(row=1, sticky="w", padx=5, pady=5)

        self.btnFrame = tk.LabelFrame(winFrame, text="", padx=5, pady=5)

        self.btnFrame.grid(row=1, column=1, pady=5, padx=5)
        self.btnFrame.config(bd=1, height=40)

        self.train_btn = tk.Button(winFrame)
        self.train_btn["text"] = " Train "
        self.train_btn["command"] = self.train
        self.train_btn.config(width = 10)
        self.train_btn.grid(row=1,column= 1, pady=5, padx=5,sticky="w")


        self.predict_btn = tk.Button(winFrame)
        self.predict_btn["text"] = "Predict"
        self.predict_btn["command"] = self.predict
        self.predict_btn.config(width = 10)
        self.predict_btn.grid(row=1, column=2,  pady=5, padx=5)

        self.out = tk.Text(self, state='disabled',height=4, width = 30, background="#272323", fg="#ffffff")
        self.out.tag_config("right", justify=tk.RIGHT)
        self.out.grid(row = 4, columnspan=1, pady=(10,0), padx=20)
        self.printLine("Started")

        self.q_btn = tk.Button(self)
        self.q_btn["text"] = "Quit"
        self.q_btn["command"] = quit
        self.q_btn.config(fg = "red", width = 20)
        self.q_btn.grid(row = 5, column=0, columnspan=3, pady=(5,10))

    def optionsWindow(self):

        window = tk.Toplevel(self)
        window.grab_set()

        self.typeFrame = tk.LabelFrame(window, text="Model Type", padx=5, pady=5, width=30)
        self.typeFrame.grid(row=0, column=0, rowspan=2, pady=10, padx=10)
        self.typeFrame.config(bd=1, height=40)
        rb1 = tk.Radiobutton(self.typeFrame, text="CNN", variable=self.model_type, value=1,
                             command=lambda: self.changeType(1))
        rb1.pack(anchor="n")
        rb2 = tk.Radiobutton(self.typeFrame, text="LSTM", variable=self.model_type, value=2,
                             command=lambda: self.changeType(2))
        rb2.pack(anchor="n")


        optionsFrame = tk.LabelFrame(window, text="Options", padx=5, pady=5)
        optionsFrame.grid(row=2, column=0, rowspan=4, pady=(10, 5), padx=10)

        tp = tk.Checkbutton(optionsFrame, text="Show Train Plot", variable=self.train_plot, anchor="w")
        tp.config(bd=2)
        tp.grid(row=2, column=0, sticky="w")

        mp = tk.Checkbutton(optionsFrame, text="Show Prediction Spectrogram", variable=self.mel_plot, anchor="w")
        mp.config(bd=2)
        mp.grid(row=3, column=0, sticky="w")

        s = tk.Checkbutton(optionsFrame, text="Show Prediction Stats", variable=self.stats, anchor="w")
        s.config(bd=2)
        s.grid(row=4, column=0, sticky="w")

        pp = tk.Checkbutton(optionsFrame, text="Play Prediction Song", variable=self.play_song, anchor="w")
        pp.config(bd=2)
        pp.grid(row=5, column=0, sticky="w")

        cnnlr_frame = tk.LabelFrame(optionsFrame, bd=0)
        cnnlr_frame.grid(row=6, sticky="w")
        cnnlr_label = tk.Label(cnnlr_frame, text="CNN LR:")
        self.cnnlr_entry = tk.Entry(cnnlr_frame, width=6)

        self.cnnlr_entry.delete(0, tk.END)
        self.cnnlr_entry.insert(0, str(self.cnn_lr.get()))

        cnnlr_label.grid(row=0, column=0, sticky="w")
        self.cnnlr_entry.grid(row=0, column=1, sticky="w")


        def close(app, w):
            try:
                app.cnn_lr = float(app.cnnlr_entry.get())
            except ValueError:
                messagebox.showerror("Bad LR Value", "Enter a float for CNN LR")
                return
            w.destroy()

        apply = tk.Button(window)
        apply["text"] = "Apply"
        apply["command"] = lambda: close(self,window)
        apply.grid(row=6)

    def printLine(self, text):
        self.out.configure(state='normal')
        if(self.lineCount> self.lineMax):
            self.out.delete(1.0, tk.END)
            self.lineCount = 0
        else:
            self.out.insert(tk.END, "\n", "right")
        self.out.insert(tk.END, text, "right")
        self.out.configure(state='disabled')
        self.lineCount += 1


    def changeType(self, type):
        self.model_built = False
        self.model_type.set(type)


    def train(self):
        self.is_train = True



        x_train, x_test, y_train, y_test = self.getData()
        if not self.model_built or self.model == None:
            if (self.model_type.get() == 1):
                self.printLine('Building CNN....')

                self.model = buildCNNModel(self.input_shape, self.cnn_lr)
                x_train = x_train.reshape([-1, 96, 1366, 1])
                x_test = x_test.reshape([-1, 96, 1366, 1])

            elif (self.model_type.get() == 2):
                self.printLine('Building LSTM....')

                self.model = buildLSTMModel(self.input_shape)
            else:
                messagebox.showerror("No model", "Please choose a model type in the configuration settings")
                return

            self.model_built = True

        history = AccuracyHistory(plotting=self.train_plot)

        self.valid = False

        window = tk.Toplevel(self)
        window.grab_set()
        tk.Label(window, text="Batch Size (400): ", anchor="e").grid(row=0, column=0)
        tk.Label(window, text="Epochs (200): ", anchor="e").grid(row=1, column=0)

        batch_entry = tk.Entry(window, takefocus=True)
        batch_entry.grid(row=0, column=1)

        epoch_entry = tk.Entry(window)
        epoch_entry.grid(row=1, column=1)

        epoch_entry.bind('<Return>', lambda event, obj=self: go(obj))

        def go(obj):
            obj.valid = False

            try:
                obj.n_epoch = int(epoch_entry.get())
                obj.batch_size = int(batch_entry.get())
                if str(epoch_entry.get()) == "":
                    obj.n_epoch = 200
                if str(batch_entry.get()) == "":
                    obj.batch_size = 400
                else:
                    obj.valid = True
                    obj.printLine("Preparing...")
                    window.destroy()
            except ValueError:
                messagebox.showwarning("Bad entry", "Please enter integers. You entered: " + str(batch_entry.get()) + ", " + str(epoch_entry.get()))
                return

        go_btn = tk.Button(window, command=lambda: go(self))
        go_btn["text"] = "Go"
        go_btn.grid(row=2, column=1)

        self.wait_window(window)

        if not self.valid:
            self.printLine("Cancelling..")
            return
        else:
            self.printLine("Starting Train...")



        self.printLine("Training...")


        try:

            def close_win():
                messagebox.showwarning("Hold on!", "Train hasn't finished yet")

            win = tk.Toplevel(self)
            win.focus_force()
            win.grab_set()
            win.protocol('WM_DELETE_WINDOW', close_win)

            text = tk.Label(win, text="Training, please wait...")
            text.pack(padx=10, pady=10)

            def stop(self, win):
                self.model.stop_training = True
                win.destroy()

            btn = tk.Button(win, text="Stop", command=lambda:stop(self, win))
            btn.pack(padx=5, pady=5)

            self.model.fit(x_train, y_train,
                      batch_size=self.batch_size,
                      epochs=self.n_epoch,
                      verbose=1,
                      validation_data=(x_test, y_test),
                      callbacks=[history],
                      shuffle=False)
        except Exception as e: # real sketchy, but we don't want tensorflow to error silently in the background
            self.printLine("Tensorflow had error during train")
            messagebox.showerror("error", e)
            return

        win.destroy()
        score = self.model.evaluate(x_test, y_test)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

        print("Saving...")

        string = 'Loss:' +  str(score[0]) + "\nAcc:" + str(score[1]) + "\nAvg epoch time:" + str(np.mean(history.times))[:6] + " seconds"
        messagebox.showinfo("Test", string)




        self.printLine('Saving...')

        if self.model_type.get() == 2:
            self.model.save_weights('./LSTMweights')
            print("Saved to: ./LSTMweights")
            self.printLine('Saved to: ./LSTMweights')

        elif self.model_type.get() == 1:
            self.model.save_weights('./CNNweights')
            self.printLine('Saved to: ./CNNweights')


        plt.plot(range(1, self.n_epoch + 1), history.acc)
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.show()

        plt.plot(range(1, self.n_epoch + 1), history.loss)
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.show()

        return score

    def getData(self):
        labels = np.load("labels.npy")
        data = np.load("data.npy")
        data = np.ndarray.astype(data, "float32")
        labels = np.ndarray.astype(labels, "int")
        # randomly shuffle data
        rng_state = np.random.get_state()
        np.random.shuffle(data)
        np.random.set_state(rng_state)
        np.random.shuffle(labels)

        x_train = data[0:train_size]
        x_test = data[train_size:]

        x_train = x_train.reshape([-1, 96, 1366])
        x_test = x_test.reshape([-1, 96, 1366])

        y_train = labels[0:train_size]
        y_test = labels[train_size:]

        return x_train, x_test, y_train, y_test


    def predict(self):
        self.is_train = False
        classes = ["jazz", "blues", "reggae", "pop", "disco", "country", "metal", "hiphop", "rock", "classical"]

        if (not self.model_built) or self.model == None:
            if (self.model_type.get() == 1):
                self.model = buildCNNModel(self.input_shape, self.cnnlr)

                self.model.load_weights("./CNNweights")
            elif (self.model_type.get() == 2):
                self.model = buildLSTMModel(self.input_shape)
                self.model.load_weights("./LSTMweights")
            else:
                messagebox.showerror("No model", "Please choose a model type in the configuration settings")
                return
            self.model_built = True

        self.printLine("Model built, choose file...")


        tk.Tk().withdraw()
        path = askopenfilename(initialdir="./data")
        if path == "":
            messagebox.showwarning("No file chosen", "Please choose a file")
            return
        self.printLine("Predicting...")

        # play!
        if self.play_song.get():
            if platform == "linux" or platform == "linux2":
                pop = Popen(['aplay', path])
            elif os.name == "nt":
                os.system("start " + path)


        if(self.stats.get()):
            x_train, x_test, y_train, y_test = self.getData()
            if self.model_type.get() == 1:
                x_train = x_train.reshape([-1, 96, 1366, 1])
                x_test = x_test.reshape([-1, 96, 1366, 1])

            x = np.concatenate((x_train,x_test), axis=0)
            y = np.concatenate((y_train,y_test),axis=0)

            score = self.model.evaluate(x, y)
            string = 'Loss:\n\t' +  str(score[0]) + "\nAcc:\n\t" + str(score[1])
            messagebox.showinfo("Test", string)



        # Build the spectrogram for this song:
        spectrogram = ourMel(path, self.mel_plot.get())
        predict_data = np.empty([1, 1366, 96])
        np.append(predict_data, spectrogram)

        predict_data = predict_data.reshape([1] + self.input_shape)


        if (self.model_type.get() == 1):
            predict_data = predict_data.reshape([-1, 96, 1366, 1])
        self.printLine("Predicting...")
        prediction = []
        # Do prediction
        try:
            for i in range(100):
                p = self.model.predict(predict_data)
                prediction.append(p)
            prediction = np.array(prediction)
            prediction = np.mean(prediction, axis=1)
        except Exception as e: # real sketchy, but we don't want tensorflow to error silently in the background
            self.printLine("Tensorflow had error during prediction")
            messagebox.showerror("Error", e)
            return

        pred_class = prediction.argmax()
        self.printLine("Built spectrogram...")
        string = "Computer thinks the genre of this song is:\n" + classes[pred_class]
        string += "\n\nwith:\n" + str(prediction[0][pred_class]*100) + "% certainty\n\n"
        for i in range(prediction.shape[1]):
            string += str(prediction[0][i]*100)[:5] + "% "+ classes[i] +"\n"

        labels = pd.read_csv("./data/labels.csv", header=0)
        i = 0
        correct = ""
        for p in labels["path"]:
            p = "/".join(p.split("/")[-3:])
            # self.printLine("P: "+p)
            if p == "/".join(path.split("/")[-3:]):
                correct = labels['label'][i]
            i += 1
        string += "\nCorrect genre was: " + str.upper(classes[int(correct)])
        messagebox.showinfo("Prediction", string)

        if self.play_song.get():
            if platform == "linux" or platform == "linux2":
                os.system("pkill aplay")
                pop.terminate()

        self.printLine("Done")





class AccuracyHistory(tf.keras.callbacks.Callback):
    def __init__(self, plotting):
        self.e_counter = 0
        self.plotting = plotting.get()
        super().__init__()

    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.acc = []
        self.loss = []
        self.val_losses = []
        self.val_acc = []

        self.times = []

        self.s_time = time()
        self.e_time = 0

        if(self.plotting):
            plt.ion()
            plt.show()
            self.f, (self.ax1, self.ax2) = plt.subplots(1, 2, sharex=True)
            self.ax1.set_yscale('log')

    def on_epoch_end(self, batch, logs={}):
        self.times.append(time()-self.s_time)
        self.s_time = time()

        self.e_counter += 1
        self.acc.append(logs.get('acc'))
        self.loss.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.val_acc.append(logs.get('val_acc'))
        if(self.plotting):
            self.ax1.plot(range(1, self.e_counter+1), self.loss, label="Loss")
            # self.ax1.plot(range(1, self.e_counter+1), self.val_losses)
            self.ax1.set_ylabel('Loss')
            self.ax1.set_xlabel('Epochs')

            self.ax2.plot(range(1, self.e_counter+1), self.acc, label="Accuracy")
            # self.ax2.plot(range(1, self.e_counter+1), self.val_acc)
            self.ax2.set_ylabel('Accuracy')
            self.ax2.set_xlabel('Epochs')

            plt.draw()
            plt.pause(0.001)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    plt.show()
    quit()





