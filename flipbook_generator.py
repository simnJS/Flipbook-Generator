import os
import math
import glob
import datetime
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk


# Set the default appearance mode and theme for customtkinter
ctk.set_appearance_mode("System")  # "System", "Dark", or "Light"
ctk.set_default_color_theme("blue")  # Theme: "blue", "green", or "dark-blue"


class FlipbookGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main window configuration
        self.title("Unreal Flipbook Grid Generator")
        # Increase the window size so all elements are visible
        self.geometry("1024x720")

        # Variables
        self.var_folder = tk.StringVar()
        self.var_output_file = tk.StringVar()
        self.var_nb_frames = tk.IntVar(value=12)
        self.var_nb_cols = tk.IntVar(value=0)  # 0 = auto (square-like)
        self.var_bg_color = (0, 0, 0, 0)  # RGBA background (default: transparent)
        self.var_appearance = tk.StringVar(value="System")
        self.var_scale = tk.DoubleVar(value=1.0)  # Scale factor (1.0 = no resize)

        # Layout: two main columns
        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=1, uniform="col")
        self.grid_rowconfigure(0, weight=1)

        # Left frame: parameters
        self.frame_left = ctk.CTkFrame(self, corner_radius=10)
        self.frame_left.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.frame_left.grid_columnconfigure(0, weight=1)

        # Right frame: previews + logs
        self.frame_right = ctk.CTkFrame(self, corner_radius=10)
        self.frame_right.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        self.frame_right.grid_rowconfigure(1, weight=1)  # logs area
        self.frame_right.grid_rowconfigure(3, weight=1)  # final preview area
        self.frame_right.grid_columnconfigure(0, weight=1)

        # ================== LEFT FRAME: PARAMETERS ==================
        row_index = 0

        # Folder (image directory)
        self.label_folder = ctk.CTkLabel(self.frame_left, text="Image Folder:")
        self.label_folder.grid(row=row_index, column=0, padx=10, pady=(10, 5), sticky="w")
        row_index += 1

        self.entry_folder = ctk.CTkEntry(self.frame_left, textvariable=self.var_folder, width=300)
        self.entry_folder.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")

        self.button_folder = ctk.CTkButton(self.frame_left, text="Browse", command=self.browse_folder)
        self.button_folder.grid(row=row_index, column=0, padx=10, pady=5, sticky="e")
        row_index += 1

        # Output file
        self.label_output = ctk.CTkLabel(self.frame_left, text="Output File:")
        self.label_output.grid(row=row_index, column=0, padx=10, pady=(10, 5), sticky="w")
        row_index += 1

        self.entry_output_file = ctk.CTkEntry(self.frame_left, textvariable=self.var_output_file, width=300)
        self.entry_output_file.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")

        self.button_output_file = ctk.CTkButton(self.frame_left, text="Browse", command=self.browse_file)
        self.button_output_file.grid(row=row_index, column=0, padx=10, pady=5, sticky="e")
        row_index += 1

        # Number of frames
        self.label_nb_frames = ctk.CTkLabel(self.frame_left, text="Number of Frames:")
        self.label_nb_frames.grid(row=row_index, column=0, padx=10, pady=(10, 5), sticky="w")
        row_index += 1

        self.option_nb_frames = ctk.CTkOptionMenu(
            self.frame_left,
            values=["12", "24", "48", "60", "90", "120", "150", "180"],
            command=self.set_nb_frames
        )
        self.option_nb_frames.set("12")
        self.option_nb_frames.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
        row_index += 1

        # Columns (auto or manual)
        self.label_nb_cols = ctk.CTkLabel(self.frame_left, text="Columns (0 = auto):")
        self.label_nb_cols.grid(row=row_index, column=0, padx=10, pady=(10, 5), sticky="w")
        row_index += 1

        self.slider_nb_cols = ctk.CTkSlider(
            self.frame_left, from_=0, to=20, number_of_steps=20, command=self.set_nb_cols
        )
        self.slider_nb_cols.set(0)
        self.slider_nb_cols.grid(row=row_index, column=0, padx=10, pady=5, sticky="we")

        self.label_nb_cols_val = ctk.CTkLabel(self.frame_left, text="0")
        self.label_nb_cols_val.grid(row=row_index, column=0, padx=10, pady=5, sticky="e")
        row_index += 1

        # Scale (resize)
        self.label_scale = ctk.CTkLabel(self.frame_left, text="Scale (resize):")
        self.label_scale.grid(row=row_index, column=0, padx=10, pady=(10, 5), sticky="w")
        row_index += 1

        self.slider_scale = ctk.CTkSlider(
            self.frame_left, from_=0.1, to=2.0, number_of_steps=19, command=self.set_scale
        )
        self.slider_scale.set(1.0)
        self.slider_scale.grid(row=row_index, column=0, padx=10, pady=5, sticky="we")

        self.label_scale_val = ctk.CTkLabel(self.frame_left, text="1.0")
        self.label_scale_val.grid(row=row_index, column=0, padx=10, pady=5, sticky="e")
        row_index += 1

        # Background color
        self.label_bg_color = ctk.CTkLabel(self.frame_left, text="Background Color:")
        self.label_bg_color.grid(row=row_index, column=0, padx=10, pady=(10, 5), sticky="w")
        row_index += 1

        self.button_bg_color = ctk.CTkButton(self.frame_left, text="Pick Color", command=self.pick_bg_color)
        self.button_bg_color.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
        row_index += 1

        # Appearance (Light/Dark/System)
        self.label_appearance = ctk.CTkLabel(self.frame_left, text="Appearance Mode:")
        self.label_appearance.grid(row=row_index, column=0, padx=10, pady=(10, 5), sticky="w")
        row_index += 1

        self.option_appearance = ctk.CTkOptionMenu(
            self.frame_left,
            values=["System", "Light", "Dark"],
            command=self.set_appearance
        )
        self.option_appearance.set("System")
        self.option_appearance.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
        row_index += 1

        # Start button
        self.button_start = ctk.CTkButton(
            self.frame_left,
            text="Start",
            fg_color="green",
            command=self.generate_grid
        )
        self.button_start.grid(row=row_index, column=0, padx=10, pady=(20, 5), sticky="ew")
        row_index += 1

        # Preview first image button
        self.button_preview = ctk.CTkButton(
            self.frame_left,
            text="Preview First Image",
            command=self.preview_first_image
        )
        self.button_preview.grid(row=row_index, column=0, padx=10, pady=(5, 20), sticky="ew")
        row_index += 1

        # ================== RIGHT FRAME: PREVIEWS & LOGS ==================
        # Preview of the first image
        self.preview_label = ctk.CTkLabel(self.frame_right, text="No preview available")
        self.preview_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # Log area
        self.text_log = ctk.CTkTextbox(self.frame_right)
        self.text_log.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.frame_right, mode='determinate')
        self.progress_bar.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        # Final preview (sprite sheet)
        self.final_preview_label = ctk.CTkLabel(self.frame_right, text="No final preview yet")
        self.final_preview_label.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")


    # --------------- Callbacks / Functions ---------------

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.var_folder.set(folder)
            self.log(f"Folder selected: {folder}")

    def browse_file(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Image PNG", "*.png"), ("All Files", "*.*")]
        )
        if file:
            self.var_output_file.set(file)
            self.log(f"Output file selected: {file}")

    def set_nb_frames(self, val):
        self.var_nb_frames.set(int(val))
        self.log(f"Number of frames set to: {val}")

    def set_nb_cols(self, val):
        val_int = int(float(val))
        self.var_nb_cols.set(val_int)
        self.label_nb_cols_val.configure(text=str(val_int))
        if val_int == 0:
            self.log("Columns set to: AUTO (0)")
        else:
            self.log(f"Columns set to: {val_int}")

    def set_scale(self, val):
        val_float = round(float(val), 2)
        self.var_scale.set(val_float)
        self.label_scale_val.configure(text=str(val_float))
        self.log(f"Scale set to: {val_float}x")

    def pick_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")
        if color and color[0]:
            r, g, b = color[0]
            # RGBA color (alpha = 255)
            self.var_bg_color = (int(r), int(g), int(b), 255)
            self.log(f"Background color picked: ({int(r)}, {int(g)}, {int(b)})")

    def set_appearance(self, mode):
        self.var_appearance.set(mode)
        ctk.set_appearance_mode(mode)
        self.log(f"Appearance mode set to: {mode}")

    def log(self, message: str):
        """Insert a timestamped message in the log box."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.text_log.insert("end", f"[{timestamp}] {message}\n")
        self.text_log.see("end")  # auto-scroll

    def preview_first_image(self):
        """Load and display the first image in the chosen folder."""
        folder = self.var_folder.get()
        if not folder or not os.path.isdir(folder):
            self.log("Cannot preview: invalid folder.")
            return

        # Find the first valid image
        all_images = []
        for ext in ("*.png", "*.jpg", "*.jpeg"):
            all_images.extend(glob.glob(os.path.join(folder, ext)))
        all_images = sorted(all_images)

        if not all_images:
            self.log("No image found for preview.")
            return

        first_image_path = all_images[0]
        self.log(f"Loading first image: {first_image_path}")
        try:
            pil_image = Image.open(first_image_path).convert("RGBA")
            max_preview_size = (300, 300)
            # Use Resampling.LANCZOS (Pillow 10+)
            pil_image.thumbnail(max_preview_size, Image.Resampling.LANCZOS)

            tk_image = ImageTk.PhotoImage(pil_image)
            self.preview_label.configure(image=tk_image, text="")
            self.preview_label.image = tk_image  # prevent GC
        except Exception as e:
            self.log(f"Error during preview: {e}")

    def generate_grid(self):
        """Generate the sprite sheet and save it."""
        self.progress_bar.set(0)
        folder = self.var_folder.get()
        output_file = self.var_output_file.get()
        nb_frames = self.var_nb_frames.get()
        nb_cols = self.var_nb_cols.get()
        bg_color = self.var_bg_color
        scale = self.var_scale.get()

        if not folder or not os.path.isdir(folder):
            self.log("Error: Invalid folder.")
            return
        if not output_file:
            self.log("Error: Missing output file.")
            return

        # Collect images
        images_paths = []
        for ext in ("*.png", "*.jpg", "*.jpeg"):
            images_paths.extend(glob.glob(os.path.join(folder, ext)))
        images_paths = sorted(images_paths)[:nb_frames]

        if not images_paths:
            self.log("No images found or nb_frames too small.")
            return

        self.log(f"{len(images_paths)} image(s) will be used.")

        # Open and resize images
        images = []
        for index, p in enumerate(images_paths):
            try:
                im = Image.open(p).convert("RGBA")
                if scale != 1.0:
                    w, h = im.size
                    new_w = int(w * scale)
                    new_h = int(h * scale)
                    im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
                images.append(im)
            except Exception as e:
                self.log(f"Error opening {p}: {e}")
                continue

        total_images = len(images)
        if total_images == 0:
            self.log("No valid image after attempting to open.")
            return

        # Determine grid dimensions
        w, h = images[0].size
        if nb_cols == 0:
            nb_cols = int(math.ceil(math.sqrt(total_images)))
        nb_rows = math.ceil(total_images / nb_cols)

        total_width = nb_cols * w
        total_height = nb_rows * h

        self.log(f"Grid: {nb_rows} row(s) x {nb_cols} column(s)")
        self.log(f"Final dimension: {total_width}x{total_height}")

        sprite_sheet = Image.new("RGBA", (total_width, total_height), bg_color)

        # Paste images into the sprite sheet
        for index, im in enumerate(images):
            row = index // nb_cols
            col = index % nb_cols
            x_offset = col * w
            y_offset = row * h
            sprite_sheet.paste(im, (x_offset, y_offset))

            # Update progress bar
            progress = (index + 1) / total_images
            self.progress_bar.set(progress)
            self.update_idletasks()

        # Save the sprite sheet and show final preview
        try:
            sprite_sheet.save(output_file)
            self.log(f"Flipbook saved to: {output_file}")
            # Preview the final sprite sheet
            self.preview_sprite_sheet(output_file)
        except Exception as e:
            self.log(f"Error while saving: {e}")

    def preview_sprite_sheet(self, path):
        """Load and display the final sprite sheet."""
        self.log(f"Previewing final sprite sheet: {path}")
        try:
            pil_image = Image.open(path).convert("RGBA")
            max_size = (400, 400)
            pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)

            tk_image = ImageTk.PhotoImage(pil_image)
            self.final_preview_label.configure(image=tk_image, text="")
            self.final_preview_label.image = tk_image
        except Exception as e:
            self.log(f"Error while final preview: {e}")


if __name__ == "__main__":
    app = FlipbookGeneratorApp()
    app.mainloop()
