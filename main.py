import logging
import tkinter as tk
from tkinter import filedialog, ttk

from local_agent import decode, encode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s] - %(message)s",
    handlers=[logging.FileHandler("./logs/stegano.log"), logging.StreamHandler()],
)


def browse_file(entry):
    try:
        file_path = filedialog.askopenfilename()
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
    except Exception as e:
        logging.error("Could not load entry file: %s", str(e))


def encode_message():
    source_file = source_entry.get()
    destination_file = destination_entry.get()
    message = encode_message_entry.get("1.0", "end-1c")

    encode(source_file, destination_file, message)

    encode_info_text.config(state=tk.NORMAL)
    encode_info_text.delete(1.0, tk.END)
    encode_info_text.insert(tk.END, "Message encoded successfully.")
    encode_info_text.config(state=tk.DISABLED)


def decode_message():
    source_file = decode_entry.get()

    decoded_message = decode(source_file)

    decode_info_text.config(state=tk.NORMAL)
    decode_info_text.delete(1.0, tk.END)
    decode_info_text.insert(tk.END, decoded_message)
    decode_info_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Decoupled steganography")

    notebook = ttk.Notebook(root)

    # Encode tab
    encode_frame = ttk.Frame(notebook)
    notebook.add(encode_frame, text="Encode")

    source_label = ttk.Label(encode_frame, text="Source File:")
    source_label.grid(row=0, column=0, padx=10, pady=10)
    source_entry = ttk.Entry(encode_frame, width=40)
    source_entry.grid(row=0, column=1, padx=10, pady=10)
    source_button = ttk.Button(
        encode_frame, text="Browse", command=lambda: browse_file(source_entry)
    )
    source_button.grid(row=0, column=2, padx=10, pady=10)

    destination_label = ttk.Label(encode_frame, text="Destination File:")
    destination_label.grid(row=1, column=0, padx=10, pady=10)
    destination_entry = ttk.Entry(encode_frame, width=40)
    destination_entry.grid(row=1, column=1, padx=10, pady=10)
    destination_button = ttk.Button(
        encode_frame, text="Browse", command=lambda: browse_file(destination_entry)
    )
    destination_button.grid(row=1, column=2, padx=10, pady=10)

    message_label = ttk.Label(encode_frame, text="Message:")
    message_label.grid(row=2, column=0, padx=10, pady=10)
    encode_message_entry = tk.Text(encode_frame, height=5, width=40)
    encode_message_entry.grid(row=2, column=1, padx=10, pady=10)

    encode_button = ttk.Button(encode_frame, text="Encode", command=encode_message)
    encode_button.grid(row=3, column=2, padx=10, pady=10)

    message_label = ttk.Label(encode_frame, text="Info:")
    encode_info_text = tk.Text(encode_frame, height=2, width=40, state=tk.DISABLED)
    encode_info_text.grid(row=3, column=1, padx=10, pady=10)

    # Decode tab
    decode_frame = ttk.Frame(notebook)
    notebook.add(decode_frame, text="Decode")

    source_label = ttk.Label(decode_frame, text="Source File:")
    source_label.grid(row=0, column=0, padx=10, pady=10)
    decode_entry = ttk.Entry(decode_frame, width=40)
    decode_entry.grid(row=0, column=1, padx=10, pady=10)
    source_button = ttk.Button(
        decode_frame, text="Browse", command=lambda: browse_file(decode_entry)
    )
    source_button.grid(row=0, column=2, padx=10, pady=10)

    message_label = ttk.Label(decode_frame, text="Message:")
    message_label.grid(row=2, column=0, padx=10, pady=10)
    decode_info_text = tk.Text(decode_frame, height=5, width=40)
    decode_info_text.grid(row=2, column=1, padx=10, pady=10)

    encode_button = ttk.Button(decode_frame, text="Decode", command=decode_message)
    encode_button.grid(row=2, column=2, padx=10, pady=10)

    # Help Tab
    help_frame = ttk.Frame(notebook)
    notebook.add(help_frame, text="Help")

    notebook.pack()

    root.mainloop()
