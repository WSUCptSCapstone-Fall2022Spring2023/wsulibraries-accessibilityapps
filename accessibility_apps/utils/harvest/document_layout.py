import pdf2image
import numpy as np
from pathlib import Path
import os
import layoutparser as lp
from PIL import Image

import torchvision.ops.boxes as bops
import torch

pdf_dir : Path = Path(os.path.realpath(os.path.dirname(__file__))).parent.parent.parent.absolute()
pdf_dir = pdf_dir.joinpath("data").joinpath("input")


def set_coordinate(data):
  x1 = data.block.x_1
  y1 = data.block.y_1
  x2 = data.block.x_2
  y2 = data.block.y_2

  return torch.tensor([[x1, y1, x2, y2]], dtype=torch.float)

def compute_iou(box_1, box_2):

  return bops.box_iou(box_1, box_2)

def compute_area(box):

    width = box.tolist()[0][2] - box.tolist()[0][0]
    length = box.tolist()[0][3] - box.tolist()[0][1]
    area = width*length

    return area

def refine(block_1, block_2):

  bb1 = set_coordinate(block_1)
  bb2 = set_coordinate(block_2)

  iou = compute_iou(bb1, bb2)

  if iou.tolist()[0][0] != 0:

    a1 = compute_area(bb1)
    a2 = compute_area(bb2)

    block_2.set(type='None', inplace= True) if a1 > a2 else block_1.set(type='None', inplace= True)
    


def document_layout(pdf_name : str):
    pdf_file : Path = pdf_dir.joinpath(pdf_name)

    if not pdf_file.exists():
        raise FileNotFoundError("Pdf File does not exist: {}".format(pdf_file))
   
    img = np.asarray(pdf2image.convert_from_path(pdf_file)[0])
    
    # convert the pdf into a set of images
    pdf2image.convert_from_path(pdf_file)[0].save('pdf2img.jpeg', 'JPEG')

    # model used to detect boundary boxes for layout text.
    model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

    # use model to identify layout boxes in the pdf
    layout_result = model.detect(img)


    

    # filter results to only show layout boxes that are not images
    text_blocks = lp.Layout([b for b in layout_result if b.type == 'Text' or b.type == 'Title'])

    # get rid of redundant boxes
    for layout_i in text_blocks:
    
        for layout_j in text_blocks:
        
            if layout_i != layout_j: 

                refine(layout_i, layout_j)

    text_blocks = lp.Layout([b for b in layout_result if b.type == 'Text' or b.type == 'Title'])
    

    # sort boundary boxes by y-coordinates
    # ! Need better method for this
    text_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)

    # use text block ids to identfy read order
    text_blocks = lp.Layout([b.set(id = idx) for idx, b in enumerate(text_blocks)])
    
    for result in text_blocks:
        print(result, "\n")


    draw_im = lp.draw_box(img, text_blocks,  box_width=5, box_alpha=0.2, show_element_type=True, show_element_id=True)
    draw_im.save("layout_boxes.jpeg")

    ocr_agent = lp.TesseractAgent(languages='eng')

    for block in text_blocks:

        # Crop image around the detected layout
        segment_image = (block
                        .pad(left=15, right=15, top=5, bottom=5)
                        .crop_image(img))
        
        # Perform OCR
        text = ocr_agent.detect(segment_image)

        # Save OCR result
        block.set(text=text, inplace=True)
    
    for txt in text_blocks:
        print(txt.text, end='\n---\n')


def main():
    document_layout('example.pdf')


if __name__ == "__main__":
    main()