"""
"""
import numpy as np

import matplotlib.pyplot as plt

import pmmtracing

from pmmtracing._logger import logger

def _plot(stack, xyzControlPoint : np.ndarray, tracing):
    """
    Args:
        stack: pymapmanager.stack
        xyzControlPoint:
        tracing:
    """

    # max image
    maxImage = stack.getMaxProject(channel=1)

    plt.imshow(maxImage)
    
    # overlay tracing
    if tracing is not None:
        x = tracing[:,0]
        y = tracing[:,1]
        plt.scatter(x, y, c='y', s=5)

    # overlay controlPnt
    if xyzControlPoint is not None:
        x = xyzControlPoint[:,0]
        y = xyzControlPoint[:,1]
        plt.scatter(x, y, c='r', s=8)

    #plt.show()

def test_tracing_fiji_reconstruct(tifPath):
    """Trace all segments in an existing stack.
    """

    import pymapmanager

    stack = pymapmanager.stack(tifPath)
    pa = stack.getPointAnnotations()

    # TODO: (cudmore) some point annotations do not have segmentID -->> NAN
    #segmentID = pa.getValues(colName = 'segmentID')
    
    roiType = pymapmanager.annotations.pointTypes.controlPnt
    segmentID = pa.getRoiType_col(['segmentID'], roiType)
    # segmentID is coming back as dtype 'object'

    segmentList = np.unique(segmentID)
    print('segmentList:', segmentList)

    tracing = pmmtracing.fijiTracer()

    for segmentID in segmentList:
        roiType = 'controlPnt'
        #segmentID = 0
        compareEqual = pymapmanager.annotations.comparisonTypes.equal    

        # get [[x,y,z]] of columns natchiing roitType and segmentID
        getColumns = ['x', 'y', 'z']
        compareColNames = ['roiType', 'segmentID']
        comparisons = [compareEqual, compareEqual]
        compareValues = [roiType, segmentID]
        xyzControlPoint = pa.getValuesWithCondition(getColumns,
                                    compareColNames,
                                    comparisons,
                                    compareValues)
        xyzControlPoint = xyzControlPoint.astype(int)

        fullTracing = tracing.trace(tifPath, xyzControlPoint)

        if fullTracing is None:
            logger.error(f'TRACING FAILED for segmentID:{segmentID}')
            continue
        
        logger.info(f'Got {len(fullTracing)} points in tracing.')
        
        if 1:
            npFullTracing = np.array(fullTracing)  # List[List[int]] -> np.ndarray
            _plot(stack, xyzControlPoint, npFullTracing)
    #
    plt.show()

def test_tracing_pymapmanager():
    """Test tracing by loading a stack/annotations with pymapmanager.
    """

    import pymapmanager

    # trace existing segment ID 0
    tifPath = '/Users/cudmore/Sites/PyMapManager-Data/one-timepoint/rr30a_s0_ch2.tif'

    stack = pymapmanager.stack(tifPath)

    pa = stack.getPointAnnotations()
    #la = stack.getLineAnnotations

    # pull out what we will trace
    # we will trace segment 0
    # we need controlPnt from segmentID 0

    roiType = 'controlPnt'
    segmentID = 0
    compareEqual = pymapmanager.annotations.comparisonTypes.equal    

    # get [[x,y,z]] of columns natchiing roitType and segmentID
    getColumns = ['x', 'y', 'z']
    compareColNames = ['roiType', 'segmentID']
    comparisons = [compareEqual, compareEqual]
    compareValues = [roiType, segmentID]
    xyzControlPoint = pa.getValuesWithCondition(getColumns,
                                compareColNames,
                                comparisons,
                                compareValues)
    xyzControlPoint = xyzControlPoint.astype(int)

    #print(f'xyzControlPoint: {type(xyzControlPoint)}, {xyzControlPoint.shape}')

    # do the tracing
    tracing = pmmtracing.fijiTracer()
    
    #fijiPath = '/Users/cudmore/Downloads/Fiji_20170530.app/Contents/MacOS/ImageJ-macosx'
    #tracing.setFijiPath(fijiPath)
    
    fullTracing = tracing.trace(tifPath, xyzControlPoint)

    if fullTracing is None:
        logger.error('TRACING FAILED')
        return
    
    logger.info(f'Got {len(fullTracing)} points in tracing.')
    
    if 1:
        npFullTracing = np.array(fullTracing)  # List[List[int]] -> np.ndarray
        _plot(stack, xyzControlPoint, npFullTracing)
        plt.show()

if __name__ == '__main__':
    
    # works
    # one segment reconstructions
    test_tracing_pymapmanager()

    # full reconstruction
    #tifPath = '/Users/cudmore/Sites/PyMapManager-Data/one-timepoint/rr30a_s0_ch2.tif'
    #test_tracing_fiji_reconstruct(tifPath)
