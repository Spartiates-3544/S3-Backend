import tba
from tkinter import *
from tkinter import messagebox
import backend

width = 1920
height = 500

root = Tk()
root.geometry(f'{width}x{height}')
root.title('Robotics scouting tool')
frame = Frame(root)
frame.pack()

f_req = Frame(frame)
f_req.pack(side=LEFT)

bg = PhotoImage(file = 'ressources/bg.png')
bg_label = Label(f_req, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.pack()

# team_label = Label(f_req, text='Enter team number here...')
# team_label.pack(padx=3, pady=3)
# team_entry = Entry(f_req)
# team_entry.pack(padx=3, pady=10)
# team_entry.bind('<Return>', teamEnterEvent)

# def teamEnterEvent(event):
#     try:
#         tn = int(team_entry.get())
#     except:
#         raise Exception('Not an integer!')

# def displayTeamInfo(response):
#     popup = Toplevel(root)
#     popup.geometry('250x500')
#     popup.title('Team info')
    
#     info = tba.getTeamInfo(f'frc{tn}')
#     displayTeamInfo(info)

# team_name_label = Label(f_req)
# #team_name_label.config(width=200)
# team_name_label.pack(padx=3, pady=12)

def export_button_click():
    try:
        backend.generateExcel()
    except Exception as e:
        messagebox.showerror(title="Export", message=e)
    else:
        messagebox.showinfo(title="Export", message='Successfully exported data to excel!')

qrcode_button = Button(f_req, text='Scan QR Code', command= lambda: backend.scanAndDecode())
qrcode_button.pack(padx=3, pady=15)

export_button = Button(f_req, text='Export data to excel', command= lambda: export_button_click())
export_button.pack(padx=3, pady=16)


root.mainloop()
# r = tba.getEventInfo('2024qcmo')
# print(r.status_code)
# print(r.json()['name'])