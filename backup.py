import base64
import tkinter as tk
from tkinter import filedialog, messagebox
import time

import ecdsa


class ImageEncryptionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jemi's Image Cryptography System")

        self.master.configure(bg="white")

        self.label1 = tk.Label(master, text="Good Day!,Thank you for using Jemi's Image Cryptography System,", font=("Times New Roman", 25), bg="white",
                               foreground="black")
        self.label1.grid(row=1, column=1)
        self.label2 = tk.Label(master, text="Please generate your Public and Private Keys before Proceeding to encrypt!",
                               font=("Times New Roman", 25), bg="white",
                               foreground="black")
        self.label2.grid(row=2, column=1)
        self.generate_keys = tk.Button(master, text="Generate keys", fg="black", highlightbackground="white",
                                       font=("Times New Roman", 18),
                                       command=self.generate_keys)
        self.generate_keys.grid(row=3, column=1)

        self.label = tk.Label(master, text="Select a Medical image to encrypt or decrypt:", bg="white", font=("Times "
                                                                                                              "New "
                                                                                                              "Roman",
                                                                                                              18),
                              foreground="black")
        self.label.grid(row=4, column=1)

        self.encrypt_button = tk.Button(master, text="Encrypt Image", fg="black", highlightbackground="white",
                                        font=("Times New Roman", 18),
                                        command=self.encrypt_image)
        self.encrypt_button.grid(row=5, column=1)

        self.decrypt_button = tk.Button(master, text="Decrypt Image", fg="black", highlightbackground="white",
                                        font=("Times New Roman", 18),
                                        command=self.decrypt_image)
        self.decrypt_button.grid(row=6, column=1)

        self.public_key_Label = tk.Label(master, text="Enter Public Key:", bg="white", foreground="black",
                                         font=("Times New Roman", 18))
        self.public_key_Label.grid(row=7, column=1)
        self.public_key_entry = tk.Text(master, height="5", bg="Gray")
        self.public_key_entry.grid(row=8, column=1)
        self.private_key_Label = tk.Label(master, text="Enter Private Key:", bg="white", foreground="black",
                                          font=("Times New Roman", 18))
        self.private_key_Label.grid(row=9, column=1)
        self.private_key_entry = tk.Text(master, height="5", width=30, bg="Gray")
        self.private_key_entry.grid(row=10, column=1)

        self.exit_button = tk.Button(master, text="Exit System.", font=("Times New Roman", 18),
                                     fg="black", highlightbackground="white",
                                     command=master.quit)
        self.exit_button.grid(row=11, column=1)

        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(0, weight=0)

    def generate_keys(self):
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        self.private_key = sk.to_string().hex()
        self.public_key = vk.to_string().hex()

        messagebox.showinfo("Keys Generated",
                            f"Public Key: {self.public_key}\nPrivate Key: {self.private_key}")

    def load_keys(self):
        self.public_key = self.public_key_entry.get("1.0", "end-1c")
        self.private_key = self.private_key_entry.get("1.0", "end-1c")

    def encrypt_image(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                              filetypes=(
                                                  ("Image files", "*.png *.jpg *.jpeg *.bmp"), ("all files", "*.*")))
        if filename:
            self.load_keys()
            with open(filename, "rb") as file:
                image_bytes = file.read()
            start_time = time.time()
            sk = ecdsa.SigningKey.from_string(bytes.fromhex(self.private_key), curve=ecdsa.SECP256k1)
            signature = sk.sign(image_bytes)
            end_time = time.time()
            encryption_time = end_time - start_time
            print(encryption_time)

            encrypted_image = base64.b64encode(signature + image_bytes)

            with open("encrypted_image.enc", "wb") as file:
                file.write(encrypted_image)

            messagebox.showinfo("Encryption Complete", "Image has been encrypted successfully!")

    def decrypt_image(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select Encrypted Image",
                                              filetypes=(("Encrypted image files", "*.enc"), ("all files", "*.*")))
        if filename:
            self.load_keys()
            with open(filename, "rb") as file:
                encrypted_image = base64.b64decode(file.read())

            signature = encrypted_image[:64]

            vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.public_key), curve=ecdsa.SECP256k1)
            start_time = time.time()
            try:
                vk.verify(signature, encrypted_image[64:])
                end_time = time.time()
                decryption_time = end_time - start_time
                print(decryption_time)
                image_bytes = encrypted_image[64:]

                with open("decrypted_image.png", "wb") as file:
                    file.write(image_bytes)

                messagebox.showinfo("Decryption Complete", "Image has been decrypted successfully!")
            except ecdsa.BadSignatureError:
                messagebox.showerror("Decryption Error", "Invalid signature. Decryption failed.")


def main():
    root = tk.Tk()
    ImageEncryptionApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
