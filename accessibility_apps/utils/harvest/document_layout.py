import pdf2image
import numpy as np
from pathlib import Path
import os
import layoutparser as lp

pdf_dir : Path = Path(os.path.realpath(os.path.dirname(__file__))).parent.parent.parent.absolute()
pdf_dir = pdf_dir.joinpath("data").joinpath("input")


def document_layout(pdf_name : str):
    pdf_file : Path = pdf_dir.joinpath(pdf_name)

    if not pdf_file.exists():
        raise FileNotFoundError("Pdf File does not exist: {}".format(pdf_file))
   
    img = np.asarray(pdf2image.convert_from_path(pdf_file)[0])
    
    #print(type(img))
    #pdf2image.convert_from_path(pdf_file)[0].save('test.jpg', 'JPEG')

    model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

    layout_result = model.detect(img)

    for result in layout_result:
        print(result)

def main():
    document_layout('example.pdf')


if __name__ == "__main__":
    main()