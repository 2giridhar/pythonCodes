from pylab import *
from skimage import img_as_float


def dual_gradient_energy(img):
    """
    >>> dual_gradient_energy(img_as_float(imread("test.jpg")))
    array([[ 0.00596694,  0.02738947,  0.00788927],
           [ 0.00596694,  0.02965013,  0.00904268]])
    """
    # Function for calculating energy of each pixel
    h, w = img.shape[:2]
    energy = zeros((h, w))
    for i in range(0, w):
        for j in range(0, h):
            # Calculate the energy of each pixel
            xlow = i - 1
            xhigh = i + 1
            ylow = j - 1
            yhigh = j + 1
            if i == 0:
                # when it is first row difference need to be calculated with reference to last row
                xlow = w - 1
            if i == w - 1:
                # when it is last row difference need to be calculated with reference to first row
                xhigh = 0
            if j == 0:
                # when it is first column difference need to be calculated with reference to last column
                ylow = h - 1
            if j == h - 1:
                # when it is last column difference need to be calculated with reference to first column
                yhigh = 0
            ry = (img[yhigh, i, 0] - img[ylow, i, 0]) ** 2
            gy = (img[yhigh, i, 1] - img[ylow, i, 1]) ** 2
            by = (img[yhigh, i, 2] - img[ylow, i, 2]) ** 2
            rx = (img[j, xhigh, 0] - img[j, xlow, 0]) ** 2
            gx = (img[j, xhigh, 1] - img[j, xlow, 1]) ** 2
            bx = (img[j, xhigh, 2] - img[j, xlow, 2]) ** 2
            energy[j, i] = rx + gx + bx + ry + gy + by
    return energy


def find_cost(img):
    """
    >>> find_cost(img_as_float(imread("test.jpg")))
    (array([[ 0.00596694,  0.02738947,  0.00788927],
           [ 0.01193387,  0.03561707,  0.01693195]]), array([[ 0.00596694,  0.02738947,  0.00788927],
           [ 0.00596694,  0.02965013,  0.00904268]]))
    """
    # function for finding seam
    energy_arr = dual_gradient_energy(img)
    h, w = img.shape[:2]
    costs = zeros((h, w))
    for x in range(0, w):
        costs[0, x] = energy_arr[0, x]

    for y in range(1, h):
        for x in range(0, w):
            if x == 0:
                costs[y, x] = minimum(costs[y - 1, x], costs[y - 1, x + 1])
            elif x == w - 1:
                costs[y, x] = minimum(costs[y - 1, x], costs[y - 1, x - 1])
            else:
                min_cost = minimum(costs[y - 1, x], costs[y - 1, x + 1])
                costs[y, x] = minimum(min_cost, costs[y - 1, x - 1])
            costs[y, x] = energy_arr[y, x] + costs[y, x]
    return costs, energy_arr


def find_seam(img):
    """
    >>> find_seam(img_as_float(imread("test.jpg")))
    [(1, 0), (0, 0)]
    """
    costs, energy_arr = find_cost(img)
    h, w = img.shape[:2]
    # finding the seam with lowest energy
    min_seam = []
    min_val = inf
    min_pos = -1
    for x in range(0, w):
        if costs[h - 1, x] < min_val:
            min_val = costs[h - 1, x]
            min_pos = x

    # Tracing the seam from bottom to the top
    pos = (h - 1, min_pos)
    min_seam.append(pos)
    while pos[0] != 0:
        next_node_cost = costs[pos] - energy_arr[pos]
        y, x = pos
        if x == 0:
            if next_node_cost == costs[y - 1, x + 1]:
                pos = (y - 1, x + 1)
            else:
                pos = (y - 1, x)
        elif x < w - 1:
            if next_node_cost == costs[y - 1, x + 1]:
                pos = (y - 1, x + 1)
            elif next_node_cost == costs[y - 1, x]:
                pos = (y - 1, x)
            else:
                pos = (y - 1, x - 1)
        else:
            if next_node_cost == costs[y - 1, x]:
                pos = (y - 1, x)
            else:
                pos = (y - 1, x - 1)
        min_seam.append(pos)
    return min_seam


def plot_seam(img, seam):
    """
    >>> plot_seam(img_as_float(imread("test.jpg")), [(1, 0), (0, 0)])
    array([[[  2.55000000e+02,   2.55000000e+02,   2.55000000e+02],
            [  6.66666667e-02,   6.27450980e-02,   4.31372549e-02],
            [  1.05882353e-01,   1.09803922e-01,   9.01960784e-02]],
    <BLANKLINE>
           [[  2.55000000e+02,   2.55000000e+02,   2.55000000e+02],
            [  3.60784314e-01,   3.56862745e-01,   3.37254902e-01],
            [  4.00000000e-01,   4.03921569e-01,   3.84313725e-01]]])
    """
    # Plotting seam on the image
    plot_image = img.copy()
    for pixel in seam:
        plot_image[pixel] = 255
    return plot_image


def remove_seam(img, seam):
    """
    >>> remove_seam(img_as_float(imread("test.jpg")), [(1, 0), (0, 0)])
    array([[[ 0.06666667,  0.0627451 ,  0.04313725],
            [ 0.10588235,  0.10980392,  0.09019608]],
    <BLANKLINE>
           [[ 0.36078431,  0.35686275,  0.3372549 ],
            [ 0.4       ,  0.40392157,  0.38431373]]])
    """
    h, w = img.shape[:2]
    new_img = zeros((h, w - 1, 3))
    for y in range(0, h):
        index = 0
        for x in range(0, w):
            if (y, x) not in seam:
                new_img[y, index] = img[y, x]
                index += 1
    return new_img


def main():
    img = imread("HJoceanSmall.png")
    img = img_as_float(img)
    h, w = img.shape[:2]
    print "Initial Image Size: ", h, " x ", w
    figure()
    gray()
    subplot(1, 3, 1)
    imshow(img)
    title('Original Image')
    seam = find_seam(img)
    plot_image = plot_seam(img, seam)
    subplot(1, 3, 2)
    imshow(plot_image)
    title('Intermediate Plot Image')
    new_image = remove_seam(img, seam)
    h, w = new_image.shape[:2]
    print "Final Image Size: ", h, " x ", w
    subplot(1, 3, 3)
    imshow(new_image)
    title('Final Image')
    show()


if __name__ == '__main__':
    main()
