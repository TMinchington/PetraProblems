""" Mask functions """

import numpy as np
import tifffile
from scipy.sparse import csr_matrix
import pandas as pd  # Required for the DataFrame in check_masks
from skimage.filters import threshold_li


def grow_labels_skimage(labels, distance):
    from skimage.segmentation import expand_labels
    return expand_labels(labels, distance=distance)



def get_all_indicies(TIFF_array):
    sparseTIFF = get_sparse_matrix(TIFF_array)
    return [np.unravel_index(row.data, TIFF_array.shape) for row in sparseTIFF]





def get_sparse_matrix(tiffArray):
    
    
    """getSparseMatrix: generates a sparse matrix where the
    columns are the unique intensity values in the supplied tiffArray and the rows represent
    all possible indicies in the original Array converted to 1D

    ----
    Args
    ----
        tiffArray (np.array):               numpy array made from a single channel tiff image, the current usecase is 
                                            a cellpose2 tiff mask file where unique values in the array represent individual
                                            cells.  

    -------
    Returns
    -------

        sparseMatrix (scipy.csr_matrix):    returns an empty sparse matrix which is shaped such that columns are the unqiue
                                            values inside the TIFF array and the nuber of rows is the positions in the 1D array 

    """

    cols = np.arange(tiffArray.size)

    tiffSparseMatrix = csr_matrix((cols, (tiffArray.ravel(), cols)),
                      shape=(tiffArray.max() + 1, tiffArray.size))

    # print(tiffArray.max())

    return tiffSparseMatrix


def check_masks(main_frameX, mask, nuc_index, file, tiff):
    # print(tiff.shape)
    # exit()
    
    zeros = np.zeros(mask.shape)
    
    for cell_id in main_frameX[main_frameX.positive == "Yes"].cell_id:
        zeros[nuc_index[cell_id]] = 70
    tiff[:, 0, :, :] = zeros
    tifffile.imwrite(f"/Users/thomas.minchington/Documents/petra/tempMasks/temp-mask{file}", tiff, imagej=True)



def get_transplant(cyto_index, tiff_image, channel=1):

    """
    Detects the transplant based on the selected channel
    Expects the cyto index to be the cyto mask
    
    Args:
        cyto_index (list): list of cyto index
        tiff_image (np.array): tiff image
        channel (int, optional): channel to use. Defaults to 1.
    
    Returns:
        list: list of transplant ids
    """
    
    cyto_mean_vals = []
    temp_ids = []
    channel_matrix = tiff_image[:, channel, :, :]
    
    new_trans_mask = np.zeros(channel_matrix.shape)
    
    for cell_id in range(1, len(cyto_index)):
                
        cyto_values = channel_matrix[cyto_index[cell_id]]
        cyto_mean_vals.append(np.mean(cyto_values))
        temp_ids.append(cell_id)
    
    threshold = threshold_li(np.array(cyto_mean_vals))
    threshold_ids = []
    
    for cell_id, value in zip(temp_ids, cyto_mean_vals):
        if value > threshold:
            new_trans_mask[cyto_index[cell_id]] = 10
            threshold_ids.append(cell_id)

    
    return threshold_ids


if __name__ == "__main__":
    pass