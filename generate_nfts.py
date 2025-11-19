import os
import random
from PIL import Image
import json

# --- CONFIG ---
NUM_NFTS = 1000
OUTPUT_FOLDER = "output"
IMAGE_FOLDER = "layers"
METADATA_FOLDER = os.path.join(OUTPUT_FOLDER, "metadata")
IMAGES_FOLDER = os.path.join(OUTPUT_FOLDER, "images")
BACKGROUND_FOLDER = "backgrounds"

# Layer files
classes = sorted(os.listdir(os.path.join(IMAGE_FOLDER, "classes")))
items = sorted(os.listdir(os.path.join(IMAGE_FOLDER, "items")))
traits = sorted(os.listdir(os.path.join(IMAGE_FOLDER, "hidden_traits")))
backgrounds = sorted(os.listdir(BACKGROUND_FOLDER))

# Rarity weights example (adjust as desired)
# Higher weight → more common
class_weights = [1]*25
item_weights = [5]*15
trait_weights = [5]*10
background_weights = [1]*5

# Ensure output folders exist
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(METADATA_FOLDER, exist_ok=True)

# Keep track of combinations to avoid exact duplicates
generated_combos = set()

for nft_index in range(1, NUM_NFTS + 1):
    while True:
        cls = random.choices(classes, weights=class_weights)[0]
        item = random.choices(items, weights=item_weights)[0]
        trait = random.choices(traits, weights=trait_weights)[0]
        bg = random.choices(backgrounds, weights=background_weights)[0]
        combo_key = (cls, item, trait, bg)
        if combo_key not in generated_combos:
            generated_combos.add(combo_key)
            break

    # Load images
    background_img = Image.open(os.path.join(BACKGROUND_FOLDER, bg)).convert("RGBA")
    class_img = Image.open(os.path.join(IMAGE_FOLDER, "classes", cls)).convert("RGBA")
    item_img = Image.open(os.path.join(IMAGE_FOLDER, "items", item)).convert("RGBA")
    trait_img = Image.open(os.path.join(IMAGE_FOLDER, "hidden_traits", trait)).convert("RGBA")

    # Compose final image
    final_img = Image.alpha_composite(background_img, class_img)
    final_img = Image.alpha_composite(final_img, item_img)
    final_img = Image.alpha_composite(final_img, trait_img)

    # Save final image
    nft_filename = f"NFT_{nft_index:04d}.png"
    final_img.save(os.path.join(IMAGES_FOLDER, nft_filename))

    # Create metadata JSON
    metadata = {
        "name": f"ROE

