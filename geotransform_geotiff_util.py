import rasterio

def save_geo_referenced_image(image_file, out_image, out_image_file):
    image = rasterio.open(image_file)
    bands = out_image.ndim if out_image.ndim > 2 else 1
    georef_out_image = rasterio.open( out_image_file, mode="w", driver=image.driver,
                                     width=image.width, height=image.height, crs=image.crs,
                                     transform=image.transform, dtype=out_image.dtype, count=bands)
    if bands > 2:
        for band in range(out_image.shape[2]):
            georef_out_image.write(out_image[:, :, band], band + 1)
    else:
        georef_out_image.write(out_image, 1)
    image.close()
    georef_out_image.close()
