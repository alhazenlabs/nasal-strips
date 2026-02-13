import qrcode
from PIL import Image, ImageDraw, ImageFont

# 1. Dimensions at 300 DPI for 12cm x 14.5cm
WIDTH, HEIGHT = 1417, 1713
LINK = "https://alhazenlabs.com/strips"
LOGO_PATH = "assets/icon.png"  # Ensure this file exists
OUTPUT_PATH = "alhazen_qr.png"

# 2. Generate High-Correction QR
qr = qrcode.QRCode(
    version=None, # Auto-detect version
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=30,  # Larger box size for better resolution
    border=2,
)
qr.add_data(LINK)
qr.make(fit=True)

# Create QR image
qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# 3. Create Canvas
canvas = Image.new('RGB', (WIDTH, HEIGHT), 'white')
draw = ImageDraw.Draw(canvas)

# 4. Resize QR to fit comfortably (leaving room for text)
# We use ~80% of the width for the QR code
qr_display_size = int(WIDTH * 0.85)
qr_img = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)

# Position QR centered horizontally, slightly towards the top
qr_x = (WIDTH - qr_display_size) // 2
qr_y = 100 # Top margin
canvas.paste(qr_img, (qr_x, qr_y))

# 5. Add Logo in Center
try:
    logo = Image.open(LOGO_PATH).convert("RGBA")
    # Logo size (roughly 22% of QR size is safe for 'H' correction)
    logo_size = qr_display_size // 4.5
    logo = logo.resize((int(logo_size), int(logo_size)), Image.Resampling.LANCZOS)
    
    # Center logo inside the QR
    logo_pos = (qr_x + (qr_display_size - logo.width) // 2, 
                qr_y + (qr_display_size - logo.height) // 2)
    
    # Paste logo (using itself as mask for transparency)
    canvas.paste(logo, logo_pos, logo)
except FileNotFoundError:
    print("Logo not found. Generating without center icon.")

# 6. Add Bold, Readable Text
text = "PRODUCT DETAILS"
try:
    # Set a very large font size for readability (e.g., 120pt)
    # On Windows: "arialbd.ttf" for bold. On Mac/Linux: "/Library/Fonts/Arial Bold.ttf"
    font = ImageFont.truetype("arialbd.ttf", 130) 
except:
    font = ImageFont.load_default()

# Calculate text position to center it in the remaining bottom space
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

text_x = (WIDTH - text_width) // 2
# Place text in the center of the vertical gap between QR and bottom
text_y = qr_y + qr_display_size + ((HEIGHT - (qr_y + qr_display_size) - text_height) // 2)

draw.text((text_x, text_y), text, fill="black", font=font)

# 7. Final Save
canvas.save(OUTPUT_PATH, dpi=(300, 300))
print(f"Success! Saved to {OUTPUT_PATH}")