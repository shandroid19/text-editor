import os  
import pickle
from tkinter import *
from tkinter import messagebox  
from tkinter.messagebox import *  
from tkinter.filedialog import *  
from tkinter.simpledialog import *
from tkinter import ttk
import tkinter.font as tkfonts

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

  


class Notepad_file:  #GUI starts here 
  
    __root = Tk()  
    coolfont = tkfonts.Font(family='consolas',size='11')
    # default window width and height  
    __width = 350  
    __height = 350  
    __text = Text(__root,undo=True,font=coolfont,pady=10,autoseparators=True,background='gray10',foreground='lawngreen',insertbackground='white')  
    # menubar components:
    __menubar = Menu(__root)  
    __filemenu = Menu(__menubar, tearoff = 0)  
    __editmenu = Menu(__menubar, tearoff = 0)  
    __currentFind = 1
    __hashtable = Hash()
    # For adding the scrollbar  
    __scrollbar = Scrollbar(__text)  
    #Search bar components:
    __frame = Frame(__root) 
    __edit = Entry(__frame)
    __file = None 
    __findnext= Button(__frame, text='Find Next') 
    __occurances= Label(__frame, text='')
    __findprev= Button(__frame, text='Find Previous') 
    __findbutton= Button(__frame, text='Search') 
    __closebutton= Button(__frame, text='Close') 


  
    def __init__(self, **kwargs):  
  
        # Here, we will Set the icon  
        try:  
                self.__root.wm_iconbitmap("notepad.ico")  #for icon on top right
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
      
        self.__root.geometry('600x600')
    # Here, we are making the text-area auto resizable  
        self.__root.grid_rowconfigure(0, weight = 1)  
        self.__root.grid_columnconfigure(0, weight = 1)  
        # Here, we will add the controls such as widgets  
        self.__text.grid(sticky = N + E + S + W)  #sticky means it covers extra space from N E S W (directions as specified)

        self.__frame.grid(row=3) #tkinter follows grid system ( here row0 is the menu bar, row1 is the text area, row3 is the find bar)
        self.__findprev.grid(row=3,column=0)
        self.__findnext.grid(row=3,column=1)
        self.__edit.grid(row=3,column=3)
        self.__occurances.grid(row=3,columnspan=2,column=7)
        self.__findbutton.grid(row=3,column=5)
        self.__closebutton.grid(row=3,column=6)
        self.__findnext.config(command=self.__findNext)
        self.__findprev.config(command=self.__findPrev)
        self.__closebutton.config(command=self.__closeFind)
        self.__findbutton.config(command=self.__find)
        self.__frame.grid_forget()


          
        # For opening the new file  
        self.__filemenu.add_command(label = "New File",  
                                        command = self.__newFile1)  
          
        # For opening the already existing file from the menu  
        self.__filemenu.add_command(label = "Open",  
                                        command = self.__openFile1)  
          
        # For saving the current working file  
        self.__filemenu.add_command(label = "Save",  
                                        command = self.__saveFile1) 
 
  
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
        # self.__helpmenu.add_command(label = "About",  
        #                                 command = self.__showAbout1)  
        self.__menubar.add_cascade(label = "About",  
                                    command = self.__showAbout1)  
        self.__menubar.add_cascade(label="Find",command= self.__showfind)
        # self.__menubar.add_cascade(label="Close find",command= self.__closeFind,state='disabled')

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

    #for loading the saved hashfile (filenamehash.txt)
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
                self.__loadHashFile() # loading hash file if it exists
                print('loaded')

            except:
                print('execpted')
                self.__createHashFile() # creating and loading hashfile if it does not exist
                self.__loadHashFile()
            # For trying to open the file set the window title  
            self.__root.title(os.path.basename(self.__file) + " - Notepad File")  #setting titlebar to filename 
            self.__text.delete(1.0, END)  
            file = open(self.__file, "r")  
            self.__text.insert(1.0, file.read())  #to the textarea, insert the contents of the file
            file.close()  
  
          
    def __newFile1(self):  
        self.__root.title("Untitled- Notepad File")  
        self.__file = None  
        self.__text.delete(1.0, END)  

  
    def __saveFile1(self):  
        if self.__file == None:  #if file is being saved for the first time
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

    def __showfind(self): # to unhide the find bar (opposite of grid_forget() function )
        self.__frame.grid()

    def __find(self): 

        key = self.__edit.get() # get text from "edit" text box in the find bar
        if key and self.__hashtable[key]: #if key exists in the hashtable
            idx = '1.0'                     #format for index is rownumber.columnumber
            #row starts from 1, column starts from 0
            idx = self.__hashtable[key][self.__currentFind]   # get list of indices if it occurs in the text
            self.__occurances.config(text="Found "+str(len(self.__hashtable[key])-1)+" occurance(s)") # display on label
            lastidx = '%s+%dc' % (idx, len(key)) # get the word's last character index
            self.__text.tag_add('found', idx, lastidx) #change color of the text which is found
            self.__text.see(idx)
            idx = lastidx
            self.__text.tag_config('found', background='white', foreground='gray') #configuring the color for highlighting
            
        else:
            self.__occurances.config(text = "No matches found")
    
    def __findNext(self): #find next occurance
        self.__text.tag_remove('found', '1.0', END)
        key = self.__edit.get()
        finds = self.__hashtable[key] #list of indices of occurances
        if self.__currentFind<len(finds)-1:
            self.__currentFind+=1
            idx = finds[self.__currentFind]
            print(self.__currentFind)
            print(idx,finds)
            lastidx = '%s+%dc' % (idx, len(key))
            self.__text.tag_add('found', idx, lastidx)
            self.__text.see(idx)
            idx = lastidx 
            self.__text.tag_config('found', background='white', foreground='gray')



            
    def __findPrev(self):
        self.__text.tag_remove('found', '1.0', END)
        key = self.__edit.get()
        finds = self.__hashtable[key]
        if self.__currentFind>1:
            self.__currentFind-=1
            idx = finds[self.__currentFind]
            print(idx,finds)
            lastidx = '%s+%dc' % (idx, len(key))
            self.__text.tag_add('found', idx, lastidx)
            self.__text.see(idx)
            idx = lastidx 
            self.__text.tag_config('found', background='white', foreground='gray')

    def __closeFind(self): #to close searchbar
        self.__occurances.config(text="")
        self.__frame.grid_forget() #to hide the frame (searchbar)
        self.__text.tag_remove('found', '1.0', END)


    def __cut1(self):  
        self.__text.event_generate("<<Cut in File>>")  
    
  
    def __copy1(self):  
        self.__text.event_generate("<<Copy in File>>")  
  
    def __paste1(self):  
        self.__text.event_generate("<<Paste in File>>")  
  
    def run1(self):  
  
        # For running the main application  
        # self.__root.bind('<Motion>', motion)

        self.__root.mainloop()  #run the gui

# For running the main application  
notepad1 = Notepad_file(width = 650, height = 450)  
notepad1.run1() 