from  tkinter import *
from customtkinter import *
import qrcode
import string

from tkinter import filedialog
import secrets

import customtkinter
from typing import Union, Callable


class CTkSpinbox(customtkinter.CTkFrame):
   def __init__(self, *args,
                width: int = 95,
                height: int = 32,
                from_,
                to,
                step_size= 1,
                command: Callable = None,
                **kwargs):
      super().__init__(*args, width=width, height=height, **kwargs)

      self.from_ = from_
      self.to = to
      self.step_size = step_size
      self.command = command



      self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
      self.grid_columnconfigure(1, weight=1)  # entry expands

      self.subtract_button = customtkinter.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                                     command=self.subtract_button_callback)
      self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

      self.entry = customtkinter.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
      self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

      self.add_button = customtkinter.CTkButton(self, text="+", width=height - 6, height=height - 6,
                                                command=self.add_button_callback)
      self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

      # default value
      self.entry.insert(0, str(from_))

   def add_button_callback(self):
      if self.command is not None:
         self.command()
      try:
         value = int(self.entry.get()) + self.step_size
         if value > self.to:
            value = self.from_
         self.entry.delete(0, "end")
         self.entry.insert(0, value)
      except ValueError:
         return

   def subtract_button_callback(self):
      if self.command is not None:
         self.command()
      try:
         value = int(self.entry.get()) - self.step_size
         if value < self.from_:
            value = self.to
         self.entry.delete(0, "end")
         self.entry.insert(0, value)
      except ValueError:
         return

   def get(self) -> Union[int, None]:
      try:
         return int(self.entry.get())
      except ValueError:
         return None

   def set(self, value: int):
      self.entry.delete(0, "end")
      self.entry.insert(0, str(value))


def modern_window(title):
   set_appearance_mode("dark")
   app = CTk()
   app.title(title)
   canvas = CTkScrollableFrame(app, orientation="vertical")
   canvas.pack(fill='both', expand=True)
   return app, canvas


def new_window(name):
   screen = Tk()
   screen.title(name)
   canvas = Canvas(screen)
   scrollbar = Scrollbar(screen, orient="vertical")
   scrollbar.config(command=canvas.yview)
   canvas.configure(yscrollcommand=scrollbar.set)
   frame = Frame(canvas)
   canvas.create_window((0, 0), window=frame, anchor='nw')
   scrollbar.pack(side='right', fill='y')
   canvas.pack(side='left', fill='both', expand=True)
   return screen, canvas, frame

def Qrcode(data):
    folder_path = filedialog.askdirectory(initialdir="C:/Users/yasse/OneDrive/Pictures")
    # Generate the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    with open(f"{folder_path}/qrcode.jpeg", "wb") as file_path:
       img.save(file_path, "JPEG")


def generate_secret_code():
   alphabet = string.ascii_letters + string.digits
   secret_code = ''.join(secrets.choice(alphabet) for i in range(48))
   return secret_code