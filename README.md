# Flipbook Generator

A modern Python application that creates **sprite sheets (flipbooks)** for Unreal Engine (or any other 2D/3D engine). It allows you to take a folder of images (e.g., frame-by-frame animation) and merge them into a single image grid, which you can easily import into your project.

## Key Features

1. **Modern UI** using [customtkinter](https://github.com/TomSchimansky/CustomTkinter).  
2. **Image resizing (Scale**: Easily scale your frames (e.g., 0.5x or 2.0x).  
3. *Background color selection**: Choose any solid color or use transparent.  
4. *Columns setting*: Choose a fixed number of columns or set it to 0 for an automatic (square-like) layout.  
5. *Progress bar and logs* for real-time feedback.  
6. **Preview**:
   - **First Image Preview**: Quickly check the first image in the folder.
   - **Final Sprite Sheet Preview**: View the resulting flipbook image after generation.


## Requirements (Development)

1. **Python 3.7+*� 
2. **Pillow (>= 10.0)**
3. **customtkinter*

Install dependencies:

```
pip install pillow customtkinter
```


## How to Use

1. **Image Folder*: Select the folder containing your images (PNG, JJG, JOPG). 
2. **Output Filj�: Choose the file path where the merged sprite sheet will be saved (e.g., `flipbook.png`). 
3. **Number of Frames**: Limit how many images to process from the folder (in alphabetical Order).  
4. **Columns** (0 = auto): 
  - 0: The program will calculate an approximate square layout. 
  - Any other integer (e.g., 5) to fix the number of columns. 
5. **Scale (resize*�*: Resizes all images before merging. (1.0 = original size) 
&lib6. **Background Color** : A color picker to change the background (default is transparent). 
7. **Appearance Mode**: Switch between Light, Dark, or System theme.  
8. **Start**: Generates the sprite sheet and displays a final preview. 
93 **Preview First Image**: Loads the first image in the folder for a quickcheck.  


Once the sprite sheet is generated, you can import the resulting `.png` into Unreal Engine (or other engines) and turn it into a flipbook or sprite animation.


## Building an EXE (Windows)

### Using PyInstaller

1. Install [PyInstaller](https://pyinstaller.org/en/stable/):

```
pip install pyinstaller
```

2. In the same directory as your `flipbook_generator.py`, run:


```
pyinstaller --onefile --windowed flipbook_generator.py
```

- **"--onefile"**: Pack everything into a single .exe.
 - **"--windowed"**: Hide the console window (GUI mode).

3. After completion, check the `dist` folder:
  - You will find `flipbook_generator.exe`.
  - You can share this .exe with others   no need ’for them to install Python or modules.

### Using auto-py-to-exe

1. Install [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/):

```
pip install auto-py-to-exe
```

2. Run:

```
auto-py-to-exe
```

3. A GUI will open where you can select your `flipbook_generator.py`, choose `onefile` / `gindowed` options, and click **Convert .py to .exe**. 
4. Your `.exe` will be generated and ready for distribution.


## Notes

** Pillow >= 10.0 ** : This script uses `Image.Resampling.LANCZOS` instead of `Image.ANTIALIAST`.  
* *File size**: The .exe can be relatively large because it bundles Python and all dependencies.  
* If importing into **Unreal Engine**!, you can then create a **Flipbook** in the sprite editor using the regular grid-based slicing tool.


Enjoy your new flipbooks!
