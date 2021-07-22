import qrcode
import time
from tkinter import *
from tkinter import messagebox
import sqlite3
import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt   

def qr_page():
    i_nama = e_nama.get()
    i_nohp = e_nohp.get()
    i_email = e_email.get()
    i_kota = (e_kota.get()).upper()    
    
    if len(i_nama)<1 or len(i_nohp)<1 or len(i_email)<1 or len(i_kota)<1:
        messagebox.showwarning('Warning!','There is empty data. Please fill in first!')
    else:
        i_nama = e_nama.get()
        i_nohp = e_nohp.get()
        i_email = e_email.get()
        i_kota = (e_kota.get()).upper()
        conn = sqlite3.connect('registrasi.db')
        c = conn.cursor()
        c.execute('INSERT INTO pengguna (nama,nohp,email,kota) VALUES (?,?,?,?)', (i_nama,i_nohp,i_email,i_kota))
        conn.commit()
        conn.close()
        messagebox.showinfo('Info','Registration Successful.')
    
        def QRCode():
            qr_code = e_data.get()
            try:
                img = qr_code.split('.')
                if qr_code.endswith('gmail.com'):
                    fileName = img[1]+'.jpeg'
                else:
                    fileName = img[0]+'.jpeg'
            except:
                fileName = qr_code

            if len(qr_code)<1:
                messagebox.showwarning('Warning!','Please enter the QR Code data first!')
                e_data.config(bg='white')
                t_data.config(text='Error when creating QR Code!',image='',width=50,height=10,fg='black')
            else:
                img = qrcode.make(qr_code)
                img.save(fileName)
                root.photo = PhotoImage(file=fileName)
                t_data.config(image=root.photo,text='QR Code generated successfully!',fg='black',compound=TOP,width=315,height=300)
                messagebox.showinfo('Success','QR code " '+fileName+' " saved successfully!\n\tin the specified folder location!')
        
        def reset():
            e_data.delete(0,END)
            e_data.config(bg='white')
            t_data.config(image='',text='',width=60,height=20)
        
        popup = Toplevel()
        popup.grab_set()
        popup.title('Simple QR Code Program')
        popup.config(bg='white')
        popup.geometry('520x550')
        popup.resizable(0,0)
        
        Tops = Frame(popup,width = 520,height=10)
        Tops.pack(side=BOTTOM)

        lblinfo_regis = Label(Tops, font=( 'forte' ,15, ),text=localtime,fg="black",bg= "white",anchor=W)
        lblinfo_regis.grid(row=1,column=0)

        l_qr = Label(popup,text='Quick Response Code',bg='black',fg='white',font=('stencil',25,'bold','italic'))
        l_qr.pack(side=TOP,fill=BOTH)
        t_data = Label(popup,bg= "white", text="Enter QR Code Data:",font=('impact',12))
        t_data.place(x=10,y=65)
        e_data = Entry(popup,fg='black',bd=5,width=50)
        e_data.place(x=180,y=65)
        getQRCode = Button(popup,text='GENERATE QR CODE',bg='black',fg='white',activebackground='black',width=20,activeforeground='yellow',command=QRCode)
        getQRCode.place(x=340,y=105)
        b_statpage = Button(popup,text='VIEW STATISTICS',bg='yellow',fg='black',activebackground='black',width=20,activeforeground='red',command=stat_page)
        b_statpage.place(x=180,y=105)

        resetApp= Button(popup,text='RESET QR CODE',bg='black',fg='white',width=25,bd=5,command=reset)
        resetApp.place(x=165,y=475)
        t_data = Label(popup,image='',bg='white')
        t_data.place(x=100,y=170)


def stat_page():
    
    
    statpage = Toplevel()
    statpage.grab_set()
    statpage.title('Simple QR Code Program')
    statpage.config(bg='white')
    statpage.geometry('520x550')
    statpage.resizable(0,0)
    
    statpage_top = Frame(statpage,width = 520,height=10)
    statpage_top.pack(side=BOTTOM)
    
    lblinfo_regis = Label(statpage_top, font=( 'forte' ,15, ),text=localtime,fg="black",bg= "white",anchor=W)
    lblinfo_regis.grid(row=1,column=0)

    l_qr = Label(statpage,text='User Statistics',bg='black',fg='white',font=('stencil',25,'bold','italic'))
    l_qr.pack(side=TOP,fill=BOTH)
    
    conn = sqlite3.connect('registrasi.db')
    c = conn.cursor()
    c.execute('SELECT kota,COUNT(*) FROM pengguna GROUP BY kota ORDER BY COUNT(*) DESC')
    c_result = c.fetchall()
    rows = c_result[0]
    total_rows = len(c_result)
    total_columns = len(rows)
    #print(c_result)
    #print(len(c_result))
    #print(rows)
    
    df = pd.DataFrame(c_result, columns= ['kota', 'jumlah'])
    df.sort_values(by=['jumlah'], inplace=True, ascending=False)
    #print(df)

    statpage_frame = Frame(statpage,width=520,height=550, relief=RIDGE, bd=6)
    statpage_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    for row in c_result:
        print("Kota: ", row[0])
        print("Jumlah: ", row[1], "pengguna")
        c.close()
    
    for i in range(total_rows):
        for j in range(total_columns):
            e = Entry(statpage_frame, width=18, fg='black',font=('Arial',14,'bold'))
            e.grid(row=i, column=j)
            e.insert(END, c_result[i][j])


#DESAIN GUI   
root = Tk()
root.title('Simple QR Code Program')
root.config(bg='white')
root.geometry('520x550')
root.resizable(0,0)

Tops = Frame(root,width = 520,height=10)
Tops.pack(side=BOTTOM)

localtime=time.asctime(time.localtime(time.time()))
lblinfo = Label(Tops, font=( 'forte' ,15, ),text=localtime,fg="black",bg= "white",anchor=W)
lblinfo.grid(row=1,column=0)


appName = Label(root,text='REGISTRATION',bg='black',fg='white',font=('stencil',25,'bold','italic'))
appName.pack(side=TOP,fill=BOTH)

t_nama = Label(root,bg= "white", text="Name:",font=('impact',12))
t_nama.place(x=10,y=50)
e_nama = Entry(root,fg='black',bd=5,width=63)
e_nama.place(x=115,y=50)

t_nohp = Label(root,bg= "white", text="Phone Number:",font=('impact',12))
t_nohp.place(x=10,y=100)
e_nohp = Entry(root,fg='black',bd=5,width=63)
e_nohp.place(x=115,y=100)

t_email = Label(root,bg= "white", text="Email:",font=('impact',12))
t_email.place(x=10,y=150)
e_email = Entry(root,fg='black',bd=5,width=63)
e_email.place(x=115,y=150)

t_kota = Label(root,bg= "white", text="City:",font=('impact',12))
t_kota.place(x=10,y=200)
e_kota = Entry(root,fg='black',bd=5,width=63)
e_kota.place(x=115,y=200)

b_daftar = Button(root,text='REGISTER',bg='black',fg='white',activebackground='black',width=20,activeforeground='yellow',command=qr_page)
b_daftar.place(x=350,y=250)

root.mainloop()