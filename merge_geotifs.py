import rasterio
from rasterio.merge import merge
import glob
import os
from tqdm.auto import tqdm


def merge_geo_tif_images(input_dir, out_file):
    q = os.path.join(input_dir, "*.tif")
    dem_fps = glob.glob(q)
    src_files_to_mosaic = []
    for fp in tqdm(dem_fps):
        src = rasterio.open(fp)
        src_files_to_mosaic.append(src)

    print('Merging...')
    mosaic, out_trans = merge(src_files_to_mosaic)
    out_meta = src_files_to_mosaic[0].meta.copy()
    print('Done Merging.')

    out_meta.update({"driver": "GTiff",
                     "height": mosaic.shape[1],
                     "width": mosaic.shape[2],
                     "transform": out_trans,
                     "crs": out_meta['crs']
                     }
                    )

    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(mosaic)


if __name__ == "__main__":
   input_dir = r'C:\geo_tif_files'
   out_file = r'C:\merged_geo_tif.tif'
   merge_geo_tif_images(input_dir, out_file)
