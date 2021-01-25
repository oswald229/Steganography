from os import path
from tkinter import *
from tkinter.filedialog import askopenfile
from PIL import Image

import imageio
import ntpath

from globals import filetypes, window_config, paths
from Steganographor import Steganographor


def path_leaf(_path):
    """
    Get filename from path.
    :param _path: string
    :return: string
    """
    head, tail = ntpath.split(_path)

    return tail or ntpath.basename(head)


class Interface(Frame):
    """The main window.
    """

    def __init__(self, window_label, **kwargs):

        # Init Tkinter window
        window = Tk()
        window.title(str(window_label))
        # Set the window size
        window.geometry(
            str(window_config['width']) + 'x' + str(window_config['height']))
        window.update_idletasks()

        # Init attributes
        self.receiver_path = StringVar()

        self.receiver = None

        self.secret_path = StringVar()

        self.secret = None

        self.message_path = StringVar()

        self.message = None

        self.result = None
        self.result_path = StringVar()
        self.result_path.set("Result path...")

        self.pictures = [
            # {'picture':PhotoImage, 'tag':'Receiver|Secret|Message}, 'path': String
        ]
        self.current = None
        

        self.button_width = 12
        self.spinbox_width = 8

        # Build frames inside the window

        Frame.__init__(self, window, **kwargs)

        # Left side of the window

        self.leftFrame = Frame(window, width=window.winfo_width() / 2,
                               height=window.winfo_height(), bg='red')

        self.leftFrame.grid(row=0, column=0)
        self.leftFrame.grid_propagate(False)
        self.leftFrame.update_idletasks()

        hiddingFrame = Frame(self.leftFrame, height=self.leftFrame.winfo_height() / 2,
                             width=self.leftFrame.winfo_width(),
                             bg='pink')
        hiddingFrame.grid(row=0, column=0)
        hiddingFrame.grid_propagate(False)
        hiddingFrame.update_idletasks()

        decodingFrame = Frame(self.leftFrame,
                              height=self.leftFrame.winfo_height() / 2,
                              width=self.leftFrame.winfo_width(),
                              bg='orange')
        decodingFrame.grid(row=1, column=0)
        decodingFrame.grid_propagate(False)
        decodingFrame.update_idletasks()

        receiverFrame = Frame(hiddingFrame,
                              width=hiddingFrame.winfo_width(),
                              height=hiddingFrame.winfo_height() / 4,
                              bg='green')
        receiverFrame.grid()
        receiverFrame.grid_propagate(False)

        self.buttonLoadReceiver = Button(receiverFrame, width=self.button_width, text="Load Receiver",
                                         command=self.open_receiver)
        self.buttonLoadReceiver.grid(row=0, column=0, padx=10, pady=10)
        self.entryReceiverPath = Entry(receiverFrame, width=60)
        self.entryReceiverPath.grid(row=0, column=1, padx=10)
        self.entryReceiverPath.insert(0, self.receiver_path.get())

        secretLoaderFrame = Frame(hiddingFrame,
                                  width=hiddingFrame.winfo_width(),
                                  height=hiddingFrame.winfo_height() / 4,
                                  bg='cyan')
        secretLoaderFrame.grid()
        secretLoaderFrame.grid_propagate(False)

        self.buttonLoadSecret = Button(secretLoaderFrame, width=self.button_width, text="Load Secret",
                                       command=self.open_secret)
        self.buttonLoadSecret.grid(row=0, column=0, padx=10, pady=10)

        self.entrySecretPath = Entry(secretLoaderFrame, width=60)
        self.entrySecretPath.grid(row=0, column=1, padx=10)
        self.entrySecretPath.insert(0, self.secret_path.get())

        indexesSelectionFrame = Frame(hiddingFrame,
                                      width=hiddingFrame.winfo_width(),
                                      height=hiddingFrame.winfo_height() / 4,
                                      bg='purple')
        indexesSelectionFrame.grid()
        indexesSelectionFrame.grid_propagate(False)

        Button(indexesSelectionFrame, text="Starting Index", width=self.button_width).grid(row=0, column=0, pady=0,
                                                                                           padx=10)

        self.entryStartingIdxsRow = Spinbox(
            indexesSelectionFrame, width=self.spinbox_width, from_=0, to=99999)
        self.entryStartingIdxsRow.grid(row=0, column=1, padx=10, pady=10)
        self.entryStartingIdxsCol = Spinbox(
            indexesSelectionFrame, width=self.spinbox_width, from_=0, to=99999)
        self.entryStartingIdxsCol.grid(row=0, column=2)

        self.labelIdxs = Label(self.leftFrame, text="[,]")
        self.labelIdxs.grid(row=1, column=1)

        self.buttonProcessHidding = Button(hiddingFrame, text='Process Hidding',
                                           command=self.process_hidding)
        self.buttonProcessHidding.grid(sticky='s', pady=20)

        self.buttonProcessDecoding = Button(decodingFrame, text='Decode Hidding',
                                            command=self.process_decoding)
        self.buttonProcessDecoding.place(relx=0.5, rely=0.4, anchor=CENTER)

        buttonLoadMessage = Button(decodingFrame, width=self.button_width, text="Load Message",
                                   command=self.open_message)

        buttonLoadMessage.grid(row=0, column=0, padx=10, pady=10)
        self.entryMessagePath = Entry(decodingFrame, width=60)
        self.entryMessagePath.grid(row=0, column=1, padx=10)

        self.buttonLeftArrow = Button(decodingFrame, text='<', command=self.previous_picture)
        self.buttonLeftArrow.place(relx=0.4, rely=0.7, anchor=CENTER)

        self.buttonRightArrow = Button(decodingFrame, text='>', command=self.next_picture)
        self.buttonRightArrow.place(relx=0.6, rely=0.7, anchor=CENTER)


        # Right side of the window

        rightFrame = Frame(window, width=window.winfo_width() / 2,
                           height=window.winfo_height(), bg='brown')

        rightFrame.grid(row=0, column=1)
        rightFrame.grid_propagate(False)
        rightFrame.update_idletasks()

        self.displayerCanvas = Canvas(rightFrame, bg='gray',
                                      width=int(
                                          0.95 * rightFrame.winfo_width()),
                                      height=int(0.95 * rightFrame.winfo_height()))

        self.displayerCanvas.grid(row=0, column=0, padx=10, pady=10)

    def quit(self):
        pass

    def open_receiver(self):
        """
        Function to load your picture. (Format must be 'png'.)

        :return: PhotoImage object.
        """

        file = askopenfile(mode='r', filetypes=filetypes['pictures'])
        if file is not None:
            self.receiver_path.set(file.name)

            self.receiver = PhotoImage(file=self.receiver_path.get())

            self.entryReceiverPath.delete(0, 'end')

            self.entryReceiverPath.insert(0, file.name)

            tmpReceiver = imageio.imread(self.entryReceiverPath.get())

            self.entryStartingIdxsRow.config(from_=0, to=tmpReceiver.shape[0])
            self.entryStartingIdxsCol.config(from_=0, to=tmpReceiver.shape[1])
            
            self.labelIdxs.config(
                text='[' + str(tmpReceiver.shape[0]) + ', ' + str(tmpReceiver.shape[1]) + ']')

            
            if len(self.pictures) == 0:
                self.pictures.append({'picture': self.receiver.subsample(3,3), 'tag': "Receiver", 'path':self.receiver_path.get()})
            else:
                self.pictures[0] = {'picture': self.receiver.subsample(3,3), 'tag': "Receiver", 'path':self.receiver_path.get()}
            
            self.display_picture(0, tag='Receiver')
       


            return self.receiver

    

    def open_secret(self):
        """
        Function to load your secret picture. (Format must be 'png'.)

        :return: PhotoImage object.
        """

        file = askopenfile(mode='r', filetypes=filetypes['pictures'])
        if file is not None:
            self.secret_path.set(file.name)

            # self.SecretPathLabel['text'] = self.secret_path

            self.secret = PhotoImage(file=self.secret_path.get())

            self.entrySecretPath.delete(0, 'end')

            self.entrySecretPath.insert(0, self.secret_path.get())

            if len(self.pictures) == 1:
                self.pictures.append({'picture': self.secret.subsample(3,3), 'tag': "Secret",'path':self.secret_path.get()})
            else:
                self.pictures[1] = {'picture': self.secret.subsample(3,3), 'tag': "Secret", 'path':self.secret_path.get()}                

            

            return self.secret

        

    def open_message(self):
        """
        Function to load your picture which containing a secret. (Format must be 'png'.)

        :return: PhotoImage object.
        """
        file = askopenfile(mode='r', filetypes=filetypes['pictures'])
        if file is not None:
            self.message_path.set(file.name)

            # self.SecretPathLabel['text'] = self.secret_path

            self.message = PhotoImage(file=self.message_path.get())

            self.entryMessagePath.delete(0, 'end')

            self.entryMessagePath.insert(0, self.message_path.get())

            # if len(self.pictures) == 2:
            #     self.pictures.append(self.message.subsample(3,3))
            # else:
            #     self.pictures[2] = self.message.subsample(3,3)

            # self.secret = self.secret.subsample(2)
            #
            # self.hiddenDisplayerCanvas.create_image(0, 0, anchor=NW, image=self.secret)

            # plt.imshow(imageio.imread(self.secret_path))
            #
            # plt.show()

            return self.message

    def process_hidding(self):
        """
        Process hiding a secret picture into another one.
        :return: imageio object.
        """

        if (path.exists(self.entryReceiverPath.get())):

            if (path.exists(self.entrySecretPath.get())):
                """
                Compute output file path.
                If the output already exists, open it.
                """

                output = paths['encoded_pictures'] + \
                    path_leaf(self.entrySecretPath.get()).replace(
                        '.png', '') + '_in_'
                output += path_leaf(self.entryReceiverPath.get()
                                    ).replace('.png', '') + "_"
                output += self.entryStartingIdxsRow.get() + "_"
                output += self.entryStartingIdxsCol.get() + '.png'

                if path.exists(output):
                    
                    print("Already made : Opening picture....")

                else:
                    stegano = Steganographor(
                        [int(self.entryStartingIdxsRow.get()),
                         int(self.entryStartingIdxsCol.get())],
                        self.entryReceiverPath.get(),
                        self.entrySecretPath.get(),

                    )

                    result = stegano.encode()

                    imageio.imwrite(output, result)
                    
                    self.pictures.append({'picture':PhotoImage(file=output).subsample(3,3), 'tag':'Encode', 'path':output})
                    self.display_picture(len(self.pictures)-1)

                    return result

            else:
                print('No secret specified.')
        else:
            print('No receiver specified.')

    def process_decoding(self):
        """
        Process decoding a secret picture .
        :return: imageio object.
        """
        result = Steganographor.decode(imageio.imread(self.message_path.get()))

        output = paths['decoded_pictures'] + path_leaf(self.message_path.get())

        imageio.imwrite(output, result)

    def display_picture(self, picture_idx, tag=''):
        
                
        if self.current != None : self.displayerCanvas.delete(self.current['tag'])
        
        self.current = self.pictures[int(picture_idx)]

        if tag=='':
            tag = self.current['tag']

        self.displayerCanvas.create_image(self.displayerCanvas.winfo_width(
            )/2, self.displayerCanvas.winfo_height()/2, anchor=CENTER, image=self.current['picture'], tag=tag)
    
    def next_picture(self):
        
        if self.current!=None:
            try:
                idx = self.pictures.index(self.current)+1
                if(idx<len(self.pictures)):
                    self.display_picture(idx)


            except IndexError:
                
                pass

    def previous_picture(self):
        
        if self.current!=None:
            try:
                idx = self.pictures.index(self.current)-1
                if(idx>=0):
                    self.display_picture(idx)


            except IndexError:
                
                pass

    def get_from_path(self, path):
        path = str(path)
        
        for pic in self.pictures:
            
            if path in pic['path']:
                return pic

        return None