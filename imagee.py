import os
from PIL import Image

# Input and Output folders
INPUT_DIR = "images_input"
OUTPUT_DIR = "images_output"

# Make sure both folders exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Resize dimensions (change if you want different size)
SIZE = (800, 800)

def process_image(path):
    try:
        with Image.open(path) as img:
            print(f"Opening {path} | Original size={img.size}")
            img_resized = img.resize(SIZE)

            base = os.path.splitext(os.path.basename(path))[0]
            out_path = os.path.join(OUTPUT_DIR, base + ".png")

            img_resized.save(out_path)
            print(f"✅ Saved: {out_path}")
    except Exception as e:
        print(f"❌ Error processing {path}: {e}")

def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not files:
        print(f"⚠️ No images found in '{INPUT_DIR}'. Please add some JPG/PNG files.")
        return

    for f in files:
        process_image(os.path.join(INPUT_DIR, f))

if __name__ == "__main__":
    print("📂 Current working directory:", os.getcwd())
    main()
