#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
import pandas as pd
import numpy as np
import tkinter as tk
import re
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
    
print("Please wait in every step and don't close the window. It'll be automatically closed after completion. ")
selectedfile = []


def check_file():
    if not selectedfile:
        print("Please select a file")
        return False
    else:
        return True


while not check_file():
    root = tk.Tk()
    root.title('Choose your file')
    root.resizable(False, False)
    root.geometry('300x150')
    selectedfile = []

    def select_file():
        filetypes = (
            ('All files', ('*.csv','*.xlsx', '*.xls')),
            ('CSV files', '*.csv'),
            ('Excel files', ('*.xlsx', '*.xls'))
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        showinfo(
            title='Selected File',
            message=filename
        )
        selectedfile.append(filename)
        root.destroy()

    # open button
    open_button = ttk.Button(
        root,
        text='Open a File',
        command=select_file
    )

    open_button.pack(expand=True)

    # run the application
    root.mainloop()

if check_file():
    file_extension = os.path.splitext(selectedfile[0])[1]
    print(file_extension)
    if file_extension == '.csv':
        df1 = pd.read_csv(selectedfile[0], low_memory=False, encoding='utf-8')
    elif file_extension == '.xlsx' or file_extension == '.xls':
        df1 = pd.read_excel(selectedfile[0], engine='openpyxl')
    else:
        print("Unsupported file format")

    df = df1.iloc[3:]
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)


# In[2]:


df_productId= df.loc[:,'Part Number']


# In[3]:


# Filter the DataFrame based on the conditions
filtered_df = df.loc[(df['Drawing Release Status only'] == '2.VOB Release') | (df['Drawing Release Status only'] == '3.Tooling Release')]
#Extract the 'Part Number' values from the filtered DataFrame
filtered_product_ids = (filtered_df['Part Number'].to_list())


# In[4]:


filtered_product_ids = [id.replace('-', '_') for id in filtered_product_ids]


# In[5]:


root = tk.Tk()
root.withdraw()

directory_path = fd.askdirectory(title='Select a folder')

if directory_path:
    var1 = []

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            var1.append(file_path)

#     for file_path in var1:
#         print(file_path)
# else:
#     print("No folder selected")


# In[6]:


df2=[]  
for i in var1:
    df2.append(os.path.basename(i).split('/')[-1].upper())

df_2 = []
for i in range(len(df2)):
    converted_list = re.sub(r'[^a-zA-Z0-9\s.]', '_', str(df2[i]))
    df_2.append(converted_list)


# In[7]:


filename_df = pd.DataFrame(df_2) 


# In[8]:


not_matching_list = []

for product_id in filtered_product_ids:
    matching = False
    for file_name in df_2:
        if product_id in file_name:
            matching = True
            break
    if not matching:
        product_id=product_id.replace('_','-')
        not_matching_list.append(product_id)


# In[9]:


a=[]
for i in range(len(not_matching_list)):
    matching_rows=df.loc[df['Part Number'] == not_matching_list[i]]
    for index in matching_rows.index:
        a.append(index)


# In[10]:


matches ={}
print('Processing')
for i in range(len(not_matching_list)):  
    for index, row in df.iterrows():
        if row['Part Number'] == not_matching_list[i]:
            if not_matching_list[i] in matches:
                matches[not_matching_list[i]].append(index)
            else:
                matches[not_matching_list[i]] = [index]


# In[ ]:


def save_csv():
    # Open a file save dialog to select the location and filename
    save_path = fd.asksaveasfilename(
        defaultextension='.csv',
        filetypes=(('CSV files', '*.csv'), ('All files', '*.*'))
    )

    if save_path:
        df_matches = pd.DataFrame({'Unmatched Part Number': list(matches.keys()), 'Index in E-BOM': list(matches.values())})
        df_matches.to_csv(save_path, index=False)  # Save DataFrame to CSV file at the selected location
        root.destroy()

root = tk.Tk()
root.title('Choose your file')
root.resizable(False, False)
root.geometry('300x150')

save_csv() 

root.mainloop()


# In[ ]:


number = 30
remaining_string = "Window will close automatically in " 
end_string= " seconds"
while number>0: 
    number2="{:2d}".format(number)
    #if(number==1):
        #end_string= " second"
        #print(remaining_string+ "{:2d}".format(number) + end_string, end='\r')
    print(f"{remaining_string} {number2} {'second ' if number == 1 else 'seconds'}", end='\r') 
    number -= 1
    time.sleep(1)


# In[ ]:




