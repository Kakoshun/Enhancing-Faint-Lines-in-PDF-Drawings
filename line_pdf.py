# Betounis Robotics
# kakoshund@yahoo.com
import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, simpledialog

def enhance_black(img, expansion_factor):
    """Ενισχύει τα μαύρα pixels επεκτείνοντάς τα στα γειτονικά pixels ανάλογα με τον συντελεστή."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Μετατροπή σε grayscale
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)  # Ανίχνευση μαύρων pixels
    
    # Ορίζουμε έναν πυρήνα που επεκτείνει τα μαύρα pixel με βάση τον expansion_factor
    kernel_size = (2 * expansion_factor + 1, 2 * expansion_factor + 1)
    kernel = np.ones(kernel_size, np.uint8)
    expanded_black = cv2.dilate(binary, kernel, iterations=1)  # Διαστολή των μαύρων pixel
    
    # Αντικατάσταση των νέων μαύρων περιοχών στην αρχική εικόνα
    img[expanded_black == 255] = [0, 0, 0]  # Τα επιπλέον μαύρα γίνονται μαύρα στην εικόνα
    return img

def pdf_to_images(pdf_path, expansion_factor):
    """Μετατρέπει το PDF σε εικόνες, ενισχύει το μαύρο και αποθηκεύει νέο PDF."""
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(len(doc)):
        pix = doc[page_num].get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Μετατροπή της εικόνας σε OpenCV format
        img_cv = np.array(img)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

        # Ενίσχυση του μαύρου
        enhanced_img = enhance_black(img_cv, expansion_factor)

        # Επαναφορά σε PIL format
        images.append(Image.fromarray(cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2RGB)))

    return images

def save_images_as_pdf(images):
    """Αποθηκεύει τις εικόνες ως νέο PDF αρχείο."""
    output_pdf_path = filedialog.asksaveasfilename(title="Αποθήκευση ως", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if output_pdf_path:
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
        print(f"Το νέο PDF αποθηκεύτηκε στο: {output_pdf_path}")

def select_file():
    """Ανοίγει παράθυρο διαλόγου για την επιλογή του PDF αρχείου."""
    global pdf_path
    pdf_path = filedialog.askopenfilename(title="Επιλέξτε PDF αρχείο", filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        print(f"Επιλέχθηκε αρχείο: {pdf_path}")

def start_processing():
    """Ξεκινά την επεξεργασία του PDF."""
    if not pdf_path:
        print("Δεν επιλέχθηκε αρχείο.")
        return
    
    expansion_factor = simpledialog.askinteger("Ενίσχυση μαύρου", "Δώστε επίπεδο ενίσχυσης (1 - 10):", minvalue=1, maxvalue=10)
    if not expansion_factor:
        print("Δεν επιλέχθηκε ποσοστό.")
        return
    
    enhanced_images = pdf_to_images(pdf_path, expansion_factor)
    save_images_as_pdf(enhanced_images)

def close_app():
    """Κλείνει την εφαρμογή."""
    root.destroy()

# Δημιουργία κύριου παραθύρου
root = tk.Tk()
root.title("Ενίσχυση Μαύρου σε PDF")
root.geometry("400x200")

pdf_path = ""

btn_select = tk.Button(root, text="Επιλογή Αρχείου PDF", command=select_file)
btn_select.pack(pady=10)

btn_process = tk.Button(root, text="Εκκίνηση Επεξεργασίας", command=start_processing)
btn_process.pack(pady=10)

btn_exit = tk.Button(root, text="Έξοδος", command=close_app)
btn_exit.pack(pady=10)

root.mainloop()
