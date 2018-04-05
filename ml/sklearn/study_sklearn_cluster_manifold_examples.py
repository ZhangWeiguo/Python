def example_Scurve():
    from time import time

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.ticker import NullFormatter

    from sklearn import manifold, datasets

    # Next line to silence pyflakes. This import is needed.
    Axes3D

    n_points = 1000
    X, color = datasets.samples_generator.make_s_curve(n_points, random_state=0)
    n_neighbors = 10
    n_components = 2

    fig = plt.figure(figsize=(15, 8))
    plt.suptitle("Manifold Learning with %i points, %i neighbors"
                 % (1000, n_neighbors), fontsize=14)

    try:
        # compatibility matplotlib < 1.0
        ax = fig.add_subplot(251, projection='3d')
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, cmap=plt.cm.Spectral)
        ax.view_init(4, -72)
    except:
        ax = fig.add_subplot(251, projection='3d')
        plt.scatter(X[:, 0], X[:, 2], c=color, cmap=plt.cm.Spectral)

    methods = ['standard', 'ltsa', 'hessian', 'modified']
    labels = ['LLE', 'LTSA', 'Hessian LLE', 'Modified LLE']

    for i, method in enumerate(methods):
        t0 = time()
        Y = manifold.LocallyLinearEmbedding(n_neighbors, n_components,
                                            eigen_solver='auto',
                                            method=method).fit_transform(X)
        t1 = time()
        print("%s: %.2g sec" % (methods[i], t1 - t0))

        ax = fig.add_subplot(252 + i)
        plt.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral)
        plt.title("%s (%.2g sec)" % (labels[i], t1 - t0))
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(NullFormatter())
        plt.axis('tight')

    t0 = time()
    Y = manifold.Isomap(n_neighbors, n_components).fit_transform(X)
    t1 = time()
    print("Isomap: %.2g sec" % (t1 - t0))
    ax = fig.add_subplot(257)
    plt.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral)
    plt.title("Isomap (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    t0 = time()
    mds = manifold.MDS(n_components, max_iter=100, n_init=1)
    Y = mds.fit_transform(X)
    t1 = time()
    print("MDS: %.2g sec" % (t1 - t0))
    ax = fig.add_subplot(258)
    plt.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral)
    plt.title("MDS (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    t0 = time()
    se = manifold.SpectralEmbedding(n_components=n_components,
                                    n_neighbors=n_neighbors)
    Y = se.fit_transform(X)
    t1 = time()
    print("SpectralEmbedding: %.2g sec" % (t1 - t0))
    ax = fig.add_subplot(259)
    plt.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral)
    plt.title("SpectralEmbedding (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    t0 = time()
    tsne = manifold.TSNE(n_components=n_components, init='pca', random_state=0)
    Y = tsne.fit_transform(X)
    t1 = time()
    print("t-SNE: %.2g sec" % (t1 - t0))
    ax = fig.add_subplot(2, 5, 10)
    plt.scatter(Y[:, 0], Y[:, 1], c=color, cmap=plt.cm.Spectral)
    plt.title("t-SNE (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    plt.show()

def example_ball():
    from time import time

    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.ticker import NullFormatter

    from sklearn import manifold
    from sklearn.utils import check_random_state

    # Next line to silence pyflakes.
    Axes3D

    # Variables for manifold learning.
    n_neighbors = 10
    n_samples = 1000

    # Create our sphere.
    random_state = check_random_state(0)
    p = random_state.rand(n_samples) * (2 * np.pi - 0.55)
    t = random_state.rand(n_samples) * np.pi

    # Sever the poles from the sphere.
    indices = ((t < (np.pi - (np.pi / 8))) & (t > ((np.pi / 8))))
    colors = p[indices]
    x, y, z = np.sin(t[indices]) * np.cos(p[indices]), \
              np.sin(t[indices]) * np.sin(p[indices]), \
              np.cos(t[indices])

    # Plot our dataset.
    fig = plt.figure(figsize=(15, 8))
    plt.suptitle("Manifold Learning with %i points, %i neighbors"
                 % (1000, n_neighbors), fontsize=14)

    ax = fig.add_subplot(251, projection='3d')
    ax.scatter(x, y, z, c=p[indices], cmap=plt.cm.rainbow)
    try:
        # compatibility matplotlib < 1.0
        ax.view_init(40, -10)
    except:
        pass

    sphere_data = np.array([x, y, z]).T

    # Perform Locally Linear Embedding Manifold learning
    methods = ['standard', 'ltsa', 'hessian', 'modified']
    labels = ['LLE', 'LTSA', 'Hessian LLE', 'Modified LLE']

    for i, method in enumerate(methods):
        t0 = time()
        trans_data = manifold \
            .LocallyLinearEmbedding(n_neighbors, 2,
                                    method=method).fit_transform(sphere_data).T
        t1 = time()
        print("%s: %.2g sec" % (methods[i], t1 - t0))

        ax = fig.add_subplot(252 + i)
        plt.scatter(trans_data[0], trans_data[1], c=colors, cmap=plt.cm.rainbow)
        plt.title("%s (%.2g sec)" % (labels[i], t1 - t0))
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(NullFormatter())
        plt.axis('tight')

    # Perform Isomap Manifold learning.
    t0 = time()
    trans_data = manifold.Isomap(n_neighbors, n_components=2) \
        .fit_transform(sphere_data).T
    t1 = time()
    print("%s: %.2g sec" % ('ISO', t1 - t0))

    ax = fig.add_subplot(257)
    plt.scatter(trans_data[0], trans_data[1], c=colors, cmap=plt.cm.rainbow)
    plt.title("%s (%.2g sec)" % ('Isomap', t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    # Perform Multi-dimensional scaling.
    t0 = time()
    mds = manifold.MDS(2, max_iter=100, n_init=1)
    trans_data = mds.fit_transform(sphere_data).T
    t1 = time()
    print("MDS: %.2g sec" % (t1 - t0))

    ax = fig.add_subplot(258)
    plt.scatter(trans_data[0], trans_data[1], c=colors, cmap=plt.cm.rainbow)
    plt.title("MDS (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    # Perform Spectral Embedding.
    t0 = time()
    se = manifold.SpectralEmbedding(n_components=2,
                                    n_neighbors=n_neighbors)
    trans_data = se.fit_transform(sphere_data).T
    t1 = time()
    print("Spectral Embedding: %.2g sec" % (t1 - t0))

    ax = fig.add_subplot(259)
    plt.scatter(trans_data[0], trans_data[1], c=colors, cmap=plt.cm.rainbow)
    plt.title("Spectral Embedding (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    # Perform t-distributed stochastic neighbor embedding.
    t0 = time()
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    trans_data = tsne.fit_transform(sphere_data).T
    t1 = time()
    print("t-SNE: %.2g sec" % (t1 - t0))

    ax = fig.add_subplot(2, 5, 10)
    plt.scatter(trans_data[0], trans_data[1], c=colors, cmap=plt.cm.rainbow)
    plt.title("t-SNE (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    plt.show()

def example_digits():
    from time import time

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import offsetbox
    from sklearn import (manifold, datasets, decomposition, ensemble,
                         discriminant_analysis, random_projection)

    digits = datasets.load_digits(n_class=6)
    X = digits.data
    y = digits.target
    n_samples, n_features = X.shape
    n_neighbors = 30

    # ----------------------------------------------------------------------
    # Scale and visualize the embedding vectors
    def plot_embedding(X, title=None):
        x_min, x_max = np.min(X, 0), np.max(X, 0)
        X = (X - x_min) / (x_max - x_min)

        plt.figure()
        ax = plt.subplot(111)
        for i in range(X.shape[0]):
            plt.text(X[i, 0], X[i, 1], str(digits.target[i]),
                     color=plt.cm.Set1(y[i] / 10.),
                     fontdict={'weight': 'bold', 'size': 9})

        if hasattr(offsetbox, 'AnnotationBbox'):
            # only print thumbnails with matplotlib > 1.0
            shown_images = np.array([[1., 1.]])  # just something big
            for i in range(digits.data.shape[0]):
                dist = np.sum((X[i] - shown_images) ** 2, 1)
                if np.min(dist) < 4e-3:
                    # don't show points that are too close
                    continue
                shown_images = np.r_[shown_images, [X[i]]]
                imagebox = offsetbox.AnnotationBbox(
                    offsetbox.OffsetImage(digits.images[i], cmap=plt.cm.gray_r),
                    X[i])
                ax.add_artist(imagebox)
        plt.xticks([]), plt.yticks([])
        if title is not None:
            plt.title(title)

    # ----------------------------------------------------------------------
    # Plot images of the digits
    n_img_per_row = 20
    img = np.zeros((10 * n_img_per_row, 10 * n_img_per_row))
    for i in range(n_img_per_row):
        ix = 10 * i + 1
        for j in range(n_img_per_row):
            iy = 10 * j + 1
            img[ix:ix + 8, iy:iy + 8] = X[i * n_img_per_row + j].reshape((8, 8))

    plt.imshow(img, cmap=plt.cm.binary)
    plt.xticks([])
    plt.yticks([])
    plt.title('A selection from the 64-dimensional digits dataset')

    # ----------------------------------------------------------------------
    # Random 2D projection using a random unitary matrix
    print("Computing random projection")
    rp = random_projection.SparseRandomProjection(n_components=2, random_state=42)
    X_projected = rp.fit_transform(X)
    plot_embedding(X_projected, "Random Projection of the digits")

    # ----------------------------------------------------------------------
    # Projection on to the first 2 principal components

    print("Computing PCA projection")
    t0 = time()
    X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X)
    plot_embedding(X_pca,
                   "Principal Components projection of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # Projection on to the first 2 linear discriminant components

    print("Computing Linear Discriminant Analysis projection")
    X2 = X.copy()
    X2.flat[::X.shape[1] + 1] += 0.01  # Make X invertible
    t0 = time()
    X_lda = discriminant_analysis.LinearDiscriminantAnalysis(n_components=2).fit_transform(X2, y)
    plot_embedding(X_lda,
                   "Linear Discriminant projection of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # Isomap projection of the digits dataset
    print("Computing Isomap embedding")
    t0 = time()
    X_iso = manifold.Isomap(n_neighbors, n_components=2).fit_transform(X)
    print("Done.")
    plot_embedding(X_iso,
                   "Isomap projection of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # Locally linear embedding of the digits dataset
    print("Computing LLE embedding")
    clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                          method='standard')
    t0 = time()
    X_lle = clf.fit_transform(X)
    print("Done. Reconstruction error: %g" % clf.reconstruction_error_)
    plot_embedding(X_lle,
                   "Locally Linear Embedding of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # Modified Locally linear embedding of the digits dataset
    print("Computing modified LLE embedding")
    clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                          method='modified')
    t0 = time()
    X_mlle = clf.fit_transform(X)
    print("Done. Reconstruction error: %g" % clf.reconstruction_error_)
    plot_embedding(X_mlle,
                   "Modified Locally Linear Embedding of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # HLLE embedding of the digits dataset
    print("Computing Hessian LLE embedding")
    clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                          method='hessian')
    t0 = time()
    X_hlle = clf.fit_transform(X)
    print("Done. Reconstruction error: %g" % clf.reconstruction_error_)
    plot_embedding(X_hlle,
                   "Hessian Locally Linear Embedding of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # LTSA embedding of the digits dataset
    print("Computing LTSA embedding")
    clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                          method='ltsa')
    t0 = time()
    X_ltsa = clf.fit_transform(X)
    print("Done. Reconstruction error: %g" % clf.reconstruction_error_)
    plot_embedding(X_ltsa,
                   "Local Tangent Space Alignment of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # MDS  embedding of the digits dataset
    print("Computing MDS embedding")
    clf = manifold.MDS(n_components=2, n_init=1, max_iter=100)
    t0 = time()
    X_mds = clf.fit_transform(X)
    print("Done. Stress: %f" % clf.stress_)
    plot_embedding(X_mds,
                   "MDS embedding of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # Random Trees embedding of the digits dataset
    print("Computing Totally Random Trees embedding")
    hasher = ensemble.RandomTreesEmbedding(n_estimators=200, random_state=0,
                                           max_depth=5)
    t0 = time()
    X_transformed = hasher.fit_transform(X)
    pca = decomposition.TruncatedSVD(n_components=2)
    X_reduced = pca.fit_transform(X_transformed)

    plot_embedding(X_reduced,
                   "Random forest embedding of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # Spectral embedding of the digits dataset
    print("Computing Spectral embedding")
    embedder = manifold.SpectralEmbedding(n_components=2, random_state=0,
                                          eigen_solver="arpack")
    t0 = time()
    X_se = embedder.fit_transform(X)

    plot_embedding(X_se,
                   "Spectral embedding of the digits (time %.2fs)" %
                   (time() - t0))

    # ----------------------------------------------------------------------
    # t-SNE embedding of the digits dataset
    print("Computing t-SNE embedding")
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    t0 = time()
    X_tsne = tsne.fit_transform(X)

    plot_embedding(X_tsne,
                   "t-SNE embedding of the digits (time %.2fs)" %
                   (time() - t0))
    plt.show()

if __name__=='__main__':
    #example_Scurve()
    example_ball()
    #example_digits()