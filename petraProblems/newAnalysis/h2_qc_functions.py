import matplotlib.pyplot as plt
import numpy as np
import math

# def make_qc_graph(main_frame, mask, tiff_array, nuc_index, path_to_write):


#     """
#     Makes the WC graphs
#     """

#     # I want to plot the gfp vs the mask and the positive cells vs their channel
    
#     fig, ax = plt.subplots(2, 2, figsize=(10, 10))
#     ax[0, 0].imshow(np.max(tiff_array[:, 1, :, :], axis=0), cmap='gray')
#     ax[0, 0].set_title("GFP")
#     zeros = np.zeros(mask.shape)
    
#     for cell_id in main_frame.cell_id:
#         zeros[nuc_index[cell_id]] = 10
    
#     zeros2 = np.zeros(mask.shape)
#     for cell_id in main_frame[main_frame.positive == "Yes"].cell_id:
#         zeros2[nuc_index[cell_id]] = 10
        
#     ax[0, 1].imshow(np.max(zeros, axis=0), cmap='gray')
#     ax[0, 1].set_title("Positive GFP cells")
#     chan = tiff_array.shape[1]-1

#     try:
#         ax[1, 0].imshow(np.max(tiff_array[:, chan, :, :], axis=0), cmap='plasma')
#         ax[1, 0].set_title(f"Channel {chan}")
#         ax[1, 1].imshow(np.max(zeros2, axis=0), cmap='gray')
#         ax[1, 1].set_title(f"Positive Channel {chan} cells")
#     except IndexError:
#         print("Channel out of range for QC plot: ", chan)
#         # chan -= 1
#         ax[1, 0].imshow(np.max(tiff_array[:, chan, :, :], axis=0), cmap='plasma')
#         ax[1, 0].set_title(f"Channel {chan}")
#         ax[1, 1].imshow(np.max(zeros2, axis=0), cmap='gray')
#         ax[1, 1].set_title(f"Positive Channel {chan} cells")
#     # plt.tight_layout()
#     # plt.show()
#     plt.savefig(path_to_write, dpi=200)
#     print(path_to_write)
#     plt.close()


def make_qc_graph(main_frame, mask, tiff_array, nuc_index, path_to_write):


    """
    Makes the WC graphs
    """

    # I want to plot the gfp vs the mask and the positive cells vs their channel
    
    # fig, ax = plt.subplots(2, 2, figsize=(10, 10))
    # ax[0, 0].imshow(np.max(tiff_array[:, 1, :, :], axis=0), cmap='gray')
    # ax[0, 0].set_title("GFP")
    zeros = np.zeros(mask.shape)
    
    channel_list = [2] + sorted(main_frame.channel.unique())

    # print(channel_list)
    fig, ax = plt.subplots(len(channel_list), 2, figsize=(10, 10))

    for n, chan in enumerate(channel_list):
        # print(chan)
        zeros2 = np.zeros(mask.shape)
        if chan ==2:
            for cell_id in set(main_frame.cell_id):
                # print(cell_id)
                zeros2[nuc_index[cell_id]] = 10

            # print(np.max(zeros2, axis=0))
            ax[n, 1].imshow(np.max(zeros2, axis=0), cmap='plasma')
            ax[n, 0].imshow(np.max(tiff_array[:, chan-1, :, :], axis=0), cmap='plasma')
            ax[n, 0].set_title(f"\nGFP")
            ax[n, 1].set_title(f"\nPositive GFP")
            
        
        else:
            chan_frame = main_frame[(main_frame.channel == chan) & (main_frame.positive == "Yes")]
            gene = chan_frame.gene.unique()[0]
            for cell_id in set(chan_frame.cell_id):
                zeros2[nuc_index[cell_id]] = 10

            ax[n, 1].imshow(np.max(zeros2, axis=0), cmap='plasma')
            ax[n, 0].imshow(np.max(tiff_array[:, chan-1, :, :], axis=0), cmap='plasma')
            ax[n, 0].set_title(f"\n{gene.upper()}")
            ax[n, 1].set_title(f"\nPositive {gene.upper()}")

    plt.tight_layout()
    plt.savefig(path_to_write, dpi=200)
    plt.close()





if __name__ == "__main__":
    pass