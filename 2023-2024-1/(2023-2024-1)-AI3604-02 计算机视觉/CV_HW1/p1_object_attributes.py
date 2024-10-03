#!/usr/bin/env python3
import cv2
import numpy as np
import sys

# NOTE: 注释都是手写的
def binarize(gray_image, thresh_val):
  # TODO: 255 if intensity >= thresh_val else 0
  
  binary_image = np.where(gray_image >= thresh_val, 255, 0)
  return binary_image

def label(binary_image):
  # TODO
  
  # should use union-find set
  def find(s, index):
    while s[index] != index:
      index = s[index]
    return index

  H, W = binary_image.shape
  labeled_image = np.zeros((H, W), dtype=np.uint16) # allow unint16 labels at most
  (labeled_image[-1, 0], cl, labels) = (1, 1, [0, 1]) if labeled_image[-1, 0] == 255 else (0, 0, [0]) # pixel at bottom-left corner is labeled
  
  def new_label():
    nonlocal cl, labels
    cl += 1
    labels.append(cl)
    return cl

  for _i in range(H - 1):
    for j in range(W - 1):
      i = H - _i - 2 # y from bottom to top
      
      if _i == 0: # init the first row
        if binary_image[i + 1, j + 1] == 255:
          if binary_image[i + 1, j] == 255:
            labeled_image[i + 1, j + 1] = labeled_image[i + 1, j]
          else:
            labeled_image[i + 1, j + 1] = new_label()
        
      if j == 0: # init the first column except the first row
        if binary_image[i, j] == 255:
          if binary_image[i + 1, j] == 255:
            labeled_image[i, j] = labeled_image[i + 1, j]
          elif binary_image[i + 1, j + 1] == 255:
            labeled_image[i, j] = labeled_image[i + 1, j + 1] # two possible labels from the last row
          else:
            labeled_image[i, j] = new_label()
      
      # merge labels
      if binary_image[i, j] == 255 and binary_image[i + 1, j + 1] == 255:
        _m, _n = max(labeled_image[i, j], labeled_image[i + 1, j + 1]), min(labeled_image[i, j], labeled_image[i + 1, j + 1])
        labels[find(labels, _m)] = labels[_m] = find(labels, _n)
        
      # now each scan only label one new pixel based on three known pixels
      if binary_image[i, j + 1] == 255:
        if binary_image[i + 1, j + 1] == 255:
          labeled_image[i, j + 1] = labeled_image[i + 1, j + 1]
        elif binary_image[i + 1, j] == 255:
          labeled_image[i, j + 1] = labeled_image[i + 1, j]
        elif binary_image[i, j] == 255:
          labeled_image[i, j + 1] = labeled_image[i, j]
        else:
          labeled_image[i, j + 1] = new_label()
  
  # update labels and rearrange
  for i in range(len(labels)):
    labels[i] = find(labels, labels[i])
  sl = enumerate(sorted(list(set(labels))))
  rank = {x[1]: x[0] for x in sl}
  for i in range(len(labels)):
    labels[i] = rank[labels[i]]
  
  # two better visualize, use gamma correction function to produce gray scale image
  gamma_correction = lambda x: x ** (1/2.2)
  max_scale = max(labels)
  for i in range(H):
    for j in range(W):
      if labeled_image[i, j] != 0:
        labeled_image[i, j] = gamma_correction(labels[labeled_image[i, j]]) * (255 / max_scale)
    
  return labeled_image.astype(np.uint8)

def get_attribute(labeled_image):
  # TODO
  
  attribute_list = []
  labels = sorted(list(set(labeled_image.flatten())))
  for l in labels[1:]: # exclude background
    current_list = {}
    
    # position
    y, x = np.where(labeled_image == l)
    y = labeled_image.shape[0] - y - 1 # y from bottom to top
    x_bar, y_bar = np.mean(x), np.mean(y)
    current_list['position'] = {'x': x_bar, 'y': y_bar}
    
    # orientation 
    a = np.sum((x - x_bar)**2)
    b = 2 * np.sum((x - x_bar) * (y - y_bar))
    c = np.sum((y - y_bar)**2)
    orientation = 0.5 * np.arctan2(b, a - c)
    current_list['orientation'] = orientation
    
    # roundness: 
    st = np.sin(orientation)
    ct = np.cos(orientation)
    current_list['roundness'] = (a * st**2 + b * st * ct + c * ct**2) / (a * st**2 - b * st * ct + c * ct**2)
    
    attribute_list.append(current_list)
  return attribute_list

def main(argv):
  img_name = argv[0]
  thresh_val = int(argv[1])
  img = cv2.imread('data/' + img_name + '.png', cv2.IMREAD_COLOR)
  gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  binary_image = binarize(gray_image, thresh_val=thresh_val)
  labeled_image = label(binary_image)
  attribute_list = get_attribute(labeled_image)

  cv2.imwrite('output/' + img_name + "_gray.png", gray_image)
  cv2.imwrite('output/' + img_name + "_binary.png", binary_image)
  cv2.imwrite('output/' + img_name + "_labeled.png", labeled_image)
  print(attribute_list)


if __name__ == '__main__':
  main(sys.argv[1:])
