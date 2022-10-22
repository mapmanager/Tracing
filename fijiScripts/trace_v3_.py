"""
Try using new fiji

Of course this does not work

See here for code snippet:
    https://forum.image.sc/t/minimal-autotrace-code-for-snt-java/51654
    
Install
	- Need to upgrade stock Fiji with 'Neuroanatomy' update site
    - See: https://imagej.net/update-sites/neuroanatomy/

Fiji.app
/Users/cudmore/Documents/fiji_new/Fiji.app/Contents/MacOS/ImageJ-macosx
"""

import org.scijava

from ij import IJ

from sc.fiji import snt
from sc.fiji.snt.util import PointInImage
from sc.fiji.snt.tracing import TracerThread

doDebug = True

def myPrint(theStr):
	global doDebug
	if doDebug:
		print('[BobNeuriteTracer Jython]: ' + theStr)

def runTest():
	#fijiApp = '/Users/cudmore/Documents/fiji_new/Fiji.app/Contents/MacOS/ImageJ-macosx'
	
	tifPath = '/Users/cudmore/Sites/PyMapManager-Data/one-timepoint/rr30a_s0_ch2.tif'
	
	# Load tif
	imp = IJ.openImage(tifPath)  
	if imp is None:
		myPrint('ERROR: opening tiff file:'+tifPath)
		myPrint('  ->> Aborting')
		return 0
		
	myPrint('  opened tifPath: '+tifPath)

	# remove calibration, all tracing is done in pixels
	imp.setCalibration(None)

	# initialize(boolean singlePane, int channel, int frame)
	#plugin = snt.SNT.initialize(imp, False)
	myContext = org.scijava.Context()
	plugin = snt.SNT(myContext, imp)
	plugin.enableAstar(True)
	plugin.getPathAndFillManager().clear();
	#plugin.startHessian("primary", 1.0, 25.0, True)

	start_point = PointInImage(400,500,0)
	end_point = PointInImage(365,0,0)

	print(start_point,end_point)

	primary_path = plugin.autoTrace(start_point, end_point, None)

print(__name__)

if __name__ == '__main__':
	runTest()