from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image
from stegano import lsb

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Steganography App')
        self.master.geometry("500x400")

        self.title_label = Label(self.master, text="Image Steganography", font=("Helvetica", 24))
        self.title_label.pack(pady=10)

        self.encode_button = Button(self.master, text="Encode", font=("Helvetica", 16), command=self.encode)
        self.encode_button.pack(pady=20)

        self.decode_button = Button(self.master, text="Decode", font=("Helvetica", 16), command=self.decode)
        self.decode_button.pack(pady=20)

        self.exit_button = Button(self.master, text="Exit", font=("Helvetica", 16), command=self.master.destroy)
        self.exit_button.pack(pady=20)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select File",
                                               filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("all files", "*.*")))
        return file_path

    def encode(self):
        file_path = self.open_file_dialog()
        if file_path:
            secret_text = simpledialog.askstring("Input", "Enter the secret text:")
            if secret_text:
                secret_key = simpledialog.askinteger("Input", "Enter the secret key:")
                if secret_key is not None:
                    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                    if output_path:
                        lsb.hide(file_path, f"{secret_text}||{secret_key}").save(output_path)
                        messagebox.showinfo("Success", "Image encoded successfully!")

    def decode(self):
        file_path = self.open_file_dialog()
        if file_path:
            try:
                encoded_text = lsb.reveal(file_path)
                decoded_data = encoded_text.split("||")
                secret_text = decoded_data[0]
                secret_key = decoded_data[1]
                user_key = simpledialog.askinteger("Input", "Enter the secret key:")
                if user_key is not None:
                    if user_key == int(secret_key):
                        messagebox.showinfo("Decoded Text", f"The hidden text is:\n\n{secret_text}")
                    else:
                        messagebox.showwarning("Error", "Wrong key. Unable to reveal the message.")
            except ValueError:
                messagebox.showwarning("Error", "No hidden text found in the selected image.")

if __name__ == "__main__":
    root = Tk()
    app = SteganographyApp(root)
    root.mainloop()
