def getHOGfeat( image,stride = 8, orientations=8, pixels_per_cell=(8, 8),cells_per_block=(2, 2)):
    cx, cy = pixels_per_cell
    bx, by = cells_per_block
    sx, sy = image.shape
    n_cellsx = int(np.floor(sx // cx))  # number of cells in x
    n_cellsy = int(np.floor(sy // cy))  # number of cells in y
    n_blocksx = (n_cellsx - bx) + 1
    n_blocksy = (n_cellsy - by) + 1
    gx = zeros((sx, sy), dtype=np.double)
    gy = zeros((sx, sy), dtype=np.double)
    eps = 1e-5
    grad = zeros((sx, sy, 2), dtype=np.double)
    for i in xrange(1, sx-1):
        for j in xrange(1, sy-1):
            gx[i, j] = image[i, j-1] - image[i, j+1]
            gy[i, j] = image[i+1, j] - image[i-1, j]
            grad[i, j, 0] = arctan(gy[i, j] / (gx[i, j] + eps)) * 180 / math.pi
            if gx[i, j] < 0:
                grad[i, j, 0] += 180
            grad[i, j, 0] = (grad[i, j, 0] + 360) % 360
            grad[i, j, 1] = sqrt(gy[i, j] ** 2 + gx[i, j] ** 2)
    normalised_blocks = np.zeros((n_blocksy, n_blocksx, by * bx * orientations))
    for y in xrange(n_blocksy):
        for x in xrange(n_blocksx):
            block = grad[y*stride:y*stride+16, x*stride:x*stride+16]
            hist_block = zeros(32, dtype=double)
            eps = 1e-5
            for k in xrange(by):
                for m in xrange(bx):
                    cell = block[k*8:(k+1)*8, m*8:(m+1)*8]
                    hist_cell = zeros(8, dtype=double)
                    for i in xrange(cy):
                        for j in xrange(cx):
                            n = int(cell[i, j, 0] / 45)
                            hist_cell[n] += cell[i, j, 1]
                    hist_block[(k * bx + m) * orientations:(k * bx + m + 1) * orientations] = hist_cell[:]
            normalised_blocks[y, x, :] = hist_block / np.sqrt(hist_block.sum() ** 2 + eps)
    return normalised_blocks.ravel()