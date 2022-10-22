import os
import subprocess

def runScript():
    
    # is not part of pymapmanager, an app installed on users computer
    fijiPath = '/Users/cudmore/Downloads/Fiji_20170530.app/Contents/MacOS/ImageJ-macosx'

    if not os.path.isfile(fijiPath):
        print(f'ERROR: Did not find fijiPath:{fijiPath}')
        return

    # __file__ is full path to this file
    _folder, _ = os.path.split(__file__)  # _folder is Tracing/sandbox/
    _folder, _ = os.path.split(_folder)  # _folder is Tracing/

    # folder with
    #  - Fiji Jython script
    #  - where we save what to trace 'tracingparameters.txt'
    #  - where we load full tracing results 'tracing_out.txt'
    tracingFolderPath = os.path.join(_folder, 'fijiScripts')

    if not os.path.isdir(tracingFolderPath):
        print(f'ERROR: Did not find fijiPath:{tracingFolderPath}')
        return

    # Our Fiji Jython script to do the tracing
    pluginPath = os.path.join(tracingFolderPath, 'BobNeuriteTracer_v1_.py')

    # File where we write path to tif and [points] to seed the tracing
    tracingParametersPath = os.path.join(tracingFolderPath, 'tracingparameters.txt')

    # File that is saved by Jython plugin when tracing is finished
    #tracingFinishedPath = os.path.join(tracingFolderPath, 'tracing_finished.txt')

    # file that Fiji Jython script saves the full tracing results
    # each row contains one point in tracing (x,y,z)
    # x, y, z, is float but should always be '.0'
    tracingOutPath = os.path.join(tracingFolderPath, 'tracing_out.txt')

    print(f'  fijiPath:', fijiPath)
    print(f'  pluginPath:', pluginPath)
    #print(f'  tracingFinishedPath:', tracingFinishedPath)
    print(f'  tracingParametersPath:', tracingParametersPath)
    print(f'  tracingOutPath:', tracingOutPath)

    # run the plugin

    # 1) save 'tracingparameters.txt' with tif and seed points, looks like this
    #    tiffFile=/Volumes/mapmanager/Users/cudmore/Dropbox/data/Shu-Ling/Shu-Ling_tif/mm_maps/ling_map_1/raw/ling_map_1_s0_ch2.tif
    #    point=228,343,18
    #    point=261,341,18
    #    point=285,327,18

    # this works but blocks
    #commandLineStr = f'{fijiPath} {pluginPath}'
    #os.system(commandLineStr)

    print('  == traceInFiji starting with subprocess.Popen')
    print('    ', [fijiPath, pluginPath])

    _popen = subprocess.Popen([fijiPath, pluginPath])
    print('  == entering while not done')
    while _popen.poll() is None:
        continue
        # allow ctrl-c ???
        # we need to embed this into PyQt to handle event loop?

    print('  == traceInFiji is done.')

    # when tracing is finished, it saves 'tracing_finished.txt'
    # this is not needed, we are using _popen.poll() that returns True (?) when finished

    # full tracing is now saved in 'tracing_out.txt'
    with open(tracingOutPath) as f:
        lines = f.read().splitlines()
    numPoints = len(lines)
    for line in lines:
        print(line)  # need to convert str to either list or tuple

    print(f'  == loaded {numPoints} points in fit')

if __name__ == '__main__':
    runScript()