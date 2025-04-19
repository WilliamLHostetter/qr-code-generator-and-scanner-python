'''
Python implementation of a QR Code Scanner with a GUI.

'''
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import ctypes # to get screen size
import os
from tkinter import filedialog
import cv2



def scan_qr_code(image_filepath):
    try:
        # reading the image file with cv2 
        qr_img = cv2.imread(f"{image_filepath}")  
        # using the QRCodeDetector() function  
        qr_detector = cv2.QRCodeDetector()  
        # using the detectAndDecode() function detect and decode the QR code
        data, pts, st_code = qr_detector.detectAndDecode(qr_img)  
        return data
    except: # this catches any errors that might occur
        # displaying an error message
        error_msg = "Error could be the wrong image file. Make sure the image file is a valid QRCode"
        messagebox.showerror("Input Error", error_msg)
        return None

    
def get_image(input_window, image_frame, file_entry):
    image_filepath = filedialog.askopenfilename(initialdir=os.getcwd())
    print("image_filepath =", image_filepath)
    
    if image_filepath == '':
        error_msg = "Please provide a QR Code image file to scan"
        messagebox.showerror("Input Error", error_msg)
        return None
    
    # deleting every data from the file_entry
    file_entry.delete(0, 'end')
    # inserting the file in the file_entry
    file_entry.insert(0, image_filepath)

    qr_code_image = tk.PhotoImage(file=image_filepath)
    image_label = tk.Label(image_frame, image=qr_code_image)
    image_label.image = qr_code_image
    image_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Configure rows and columns to take up all available space
    image_label.grid_rowconfigure(0, weight=1)
    image_label.grid_columnconfigure(0, weight=1)
    
    data = scan_qr_code(image_filepath)
    
    tk.Label(input_window, text="QR Code Data", font=("Segoe UI", 14)).grid(row=3, column=0, pady=(25,0), columnspan=2, sticky="", )
    scrolledText = scrolledtext.ScrolledText(input_window, width=60, height=5) # width and height units are number of characters
    scrolledText.insert(tk.INSERT, data)
    scrolledText.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=(10, 10))

    # Right click menu for copy and select all
    menu = tk.Menu(scrolledText, tearoff=0)
    # Menu options
    menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: scrolledText.event_generate("<<Copy>>"))
    menu.add_command(label="Select All", accelerator="Ctrl+A", command=lambda: scrolledText.event_generate("<<SelectAll>>"))
    # Make menu pop up on right click event
    scrolledText.bind("<Button -3>", lambda event: menu.tk_popup(event.x_root, event.y_root))


def main() -> None:
    user32 = ctypes.windll.user32
    (screensize_width, screensize_height) = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print("(screensize_width, screensize_height) =", (screensize_width, screensize_height))
    input_window = tk.Tk()
    input_window.title("QR Code Scanner")
    input_window.iconbitmap(input_window, 'QR_Code_Scanner.ico') # adding the window's icon
    input_window_width = int(0.3*screensize_width)
    input_window_height = int(0.6*screensize_height)
    print("(input_window_width, input_window_height) =", (input_window_width,input_window_height))
    input_window.geometry(f"{input_window_width}x{input_window_height}")
    # Calculate the position of the window to center it
    x = (input_window.winfo_screenwidth() - input_window_width) // 2
    y = (input_window.winfo_screenheight() - input_window_height) // 2
    input_window.geometry(f"+{x}+{y}")

    input_window.columnconfigure(0, weight=1)
    input_window.columnconfigure(1, weight=1)
    
    tk.Label(input_window, text="QR Code Image Preview", font=("Segoe UI", 14)).grid(row=0, column=0, pady=(5,0), columnspan=2, sticky="", )
    image_frame = tk.Frame(input_window, width=350, height=350, bg="white")
    image_frame.grid(row=1, column=0, columnspan=2, sticky="", padx=5, pady=(10, 30))
    
    file_entry = ttk.Entry(input_window, width=60, style='TEntry')
    file_entry.grid(row=2, column=0, sticky="ew", padx=(15,0))
    
    browse_button = ttk.Button(input_window, text='Browse', style='TButton', command=lambda: get_image(input_window, image_frame, file_entry))
    browse_button.grid(row=2, column=1, sticky="ew", padx=(0,15))
    
    
    input_window.mainloop()


if __name__ == "__main__":
    main()
