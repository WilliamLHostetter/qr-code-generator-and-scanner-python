'''
Python implementation of a QR Code Generator with a GUI.

'''
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import ctypes # to get screen size
import qrcode
import os



image_size_list = ["Small (120x120)", "Medium (230x230)", "Large (350x350)"]
image_size_menu_default = "Large (350x350)"
error_correction_list = ["L: About 7% or less errors can be corrected.", 
                        "M: About 15% or less errors can be corrected.", 
                        "Q: About 25% or less errors can be corrected.", 
                        "H: About 30% or less errors can be corrected"]
error_correction_menu_default = "L: About 7% or less errors can be corrected."



def generate_qr_code_image(text: str, 
                            image_size_selection: str, 
                            error_correction_selection: str, 
                            output_filename: str) -> tk.PhotoImage:
    
    if image_size_selection == image_size_list[0]: # Small (120x120)
        image_size = 120
    elif image_size_selection == image_size_list[1]: # Medium (230x230)
        image_size = 230
    elif image_size_selection == image_size_list[2]: # Large (350x350)
        image_size = 350
    else:
        image_size = 350

    if error_correction_selection == error_correction_list[0]:
        error_correction = qrcode.constants.ERROR_CORRECT_L #(Approx 7%)
    elif error_correction_selection == error_correction_list[1]:
        error_correction = qrcode.constants.ERROR_CORRECT_M # (Approx 15%)
    elif error_correction_selection == error_correction_list[2]:
        error_correction = qrcode.constants.ERROR_CORRECT_Q # (Approx 25%)
    elif error_correction_selection == error_correction_list[3]:
        error_correction = qrcode.constants.ERROR_CORRECT_H # (Approx 30%)
    else:
        error_correction = qrcode.constants.ERROR_CORRECT_L #(Approx 7%)
    
    # Creating an instance of QRCode class
    qr = qrcode.QRCode(version=1, box_size=6, border=4, error_correction=error_correction)
    # Adding text data to the instance
    qr.add_data(text)
    # setting fit=True in the make() method ensures that the entire dimension of 
    # the QR code is utilized, even if the input data could fit into fewer boxes.            
    qr.make(fit=True)
    # output filename for the QRCode
    output_filename = os.path.basename(output_filename) + '.png'
    # make the QR code image
    qrcode_image = qr.make_image(fill_color = 'black', back_color = 'white') # type <class 'qrcode.image.pil.PilImage'>
    # resize image according to input selection
    width, height = qrcode_image.size
    print(f"resizing output image from {width}x{height} to {image_size}x{image_size}")
    qrcode_image_resized = qrcode_image.resize((image_size, image_size))
    # saving the QR code image
    qrcode_image_resized.save(output_filename) # using PIL
    # opening the qrcode image file
    output_image = tk.PhotoImage(file=output_filename)
    return output_image


def submit_text(input_window: tk.Tk, 
                scrolledText: tk.scrolledtext.ScrolledText, 
                combo_error_correction_menu: tk.ttk.Combobox, 
                combo_image_size_menu: tk.ttk.Combobox, 
                output_filename_entry_var: tk.StringVar) -> None:
    output_image = None
    input_text = scrolledText.get('1.0', 'end-1c')
    if not input_text:
        error_msg = "Enter text to convert to QR code"
        messagebox.showerror("Input Error", error_msg)
        return None
    
    output_filename = output_filename_entry_var.get()
    if not output_filename:
        output_filename = "output_image"
    
    image_size_selection = combo_image_size_menu.get()
    error_correction_selection = combo_error_correction_menu.get()
    
    output_image = generate_qr_code_image(input_text, image_size_selection, error_correction_selection, output_filename)
    
    results_window = tk.Toplevel(input_window)
    results_window.resizable(height=False, width=False)
    results_window_width = 400
    results_window_height = 400
    results_window.geometry(f"{results_window_width}x{results_window_height}")
    # Calculate the position of the window to center it
    x = (results_window.winfo_screenwidth() - results_window_width) // 2
    y = (results_window.winfo_screenheight() - results_window_height) // 2
    results_window.geometry(f"+{x}+{y}")
    results_window.title("Output")
    image_label = tk.Label(results_window, image=output_image)
    image_label.image = output_image
    # Place the frame and the image within the frame using grid
    image_label.grid(row=0, column=0, pady=10)
    # Configure rows and columns to take up all available space
    results_window.grid_rowconfigure(0, weight=1)
    results_window.grid_columnconfigure(0, weight=1)


def main() -> None:
    user32 = ctypes.windll.user32
    (screensize_width, screensize_height) = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print("(screensize_width, screensize_height) =", (screensize_width, screensize_height))
    input_window = tk.Tk()
    input_window.title("QR Code Generator")
    input_window.iconbitmap(input_window, 'QR_Code_Generator.ico') # adding the window's icon
    input_window_width = int(0.3*screensize_width)
    input_window_height = int(0.5*screensize_height)
    print("(input_window_width, input_window_height) =", (input_window_width,input_window_height))
    input_window.geometry(f"{input_window_width}x{input_window_height}")
    # Calculate the position of the window to center it
    x = (input_window.winfo_screenwidth() - input_window_width) // 2
    y = (input_window.winfo_screenheight() - input_window_height) // 2
    input_window.geometry(f"+{x}+{y}")
    
    tk.Label(input_window, text="Enter text to for QR Code", font=("Segoe UI", 14)).grid(row=1, pady=(10,0))
    scrolledText = scrolledtext.ScrolledText(input_window, wrap=tk.WORD, width=60, height=10) # width and height units are number of characters
    scrolledText.grid(row=2, column=0, sticky="nsew", padx=10)
    input_window.columnconfigure(0, weight=1)
    
    # QR Code Image Size Dropdown Menu
    tk.Label(input_window, text="QR Code Image Size", font=("Segoe UI", 14)).grid(row=3, pady=(5,0))
    combo_image_size_menu = ttk.Combobox(state="readonly", values=image_size_list)
    combo_image_size_menu.set(image_size_menu_default)
    combo_image_size_menu.grid(row=4, column=0, pady=5)
    max_width_in_num_char = max(len(item) for item in image_size_list)
    combo_image_size_menu.configure(width=max_width_in_num_char)

    # Error Correction Dropdown Menu
    # L: About 7% or less errors can be corrected.
    # M: About 15% or less errors can be corrected.
    # Q: About 25% or less errors can be corrected.
    # H: About 30% or less errors can be corrected.
    tk.Label(input_window, text="Error Correction", font=("Segoe UI", 14)).grid(row=5, pady=(10,0))
    combo_error_correction_menu = ttk.Combobox(state="readonly", values=error_correction_list)
    combo_error_correction_menu.set(error_correction_menu_default)
    combo_error_correction_menu.grid(row=6, column=0, pady=5)
    max_width_in_num_char = max(len(item) for item in error_correction_list)
    combo_error_correction_menu.configure(width=max_width_in_num_char)
    
    # Output filename
    output_filename_entry_var = tk.StringVar()
    tk.Label(input_window, text="Output Filename", font=("Segoe UI", 14)).grid(row=9, pady=(10,0))
    output_filename_entry = tk.Entry(input_window, font=("Arial", 11), textvariable=output_filename_entry_var, justify='center', width=40)
    output_filename_entry.grid(row=10, column=0)
        
    btn = tk.Button(input_window, text="Submit", command=lambda: submit_text(input_window, scrolledText, combo_error_correction_menu, combo_image_size_menu, output_filename_entry_var))
    btn.grid(row=11, column=0, pady=(50,20))
    
    # Right click menu for copy and select all
    right_click_menu = tk.Menu(scrolledText, tearoff=0)
    # Menu options
    right_click_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: scrolledText.event_generate("<<Copy>>"))
    right_click_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: scrolledText.event_generate("<<Paste>>"))
    right_click_menu.add_command(label="Select All", accelerator="Ctrl+A", command=lambda: scrolledText.event_generate("<<SelectAll>>"))
    # Make menu pop up on right click event
    scrolledText.bind("<Button -3>", lambda event: right_click_menu.tk_popup(event.x_root, event.y_root))
    
    input_window.mainloop()


if __name__ == "__main__":
    main()