# from tkinter import *
# from tkinter.messagebox import showinfo
# from tkinter.filedialog import askopenfilename, asksaveasfilename
# import os

# def newFile():
#     global file
#     root.title("Untitled - Notepad")
#     file = None
#     TextArea.delete(1.0, END)


# def openFile():
#     global file
#     file = askopenfilename(defaultextension=".txt",
#                            filetypes=[("All Files", "*.*"),
#                                      ("Text Documents", "*.txt")])
#     if file == "":
#         file = None
#     else:
#         root.title(os.path.basename(file) + " - Notepad")
#         TextArea.delete(1.0, END)
#         f = open(file, "r")
#         TextArea.insert(1.0, f.read())
#         f.close()


# def saveFile():
#     global file
#     if file == None:
#         file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",
#                            filetypes=[("All Files", "*.*"),
#                                      ("Text Documents", "*.txt")])
#         if file =="":
#             file = None

#         else:
#             #Save as a new file
#             f = open(file, "w")
#             f.write(TextArea.get(1.0, END))
#             f.close()

#             root.title(os.path.basename(file) + " - Notepad")
#             print("File Saved")
#     else:
#         # Save the file
#         f = open(file, "w")
#         f.write(TextArea.get(1.0, END))
#         f.close()


# def quitApp():
#     root.destroy()

# def cut():
#     TextArea.event_generate(("<>"))

# def copy():
#     TextArea.event_generate(("<>"))

# def paste():
#     TextArea.event_generate(("<>"))

# def about():
#     showinfo("nextGen", "File structures mini project")

# if __name__ == '__main__':
#     #Basic tkinter setup
#     root = Tk()
#     root.title("Untitled - Notepad")
#     # root.wm_iconbitmap("1.ico")
#     root.geometry("600x600")

#     #Add TextArea
#     TextArea = Text(root, font="lucida 13")
#     file = None
#     TextArea.pack(expand=True, fill=BOTH)

#     # Lets create a menubar
#     MenuBar = Menu(root)

#     #File Menu Starts
#     FileMenu = Menu(MenuBar, tearoff=0)
#     # To open new file
#     FileMenu.add_command(label="New", command=newFile)

#     #To Open already existing file
#     FileMenu.add_command(label="Open", command = openFile)

#     # To save the current file

#     FileMenu.add_command(label = "Save", command = saveFile)
#     FileMenu.add_separator()
#     FileMenu.add_command(label = "Exit", command = quitApp)
#     MenuBar.add_cascade(label = "File", menu=FileMenu)
#     # File Menu ends

#     # Edit Menu Starts
#     EditMenu = Menu(MenuBar, tearoff=0)
#     #To give a feature of cut, copy and paste
#     EditMenu.add_command(label = "Cut", command=cut)
#     EditMenu.add_command(label = "Copy", command=copy)
#     EditMenu.add_command(label = "Paste", command=paste)

#     MenuBar.add_cascade(label="Edit", menu = EditMenu)

#     # Edit Menu Ends

#     # Help Menu Starts
#     HelpMenu = Menu(MenuBar, tearoff=0)
#     HelpMenu.add_command(label = "About Notepad", command=about)
#     MenuBar.add_cascade(label="Help", menu=HelpMenu)

#     # Help Menu Ends

#     root.config(menu=MenuBar)

#     #Adding Scrollbar using rules from Tkinter lecture no 22
#     Scroll = Scrollbar(TextArea)
#     Scroll.pack(side=RIGHT,  fill=Y)
#     Scroll.config(command=TextArea.yview)
#     TextArea.config(yscrollcommand=Scroll.set)

#     root.mainloop()
# def motion(event):
#     x, y = event.x, event.y
#     print('{}, {}'.format(x, y))

import os  
import pickle
from tkinter import *
from tkinter import messagebox  
from tkinter.messagebox import *  
from tkinter.filedialog import *  
from tkinter.simpledialog import *

def custom_hash(key):
        h=0
        for i in key:
            h = ord(i)+(h<<6)+(h<<16)-h 
        return h

class Hash(object):
    def __init__(self, size=1000):
        self.storage = [[] for _ in range(size)] # for resolving collisions
        self.size = size
        self.length = 0
    

    def __setitem__(self, key, value):
        # if there is any collision, add it to sub list
        storage_idx = custom_hash(key) % self.size
        for ele in self.storage[storage_idx]:
            if key == ele[0]:  # already exist, add the next occurance
                ele.append(value)
                break
        else:
            self.storage[storage_idx].append([key, value]) #if new item
            self.length += 1
    
    def __getitem__(self, key):

        storage_idx = custom_hash(key) % self.size
        for ele in self.storage[storage_idx]:
            if ele[0] == key:
                # return ele[1] # for latest value
                return ele
        return None
        # raise KeyError('Key {} dont exist'.format(key))

  
class Notepad_file:  
  
    __root = Tk()  
  
    # default window width and height  
    __thisWidth = 350  
    __thisHeight = 350  
    __thisTextArea = Text(__root,undo=True, autoseparators=True)  
    # __thisSearchKey =
    __thisMenuBar = Menu(__root)  
    __thisFileMenu = Menu(__thisMenuBar, tearoff = 0)  
    __thisEditMenu = Menu(__thisMenuBar, tearoff = 0)  
    __thisHelpMenu = Menu(__thisMenuBar, tearoff = 0)
    __thisHashTable = Hash()
      
    # For adding the scrollbar  
    __thisScrollBar = Scrollbar(__thisTextArea)   
    __file = None 
  
    def __init__(self, **kwargs):  
  
        # Here, we will Set the icon  
        try:  
                self.__root.wm_iconbitmap("notepad.ico")  
        except:  
                pass  
  
# here, we will set the window size, the default window size is 300 x 300  
  
        try:  
            self.__thisWidth = kwargs['width']  
        except KeyError:  
            pass  
  
        try:  
            self.__thisHeight = kwargs['height']  
        except KeyError:  
            pass  
  
        # here, we will set the window text  
        self.__root.title("Untitled - Text editor")  
  
        # here, we will set the center the window  
        screenWidth = self.__root.winfo_screenwidth()  
        screenHeight = self.__root.winfo_screenheight()  
      
        # For left-align  
        left = (screenWidth / 2) - (self.__thisWidth / 2)  
          
        # For right-align  
        top = (screenHeight / 2) - (self.__thisHeight /2)  
          
        # For top and bottom  
        # self.__root.geometry('%d + %d * %d + %d' % (self.__thisWidth,  
        #                                     self.__thisHeight,  
        #                                     left, top))  
        self.__root.geometry('600x600')
    # Here, we are making the text-area auto resizable  
        self.__root.grid_rowconfigure(0, weight = 1)  
        self.__root.grid_columnconfigure(0, weight = 1)  
  
        # Here, we will add the controls such as widgets  
        self.__thisTextArea.grid(sticky = N + E + S + W)  
          
        # For opening the new file  
        self.__thisFileMenu.add_command(label = "New File",  
                                        command = self.__newFile1)  
          
        # For opening the already existing file from the menu  
        self.__thisFileMenu.add_command(label = "Open",  
                                        command = self.__openFile1)  
          
        # For saving the current working file  
        self.__thisFileMenu.add_command(label = "Save",  
                                        command = self.__saveFile1) 
        self.__thisFileMenu.add_command(label='Find',command=self.__find)
        # self.__thisFileMenu.add_command(label="move",command=self.__thisTextArea.mark_set("insert", "%d.%d" %  (1, 1)))
 
  
        # For creating the line in the dialog Box     
        self.__thisFileMenu.add_separator()                                       
        self.__thisFileMenu.add_command(label = "Exit",  
                                        command=self.__quitApplication1)  
        self.__thisMenuBar.add_cascade(label = "File",  
                                    menu = self.__thisFileMenu)   
          
        # for giving the feature of cutting in Files  
        self.__thisEditMenu.add_command(label = "Cut",  
                                        command = self.__cut1)            
      
        # For giving the feature of copying in file  
        self.__thisEditMenu.add_command(label = "Copy",  
                                        command = self.__copy1)       
          
        # for giving the feature of pasting in file  
        self.__thisEditMenu.add_command(label = "Paste",  
                                        command = self.__paste1)          
          
        # for giving the feature of editing in file  
        self.__thisMenuBar.add_cascade(label = "Edit",  
                                    menu = self.__thisEditMenu)   
          
        # FOr creating the feature of description of the notepad File  
        self.__thisHelpMenu.add_command(label = "About",  
                                        command = self.__showAbout1)  
        self.__thisMenuBar.add_cascade(label = "Help",  
                                    menu = self.__thisHelpMenu)  
        self.__thisMenuBar.add_cascade(label="Find",command= self.__find)
  
        self.__root.config(menu = self.__thisMenuBar)  
  
        self.__thisScrollBar.pack(side = RIGHT,fill=Y)                
# Here, the scroll-bar will get adjusted automatically according to the content   
# of the file  
        self.__thisScrollBar.config(command = self.__thisTextArea.yview)      
        self.__thisTextArea.config(yscrollcommand = self.__thisScrollBar.set)  
      
          
    def __quitApplication1(self):  
        self.__root.destroy()  
        # exit()  
  
    def __showAbout1(self):  
        showinfo("Notepad File","Javatpoint")  
  
    def __openFile1(self):  

        self.__file = askopenfilename(defaultextension = ".txt",  
                                    filetypes = [("All Files","*.*"),  
                                        ("Text Documents","*.txt")])  
  
        if self.__file == "":  
              
            # If there is no file to open  
            self.__file = None  
        else:  
            try:
                hashfile = open (self.__file[:-4]+'hash.txt', "rb")
                self.__thisHashTable = pickle.load(hashfile)
            except:
                col=0
                d=Hash()
                # with open(self.__file, 'r') as fp:
                #     for count, row in enumerate(fp):
                #         for j in row.split():
                #             d[j] = str(count+1)+"."+str(col)
                #             col+=len(j)+1
                #         col=0
                # self.__thisHashTable = d
            # For trying to open the file set the window title  
            self.__root.title(os.path.basename(self.__file) + " - Notepad File")  
            self.__thisTextArea.delete(1.0, END)  
  
            file = open(self.__file, "r")  
  
            self.__thisTextArea.insert(1.0, file.read())  
  
            file.close()  
  
          
    def __newFile1(self):  
        self.__root.title("Untitled- Notepad File")  
        self.__file = None  
        self.__thisTextArea.delete(1.0, END)  

  
    def __saveFile1(self):  

  
        if self.__file == None:  
            # For Saving as new file  
            self.__file = asksaveasfilename(initialfile = 'UntitledFile.txt',  
                                            defaultextension = ".txt",  
                                            filetypes = [("All Files","*.*"),  
                                                ("Text Documents", "*.txt")])  
  
            if self.__file == "":  
                self.__file = None  
            else:  
                  
                # For trying to  save the file  
                file = open(self.__file,"w")  
                file.write(self.__thisTextArea.get(1.0, END))  
                file.close()  
                  
                # For changing the window title  
                self.__root.title(os.path.basename(self.__file) + " - Notepad File")  
                  
              
        else:  
            file = open(self.__file,"w")  
            file.write(self.__thisTextArea.get(1.0, END))  
            file.close()
            d = Hash()
            col=0
            with open(self.__file, 'r') as fp:
                for count, row in enumerate(fp):
                    for j in row.split():
                        d[j] = str(count+1)+"."+str(col)
                        col+=len(j)+1
                    col=0
            with open(self.__file[:-4]+'hash.txt', 'wb') as fh:
                pickle.dump(d, fh)
            # with open(self.__file, 'r') as fp:
            #     for count, row in enumerate(fp):
            #         for j in row.split():
            #             d[j] = str(count+1)+"."+str(col)
            #             col+=len(j)+1
            #         col=0
            # self.__thisHashTable = d
            # with open(self.__file[:-4]+'hash.txt', 'wb') as fh:
            #     pickle.dump(d, fh)  

    def __find(self):
        
        # hashfile = open ("datafile.txt", "rb")
        # self.__thisHashTable = pickle.load(hashfile)
        self.__thisTextArea.tag_remove('found', '1.0', END)
        key = askstring("Find","Enter the word to be searched")
        # print(self.__thisHashTable['in'])
        if key and self.__thisHashTable[key]:
            idx = '1.0'
            # while 1:
            # print(key)



            '''for i in len(self.__thisHashTable[key])-1:
                idx = self.__thisHashTable[key][i]
                lastidx = '%s+%dc' % (idx, len(key))
                self.__thisTextArea.see(idx)
                idx = lastidx '''
            # self.__findNext(self.__thisHashTable[key][1:],key)

            idx = self.__thisHashTable[key][1]
            # if not idx: break
            lastidx = '%s+%dc' % (idx, len(key))
            self.__thisTextArea.tag_add('found', idx, lastidx)
            # self.__thisMenuBar.add_command(label = "Find Next",  
            #                         command = self.__findNext)   
            self.__thisTextArea.see(idx)
            idx = lastidx
            self.__thisTextArea.tag_config('found', background='lightgreen')
        else:
            messagebox.showinfo('Find',"No matches found!(Save the file before searching)")
    
    def __findNext(self,finds,key):
        if self.__currentFind<len(finds):
            self.__currentFind+=1
            idx = finds[self.__currentFind]
            lastidx = '%s+%dc' % (idx, len(key))
            self.__thisTextArea.see(idx)
            idx = lastidx 
            
    def __findPrev(self,finds,key):
        if self.__currentFind>1:
            self.__currentFind-=1
            idx = finds[self.__currentFind]
            lastidx = '%s+%dc' % (idx, len(key))
            self.__thisTextArea.see(idx)
            idx = lastidx 



    def __cut1(self):  
        self.__thisTextArea.event_generate("<<Cut in File>>")  
    
  
    def __copy1(self):  
        self.__thisTextArea.event_generate("<<Copy in File>>")  
  
    def __paste1(self):  
        self.__thisTextArea.event_generate("<<Paste in File>>")  
  
    def run1(self):  
  
        # For running the main application  
        # self.__root.bind('<Motion>', motion)

        self.__root.mainloop()  

  
  
  
  
# For running the main application  
notepad1 = Notepad_file(width = 650, height = 450)  
notepad1.run1() 