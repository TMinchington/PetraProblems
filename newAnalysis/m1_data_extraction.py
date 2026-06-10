import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from skimage.filters import threshold_otsu, threshold_yen, threshold_li
from skimage.filters import gaussian, median
from skimage.morphology import ball, area_opening
from scipy.sparse import csr_matrix
import tifffile
from numba import njit


from h1_mask_functions import grow_labels_skimage, get_sparse_matrix, check_masks, get_all_indicies, get_transplant
from h2_qc_functions import make_qc_graph
from h3_position_functions import get_centroid, get_distance_to_line

def bins(value):
    bin_dic = {89.74494: "L1" , 
      318.4708: "L2/3",
    503.638: "L4" ,
    783.3052:"L5",
   1141.693:"L6"}
  
    for x in sorted(list(bin_dic)):
        if value <= x:
            return bin_dic[x]

    return "L6"

def create_paths(path):
    data_path = os.path.join(path, "data/measurements")
    mask_path = os.path.join(path, "data/masks")
    line_path = os.path.join(path, "data/lines")
    qc_path = os.path.join(path, "data/qc")

    if not os.path.exists(qc_path):
        os.makedirs(qc_path)
    
    return data_path, mask_path, line_path, qc_path



def process_file(file, tiff_path, mask_path, line_path, qc_path, quant_chans=[-1,], transplant_chan=1):

    mask_match = file.replace(".tif", "-masks.tif")
    mask_full_path = os.path.join(mask_path, mask_match)
    lineFrame = pd.read_csv(os.path.join(line_path, file.replace(".tif", "-line.txt")), header=0, sep='\t')

    pixel_scale = lineFrame.x_pixel[0] / lineFrame.x_um[0]
    i = 0
    while np.isnan(pixel_scale):
        
        pixel_scale = lineFrame.x_pixel[i] / lineFrame.x_um[i]
        i += 1

        # print("rescale:", pixel_scale, i)

    print("PIXEL_SCALE: ",round(pixel_scale, 2))
    # print(lineFrame.head())
    # print(file, np.mean(lineFrame.y_um))
    # exit()
    try:
        mask = tifffile.imread(mask_full_path)
    except FileNotFoundError:
        print("No mask found for: ", file)
        return 0
    
    mask_big = grow_labels_skimage(mask, 5)
    cyto = mask_big - mask

    nuc_index = get_all_indicies(mask)
    cyto_index = get_all_indicies(cyto)
    
    try:
        tiff_loaded = tifffile.imread(os.path.join(tiff_path, file))
    except RuntimeError:
        print("Runtime error with: ", file)
        return 0
    # print("check2:", tiff_loaded.shape)

    channel_dic = add_gene_names(file, tiff_loaded.shape[1])
    index_dic = {}
    for x in channel_dic:
        index_dic[x] = x - ( tiff_loaded.shape[1] + 1)
    

    if "healthy_tissue" in file:
        transplant_ids = range(1, len(nuc_index))
    else:
        transplant_ids = get_transplant(cyto_index, tiff_loaded, transplant_chan)
    quant_chans = channel_dic.keys()
    # print(channel_dic)
    
    for chan in quant_chans:
        temp_frame_chan = process_channel(index_dic[chan], file, transplant_ids, tiff_loaded, nuc_index, cyto_index, mask, lineFrame, pixel_scale)
        temp_frame_chan['channel'] = chan
        try:
            temp_frame = pd.concat([temp_frame, temp_frame_chan])
            
        except NameError:
            temp_frame = temp_frame_chan.copy()
    # print("check2:", tiff_loaded.shape)
    temp_frame['file'] = file
    check_masks(temp_frame, mask, nuc_index, file, tiff_loaded[:, [index_dic[chan], 1], :, :])
    gene_dic = channel_dic
    if 0 not in gene_dic:
        gene_dic[0] = "DAPI"
    if 1 not in gene_dic:
        gene_dic[1] = "GFP"
    # print(set(temp_frame['channel']))
    temp_frame['gene'] = [gene_dic[x] for x in temp_frame['channel']]
    make_qc_graph(temp_frame, mask, tiff_loaded, nuc_index, os.path.join(qc_path, "QC-"+file.replace(".tif", ".png")))
    return temp_frame



def process_channel(chan, file, transplant_ids, tiff_loaded, nuc_index, cyto_index, mask, lineFrame, pixel_scale):
    dis_ls, cell_mean, id_ls, pos_ls, vol_ls = [], [], [], [], []
    x_ls, y_ls, z_ls = [], [], []
    try:
        channel_matrix = tiff_loaded[:, chan, :, :]
    except IndexError:
        raise ValueError("Channel out of range")

    nuc_mean_vals = []
    cyto_mean_vals = []
    mean_threhold_values = []
    pos_ls = []
    
    for cell_id in transplant_ids:
        nuc_values = channel_matrix[nuc_index[cell_id]]
        cyto_values = channel_matrix[cyto_index[cell_id]]
        nuc_mean_vals.append(np.mean(nuc_values))
        cyto_mean_vals.append(np.mean(cyto_values))
    
    for x in range(1, len(nuc_index)):
        mean_threhold_values.append(np.mean(channel_matrix[nuc_index[x]]))

    if "NECAB" in file:
        threshold = threshold_yen(np.array(cyto_mean_vals)+np.mean(channel_matrix[nuc_index[0]]))

    else:
        threshold1 = threshold_otsu(channel_matrix)
        threshold = threshold_otsu(np.array(mean_threhold_values))

        print("current threshold: ", np.mean([threshold, threshold1]), file)
        threshold = np.mean([threshold, threshold1])

    mask_copy_new = np.zeros(mask.shape)
    
    for id, nuc_mean in zip(transplant_ids, nuc_mean_vals):
        if nuc_mean >= threshold:
            mask_copy_new[nuc_index[id]] = nuc_mean
            pos_ls.append("Yes")
            
        else:
            pos_ls.append("No")
        centroid = get_centroid(nuc_index[id])
        dis_line = get_distance_to_line(lineFrame, centroid[0], centroid[1])
        volume = len(nuc_index[id][0])
        x, y, z = centroid
        
        # update lists for frame
        
        x_ls.append(x)
        y_ls.append(y)
        z_ls.append(z)
        vol_ls.append(volume)
        id_ls.append(id)
        cell_mean.append(nuc_mean)
        dis_ls.append(dis_line/pixel_scale)
            
    temp_frame = pd.DataFrame({"cell_id":id_ls, "mean_intensity":cell_mean,  "x": x_ls, "y":y_ls, "z":z_ls, "volume":vol_ls, "distance_line": dis_ls, "positive":pos_ls})
    # temp_frame["channel"] = chan +1
    
    return temp_frame


def add_gene_names(file, channel_n):

    file_lower = file.lower()

    hit_dic = {}
    genes_to_find = ["satb2", "ctip", "necab", "hunu", "tbr1", "cux1-2"]

    for gene in genes_to_find:
        try:
            pos = file_lower.index(gene)
            hit_dic[pos] = gene 
        except ValueError:
            continue
    
    sorted_keys = sorted(list(hit_dic.keys()), reverse=True)

    channels = sorted(list(range(1, channel_n+1)), reverse=True)
    channel_dic = {}
    for n, key in enumerate(sorted_keys):
        channel_dic[channels[n]] = hit_dic[key]

    return channel_dic
    

def main(path):

    if not os.path.exists(path):
        raise ValueError("Path does not exist")
    
    data_path, mask_path, line_path, qc_path = create_paths(path)
    
    tif_list = [x for x in os.listdir(path) if x.endswith("tif")]
    # print(tif_list)

    for file in tif_list:
        # if not "M149_40x-GFP_NECAB__HuNu_s41_" in file:
        #     continue
        print("Processing: ", file)
        temp_frame = process_file(file, path, mask_path, line_path, qc_path)
    
        if type(temp_frame) != pd.DataFrame:
            continue


        try:
            main_frame = pd.concat([main_frame, temp_frame])
            
        except NameError:
            main_frame = temp_frame.copy()

        
    main_frame['bins'] = [bins(x)   for x in main_frame['distance_line']]
    
    pd.DataFrame.to_csv(main_frame, os.path.join(data_path, "new_counts_tables-intensePositions.tsv"), sep='\t', index=None)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, required=True)
    args = parser.parse_args()
    main(args.path)