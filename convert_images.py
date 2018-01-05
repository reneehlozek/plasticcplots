from PIL import Image
from PyPDF2 import PdfFileMerger
import os
import glob
path = "/project/rkessler/rhlozek/PLAsTiCC_outputs/"
list = glob.glob('*.png')

merger=PdfFileMerger()

for filename in list:

    im = Image.open(filename)

    if im.mode=='RGBA':
        im=im.convert('RGB')

    outputfilename = filename[:-3] + 'pdf'

    im.save(outputfilename, 'PDF', resolution=100.0)
    


for filename in glob.glob('*.pdf'):
    merger.append(filename)

if not os.path.exists(path+'merged.pdf'):

    merger.write(path+'merged.pdf')
merger.close()
