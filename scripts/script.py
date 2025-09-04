
import os
from urllib.parse import quote

def generate_indexes(
    folder,
    repo_raw_base="https://raw.githubusercontent.com/rubiin/wallpapers/master/wallpapers",
    output_folder="indexes",
    grids_per_index=2,                # number of 4x2 grids per index
    grid_cols=4,
    grid_rows=2,
    img_width=300,
    img_height=200
):
    os.makedirs(output_folder, exist_ok=True)

    # Collect image files (sorted sequentially)
    exts = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    files = sorted(f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in exts)

    if not files:
        print("No images found in the given folder.")
        return

    grid_size = grid_cols * grid_rows
    images_per_index = grids_per_index * grid_size

    # Split into index chunks sequentially
    chunks = [files[i:i + images_per_index] for i in range(0, len(files), images_per_index)]
    total_indexes = len(chunks)

    for idx, chunk in enumerate(chunks, start=1):
        index_filename = f"index_{idx}.md"
        index_path = os.path.join(output_folder, index_filename)
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(f"# Wallpapers – Batch {idx}\n\n")
            f.write("_Auto-generated gallery. Click any image to view full size._\n\n")

            # Break the chunk into grids
            for gstart in range(0, len(chunk), grid_size):
                grid = chunk[gstart:gstart + grid_size]
                if not grid:
                    break

                f.write('<table style="border-collapse:collapse; width:100%;">\n')
                for r in range(grid_rows):
                    f.write("  <tr>\n")
                    for c in range(grid_cols):
                        i = r * grid_cols + c
                        if i < len(grid):
                            name = grid[i]
                            url = f"{repo_raw_base}/{quote(name)}"
                            alt = os.path.splitext(name)[0]
                            f.write(
                                '    <td style="padding:6px; vertical-align:middle; text-align:center;">'
                                f'<a href="{url}">'
                                f'<img src="{url}" alt="{alt}" loading="lazy" '
                                f'style="width:{img_width}px; height:{img_height}px; object-fit:cover; '
                                'border-radius:8px; box-shadow:0 1px 4px rgba(0,0,0,0.15);"></a>'
                                "</td>\n"
                            )
                        else:
                            f.write('    <td style="padding:6px;"></td>\n')
                    f.write("  </tr>\n")
                f.write("</table>\n\n")
                f.write("<hr/>\n\n")

            # Navigation
            f.write("## Navigation\n\n")
            nav_links = []
            if idx > 1:
                nav_links.append(f"[⬅️ Prev](index_{idx-1}.md)")
            if idx < total_indexes:
                nav_links.append(f"[Next ➡️](index_{idx+1}.md)")
            f.write(" | ".join(nav_links) + "\n")

        print(f"Created {index_path}")

if __name__ == "__main__":
    wallpapers_folder = "wallpapers"

    generate_indexes(
        folder=wallpapers_folder,
        output_folder="indexes",
        repo_raw_base="https://raw.githubusercontent.com/rubiin/wallpapers/master/wallpapers",
        grids_per_index=2,   # 2 grids × (4×2) = 16 images per index
        grid_cols=4,
        grid_rows=2,
        img_width=300,
        img_height=200
    )
