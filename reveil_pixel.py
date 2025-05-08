import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import random

def select_image():
    global img, img_label, img_preview, is_image_hidden, img_width, img_height, revealed_image, revealed_img_tk, scaled_img, scale_factor
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img_width, img_height = img.size

        # Calcul du facteur d'échelle pour l'image à afficher
        max_display_width = app.winfo_screenwidth() - 100  # Marge pour éviter le dépassement
        max_display_height = app.winfo_screenheight() // 2  # Utilisation de la moitié de l'écran pour l'image

        scale_factor = min(max_display_width / img_width, max_display_height / img_height)
        display_width = int(img_width * scale_factor)
        display_height = int(img_height * scale_factor)

        scaled_img = img.resize((display_width, display_height))
        img_preview = ImageTk.PhotoImage(scaled_img)
        img_label.config(image=img_preview)
        img_label.image = img_preview
        pixel_count_label.config(text=f"Nombre de pixels total: {img_width * img_height}")
        img_label.config(borderwidth=2, relief="solid")
        is_image_hidden = False  # Image est visible au départ

        # Réinitialise l'image révélée
        revealed_image = Image.new('RGB', (img_width, img_height), color='white')
        revealed_img_tk = ImageTk.PhotoImage(revealed_image.resize((display_width, display_height)))
        canvas.config(width=display_width, height=display_height)
        canvas.create_image(0, 0, anchor="nw", image=revealed_img_tk)

        # Réinitialise les pixels révélés
        revealed_pixels.clear()

def toggle_image_visibility(event=None):
    global is_image_hidden
    if not is_image_hidden:
        img_label.config(image='', text='Caché', bg="#f0f0f0")
        is_image_hidden = True
    else:
        img_label.config(image=img_preview, text='', bg="white")
        is_image_hidden = False

def reveal_pixels():
    global img, img_width, img_height, revealed_image, revealed_img_tk, scale_factor, scaled_img
    try:
        reveal_count = int(pixel_entry.get())
        remaining_pixels = img_width * img_height - len(revealed_pixels)
        
        if reveal_count > remaining_pixels:
            messagebox.showwarning("Trop de pixels", f"Vous avez demandé {reveal_count} pixels, mais il ne reste que {remaining_pixels} pixels à révéler.")
            return

        pixels = img.load()  # Charge les pixels de l'image

        draw = ImageDraw.Draw(revealed_image)

        # Génère et affiche les pixels aléatoires, en ajoutant aux précédents
        for _ in range(reveal_count):
            while True:
                x = random.randint(0, img_width - 1)
                y = random.randint(0, img_height - 1)
                if (x, y) not in revealed_pixels:
                    revealed_pixels.add((x, y))
                    pixel_color = pixels[x, y]
                    draw.point((x, y), fill=pixel_color)
                    break

        # Redimensionne l'image révélée pour l'affichage
        resized_revealed_image = revealed_image.resize((int(img_width * scale_factor), int(img_height * scale_factor)))
        revealed_img_tk = ImageTk.PhotoImage(resized_revealed_image)
        canvas.create_image(0, 0, anchor="nw", image=revealed_img_tk)

        # Mise à jour du label pour le nombre total de pixels révélés
        revealed_label.config(text=f"Pixels Révélés : {len(revealed_pixels)}", fg="black")

        # Vérification si tous les pixels sont révélés
        if len(revealed_pixels) == img_width * img_height:
            messagebox.showinfo("GG!", "GG! Tous les pixels ont été révélés.")

    except ValueError:
        revealed_label.config(text="Veuillez entrer un nombre valide", fg="red")

def reset_pixels():
    global revealed_image, revealed_img_tk
    # Supprime les pixels affichés et réinitialise l'entrée
    canvas.delete("all")
    pixel_entry.delete(0, 'end')
    revealed_pixels.clear()  # Vide la liste des pixels révélés
    revealed_image = Image.new('RGB', (img_width, img_height), color='white')
    revealed_img_tk = ImageTk.PhotoImage(revealed_image.resize((int(img_width * scale_factor), int(img_height * scale_factor))))
    canvas.create_image(0, 0, anchor="nw", image=revealed_img_tk)
    revealed_label.config(text="Pixels Révélés : 0", fg="black")

# Création de la fenêtre principale
app = tk.Tk()
app.title("Réveil de Pixels")
app.state('zoomed')  # Met la fenêtre en plein écran
app.config(bg="#f0f0f0")

# Bouton de sélection de l'image
select_button = tk.Button(app, text="Sélectionner une image", command=select_image, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
select_button.pack(pady=10)

# Aperçu de l'image (cliquable)
img_label = tk.Label(app, text="Pas d'image sélectionnée", bg="#f0f0f0", font=("Arial", 12))
img_label.pack(pady=10)
img_label.bind("<Button-1>", toggle_image_visibility)  # Attache l'événement de clic gauche

# Affichage du nombre total de pixels
pixel_count_label = tk.Label(app, text="Nombre de pixels total: 0", bg="#f0f0f0", font=("Arial", 12))
pixel_count_label.pack(pady=10)

# Label pour afficher le nombre de pixels révélés juste en dessous du nombre total de pixels
revealed_label = tk.Label(app, text="Pixels Révélés : 0", bg="#f0f0f0", font=("Arial", 12))
revealed_label.pack(pady=5)

# Entrée pour le nombre de pixels à révéler avec les boutons autour
entry_frame = tk.Frame(app, bg="#f0f0f0")
entry_frame.pack(pady=10)

# Bouton reset pour réinitialiser l'affichage
reset_button = tk.Button(entry_frame, text="Reset", command=reset_pixels, bg="#FF0000", fg="white", font=("Arial", 12), padx=10, pady=5)
reset_button.pack(side="left", padx=5)

# Entrée du nombre de pixels à révéler
pixel_entry = tk.Entry(entry_frame, font=("Arial", 12), justify='center', width=20)
pixel_entry.pack(side="left", padx=5)

# Bouton pour révéler les pixels
reveal_button = tk.Button(entry_frame, text="Envoyer", command=reveal_pixels, bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
reveal_button.pack(side="left", padx=5)

# Canvas pour afficher les pixels révélés
canvas = tk.Canvas(app, bg="white")
canvas.pack(pady=10, expand=True)

# Variable pour suivre l'état de l'image (visible ou cachée)
is_image_hidden = False

# Ensemble pour stocker les pixels révélés
revealed_pixels = set()

# Lancement de l'application
app.mainloop()
