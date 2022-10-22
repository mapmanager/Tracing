"""
Follow installation of PyImageJ here

https://pyimagej.readthedocs.io/en/latest/Install.html

conda install mamba -n base -c conda-forge 
mamba create -n pyimagej -c conda-forge pyimagej openjdk=8
conda activate pyimagej    
"""

# Create an ImageJ2 gateway with the newest available version of ImageJ2.
import imagej
import matplotlib.pyplot as plt
import xarray

from scyjava import jimport


def runSnt():
    
    # fiji/imagej with plugins
    ij = imagej.init('sc.fiji:fiji')

    # not available on macos
    # ij = imagej.init('sc.fiji:fiji', mode='interactive')

    print('ij version:', ij.getVersion())  # 2.9.0/1.53t

    # does not work
    # MouseLightLoader = jimport('tracing.io.MouseLightLoader')
    # TreeStatistics = jimport('tracing.analysis.TreeStatistics')

    # does not work, see
    # https://github.com/morphonets/SNT/issues/67
    # SNTUtils = jimport('sc.fiji.snt.SNTUtils')
    # print("We are running SNT %s" % SNTUtils.VERSION)

def run2():
    image0 = [
            [1,2,3],
            [4,5,6],
            [7,8,9]
    ]
    plt.imshow(image0)

    print('show done')

    plt.show()

def run():
    print('start')

    print('import done')

    # imagej
    #ij = imagej.init()
    
    # fiji/imagej with plugins
    ij = imagej.init('sc.fiji:fiji')

    print('init done')

    # Load an image.
    image_url = 'https://imagej.net/images/clown.jpg'
    jimage = ij.io().open(image_url)

    # <java class 'net.imagej.DefaultDataset'>
    print('image open done jimage:', type(jimage))

    # Convert the image from ImageJ2 to xarray, a package that adds
    # labeled datasets to numpy (http://xarray.pydata.org/en/stable/).
    # image is <class 'xarray.core.dataarray.DataArray'>
    image = ij.py.from_java(jimage)

    #print(image)

    # shape is (200, 320, 3)
    print('conversion done image:', image.shape, type(image))

    print('plotting ...')

    # <class 'xarray.core.dataarray.DataArray'>
    image0 = image[:,:,0]
    print('image0', image0.shape, type(image0))

    # Display the image (backed by matplotlib).
    #ij.py.show(image, cmap='gray')

    image0 = [
            [1,2,3],
            [4,5,6],
            [7,8,9]
    ]
    plt.imshow(image0)

    #xarray.plot.imshow(image0)
    #image0.plot()

    print('show done')

    plt.show()

if __name__ == '__main__':
    #run()
    #run2()
    runSnt()
