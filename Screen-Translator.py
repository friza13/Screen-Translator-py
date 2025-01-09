from PIL import ImageGrab
import pytesseract
from tkinter import Tk, Canvas, Toplevel, Label, messagebox, Button
from deep_translator import GoogleTranslator

# Konfigurasi path Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenCaptureApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Translator")
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.capture_area = None

        # Tombol GUI utama
        self.select_button = Button(master, text="Select Area", command=self.select_area, width=20)
        self.select_button.pack(pady=10)

        self.translate_button = Button(master, text="Translate", command=self.capture_and_translate, width=20)
        self.translate_button.pack(pady=10)

    def select_area(self):
        # Jendela untuk memilih area
        selection_window = Tk()
        selection_window.attributes('-fullscreen', True)
        selection_window.attributes('-alpha', 0.3)  # Transparansi untuk layar penuh
        selection_window.config(cursor="cross")

        canvas = Canvas(selection_window, bg="black")
        canvas.pack(fill="both", expand=True)

        def on_button_press(event):
            self.start_x = selection_window.winfo_pointerx()
            self.start_y = selection_window.winfo_pointery()
            self.rect = canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

        def on_mouse_drag(event):
            current_x = selection_window.winfo_pointerx()
            current_y = selection_window.winfo_pointery()
            canvas.coords(self.rect, self.start_x, self.start_y, current_x, current_y)

        def on_button_release(event):
            current_x = selection_window.winfo_pointerx()
            current_y = selection_window.winfo_pointery()

            if current_x < self.start_x:
                self.start_x, current_x = current_x, self.start_x
            if current_y < self.start_y:
                self.start_y, current_y = current_y, self.start_y

            self.capture_area = (self.start_x, self.start_y, current_x, current_y)
            selection_window.destroy()

        canvas.bind("<ButtonPress-1>", on_button_press)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_button_release)
        selection_window.mainloop()

    def capture_and_translate(self, target_lang="id"):
        if not self.capture_area:
            messagebox.showerror("Error", "No area selected.")
            return

        try:
            screenshot = ImageGrab.grab(self.capture_area)
            text = pytesseract.image_to_string(screenshot, lang='eng', config='--psm 6')

            print(f"Extracted text: '{text}'")  # Debugging

            if not text.strip():
                print("No text found for translation.")  # Debugging
                messagebox.showinfo("Info", "No text found in the selected area.")
                return

            translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)

            print(f"Translated text: '{translated_text}'")  # Debugging

            if not translated_text.strip():
                messagebox.showerror("Error", "Translation failed or empty text.")
                return

            # Debugging untuk teks sebelum ditampilkan
            print(f"Text for GUI display: '{translated_text}'")

            # Membuat jendela hasil
            print("Creating result window...")  # Debugging
            result_window = Toplevel(self.master)
            result_window.title("Translated Text")
            result_window.attributes('-topmost', True)  # Pastikan muncul di atas
            result_label = Label(result_window, text=translated_text, wraplength=800, justify="left", padx=10, pady=10)
            result_label.pack(fill="both", expand=True)
            result_window.update_idletasks()  # Perbarui jendela
            result_window.deiconify()
            result_window.lift()
            print("Result window created.")  # Debugging
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def main():
    root = Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
