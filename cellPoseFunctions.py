"""

Cellpose Petra

3D segmentation using the base model

"""


def run3Dbase(path_to_folder, dapi, cyto):
    
    import os
    import torch
    from cellpose import models
    from cellpose.io import imread, imsave
    import numpy as np

    
    model = models.CellposeModel(gpu=True)
    mask_path = os.path.join(path_to_folder, "data/masks")
    
    images = [x for x in os.listdir(path_to_folder) if x.endswith("tif")]
    masked_images = [x for x in os.listdir(mask_path) if x.endswith("tif")]
    missing_masks = [x for x in images if x.replace(".tif", "-masks.tif") not in masked_images]    
    # print(images)
    # print(masked_images)
    print(missing_masks)
    for imageX in missing_masks:
        image_full_path = os.path.join(path_to_folder, imageX)
        image_out_path = os.path.join(mask_path, imageX.replace(".tif", "-masks.tif"))
        # print(image_full_path)
        img = imread(image_full_path)
        # img_copy = img[:,(dapi,cyto)]
        img_copy = img[:,(dapi,)]
        masks, flows, styles = model.eval(img_copy, do_3D=True, z_axis=0, channel_axis=1)
        imsave(image_out_path, masks)

if __name__ == "__main__":

    import torch

    print(torch.__version__)
    print(torch.cuda.is_available())
    print(torch.version.cuda)
    print(torch.cuda.get_device_name(0))
    print(torch.cuda.is_available())

    # exit()
    dapi = 1
    cyto = 3
    run3Dbase("C:\\Users\\petra.schaffer\\Documents\\cellpose test\\trial run 7.7.25", dapi, cyto)
    pass



# img = imread(test_image)/

# print(img.shape)
# dapi = 0
# cyto = 1
# img_cp = img[:,(dapi,cyto)] # keep first two channels
# print(img_cp.shape)
# if nuclei and cytoplasm are in different channels from first two
# img_cp = img[[1, 3]] # keep 1 and 3 (2nd and 4th channels)

# if you want to combine two stains to create your "cytoplasm" channel
# in this example indices 0 and 2 (1st and 3rd) have two cellular stains
# and nuclei are in index 1 (2nd channel)
# img_cp = np.stack((img[[0,2]].sum(axis=0), img[1]), axis=0)

# masks, flows, styles = model.eval(img_cp, do_3D=True, z_axis=0, channel_axis=1)

# imsave(test_image.replace(".tif", "-masks.tif"), masks)
# imsave("test_flows_nuc_only.tiff", flows)

