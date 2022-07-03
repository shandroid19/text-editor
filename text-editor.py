
import os  
import pickle
from tkinter import *
from tkinter import messagebox  
from tkinter.messagebox import *  
from tkinter.filedialog import *  
from tkinter.simpledialog import *
from tkinter import ttk

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
    __width = 350  
    __height = 350  
    __text = Text(__root,undo=True, autoseparators=True)  
    # __thisSearchKey =
    __menubar = Menu(__root)  
    __filemenu = Menu(__menubar, tearoff = 0)  
    __editmenu = Menu(__menubar, tearoff = 0)  
    __helpmenu = Menu(__menubar, tearoff = 0)
    __hashtable = Hash()
      
    # For adding the scrollbar  
    __scrollbar = Scrollbar(__text)   
    __file = None 
  
    def __init__(self, **kwargs):  
  
        # Here, we will Set the icon  
        try:  
                self.__root.wm_iconbitmap("notepad.ico")  
        except:  
                pass  
  
# here, we will set the window size, the default window size is 300 x 300  
  
        try:  
            self.__width = kwargs['width']  
        except KeyError:  
            pass  
  
        try:  
            self.__height = kwargs['height']  
        except KeyError:  
            pass  
  
        # here, we will set the window text  
        self.__root.title("Untitled - Text editor")  
  
        # here, we will set the center the window  
        screenWidth = self.__root.winfo_screenwidth()  
        screenHeight = self.__root.winfo_screenheight()  
      
        # For left-align  
        left = (screenWidth / 2) - (self.__width / 2)  
          
        # For right-align  
        top = (screenHeight / 2) - (self.__height /2)  
          
        # For top and bottom  
        # self.__root.geometry('%d + %d * %d + %d' % (self.__width,  
        #                                     self.__height,  
        #                                     left, top))  
        self.__root.geometry('600x600')
    # Here, we are making the text-area auto resizable  
        self.__root.grid_rowconfigure(0, weight = 1)  
        self.__root.grid_columnconfigure(0, weight = 1)  
  
        # Here, we will add the controls such as widgets  
        self.__text.grid(sticky = N + E + S + W)  
          
        # For opening the new file  
        self.__filemenu.add_command(label = "New File",  
                                        command = self.__newFile1)  
          
        # For opening the already existing file from the menu  
        self.__filemenu.add_command(label = "Open",  
                                        command = self.__openFile1)  
          
        # For saving the current working file  
        self.__filemenu.add_command(label = "Save",  
                                        command = self.__saveFile1) 
        self.__filemenu.add_command(label='Find',command=self.__find)
        # self.__filemenu.add_command(label="move",command=self.__text.mark_set("insert", "%d.%d" %  (1, 1)))
 
  
        # For creating the line in the dialog Box     
        self.__filemenu.add_separator()                                       
        self.__filemenu.add_command(label = "Exit",  
                                        command=self.__quitApplication1)  
        self.__menubar.add_cascade(label = "File",  
                                    menu = self.__filemenu)   
          
        # for giving the feature of cutting in Files  
        self.__editmenu.add_command(label = "Cut",  
                                        command = self.__cut1)            
      
        # For giving the feature of copying in file  
        self.__editmenu.add_command(label = "Copy",  
                                        command = self.__copy1)       
          
        # for giving the feature of pasting in file  
        self.__editmenu.add_command(label = "Paste",  
                                        command = self.__paste1)          
          
        # for giving the feature of editing in file  
        self.__menubar.add_cascade(label = "Edit",  
                                    menu = self.__editmenu)   
          
        # FOr creating the feature of description of the notepad File  
        self.__helpmenu.add_command(label = "About",  
                                        command = self.__showAbout1)  
        self.__menubar.add_cascade(label = "Help",  
                                    menu = self.__helpmenu)  
        self.__menubar.add_cascade(label="Find",command= self.__find)
  
        self.__root.config(menu = self.__menubar)  
  
        self.__scrollbar.pack(side = RIGHT,fill=Y)                
# Here, the scroll-bar will get adjusted automatically according to the content   
# of the file  
        self.__scrollbar.config(command = self.__text.yview)      
        self.__text.config(yscrollcommand = self.__scrollbar.set)  
      
          
    def __quitApplication1(self):  
        self.__root.destroy()  
        # exit()  
  
    def __showAbout1(self):  
        showinfo("Text editor","Text editor developed using Tkinter which uses hashing for word searching") 

    def __createHashFile(self):
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

    def __loadHashFile(self):
        hashfile = open (self.__file[:-4]+'hash.txt', "rb")
        self.__hashtable = pickle.load(hashfile)
  
    def __openFile1(self):  

        self.__file = askopenfilename(defaultextension = ".txt",  
                                    filetypes = [("All Files","*.*"),  
                                        ("Text Documents","*.txt")])  
  
        if self.__file == "":  
              
            # If there is no file to open  
            self.__file = None  
        else:  
            try:
                self.__loadHashFile()
                print('loaded')

            except:
                print('execpted')
                self.__createHashFile()
                self.__loadHashFile()
            # For trying to open the file set the window title  
            self.__root.title(os.path.basename(self.__file) + " - Notepad File")  
            self.__text.delete(1.0, END)  
  
            file = open(self.__file, "r")  
  
            self.__text.insert(1.0, file.read())  
  
            file.close()  
  
          
    def __newFile1(self):  
        self.__root.title("Untitled- Notepad File")  
        self.__file = None  
        self.__text.delete(1.0, END)  

  
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
                file.write(self.__text.get(1.0, END))  
                file.close()  
                  
                # For changing the window title  
                self.__root.title(os.path.basename(self.__file) + " - Notepad File")  
                  
              
        else:  
            file = open(self.__file,"w")  
            file.write(self.__text.get(1.0, END))  
            file.close()
            self.__createHashFile()

    def __find(self):
        
        self.__text.tag_remove('found', '1.0', END)
        key = askstring("Find","\tEnter the word to be searched\t")
        if key and self.__hashtable[key]:
            idx = '1.0'
            # while 1:
            # print(key)
            '''for i in len(self.__hashtable[key])-1:
                idx = self.__hashtable[key][i]
                lastidx = '%s+%dc' % (idx, len(key))
                self.__text.see(idx)
                idx = lastidx '''
            # self.__findNext(self.__hashtable[key][1:],key)

            idx = self.__hashtable[key][1]
            # if not idx: break
            lastidx = '%s+%dc' % (idx, len(key))
            self.__text.tag_add('found', idx, lastidx)
            # self.__menubar.add_command(label = "Find Next",  
            #                         command = self.__findNext)   
            self.__text.see(idx)
            idx = lastidx
            self.__text.tag_config('found', background='lightgreen')
        else:
            messagebox.showinfo('Find',"No matches found!(Save the file before searching)")
    
    def __findNext(self,finds,key):
        if self.__currentFind<len(finds):
            self.__currentFind+=1
            idx = finds[self.__currentFind]
            lastidx = '%s+%dc' % (idx, len(key))
            self.__text.see(idx)
            idx = lastidx 
            
    def __findPrev(self,finds,key):
        if self.__currentFind>1:
            self.__currentFind-=1
            idx = finds[self.__currentFind]
            lastidx = '%s+%dc' % (idx, len(key))
            self.__text.see(idx)
            idx = lastidx 



    def __cut1(self):  
        self.__text.event_generate("<<Cut in File>>")  
    
  
    def __copy1(self):  
        self.__text.event_generate("<<Copy in File>>")  
  
    def __paste1(self):  
        self.__text.event_generate("<<Paste in File>>")  
  
    def run1(self):  
  
        # For running the main application  
        # self.__root.bind('<Motion>', motion)

        self.__root.mainloop()  

# For running the main application  
notepad1 = Notepad_file(width = 650, height = 450)  
notepad1.run1() 