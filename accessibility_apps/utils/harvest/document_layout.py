import pdf2image
import numpy as np
from pathlib import Path
import os
import layoutparser as lp

from layoutparser.elements import TextBlock
from torch import Tensor

from PIL import Image

import torchvision.ops.boxes as bops
import torch

pdf_dir : Path = Path(os.path.realpath(os.path.dirname(__file__))).parent.parent.parent.absolute()
pdf_dir = pdf_dir.joinpath("data").joinpath("input")

class DocumentLayout:
    def __init__(self, filepath : str):
        self.pdf_dir = Path(filepath)

# credited to: https://towardsdatascience.com/analyzing-document-layout-with-layoutparser-ed24d85f1d44
def set_coordinate(data: TextBlock) -> Tensor:
    """ Returns a coordinate matrix given a text block.

    Args:
        data (TextBlock): A text block contains locational information where text segments in a document are.

    Returns:
        Tensor: An array of coordinates
    """
    x1 = data.block.x_1
    y1 = data.block.y_1
    x2 = data.block.x_2
    y2 = data.block.y_2

    return torch.tensor([[x1, y1, x2, y2]], dtype=torch.float)

# credited to: https://towardsdatascience.com/analyzing-document-layout-with-layoutparser-ed24d85f1d44
def compute_iou(box_1 : Tensor, box_2 : Tensor) -> Tensor:
    """ Returns the intersection over union between two sets of boxes
    Args:
        box_1 (Tensor): Matrix of coordinates for Textbox 1
        box_2 (Tensor): Matrix of coordinates for Textbox 2

    Returns:
        Tensor: Matrix contains pairwise IoU values
    """

    return bops.box_iou(box_1, box_2)

# credited to: https://towardsdatascience.com/analyzing-document-layout-with-layoutparser-ed24d85f1d44
def compute_area(box : Tensor) -> float:
    """ Given a matrix of coordinates for a box, returns the area.

    Args:
        box (Tensor): Matrix of xy coordinates.

    Returns:
        float: The area of the box
    """
    width = box.tolist()[0][2] - box.tolist()[0][0]
    length = box.tolist()[0][3] - box.tolist()[0][1]
    area = width*length

    return area

# credited to: https://towardsdatascience.com/analyzing-document-layout-with-layoutparser-ed24d85f1d44
def refine(block_1 : TextBlock, block_2 : TextBlock) -> None:
    """ Checks if a text block is enclosed by the other text block. If so, removes the redudancy inplace.

    Args:
        block_1 (TextBlock): Textbox that may or may not be enclosed by the other.
        block_2 (TextBlock): Textbox that may or may not be enclosed by the other.
    """
    bb1 = set_coordinate(block_1)
    bb2 = set_coordinate(block_2)

    iou = compute_iou(bb1, bb2)

    if iou.tolist()[0][0] != 0:

        a1 = compute_area(bb1)
        a2 = compute_area(bb2)

        block_2.set(type='None', inplace= True) if a1 > a2 else block_1.set(type='None', inplace= True)
    


def document_layout(pdf_name : str, debug : bool = False) -> list[tuple]:
    """Parses a pdf in search of document element order for the purpose of tagging

    Args:
        pdf_name (str): A relative or absolute path to a pdf file. If relative, will check the data input DIR
        debug (bool, optional): Prints debugging info when True. Defaults to False.

    Raises:
        FileNotFoundError: Raises if the function could not locate the provided pdf.
    Returns:
        list[tuple]: List is ordered according to the read order. Each tuple element: (type, data)
    """

    # if pdf_name is an absolute path then this will make pdf_file -> pdf_name
    pdf_file : Path = pdf_dir.joinpath(pdf_name)

    if not pdf_file.exists():
        raise FileNotFoundError("Pdf File not found: {}".format(pdf_file))

    print("PDF FILE:",pdf_file)
    
    res_layout_data : list[tuple] = []

    # convert the pdf into a set of images
    imgs = [np.asarray(page_img) for page_img in pdf2image.convert_from_path(pdf_file)]

    #imgs = np.asarray(pdf2image.convert_from_path(pdf_file)[0])

    
    #pdf2image.convert_from_path(pdf_file)[0].save('pdf2img.jpeg', 'JPEG')

    # model used to detect boundary boxes for layout text.
    model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

    
    ocr_agent = lp.TesseractAgent(languages='eng')
    
    for index, img in enumerate(imgs):
        # use model to identify layout boxes in the pdf
        layout_result = model.detect(img)
        
        # get rid of redundant boxes
        for layout_i in layout_result:
            
            if layout_i.type != 'Text' and layout_i.type != 'Title':
                continue

            for layout_j in layout_result:
                
                if layout_j.type != 'Text' and layout_j.type != 'Title':
                    continue

                if layout_i != layout_j: 
                    refine(layout_i, layout_j)

        layout_blocks = lp.Layout([b for b in layout_result if b.type != 'None'])
        
        # sort boundary boxes by y-coordinates
        # ! Need better method for this
        layout_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)

        # use layout block ids to identfy read order
        layout_blocks = lp.Layout([b.set(id = idx) for idx, b in enumerate(layout_blocks)])
        
        


        if(debug):
            print("---------\nPage {}\n---------".format(index))
            for result in layout_blocks:
                print(result, "\n")
            draw_im = lp.draw_box(img, layout_blocks,  box_width=5, box_alpha=0.2, show_element_type=True, show_element_id=True)
            draw_im.save("page[{}]_layout_boxes.jpeg".format(index))


        for block in layout_blocks:
            if block.type == 'Text' or block.type == 'Title':
                # Crop image around the detected layout
                segment_image = (block
                                .pad(left=15, right=15, top=5, bottom=5)
                                .crop_image(img))
                
                # Perform OCR
                text = ocr_agent.detect(segment_image)
                res_layout_data.append((block.type, text))
            else:
                res_layout_data.append((block.type, "IMG DATA -- NOT ADDED"))
    
    if debug:
        for type, data in res_layout_data:
            print("Tag: {}".format(type))
            print(data, "\n")
            

def main():
    document_layout('example.pdf', True)


if __name__ == "__main__":
    main()