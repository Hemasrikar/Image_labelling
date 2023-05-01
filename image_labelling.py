# ## Program to convert JSON/COCO files to image with labels ##

# from pycocotools.coco import COCO
# import pycocotools._mask as mask
# import cv2
# import numpy as np

# # path to the COCO annotations file
# ann_file = '/Users/Srikar/Documents/MATLAB/Image Annotation/Image_labelling_coco.json'

# # initialize the COCO API
# coco = COCO(ann_file)

# # get all image IDs in the dataset
# img_ids = coco.getImgIds()

# # iterate over each image
# for img_id in img_ids:
#     # load image metadata
#     img_meta = coco.loadImgs(img_id)[0]

#     # load image data
#     img_data = cv2.imread('/Users/Srikar/Documents/MATLAB/Image Annotation/Data/' + img_meta['file_name'])

#     # get annotations for this image
#     ann_ids = coco.getAnnIds(imgIds=img_id)
#     anns = coco.loadAnns(ann_ids)

#     # draw annotations on image
#     for ann in anns:
#         segmentation = ann['segmentation']
#         category_id = ann['category_id']
#         category_name = coco.loadCats(category_id)[0]['name']
#         category_color = coco.loadCats(category_id)[0]['color']

#         # convert segmentation to numpy array
#         mask = coco.annToMask(ann)
#         poly = np.array(segmentation).reshape(-1, 2)

#         # draw polygon on image
#         color_rgb = tuple(int(c * 255) for c in category_color) # convert decimal RGB values to 0-255 range
#         cv2.fillPoly(img_data, np.array([poly],  dtype=np.int32), color_rgb)

#         # write category label
#         x, y = poly.mean(axis=0)
#         # cv2.putText(img_data, category_name, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)


#         img_name = img_meta['file_name'].split('.')[0] + '_labeled.jpg'
#         # cv2.imwrite(img_name, img_data)

#     # show the labeled image
#     cv2.imshow('Image', img_data)
#     cv2.waitKey(0)


#### With Background masked as Black ####


import numpy as np
import cv2
from pycocotools.coco import COCO

# path to the COCO annotations file
ann_file = '/Users/Srikar/Documents/MATLAB/Image Annotation/Image_labelling_coco.json'

# initialize the COCO API
coco = COCO(ann_file)

# get all image IDs in the dataset
img_ids = coco.getImgIds()

# iterate over each image
for img_id in img_ids:
    # load image metadata
    img_meta = coco.loadImgs(img_id)[0]

    # load image data
    img_data = cv2.imread('/Users/Srikar/Documents/MATLAB/Image Annotation/Data/' + img_meta['file_name'])

    # get annotations for this image
    ann_ids = coco.getAnnIds(imgIds=img_id)
    anns = coco.loadAnns(ann_ids)

    # create a binary mask of the same shape as the image
    mask = np.zeros_like(img_data[:,:,0], dtype=np.uint8)

    # iterate over each annotation and draw the mask
    for ann in anns:
        # extract the polygon coordinates and category ID
        segmentation = ann['segmentation']
        category_id = ann['category_id']
        category_color = coco.loadCats(category_id)[0]['color']

        # convert segmentation to numpy array
        poly = np.array(segmentation).reshape(-1, 2)

        # draw polygon on mask
        cv2.fillPoly(mask, np.array([poly],  dtype=np.int32), 255)

    # apply the mask to the image to black out the background
    img_data[mask == 0] = [0, 0, 0]

    for ann in anns:
        segmentation = ann['segmentation']
        category_id = ann['category_id']
        category_name = coco.loadCats(category_id)[0]['name']
        category_color = coco.loadCats(category_id)[0]['color']

        # convert segmentation to numpy array
        mask = coco.annToMask(ann)
        poly = np.array(segmentation).reshape(-1, 2)

        # draw polygon on image
        color_rgb = tuple(int(c * 255) for c in category_color) # convert decimal RGB values to 0-255 range
        cv2.fillPoly(img_data, np.array([poly],  dtype=np.int32), color_rgb)

        # write category label
        x, y = poly.mean(axis=0)
        # cv2.putText(img_data, category_name, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # write the labeled image to disk
        img_name = img_meta['file_name'].split('.')[0] + '_labeled.jpg'
        cv2.imwrite(img_name, img_data)


    # show the labeled image
    cv2.imshow('Image', img_data)
    cv2.waitKey(0)

