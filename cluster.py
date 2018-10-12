import numpy as np
from imageio import imwrite
from scipy.misc import imresize
from sklearn.cluster import k_means

k = 7

def resize_dims(dims):
    n = max(dims)
    divider = np.ceil(n/500)
    dim0 = int(dims[0]//divider)
    dim1 = int(dims[1]//divider)
    return (dim0, dim1)

def sort_it(centroids, conc):
    centroids_conc = sorted(zip(centroids, conc), key=lambda i: i[1], reverse=True)
    return centroids_conc

def get_dominant(img):
    img_new = imresize(img, resize_dims(img.shape))
    img_new = np.reshape(img_new, (img_new.shape[0]*img_new.shape[1],img_new.shape[2]))
    centroids, idx, _ = k_means(img_new, n_clusters=k)
    unique, counts = np.unique(idx, return_counts=True)
    conc = list(zip(unique, counts))
    l = [0]*k
    for i in conc:
        l[i[0]] = i[1]
    conc = l
    compressed = centroids[list(map(int, idx))]
    compressed = np.reshape(compressed,(*resize_dims(img.shape), img.shape[2]))
    if img.shape[2]==4:
        name = "new_image.png"
        imwrite("./static/"+name, compressed)
    else:
        name = "new_image.jpg"
        imwrite("./static/"+name, compressed)
    return len(idx), name, sort_it(list(centroids.astype(int)), conc)
