from argon2 import hash_password_raw
import cv2
import numpy as np
import glob
import os

def read_images(image_directory):
    # Read all jpg images from the specified directory
    return [cv2.imread(image_path) for image_path in glob.glob(f"{image_directory}/*.jpg")]

def find_image_points(images, pattern_size):
    world_points = []
    image_points = []
    
    # TODO: Initialize the chessboard world coordinate points
    def init_world_points(pattern_size):
        # Students should fill in code here to generate the world coordinates of the chessboard
        return np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    
    # TODO: Detect chessboard corners in each image
    def detect_corners(image, pattern_size):
        # Students should fill in code here to detect corners using cv2.findChessboardCorners or another method
        ret, corners = cv2.findChessboardCorners(image, pattern_size, None, cv2.CALIB_CB_ADAPTIVE_THRESH)
        if ret:
            return corners.reshape(-1, 2)
        # print("Failed to detect corners in image") # To debug.
        return None

    # TODO: Complete the loop below to obtain the corners of each image and the corresponding world coordinate points
    for image in images:
        corners = detect_corners(image, pattern_size)
        if corners is not None:
            image_points.append(corners)
            world_points.append(init_world_points(pattern_size))
    
    return world_points, image_points

def calibrate_camera(world_points, image_points, size):
    assert len(world_points) == len(image_points), "The number of world coordinates and image coordinates must match"
    world_points = np.array(world_points)
    image_points = np.array(image_points)
    num_planes, _, _ = world_points.shape
    center_point = np.array(size) / 2
    vij = lambda i, j: np.array([H[0, i] * H[0, j], H[0, i] * H[1, j] + H[1, i] * H[0, j], H[1, i] * H[1, j], H[2, i] * H[0, j] + H[0, i] * H[2, j], H[2, i] * H[1, j] + H[1, i] * H[2, j], H[2, i] * H[2, j]])
    P = []
    
    # TODO main loop, use least squares to solve for P and then decompose H to get K and R
    # The steps are as follows:
    # 1. Construct the matrix A and B
    # 2. Solve for P using least squares
    # 3. Decompose P to get K and R
    
    C = []
    for plane in range(num_planes):
        world_point, image_point = world_points[plane], image_points[plane]
        index = np.argsort(np.linalg.norm(image_point - center_point, axis=1))[:200]
        world_point, image_point = world_point[index], image_point[index]
        A = []
        
        for point in range(200):
            x, y = world_point[point]
            u, v = image_point[point]
            A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
            A.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])

        A = np.array(A)
        e_val, e_vec = np.linalg.eig(A.T @ A)
        H = e_vec[:, np.argmin(e_val)].reshape(3, 3)
        P.append(H)
        
        C.append(vij(0, 1))
        C.append(vij(0, 0) - vij(1, 1))
    
    C = np.array(C)
    e_val, e_vec = np.linalg.eig(C.T @ C)
    B = e_vec[:, np.argmin(e_val)]
    B = np.array([[B[0], B[1], B[3]], [B[1], B[2], B[4]], [B[3], B[4], B[5]]])
    K = np.linalg.cholesky(B)
    K = np.linalg.inv(K.T)
    K /= K[2, 2]
    
    # Please ensure that the diagonal elements of K are positive
    
    return K, P

# Main process
image_path = 'original_data'
images = read_images(image_path)

# TODO: I'm too lazy to count the number of chessboard squares, count them yourself
pattern_size = (31, 23)  # The pattern size of the chessboard 

if not os.path.exists('./points.npy'):
    world_points, image_points = find_image_points(images, pattern_size)
    np.save('./points.npy', (world_points, image_points))
else:
    world_points, image_points = np.load('./points.npy', allow_pickle=True)
    
camera_matrix, projection_matrix = calibrate_camera(world_points, image_points, images[0].shape[1::-1])

print("Camera Calibration Matrix:")
print(camera_matrix)

def test(image_directory, pattern_size, size):
    # In this function, you are allowed to use OpenCV to verify your results. This function is optional and will not be graded.
    # return None, directly print the results
    # TODO
    world_points, image_points = np.load('./points.npy', allow_pickle=True)
    world_points = np.array(world_points)
    image_points = np.array(image_points)
    world_points = [np.append(view, np.zeros((world_points[0].shape[0], 1), dtype=np.float32), axis=1) for view in world_points]
    _, K, _, _, _ = cv2.calibrateCamera(world_points, image_points, size, None, None)
    print("Camera Matrix:\n", K)

def reprojection_error(world_points, image_points, projection_matrix):
    # In this function, you are allowed to use OpenCV to verify your results.
    # show the reprojection error of each image
    errors = [
        np.mean(np.linalg.norm(
            (projection_matrix[i] @ np.append(wp, np.ones((len(wp), 1)), axis=1).T)[:2] / 
            (projection_matrix[i] @ np.append(wp, np.ones((len(wp), 1)), axis=1).T)[2] - 
            ip.T, axis=0
        ))
        for i, (wp, ip) in enumerate(zip(world_points, image_points))
    ]

    print("Reprojection Error:\n", errors)
    

    

print("Camera Calibration Matrix by OpenCV:")
test(image_path, pattern_size, images[0].shape[1::-1])
reprojection_error(world_points, image_points, projection_matrix)
