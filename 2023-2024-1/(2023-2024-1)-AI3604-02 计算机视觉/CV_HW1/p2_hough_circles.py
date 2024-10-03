#!/usr/bin/env python3
import cv2
import numpy as np


def detect_edges(image):
  """Find edge points in a grayscale image.

  Args:
  - image (2D uint8 array): A grayscale image.

  Return:
  - edge_image (2D float array): A heat map where the intensity at each point
      is proportional to the edge magnitude.
  """
  # raise NotImplementedError  #TODO

  def compare(image):
    gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    edge_image = np.sqrt(gradient_x**2 + gradient_y**2)
    cv2.imwrite('output/' + img_name + "_edge_raw_cv.png", edge_image)

  compare(image)
  
  sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
  sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

  # handwrite the convolution
  gradient_x, gradient_y = np.zeros(image.shape), np.zeros(image.shape)
  padded_image = np.pad(image, ((1, 1), (1, 1)), 'edge')
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      gradient_x[i, j] = np.sum(padded_image[i:i+3, j:j+3] * sobel_x)
      gradient_y[i, j] = np.sum(padded_image[i:i+3, j:j+3] * sobel_y)

  edge_image = np.sqrt(gradient_x**2 + gradient_y**2)

  return edge_image


def hough_circles(edge_image, edge_thresh, radius_values):
  """Threshold edge image and calculate the Hough transform accumulator array.

  Args:
  - edge_image (2D float array): An H x W heat map where the intensity at each
      point is proportional to the edge magnitude.
  - edge_thresh (float): A threshold on the edge magnitude values.
  - radius_values (1D int array): An array of R possible radius values.

  Return:
  - thresh_edge_image (2D bool array): Thresholded edge image indicating
      whether each pixel is an edge point or not.
  - accum_array (3D int array): Hough transform accumulator array. Should have
      shape R x H x W.
  """
  # raise NotImplementedError  #TODO
  thresh_edge_image = np.where(edge_image > edge_thresh, True, False)
  accum_array = np.zeros((len(radius_values), edge_image.shape[0], edge_image.shape[1]))
  for idx, radius in enumerate(radius_values):
    theta = np.deg2rad(np.arange(360))
    x = (radius * np.cos(theta)).astype(int)
    y = (radius * np.sin(theta) * 0.96).astype(int)
    
    # silly implementation
    # for h in range(edge_image.shape[0]):
    #   for w in range(edge_image.shape[1]):
    #     for i in range(len(theta)):
    #       _y = h + x
    #       _x = w + y
    #       a = np.maximum(0, np.minimum(edge_image.shape[0] - 1, np.arange(edge_image.shape[0]) - _y[i]))
    #       b = np.maximum(0, np.minimum(edge_image.shape[1] - 1, np.arange(edge_image.shape[1]) - _x[i]))
    #       for _a, _b in zip(a, b):
    #         if _a * _b * (edge_image.shape[0] - 1 - _a) * (edge_image.shape[1] - 1 - _b) != 0:
    #           accum_array[idx, _y, _x] += 
    for i in range(len(theta)):
      _y, _x = y[i], x[i]
      if _y>=0 and _x>=0:
        accum_array[idx, :-_y if _y else None, :-_x if _x else None] += thresh_edge_image[_y:, _x:]
      if _y>=0 and _x<0:
        accum_array[idx, :-_y if _y else None, -_x:] += thresh_edge_image[_y:, :_x]
      if _y<0 and _x>=0:
        accum_array[idx, -_y:, :-_x if _x else None] += thresh_edge_image[:_y, _x:]
      if _y<0 and _x<0:
        accum_array[idx, -_y:, -_x:] += thresh_edge_image[:_y, :_x]
  return thresh_edge_image, accum_array

def find_circles(image, accum_array, radius_values, hough_thresh):
  """Find circles in an image using output from Hough transform.

  Args:
  - image (3D uint8 array): An H x W x 3 BGR color image. Here we use the
      original color image instead of its grayscale version so the circles
      can be drawn in color.
  - accum_array (3D int array): Hough transform accumulator array having shape
      R x H x W.
  - radius_values (1D int array): An array of R radius values.
  - hough_thresh (int): A threshold of votes in the accumulator array.

  Return:
  - circles (list of 3-tuples): A list of circle parameters. Each element
      (r, y, x) represents the radius and the center coordinates of a circle
      found by the program.
  - circle_image (3D uint8 array): A copy of the original image with detected
      circles drawn in color.
  """
  # raise NotImplementedError  #TODO
  image = image.copy()
  circles = []
  for idx, radius in enumerate(radius_values):
    y, x = np.where(accum_array[idx] > hough_thresh)
    for centroid in zip(x, y):
      if accum_array[idx, centroid[1], centroid[0]]<max(accum_array[idx, centroid[1]+1, centroid[0]+1], accum_array[idx, centroid[1]+1, centroid[0]-1], accum_array[idx, centroid[1]-1, centroid[0]+1], accum_array[idx, centroid[1]-1, centroid[0]-1]):
        continue # skip if not local maximum
      circles.append((radius, centroid[1], centroid[0])) 
      cv2.circle(image, centroid, radius, (0, 255, 0), 2)
  return circles, image


if __name__ == '__main__':
  #TODO
  img_name = 'coins' # since only one image is provided, I hard code the name
  img = cv2.imread('data/' + img_name + '.png', cv2.IMREAD_COLOR)
  gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # in class we detected edges in gray scale image
  edge_raw = detect_edges(gray_image)
  cv2.imwrite('output/' + img_name + "_edge_raw.png", edge_raw)
  r = np.arange(15, 35)
  thresh_edge_image, accum_array = hough_circles(edge_raw, 350, r)
  cv2.imwrite('output/' + img_name + "_edge.png", thresh_edge_image.astype(np.uint8) * 255)
  circles, circle_image = find_circles(img, accum_array, r, 225)
  cv2.imwrite('output/' + img_name + "_circle.png", circle_image)