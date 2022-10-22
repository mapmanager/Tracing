"""
Class to trace a sequency of points in a 3D image using
the Fiji plugin "Simple Neurite Tracer.

Requires:
    This requires the 20170520 'lifeline' version of Fiji
    <user>/Documents/fiji_old/Fiji.app
"""
import os
import subprocess
import pathlib

from typing import List, Union
import ast

from pmmtracing._logger import logger

def _getUserDocumentsFolder():
    """Get <user>/Documents path.
    """
    userPath = pathlib.Path.home()
    userDocumentsFolder = os.path.join(userPath, 'Documents')
    if not os.path.isdir(userDocumentsFolder):
        logger.error(f'Did not find path "{userDocumentsFolder}"')
        logger.error(f'   Using "{userPath}"')
        return userPath
    else:
        return userDocumentsFolder

class mmTracer:
    def __init__(self):
        pass
    
    def trace(tifPath : str, controlPoints : List[List[int]]):
        pass

class fijiTracer(mmTracer):
    def __init__(self) -> None:
        
        self._fijiApp = None
        self.setFijiPath()
        # assign self._fijiApp
        # Full path to Fiji.app like
        # Fiji.app/Contents/MacOS/ImageJ-macosx
        #  This must be the 'lifeline' version dated 20170530

        # __file__ is fulll path to this file
        _folder, _ = os.path.split(__file__)  # _folder is Tracing/pmmtracing/
        _folder, _ = os.path.split(_folder)  # _folder is Tracing/

        _fijiScriptPath = os.path.join(_folder, 'fijiScripts')
        # Path to folder with all files needed for tracing.
        #  - Fiji Jython script 'BobNeuriteTracer_v2_.py'
        #  - where we save what to trace 'tracingparameters.txt'
        #  - where we load full tracing results 'tracing_out.txt'

        self._pluginScript = os.path.join(_fijiScriptPath, 'BobNeuriteTracer_v2_.py')
        # Full path to Jython script to run as Fiji plugin.

        self._seedPath = os.path.join(_fijiScriptPath, 'tracingparameters.txt')
        # Full path to text file we seed with tif and list of points to trace
        # 1) save 'tracingparameters.txt' with tif and seed points, looks like this
        #    tiffFile=/Volumes/mapmanager/Users/cudmore/Dropbox/data/Shu-Ling/Shu-Ling_tif/mm_maps/ling_map_1/raw/ling_map_1_s0_ch2.tif
        #    point=228,343,18
        #    point=261,341,18
        #    point=285,327,18

        self._tracingOutputPath = os.path.join(_fijiScriptPath, 'tracing_out.txt')
        # file that Fiji Jython script saves the full tracing results
        # each row contains one point in tracing (x,y,z)
        # x, y, z, is float but should always be '.0'

    def _defaultFijiPath(Self):
        _folder = 'fiji_old'
        #_folder = 'fiji_new'
        
        userDocuments = _getUserDocumentsFolder()
        fijiPath = os.path.join(userDocuments, _folder)
        fijiPath = os.path.join(fijiPath, 'Fiji.app/Contents/MacOS/ImageJ-macosx')
        return fijiPath

    def setFijiPath(self, path : str = None):
        """Set full path to Fiji.app.
        
        This is usually not in our source tree. It is on the users computer.

        Like:
            /Users/cudmore/Sites/Tracing/Fiji.app/Contents/MacOS/ImageJ-macosx

        """
        if path is None:
            path = self._defaultFijiPath()

        if not os.path.isfile(path):
            logger.error(f'Did not find Fiji.app path: {path}')
            logger.error(f'Fiji.app (lifeline 20170530) should be in folder:')
            logger.error(f'<user>/Documents/fiji_old')
            return
        
        self._fijiApp = path

    def _seedTracing(self, tifPath :str, points : List[List[int]]):
        """Seed the tracing with path to tif file and list of seed points.

        Args:
            tifPath: Full path to tif file.
            points: List of points to trace

        Seed file looks like this
            tiffFile=/Volumes/mapmanager/Users/cudmore/Dropbox/data/Shu-Ling/Shu-Ling_tif/mm_maps/ling_map_1/raw/ling_map_1_s0_ch2.tif
            point=228,343,18
            point=261,341,18
            point=285,327,18
            ...
        """
    
        if points is None or len(points)<2:
            logger.error(f'Must seed tracing with >=2 points but got {len(points)} points.')
            return
        
        with open(self._seedPath, 'w') as f:
            oneLine = f'tiffFile={tifPath}\n'
            #print(oneLine)
            f.write(oneLine)

        with open(self._seedPath, 'a') as f:
            for point in points:
                oneLine = f'point={point[0]},{point[1]},{point[2]}\n'
                #print(oneLine)
                f.write(oneLine)

        #logger.info(f'Seeded with {len(points)} points into {self._seedPath}')

    def trace(self, tifPath : str, seedPoints : List[List[int]]) -> List[List[int]]:
        """Perform tracing.
        
        Args:
            tifPath: Full path to tif image
            seedPoints: List of point to seed the tracing, each point is [x, y, z]

        Algorithm:
            - Uses seed points in file 'tracingparameters.txt'
            - Runs Fiji Jython script 'BobNeuriteTracer_v1_'
            - Script saves full tracing in 'tracing_out.txt'
        """
                
        # remove output, if tracing fails it will not exist
        if os.path.isfile(self._tracingOutputPath):
            #logger.info(f'Removing previous tracing output : {self._tracingOutputPath}')
            os.remove(self._tracingOutputPath)

        # save tracingparameters.txt
        self._seedTracing(tifPath, seedPoints)

        #logger.info(f'_fijiApp:{self._fijiApp}')
        #logger.info(f'_pluginScript:{self._pluginScript}')
        
        logger.info(f'Tracing ...')
        logger.info(f'  _fijiApp: {self._fijiApp}')
        logger.info(f'  _pluginScript: {self._pluginScript}')
        logger.info(f'  tifPath: {tifPath}')
        logger.info(f'  {len(seedPoints)} seed points like {seedPoints[0:3]} ...')
        
        cmd = [self._fijiApp, self._pluginScript]

        _popen = subprocess.Popen(cmd)

        while _popen.poll() is None:
            continue
            # allow ctrl-c ???
            # we need to embed this into PyQt to handle event loop?

        # load the full tracing, can be None
        tracingPoints = self._loadTracing()

        return tracingPoints

    def _loadTracing(self) -> Union[None, List[List[int]]]:
        """Load tracing results.
        """
        if not os.path.isfile(self._tracingOutputPath):
            logger.error(f'Did not find tracing output:{self._tracingOutputPath}')
            return

        with open(self._tracingOutputPath) as f:
            lines = f.read().splitlines()

        # convert strings '(x,y,z)' to [x,y,z]
        outLines = []
        for line in lines:
            oneLine = ast.literal_eval(line)
            oneLine = list(oneLine)
            outLines.append(oneLine)
        
        #logger.info(f'Loaded {len(outLines)} traced points from {self._tracingOutputPath}')

        return outLines

if __name__ == '__main__':
    pass