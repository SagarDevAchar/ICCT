import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

import webbrowser

import cv2
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits import mplot3d
from matplotlib import cm

appLinkURL = 'https://www.github.com/SagarDevAchar/'
applicationOperations = {' Adjust': [(-100, 100, "Brightness"), (-100, 100, "Contrast"), None],
                         ' Specific': [(0, 255, "Red"), (0, 255, "Green"), (0, 255, "Blue")],
                         ' Intensity': [(-255, 255, "Red"), (-255, 255, "Green"), (-255, 255, "Blue")],
                         ' Greyscale': [None, None, None],
                         ' Inverse': [(0, 255, "Amount"), None, None],
                         ' Ceiling': [(0, 255, "Red"), (0, 255, "Green"), (0, 255, "Blue")],
                         ' Floor': [(0, 255, "Red"), (0, 255, "Green"), (0, 255, "Blue")]}


def colourFmtConv(BGRA, toFmt):
    convFmt = np.array([None])

    if toFmt.upper() == 'HEX':
        convFmt[0] = "#%02x%02x%02x%02x" % (BGRA[2], BGRA[1], BGRA[0], BGRA[3])
    elif toFmt.upper() == 'HSL':
        RGB_norm = BGRA[:3][::-1] / 255
        C_max = np.max(RGB_norm)
        C_min = np.min(RGB_norm)
        D = C_max - C_min

        L = (C_max + C_min) / 2
        if D == 0:
            S = 0
            H = 0
        else:
            S = D / (1 - abs(2 * L - 1))
            H = 60
            if C_max == RGB_norm[0]:
                H *= ((RGB_norm[1] - RGB_norm[2]) / D % 6)
            elif C_max == RGB_norm[1]:
                H *= ((RGB_norm[2] - RGB_norm[0]) / D + 2)
            else:
                H *= ((RGB_norm[0] - RGB_norm[1]) / D + 4)

        convFmt = np.array([H, S * 100, L * 100])
    elif toFmt.upper() == 'CMYK':
        RGB_norm = BGRA[:3][::-1] / 255

        K = 1 - np.max(RGB_norm)
        C = (1 - RGB_norm[0] - K) / (1 - K)
        M = (1 - RGB_norm[1] - K) / (1 - K)
        Y = (1 - RGB_norm[2] - K) / (1 - K)

        convFmt = np.array([C * 100, M * 100, Y * 100, K * 100])
        convFmt[np.isnan(convFmt)] = 0

    return convFmt


def openUrl(*kwargs):
    webbrowser.open(appLinkURL)


class ApplicationVisualizer:
    def __init__(self, imgData):
        self.MainApplication = tk.Toplevel()

        self.VisualFrame = tk.Frame(self.MainApplication)

        imageRes = np.shape(imgData)

        X = np.arange(imageRes[1])
        Y = np.arange(imageRes[0])[::-1]

        X, Y = np.meshgrid(X, Y)

        imgFig = Figure(figsize=(13.5, 8), dpi=80)

        R_data = np.array(imgData[:, :, 0], dtype=np.float)
        G_data = np.array(imgData[:, :, 1], dtype=np.float)
        B_data = np.array(imgData[:, :, 2], dtype=np.float)

        R_plot = imgFig.add_subplot(2, 3, 1, projection='3d')
        G_plot = imgFig.add_subplot(2, 3, 2, projection='3d')
        B_plot = imgFig.add_subplot(2, 3, 3, projection='3d')

        R_map = imgFig.add_subplot(2, 3, 4)
        G_map = imgFig.add_subplot(2, 3, 5)
        B_map = imgFig.add_subplot(2, 3, 6)

        R_plot.plot_surface(X, Y, R_data, cmap=cm.coolwarm)
        R_plot.set_zlim(0, 256)
        R_plot.set_zlabel("R")
        G_plot.plot_surface(X, Y, G_data, cmap=cm.coolwarm)
        G_plot.set_zlim(0, 256)
        G_plot.set_zlabel("G")
        B_plot.plot_surface(X, Y, G_data, cmap=cm.coolwarm)
        B_plot.set_zlim(0, 256)
        B_plot.set_zlabel("B")

        R_map.imshow(R_data, cmap='Reds', interpolation=None)
        G_map.imshow(G_data, cmap='Greens', interpolation=None)
        B_map.imshow(B_data, cmap='Blues', interpolation=None)

        self.ImageCanvas = FigureCanvasTkAgg(imgFig, self.VisualFrame)
        self.ImageCanvas.get_tk_widget().pack()

        self.ImageToolbar = NavigationToolbar2Tk(self.ImageCanvas, self.VisualFrame)
        self.ImageToolbar.config(padx=5)
        self.ImageToolbar.update()
        self.ImageCanvas.get_tk_widget().pack()

        self.VisualFrame.pack(padx=5, pady=5)

        self.MainApplication.title('ICCT Visualizer')


class ApplicationICCT:
    def setDefaults(self):
        self.VAR_fileName.set("No file selected")

        self.ImageBGRA = None
        self.ImageOriginal = None

        self.VAR_filterR.set(0)
        self.VAR_filterG.set(0)
        self.VAR_filterB.set(0)

        self.VAR_operationMode.set('')

        self.RedChannelEntry.config(state='disabled')
        self.RedChannelScale.config(state='disabled')
        self.RedChannelLabel.config(state='disabled')
        self.GreenChannelEntry.config(state='disabled')
        self.GreenChannelScale.config(state='disabled')
        self.GreenChannelLabel.config(state='disabled')
        self.BlueChannelEntry.config(state='disabled')
        self.BlueChannelScale.config(state='disabled')
        self.BlueChannelLabel.config(state='disabled')

        self.ProcessButton.config(state='disabled')
        self.ResetButton.config(state='disabled')
        self.SaveButton.config(state='disabled')

        self.VisualizerButton.config(state='disabled')

        self.VAR_pickerR.set("---")
        self.VAR_pickerG.set("---")
        self.VAR_pickerB.set("---")

        self.VAR_pickerH.set("---")
        self.VAR_pickerS.set("---")
        self.VAR_pickerL.set("---")

        self.VAR_pickerC.set("---")
        self.VAR_pickerM.set("---")
        self.VAR_pickerY.set("---")
        self.VAR_pickerK.set("---")

        self.VAR_pickerHEX.set("#--------")

        self.PickerSampleCanvas.config(background="#f0f0f0")
        self.PickerSampleCanvas.itemconfig(self.PickerAlphaText, text="Alpha : ---", fill="#000000")

        self.ImageFigure.clear()
        self.ImageCanvas.draw()
        self.ImageCanvas.mpl_disconnect(self.pickerClickPID)

        self.BrowseFileButton.config(state='enabled')
        self.ClearFileButton.config(state='disabled')

    def modeChangeEvent(self, *kwargs):
        self.VAR_filterR.set(0)
        self.VAR_filterG.set(0)
        self.VAR_filterB.set(0)

        operationMode = self.VAR_operationMode.get()

        if operationMode != '':

            modeParams = applicationOperations[operationMode]

            if modeParams[0]:
                self.RedChannelLabel.config(state='enabled', text=modeParams[0][2])
                self.RedChannelEntry.config(state='enabled')
                self.RedChannelScale.config(state='enabled', from_=modeParams[0][0], to=modeParams[0][1])
            else:
                self.RedChannelLabel.config(state='disabled', text="Red")
                self.RedChannelEntry.config(state='disabled')
                self.RedChannelScale.config(state='disabled', from_=0, to=1)

            if modeParams[1]:
                self.GreenChannelLabel.config(state='enabled', text=modeParams[1][2])
                self.GreenChannelEntry.config(state='enabled')
                self.GreenChannelScale.config(state='enabled', from_=modeParams[1][0], to=modeParams[1][1])
            else:
                self.GreenChannelLabel.config(state='disabled', text="Green")
                self.GreenChannelEntry.config(state='disabled')
                self.GreenChannelScale.config(state='disabled', from_=0, to=1)

            if modeParams[2]:
                self.BlueChannelLabel.config(state='enabled', text=modeParams[2][2])
                self.BlueChannelEntry.config(state='enabled')
                self.BlueChannelScale.config(state='enabled', from_=modeParams[2][0], to=modeParams[2][1])
            else:
                self.BlueChannelLabel.config(state='disabled', text="Blue")
                self.BlueChannelEntry.config(state='disabled')
                self.BlueChannelScale.config(state='disabled', from_=0, to=1)

    def openFile(self):
        ImageFilePath = filedialog.askopenfilename(filetypes=[("Image files", ".jpg .jpeg .png .bmp")])

        try:
            if ImageFilePath != '':
                self.ImageBGRA = cv2.imread(ImageFilePath, cv2.IMREAD_UNCHANGED)

                if self.ImageBGRA.shape[2] == 3:
                    (W, H, X) = self.ImageBGRA.shape
                    self.ImageBGRA = np.dstack((self.ImageBGRA, np.ones((W, H), dtype=np.uint8) * 255))

                self.ImageOriginal = np.array(self.ImageBGRA)

                self.showImage()

                self.VAR_fileName.set(ImageFilePath.split('/')[-1])

                self.BrowseFileButton.config(state='disabled')
                self.ClearFileButton.config(state='enabled')

                self.ProcessButton.config(state='enabled')
                self.ResetButton.config(state='enabled')
                self.SaveButton.config(state='enabled')

                self.VisualizerButton.config(state='enabled')

                self.pickerClickPID = self.ImageCanvas.mpl_connect('button_press_event', self.colourPickerClick)
        except:
            messagebox.showerror("Error", "Invalid Image")
            self.setDefaults()

    def showImage(self):
        self.ImageFigure.clear()
        self.ImagePlot = self.ImageFigure.add_subplot()
        self.ImagePlot.imshow(cv2.cvtColor(self.ImageBGRA, cv2.COLOR_BGRA2RGBA))
        self.ImageCanvas.draw()

    def applyImageFilter(self):
        operationMode = self.ModeOptionMenu.get().upper().strip()
        if self.VAR_cumulative.get() == 0:
            self.ImageBGRA = np.array(self.ImageOriginal)

        try:
            R = self.VAR_filterR.get()
            G = self.VAR_filterG.get()
            B = self.VAR_filterB.get()
        except tk.TclError:
            messagebox.showerror("Error", "Invalid Input Parameters")
            return

        if operationMode == 'ADJUST':
            B, C = R * 2.55, 1 + G / 100

            ImageBGR = np.array(self.ImageBGRA[:, :, :3], dtype=np.float)
            self.ImageBGRA = np.dstack((np.array((C * (ImageBGR - 128) + 128 + B).clip(min=0, max=255), dtype=np.uint8),
                                        self.ImageBGRA[:, :, 3]))
        if operationMode == 'SPECIFIC':
            negative = np.where(np.logical_or(self.ImageBGRA[:, :, 0] != B,
                                              self.ImageBGRA[:, :, 1] != G,
                                              self.ImageBGRA[:, :, 2] != R))

            if colourFmtConv(np.array([B, G, R, 255]), 'hsl')[2] > 17.5:
                self.ImageBGRA[negative] = [0, 0, 0, 255]
            else:
                self.ImageBGRA[negative] = [255, 255, 255, 255]
        elif operationMode == 'INTENSITY':
            BGRA = np.array([B, G, R, 0])
            self.ImageBGRA = np.array((np.array(self.ImageBGRA) + BGRA).clip(min=0, max=255), dtype=np.uint8)
        elif operationMode == 'GREYSCALE':
            Gray = np.array(0.299 * self.ImageBGRA[:, :, 2] +
                            0.587 * self.ImageBGRA[:, :, 1] +
                            0.114 * self.ImageBGRA[:, :, 0], dtype=np.uint8)
            Alpha = self.ImageBGRA[:, :, 3]

            self.ImageBGRA = np.dstack((Gray, Gray, Gray, Alpha))
        elif operationMode == 'INVERSE':
            self.ImageBGRA = np.array(np.absolute(np.array(self.ImageBGRA, dtype=np.int) - [R, R, R, 0]),
                                      dtype=np.uint8)
        elif operationMode == 'CEILING':
            ImageBGR = self.ImageBGRA[:, :, :3]
            ImageBGR[ImageBGR[:, :, 0] > B] = 0
            ImageBGR[ImageBGR[:, :, 1] > G] = 0
            ImageBGR[ImageBGR[:, :, 2] > R] = 0
            self.ImageBGRA = np.dstack((ImageBGR, self.ImageBGRA[:, :, 3]))
        elif operationMode == 'FLOOR':
            ImageBGR = self.ImageBGRA[:, :, :3]
            ImageBGR[ImageBGR[:, :, 0] < B] = 0
            ImageBGR[ImageBGR[:, :, 1] < G] = 0
            ImageBGR[ImageBGR[:, :, 2] < R] = 0
            self.ImageBGRA = np.dstack((ImageBGR, self.ImageBGRA[:, :, 3]))

        self.showImage()

    def resetImageFilter(self):
        self.ImageBGRA = np.array(self.ImageOriginal)
        self.showImage()

    def saveImagePreview(self):
        saveFilename = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG File", '*.png'),
                                                                                        ("JPG File", '*.jpg'),
                                                                                        ("JPEG File", '*.jpeg')])
        try:
            print(saveFilename)
            if saveFilename != '':
                cv2.imwrite(saveFilename, self.ImageBGRA)

                messagebox.showinfo("Info", "Image saved successfully!")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Error while writing file")

    def visualizeImage(self):
        ApplicationVisualizer(self.ImageBGRA)

    def colourPickerClick(self, clickEvent):
        x, y = int(round(clickEvent.xdata)), int(round(clickEvent.ydata))
        pickedPixelBGRA = self.ImageBGRA[y, x, :]

        HSL = colourFmtConv(pickedPixelBGRA, 'hsl')
        CMYK = colourFmtConv(pickedPixelBGRA, 'cmyk')
        HEX = colourFmtConv(pickedPixelBGRA, 'hex')

        self.VAR_pickerR.set("%03d" % pickedPixelBGRA[2])
        self.VAR_pickerG.set("%03d" % pickedPixelBGRA[1])
        self.VAR_pickerB.set("%03d" % pickedPixelBGRA[0])

        self.VAR_pickerH.set("%03d" % HSL[0])
        self.VAR_pickerS.set("%03d" % HSL[1])
        self.VAR_pickerL.set("%03d" % HSL[2])

        self.VAR_pickerC.set("%03d" % CMYK[0])
        self.VAR_pickerM.set("%03d" % CMYK[1])
        self.VAR_pickerY.set("%03d" % CMYK[2])
        self.VAR_pickerK.set("%03d" % CMYK[3])

        self.VAR_pickerHEX.set(HEX[0].upper())

        self.PickerSampleCanvas.config(background=HEX[0][:7])

        FG = "#000000" if HSL[2] > 20 else "#ffffff"
        self.PickerSampleCanvas.itemconfig(self.PickerAlphaText, text="Alpha : %d" % pickedPixelBGRA[3], fill=FG)

    def __init__(self):
        self.ImageBGRA = None
        self.ImageOriginal = None

        self.MainApplication = tk.Tk()
        self.MainApplicationFrame = ttk.Frame(self.MainApplication)

        # <| METADATA DISPLAY FOR THE APPLICATION |>
        self.AppNameLabel = ttk.Label(self.MainApplicationFrame)
        self.AppNameLabel.config(anchor='w', font='{Arial} 20 {bold}', text='Image Colour Channel Tool')
        self.AppNameLabel.place(anchor='n', x='215', y='25')

        self.AppCreditLabel = ttk.Label(self.MainApplicationFrame)
        self.AppCreditLabel.config(text='By Sagar Dev Achar')
        self.AppCreditLabel.place(anchor='n', x='215', y='63')

        self.AppLinkLabel = ttk.Label(self.MainApplicationFrame)
        self.AppLinkLabel.config(cursor='hand2', foreground='#0000ff', text=appLinkURL)
        self.AppLinkLabel.place(anchor='n', x='215', y='85')
        self.AppLinkLabel.bind("<Button>", openUrl)

        # <| FRAME FOR IMAGE PREVIEW |>
        self.PreviewFrame = ttk.Labelframe(self.MainApplicationFrame)

        self.ImageFigure = Figure(figsize=(10.0625, 8.3125), dpi=80)
        self.ImagePlot = None

        self.pickerClickPID = None

        self.ImageCanvas = FigureCanvasTkAgg(self.ImageFigure, self.PreviewFrame)
        self.ImageCanvas.get_tk_widget().pack(padx=5)
        self.ImageToolbar = NavigationToolbar2Tk(self.ImageCanvas, self.PreviewFrame)
        self.ImageToolbar.config(padx=5)
        self.ImageToolbar.update()
        self.ImageCanvas.get_tk_widget().pack()

        self.VisualizerButton = ttk.Button(self.ImageToolbar, command=self.visualizeImage)
        self.VisualizerButton.config(text='Visualize', width='12', state='disabled')
        self.VisualizerButton.place(anchor='w', relx='0.5', rely='0.5')

        self.PreviewFrame.config(height='715', text='Image Preview', width='850')
        self.PreviewFrame.pack(padx='5', pady='5', side='right')

        self.Separator = ttk.Separator(self.MainApplicationFrame)
        self.Separator.config(orient='vertical', takefocus=False)
        self.Separator.place(anchor='n', height='715', x='440', y='5')

        # <| FRAME FOR THE CHANNEL CONTROLS OF THE APPLICATION |>
        self.ControlFrame = ttk.Labelframe(self.MainApplicationFrame)

        self.BrowseFileButton = ttk.Button(self.ControlFrame, command=self.openFile)
        self.BrowseFileButton.config(text='Browse', width='8')
        self.BrowseFileButton.place(anchor='w', x='30', y='35')

        self.VAR_fileName = tk.StringVar('')
        self.VAR_fileName.set('No file selected')
        self.FilePathEntry = ttk.Entry(self.ControlFrame, textvariable=self.VAR_fileName)
        self.FilePathEntry.config(state='readonly', justify='center')
        self.FilePathEntry.place(anchor='w', width='255', x='100', y='35')

        self.ClearFileButton = ttk.Button(self.ControlFrame, command=self.setDefaults)
        self.ClearFileButton.config(state='disabled', text='X', width='3')
        self.ClearFileButton.place(anchor='e', x='395', y='35')

        self.ModeTextLabel = ttk.Label(self.ControlFrame, text='Effect Mode')
        self.ModeTextLabel.place(anchor='w', x='100', y='95')

        self.VAR_operationMode = tk.StringVar('')
        self.VAR_operationMode.trace('w', self.modeChangeEvent)

        self.ModeOptionMenu = ttk.Combobox(self.ControlFrame, state='readonly', width='20')
        self.ModeOptionMenu.config(values=list(applicationOperations.keys()), textvariable=self.VAR_operationMode)
        self.ModeOptionMenu.place(anchor='e', x='330', y='95')

        self.VAR_cumulative = tk.IntVar()
        self.VAR_cumulative.set(0)

        self.CumulativeCheckBox = ttk.Checkbutton(self.ControlFrame, text='Cumulative Filters')
        self.CumulativeCheckBox.config(variable=self.VAR_cumulative)
        self.CumulativeCheckBox.place(anchor='center', relx='0.5', y='130')

        self.VAR_filterR = tk.IntVar()
        self.VAR_filterG = tk.IntVar()
        self.VAR_filterB = tk.IntVar()

        self.RedChannelScale = ttk.Scale(self.ControlFrame)
        self.RedChannelScale.config(length=256, orient='horizontal', variable=self.VAR_filterR)
        self.RedChannelScale.place(anchor='w', x='80', y='175')
        self.RedChannelLabel = ttk.Label(self.ControlFrame, text='Red')
        self.RedChannelLabel.place(anchor='e', x='65', y='175')
        self.RedChannelEntry = ttk.Entry(self.ControlFrame, width='5', textvariable=self.VAR_filterR)
        self.RedChannelEntry.place(anchor='w', x='355', y='175')

        self.GreenChannelScale = ttk.Scale(self.ControlFrame)
        self.GreenChannelScale.config(length=256, orient='horizontal', variable=self.VAR_filterG)
        self.GreenChannelScale.place(anchor='w', x='80', y='210')
        self.GreenChannelLabel = ttk.Label(self.ControlFrame, text='Green')
        self.GreenChannelLabel.place(anchor='e', x='65', y='210')
        self.GreenChannelEntry = ttk.Entry(self.ControlFrame, width='5', textvariable=self.VAR_filterG)
        self.GreenChannelEntry.place(anchor='w', x='355', y='210')

        self.BlueChannelScale = ttk.Scale(self.ControlFrame)
        self.BlueChannelScale.config(length=256, orient='horizontal', variable=self.VAR_filterB)
        self.BlueChannelScale.place(anchor='w', x='80', y='245')
        self.BlueChannelLabel = ttk.Label(self.ControlFrame, text='Blue')
        self.BlueChannelLabel.place(anchor='e', x='65', y='245')
        self.BlueChannelEntry = ttk.Entry(self.ControlFrame, width='5', textvariable=self.VAR_filterB)
        self.BlueChannelEntry.place(anchor='w', x='355', y='245')

        self.ProcessButton = ttk.Button(self.ControlFrame, text='Apply Parameters', command=self.applyImageFilter)
        self.ProcessButton.place(anchor='w', width='150', x='60', y='310')

        self.ResetButton = ttk.Button(self.ControlFrame, text='Reset Preview', command=self.resetImageFilter)
        self.ResetButton.place(anchor='e', width='150', x='370', y='310')

        self.SaveButton = ttk.Button(self.ControlFrame, text='Save Current Preview', command=self.saveImagePreview)
        self.SaveButton.place(anchor='w', width='310', x='60', y='345')

        # <| FRAME TO DISPLAY COLOR PICKER OUTPUT |>
        self.PickerFrame = ttk.Labelframe(self.ControlFrame)

        self.VAR_pickerA = tk.StringVar("")
        self.VAR_pickerR = tk.StringVar("")
        self.VAR_pickerG = tk.StringVar("")
        self.VAR_pickerB = tk.StringVar("")
        self.VAR_pickerH = tk.StringVar("")
        self.VAR_pickerS = tk.StringVar("")
        self.VAR_pickerL = tk.StringVar("")
        self.VAR_pickerC = tk.StringVar("")
        self.VAR_pickerM = tk.StringVar("")
        self.VAR_pickerY = tk.StringVar("")
        self.VAR_pickerK = tk.StringVar("")
        self.VAR_pickerHEX = tk.StringVar("")

        self.PickerSampleCanvas = tk.Canvas(self.PickerFrame)
        self.PickerSampleCanvas.config(borderwidth='1', width='125', height='125', highlightbackground='#000000')
        self.PickerAlphaText = self.PickerSampleCanvas.create_text(9, 7, text="ALPHA : ---", anchor='nw')
        self.PickerSampleCanvas.place(anchor='e', x='400', y='85')

        self.PickerRGBLabel = ttk.Label(self.PickerFrame, text='RGB :')
        self.PickerRGBLabel.place(anchor='e', x='65', y='30')
        self.PickerRValueLabel = ttk.Label(self.PickerFrame, background='#ff0000', foreground='#ffffff', padding='3')
        self.PickerRValueLabel.config(textvariable=self.VAR_pickerR)
        self.PickerRValueLabel.place(anchor='w', x='75', y='30')
        self.PickerGValueLabel = ttk.Label(self.PickerFrame, background='#00ff00', padding='3')
        self.PickerGValueLabel.config(textvariable=self.VAR_pickerG)
        self.PickerGValueLabel.place(anchor='w', x='115', y='30')
        self.PickerBValueLabel = ttk.Label(self.PickerFrame, background='#0000ff', foreground='#ffffff', padding='3')
        self.PickerBValueLabel.config(textvariable=self.VAR_pickerB)
        self.PickerBValueLabel.place(anchor='w', x='155', y='30')

        self.PickerHSLLabel = ttk.Label(self.PickerFrame, text='HSL :')
        self.PickerHSLLabel.place(anchor='e', x='65', y='67')
        self.PickerHValueLabel = ttk.Label(self.PickerFrame, background='#c0c0c0', padding='3')
        self.PickerHValueLabel.config(textvariable=self.VAR_pickerH)
        self.PickerHValueLabel.place(anchor='w', x='75', y='67')
        self.PickerSValueLabel = ttk.Label(self.PickerFrame, background='#c0c0c0', padding='3')
        self.PickerSValueLabel.config(textvariable=self.VAR_pickerS)
        self.PickerSValueLabel.place(anchor='w', x='115', y='67')
        self.PickerLValueLabel = ttk.Label(self.PickerFrame, background='#c0c0c0', padding='3')
        self.PickerLValueLabel.config(textvariable=self.VAR_pickerL)
        self.PickerLValueLabel.place(anchor='w', x='155', y='67')

        self.PickerCMYKLabel = ttk.Label(self.PickerFrame, text='CMYK :')
        self.PickerCMYKLabel.place(anchor='e', x='65', y='103')
        self.PickerCValueLabel = ttk.Label(self.PickerFrame, background='#00ffff', padding='3')
        self.PickerCValueLabel.config(textvariable=self.VAR_pickerC)
        self.PickerCValueLabel.place(anchor='w', x='75', y='103')
        self.PickerMValueLabel = ttk.Label(self.PickerFrame, background='#ff00ff', padding='3')
        self.PickerMValueLabel.config(textvariable=self.VAR_pickerM)
        self.PickerMValueLabel.place(anchor='w', x='115', y='103')
        self.PickerYValueLabel = ttk.Label(self.PickerFrame, background='#ffff00', padding='3')
        self.PickerYValueLabel.config(textvariable=self.VAR_pickerY)
        self.PickerYValueLabel.place(anchor='w', x='155', y='103')
        self.PickerKValueLabel = ttk.Label(self.PickerFrame, background='#000000', foreground='#ffffff', padding='3')
        self.PickerKValueLabel.config(textvariable=self.VAR_pickerK)
        self.PickerKValueLabel.place(anchor='w', x='195', y='103')

        self.PickerHexLabel = ttk.Label(self.PickerFrame, text='HEX :')
        self.PickerHexLabel.place(anchor='e', x='65', y='140')
        self.PickerHexValueLabel = ttk.Label(self.PickerFrame)
        self.PickerHexValueLabel.config(background='#c0c0c0', padding='3')
        self.PickerHexValueLabel.config(textvariable=self.VAR_pickerHEX)
        self.PickerHexValueLabel.place(anchor='w', x='75', y='140')

        self.PickerFrame.config(height='200', text='Picker', width='420')
        self.PickerFrame.place(anchor='n', relx='0.5', x=0, y='372')

        self.ControlFrame.config(height='595', text='Controls', width='430')
        self.ControlFrame.pack(padx='5', pady='5', side='bottom')

        self.setDefaults()

        self.MainApplicationFrame.config(height='720', width='1280')
        self.MainApplicationFrame.pack(side='top')

        self.MainApplication.title("ICCT")

    def run(self):
        self.MainApplication.mainloop()


if __name__ == '__main__':
    app = ApplicationICCT()
    app.run()
