from PIL import Image
import pytesseract

def load_image(file_path):
    try:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"[ImageLoader] Error OCR on {file_path}: {e}")
        return ""
