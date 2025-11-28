import os
from PIL import Image

INPUT_DIR = "images_input"
OUTPUT_DIR = "images_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
SIZE = (800, 800)

def process_image(path):
    try:
        with Image.open(path) as img:
            print(f"Opening {path} size={img.size}")
            img_resized = img.resize(SIZE)
            base = os.path.splitext(os.path.basename(path))[0]
            out_path = os.path.join(OUTPUT_DIR, base + ".png")
            img_resized.save(out_path)
            print(f"Saved {out_path}")
    except Exception as e:
        print("Error:", e)

def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".jpg",".jpeg",".png"))]
    for f in files:
        process_image(os.path.join(INPUT_DIR, f))

if __name__ == "__main__":
    main()
