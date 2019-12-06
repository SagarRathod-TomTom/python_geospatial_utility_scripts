import numpy as np
import rasterio
from rasterio.windows import Window
from os.path import join, basename


def geotiff_splitter(raw_img, split_size=1024):

        height = raw_img.height
        width = raw_img.width

        for x in range(0, height, split_size):
            if x + split_size > height:
                continue
            for y in range(0, width, split_size):
                if y + split_size > width:
                    continue

                window = Window(y, x, split_size, split_size)
                transform = raw_img.window_transform(window)

                img1 = raw_img.read(1, window=window)
                img2 = raw_img.read(2, window=window)
                img3 = raw_img.read(3, window=window)
                img = np.dstack([img1, img2, img3])

                yield img, transform


def save_geotiff(img, img_transform, crs, count, dtype, out_file):
    with rasterio.open(f"{out_file}.tif", mode="w", driver="GTiff", width=img.shape[1], height=img.shape[0],
                        count=count,
                        dtype=dtype,
                        transform=img_transform,
                        crs=crs) as dst:
        if count > 1:
            for band in range(img.shape[2]):
                dst.write(img[:, :, band], band + 1)
        else:
            dst.write(img, 1)


def split_image(tiff_file, out_dir, split_size=1024):
    raster = rasterio.open(tiff_file)
    name = basename(tiff_file)
    for index, (img, img_transform) in enumerate(geotiff_splitter(raster, split_size)):

        save_geotiff(img, img_transform, raster.crs, raster.count, raster.dtypes[0],
                     out_file=join(out_dir, "{}_{}.tif".format(name, index)))


if __name__ == '__main__':
    tiff_file = r"C:\Users\Lebanon_AOI_103001005825CF00.tif"
    out_dir = r"C:\Users\lebanon"
    split_image(tiff_file, out_dir)
