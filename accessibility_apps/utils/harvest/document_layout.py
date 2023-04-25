import pdf2image
import numpy as np
from pathlib import Path
import os
import layoutparser as lp
from collections import Counter

from layoutparser.elements import TextBlock
from torch import Tensor

from PIL import Image

import torchvision.ops.boxes as bops
import torch

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning) 

base_dir : Path = Path(os.path.realpath(os.path.dirname(__file__))).parent.parent.parent.absolute()
pdf_dir = base_dir.joinpath("data").joinpath("input")
output_dir : Path = base_dir.joinpath("data").joinpath("output")


quaddict={}
with open(str(Path(os.path.realpath(os.path.dirname(__file__))).joinpath("quadgrams.txt"))) as f:
    for line in f:
        quaddict[line.split(",")[0]]= float(line.split(",")[1])

class DocumentLayout:
    def __init__(self, filepath : str):
        self.pdf_dir = Path(filepath)

# credited to: https://towardsdatascience.com/analyzing-document-layout-with-layoutparser-ed24d85f1d44
def get_coordinate(data: TextBlock) -> Tensor:
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

def get_xy(data: TextBlock):
    return [(data.block.x_1, data.block.y_1), (data.block.x_2, data.block.y_2)]

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
    bb1 = get_coordinate(block_1)
    bb2 = get_coordinate(block_2)

    iou = compute_iou(bb1, bb2)

    if iou.tolist()[0][0] != 0:

        a1 = compute_area(bb1)
        a2 = compute_area(bb2)

        block_2.set(type='None', inplace= True) if a1 > a2 else block_1.set(type='None', inplace= True)
    


def document_layout(pdf_name : str, preprocessed_paragraphs : list[list[tuple[int, str]]] = [], debug : bool = False) -> list[tuple]:
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

    debug_out_dir = output_dir.joinpath(pdf_name.split('.')[0].split('/')[-1]) # create folder in output that is the name of the pdf.
    if not debug_out_dir.exists():
        debug_out_dir.mkdir(parents=True, exist_ok=True)

    if not pdf_file.exists():
        raise FileNotFoundError("Pdf File not found: {}".format(pdf_file))
    
    res_layout_data : list[tuple] = []

    # convert the pdf into a set of images
    page_imgs = [np.asarray(page_img) for page_img in pdf2image.convert_from_path(pdf_file)]

    #imgs = np.asarray(pdf2image.convert_from_path(pdf_file)[0])

    
    #pdf2image.convert_from_path(pdf_file)[0].save('pdf2img.jpeg', 'JPEG')

    # model used to detect boundary boxes for layout text.
    model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})
    
    ocr_agent = lp.TesseractAgent(languages='eng')
    
    if(debug):
        print("Done Loading Models...")
    
    for page_index, img in enumerate(page_imgs):
        
        current_batch = []
        # use model to identify layout boxes in the pdf
        layout_result = model.detect(img)
        
        # get rid of redundant boxes
        for layout_i in layout_result:
            
            # if layout_i.type != 'Text' and layout_i.type != 'Title' and layout_i.type != "List":
            #     continue

            for layout_j in layout_result:
                
                # if layout_j.type != 'Text' and layout_j.type != 'Title' and layout_i.type != "List":
                #     continue

                if layout_i != layout_j: 
                    refine(layout_i, layout_j)

        layout_blocks = lp.Layout([b for b in layout_result if b.type != 'None'])
        
        layout_blocks = order_layout(layout_blocks)

        # use layout block ids to identfy read order
        layout_blocks = lp.Layout([b.set(id = idx) for idx, b in enumerate(layout_blocks)])

        if(debug):
            print("---------\nPage {}\n---------".format(page_index))
            for result in layout_blocks:
                print(result, "\n")
            draw_im = lp.draw_box(img, layout_blocks,  box_width=5, box_alpha=0.2, show_element_type=True, show_element_id=True)
            draw_im.save(debug_out_dir.joinpath("page[{}]_layout_boxes.jpeg".format(page_index)))
        
        for block in layout_blocks:
            if block.type == 'Text' or block.type == 'Title' or block.type == "List":
                # Crop image around the detected layout
                segment_image = (block
                                .pad(left=15, right=15, top=5, bottom=5)
                                .crop_image(img))
                
                # Perform OCR, get rid of unneccary whitespace in texts
                words = ocr_agent.detect(segment_image).split()
                text = " ".join(words)

                current_batch.append((block.type, text))
            else:
                current_batch.append((block.type, "IMG DATA -- NOT ADDED"))
        
        # if(page_index == 3):
        #     validate_layout(preprocessed_paragraphs[page_index], current_batch)
        res_layout_data.extend(current_batch)
    return res_layout_data
            
def order_layout(layout_blocks : list[TextBlock]):
    """ Uses the x-y values of the layout_blocks to predict the read-order of the blocks according to english.

    Args:
        layout_blocks (list[TextBlock]): A batch of layout blocks detected for a page.

    Returns:
        list[TextBlock]: The layout blocks re-ordered according to read-order.
    """

    # sort boundary boxes by y-coordinates
    layout_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)
    sorted_layout = []

    # * ========================================================================================
    # *
    # *                      -- HELPER FUNCTIONS FOR ORDER_LAYOUT  --
    # *
    # * ========================================================================================
    def set_first_block(l_blocks : list[layout_blocks]):
        """ Determines which block in the list that should be first. Swaps it with the first block. (inplace)

        Args:
            l_blocks (list[layout_blocks]): Layout blocks after a page break.
        """
        y_max = get_xy(l_blocks[0])[1][1]
        first_block_index = 0

        potential_first_block_indexes = [0]

        # find all blocks where the block starts at least before the topmost block ends
        for current_block_index in range(1, len(l_blocks)):
            if get_xy(l_blocks[current_block_index])[0][1] > y_max:
                break
            potential_first_block_indexes.append(current_block_index)
        
        left_most_x2 = get_xy(l_blocks[potential_first_block_indexes[0]])[1][0]
        lm_block_x1 = get_xy(l_blocks[potential_first_block_indexes[0]])[0][0]
        
        # finds x2 limit for the possible blocks (gets all blocks that would be in the left-most column)
        for index in potential_first_block_indexes[1:]:
            if get_xy(l_blocks[index])[1][0] < lm_block_x1:
                left_most_x2 = get_xy(l_blocks[index])[1][0]
                lm_block_x1 = get_xy(l_blocks[index])[0][0]

        # get rid of right column blocks that do not belong in the left-most column
        for lb_index in reversed(potential_first_block_indexes):
            if get_xy(l_blocks[potential_first_block_indexes[lb_index]])[0][0] > left_most_x2:
                potential_first_block_indexes.pop(lb_index)
        
        if len(potential_first_block_indexes) == 1:
            first_block_index = potential_first_block_indexes[0]
        else:
            # find the top most block in the left-most column
            smallest_y1 = get_xy(l_blocks[potential_first_block_indexes[0]])[0][1]
            smallest_y1_index = potential_first_block_indexes[0]
            for lb_index in potential_first_block_indexes:
                current_y = get_xy(l_blocks[lb_index])[0][1]
                if current_y < smallest_y1:
                    smallest_y1 = current_y
                    smallest_y1_index = lb_index
            first_block_index = smallest_y1_index

        # swap the two blocks in the order
        temp = layout_blocks[0]
        layout_blocks[0] = layout_blocks[first_block_index]
        layout_blocks[first_block_index] = temp
    
    def check_right(current_block : TextBlock, l_blocks : list[TextBlock]):
        """ Returns the index of the first block in l_blocks that is to the right of this block. Indicating a column exists.

        Args:
            current_block (TextBlock): The block to check the right of.
            l_blocks (list[TextBlock]): The list of remaining blocks that aren't in the order_layout yet.   

        Returns:
            int: The index of the block that is to the right of this current block, -1 if no block found.
        """
        block_coords = get_xy(current_block)

        lb_indexes = []

        current_lb_index = 0
        while current_lb_index < len(l_blocks):
            if get_xy(l_blocks[current_lb_index])[0][1] > block_coords[1][1]:
                break
            if get_xy(l_blocks[current_lb_index])[0][0] > block_coords[1][0]:
                lb_indexes.append(current_lb_index)
            current_lb_index += 1
        
        if len(lb_indexes) == 0:
            return -1
        elif len(lb_indexes) == 1:
            return lb_indexes[0]

        left_most_x2 = get_xy(l_blocks[lb_indexes[0]])[1][0]
        lm_block_x1 = get_xy(l_blocks[lb_indexes[0]])[0][0]
        
        # finds x2 limit of the immediate right column
        for index in range(1, len(lb_indexes)):
            if get_xy(l_blocks[lb_indexes[index]])[1][0] < lm_block_x1:
                left_most_x2 = get_xy(l_blocks[lb_indexes[index]])[1][0]
                lm_block_x1 = get_xy(l_blocks[lb_indexes[index]])[0][0]
        
        # get rid of right column blocks that do not belong to the immedidate right column
        for lb_index in reversed(range(len(lb_indexes))):
            if get_xy(l_blocks[lb_indexes[lb_index]])[0][0] > left_most_x2:
                lb_indexes.pop(lb_index)
        
        if len(lb_indexes) == 1:
            return lb_indexes[0]
        
        # find the top most block in the immediate right column
        smallest_y1 = get_xy(l_blocks[lb_indexes[0]])[0][1]
        smallest_y1_index = 0
        for lb_index in range(1, len(lb_indexes)):
            current_y = get_xy(l_blocks[lb_indexes[lb_index]])[0][1]
            if current_y < smallest_y1:
                smallest_y1 = current_y
                smallest_y1_index = lb_index
        
        return smallest_y1_index

    def find_columns(left_block : TextBlock, l_blocks : list[TextBlock], relative_segment_index : int, segments : list[TextBlock]):
        """ For a given left_block finds all obvious blocks to its right that would insinuate a column. Done recursively if there is many columns.

        Args:
            left_block (TextBlock): The current block to check the right of it for more blocks
            l_blocks (list[TextBlock]): The remaining unordered layout blocks
            relative_segment_index (int): The given left blocks segment index in the res array.
        """
        right_block_index = check_right(left_block, l_blocks)

        if right_block_index >= 0:
            right_block = l_blocks.pop(right_block_index)
            segments.insert(relative_segment_index + 1, [right_block])
            find_columns(right_block, l_blocks, relative_segment_index + 1, segments)


    def find_child(parent : TextBlock, l_blocks : list[TextBlock]):
        """ Finds the first block in l_blocks directly below the parent.

        Args:
            parent (TextBlock): The current block in the read-order.
            l_blocks (list[TextBlock]): The list of remaining blocks that aren't in the order_layout yet.  

        Returns:
            int: Returns the index of the block that was found to be directly below the parent. -1 returns if no block found.
        """
        nonlocal column_break_y
        block_coords = get_xy(parent)
        lb_index = 0

        while lb_index < len(l_blocks):
            if column_break_y > 0:
                if get_xy(l_blocks[lb_index])[0][1] >= column_break_y:
                    break
            # check if any blocks intersect with the parent block's range (x, x + width)
            if get_xy(l_blocks[lb_index])[0][0] >= block_coords[0][0]:
                if get_xy(l_blocks[lb_index])[0][0] <= block_coords[1][0]:
                    return lb_index
            elif get_xy(l_blocks[lb_index])[1][0] >= block_coords[0][0]:
                return lb_index
            lb_index += 1
        return -1
    
    def is_column_break(relative_segment_index: int, child_block : TextBlock):
        """ Checks if the child block found is a column break, cutting off all the blocks above it.

        Args:
            relative_segment_index (int): The index of a segment in the read order, or a column..
            child_block (TextBlock): The potential column break block.

        Returns:
            bool, int: The boolean is true when the child block is a column break.
            When true, also returns the break index, where this block should go in the read-order.
            Returns False, -1 otherwise.
        """
        nonlocal sorted_layout
        icb = False # Is Column Break
        break_index = -1

        for current_column in range(relative_segment_index, len(sorted_layout)):
            if get_xy(child_block)[1][0] >= get_xy(sorted_layout[current_column][0])[0][0]:
                icb = True
                break_index = current_column
            else:
                break
        return icb, break_index + 1
    
    def has_missing_blocks_to_left(relative_segment_index : int, right_block : TextBlock, l_blocks : list[TextBlock]):
        """ Returns true if the right_block has unidentified blocks to the left of it. This means that a left column was missed.

        Args:
            relative_segment_index (int): Where in the current sorted_layout these missing columns would go.
            right_block (TextBlock): The current block that may have blocks to the left of it.
            l_blocks (list[TextBlock]): The list of remaining blocks that aren't in the order_layout yet.  

        Returns:
            bool: True if missing blocks/columns were found. False otherwise.
            If missing blocks were found, the block that would be first in the
            read-order of those found blocks, will be inserted to the layout order.
            The rest will remain in the l_block list.
        """
        nonlocal sorted_layout
        block_coords = get_xy(right_block)

        indexes = []
        missed_blocks = []

        lb_index = 0
        while lb_index < len(l_blocks):
            if get_xy(l_blocks[lb_index])[0][1] > block_coords[1][1]:
                break
            if get_xy(l_blocks[lb_index])[1][0] < block_coords[0][0]:
                indexes.append(lb_index)
            lb_index += 1
        
        if len(indexes) > 0:
            # grab all blocks to the left of this block that were evidently missed
            for missed_block in reversed(indexes):
                missed_blocks.insert(0, l_blocks.pop(missed_block))
            missed_blocks.append(right_block)
            l_blocks.pop(0) # the first element is the right block, remove it as it will be added to sorted_layout later
            
            # get top-left block
            set_first_block(missed_blocks)
            first_block = missed_blocks.pop(0)
            segment_list = [[first_block]]
            find_columns(first_block, missed_blocks, 0, segment_list)

            # add misssed column blocks to the ordered layout
            for segment in segment_list:
                for s_block in segment:
                    sorted_layout.insert(relative_segment_index + 1, [s_block])
                    relative_segment_index += 1
            
            # add any blocks that were not in a column and at the top back to the remaining blocks and sort to keep y-ordered constraint.
            for not_column_block in missed_blocks:
                l_blocks.insert(0, not_column_block)
            layout_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)

            return True

        return False

    def has_umbrella_column(relative_segment_index : int, left_child_block : TextBlock, l_blocks : list[TextBlock]):
        """ Determines if this child block is really the start of a new column and its parent is a top column break (umbrella)

        Args:
            relative_segment_index (int): Where in the current sorted_layout the parent block is.
            left_child_block (TextBlock): The new child block to add to the sorted_layout
            l_blocks (list[TextBlock]): The list of remaining blocks that aren't in the order_layout yet. 

        Returns:
            bool, int: True if this block is under an umbrella block, and what index in the l_blocks the right column block is.
        """
        nonlocal sorted_layout
        
        right_block_index = check_right(left_child_block, l_blocks)

        if right_block_index == -1:
            return False, -1
        
        # if right block is tucked under the parent block
        if get_xy(l_blocks[right_block_index])[0][0] < get_xy(sorted_layout[relative_segment_index][-1])[1][0]:
            return True, right_block_index
        return False, -1

    # * ========================================================================================
    # *
    # *                          -- ORDER_LAYOUT IMPLMENTATION  --
    # *
    # * ========================================================================================
    set_first_block(layout_blocks)

    current_block = layout_blocks.pop(0)    # Index 0 should be the first element to read
    sorted_layout.append([current_block])   # Add new segment (section) to the res array
    segment_index = 0                       # The current segment to be appending new blocks to
    column_break_index = -1                 # this index marks a segment found that cuts off any columns above it.
    column_break_y = -1                     # this y-coordinate for the soonest column break
    
    cycle_count = 0
    while len(layout_blocks) > 0:
        
        cycle_count += 1
        #print("Cycle count:", cycle_count)
        # if cycle_count == 3:
        #     print("Hi")

        # if this is the right most segment, make sure no other columns to the right
        if segment_index == (len(sorted_layout) - 1):
            find_columns(current_block, layout_blocks, segment_index, sorted_layout)


        possible_child_index = find_child(current_block, layout_blocks)
        

        if possible_child_index == -1:
            # if no blocks directly below the current block
            if segment_index == (len(sorted_layout) - 1):
                # if this is the last segment, restart the algorithm
                set_first_block(layout_blocks)
                current_block = layout_blocks.pop(0)    # Index 0 should be the first element to read
                sorted_layout.append([current_block])   # Add new segment (section) to the res array
                segment_index = 0                       # The current segment to be appending new blocks to
                column_break_index = -1                 # this index marks a segment found that cuts off any columns above it.
                column_break_y = -1                     # this y-coordinate for the soonest column break
                continue
            else:
                segment_index += 1
                if segment_index == column_break_index:
                    column_break_index = -1
                    column_break_y = -1
                current_block = sorted_layout[segment_index][0]
                continue
        
        if column_break_index > 0:
            icb, possible_break_index = False, -1
        else:
            icb, possible_break_index = is_column_break(segment_index + 1, layout_blocks[possible_child_index])

        if icb:
            # Add new segment where column break cuts off the right most column,
            # none of the columns above this break should look for child blocks under the break
            column_break_index = possible_break_index
            sorted_layout.insert(column_break_index, [layout_blocks.pop(possible_child_index)])
            column_break_y = get_xy(sorted_layout[column_break_index][0])[0][1]
            segment_index += 1
            current_block = sorted_layout[segment_index][0]
            continue

        # If the possible child block is under the parent block but has blocks to the left of it,
        # then we found a right column under the parent, which means we need to search to the
        # left and add segments first.
        if has_missing_blocks_to_left(segment_index, layout_blocks[possible_child_index], layout_blocks):
            segment_index += 1 # columns were added, meaning the current_block is a column break
            current_block = sorted_layout[segment_index][0]
            continue
        
        # check for umbrella columns (where it is an undetected column right column under the parent)
        child_block = layout_blocks.pop(possible_child_index)
        
        
        
        huc, possible_umbrella_index = has_umbrella_column(segment_index, child_block, layout_blocks)
        
        # if has an umbrella column cut off the child block as a new column segment, and make the right block the segment after the child block.
        if huc:
            sorted_layout.insert(segment_index + 1, [child_block])
            segment_index += 1
            sorted_layout.insert(segment_index + 1, [layout_blocks.pop(possible_umbrella_index)])
            current_block = child_block
            continue

        # if this is next block in this column segment
        sorted_layout[segment_index].append(child_block)
        current_block = child_block


    # print("current block:",current_block)
    # print("===============================")    
    
    # for rblock in layout_blocks:
    #     print(rblock)
    #     print("\n--------------\n")
    # quit()

    # return flattened block segments

    return [block for segment in sorted_layout for block in segment] 

    
def validate_layout(preprocessed_paragraphs : list[tuple[int, str]], current_batch : list[tuple[str, str]]):
    """ Uses the paragraph list created by extract_paragraphs_and_fonts_and_sizes() and
        the layout_blocks lit from document_layout() to create a better quality list document
        elements that is ordered according to read-order. This is used to create the document tags.

    Args:
        preprocessed_paragraphs (list[tuple[int, str]]):
            A list of paragraphs that includes the font size and the raw text.
            This list is "well" ordered according to the document reading order.
            Making it useful for arranging the layout_blocks in the current_batch.
            The font size will be added to the appropriate layout blocks for future use.
        
        current_batch (list[tuple[str, str]]):
            Represents all the layout blocks the layout parser found for a given page.
            Will be reordered or added to according to preprocessed_paragraphs.
    """
    # every search will either extend to the entire list or at least 5
    search_limit = min(len(preprocessed_paragraphs), 5 if len(current_batch) < 5 else len(current_batch))
    
    # how many times to expand the threshold if no match is found
    expand_limit = 3

    for layout_block in current_batch:


        #* Step 1 : Find what prepocessed_paragraph matches with the current layout_block
        potential_matches = []
        threshold = 0.4

        for _ in range(expand_limit):

            # the range for which the character count of the two paragraphs should be similar by to warrant a match check
            t_range = int(threshold * len(layout_block[1]))

            for index in range(search_limit):
                if (len(preprocessed_paragraphs[index][1]) >= len(layout_block[1]) - t_range) and\
                (len(preprocessed_paragraphs[index][1]) <= len(layout_block[1]) + t_range):
                    potential_matches.append(index)
            
            # no results found in the search limit with the provided threshold, expand search via expanding threshold
            if len(potential_matches) == 0:
                threshold += 0.2
                continue
            else:
                print("Potential Match:", potential_matches)
                print(layout_block[1], "\n-----------------------------")
                for index in potential_matches:
                    print(preprocessed_paragraphs[index][1], "\n")
                quit()
        print("No Match Found")
        quit()

    return 0


def is_this_a_paragraph(paragraph : str):
    print(calc_ioc(paragraph))
    print(quadgram_fitness(paragraph))
    print("")
    

# credited to: https://github.com/vaibhavgarg1982/MiscPythonTools/blob/main/text_fitness.ipynb
def prep_str(iptext):
    iptext = iptext.lower()
    iptext = iptext.replace(".","")
    import string

    for punc in string.punctuation:
        iptext = iptext.replace(punc,"")

    iptext = iptext.replace("’","")
    iptext = iptext.replace(" ","")
    iptext = iptext.replace("\n", "")
    iptext = iptext.replace("…","")

    for i in range(10):
        iptext = iptext.replace(str(i), "")
    
    return iptext

# https://en.wikipedia.org/wiki/Index_of_coincidence
# credited to: https://github.com/vaibhavgarg1982/MiscPythonTools/blob/main/text_fitness.ipynb
def calc_ioc(iptext):
    iptext = prep_str(iptext)
    if len(iptext) == 0 or len(iptext) == 1:
        return 0
    
    cnt = Counter(iptext)
    sum = 0
    N = len(iptext)
    for x in cnt:
        sum = sum + cnt[x]*(cnt[x]-1)
    return sum*26/(N*(N-1))

# credited to: https://github.com/vaibhavgarg1982/MiscPythonTools/blob/main/text_fitness.ipynb
def quadgram_fitness(iptext):
    a = prep_str(iptext)

    if len(a) == 0 or len(a) == 1:
        return 0
    quadtext = [a[idx:idx+4] for idx in range(len(a)-3)]
    
    sum = 0
    for quad in quadtext:
        sum += (quaddict.get(quad.upper(),0))
    return abs(sum)/len(quadtext)

def main():
    document_layout('example.pdf', True)


if __name__ == "__main__":
    main()