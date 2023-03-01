#!/usr/bin/env python

""" Tagging documents involves marking content with labels such as a header,
    paragraph, row entries within a table, etc. Tagging helps define the
    reading order, which is another accessibility feature we aim to provide, 
    especially in tables, as well as being used to define alt text for images.
"""

# * Modules
from utils.document import Document
from utils.transform.TagTree import Tag, TagTree

# Last Edit By: Reagan Kelley
# * Edit Details: Started implementing tag trees
def generate_tags(doc:Document):
    """Post-condition: Document will be a PDF tagged document.

    Args:
        doc (Document((), optional): PDF handler that allows edits to be made. Defaults to Document().
    """
    test_tag_tree()

    # TODO: Implement PDF Tagging according to W3C guidelines.
    # TODO: Get tags from metadata and edit/add them.
    return doc

def test_tag_tree():

    # ? Text from: https://rex.libraries.wsu.edu/esploro/outputs/99900502774701842
    
    introduction = "INTRODUCTION\n"
    p1 = "\tThe use of petroleum-based plastics for products and packaging has become ubiquitous in\
industry, a trend that is contributing heavily to ecological problems such as increased CO2 levels,\
pollution of land and waterways, and overloading of the solid-waste stream. Although petroleum\
plastics are extremely versatile and fulfill the performance requirements for a multitude of\
applications, increasing public awareness of their environmental impacts has spurred efforts to\
replace petroleum feedstocks with sustainable and ecofriendly alternatives.[1-15] Motivated by\
the goal to reduce our carbon footprint and dependence on fossil carbon sources, bio-based\
polymers and composites are becoming widely utilized in polymer manufacturing and medical\
applications.[16-18] One area of strong interest is the replacement of petroleum-based plastics\
with bioplastics in horticulture containers used by the nursery-crops industry. Although interest\
is high, the industry has struggled to develop a bio-based container that can fulfill the functional\
requirements for long-term nursery-crops production. Many of the difficulties are related to poor\
flexibility and low impact resistance of materials that cannot withstand the harsh treatment\
encountered during use.\n"

    p2 =  "\tThe poly(hydroxyalkanoates) (PHAs) most widely used in industry are aliphatic thermoplastic\
poly(esters) synthesized via metabolic pathways of microorganisms by fermentation of sugars or\
lipids.[19] PHAs containing over 90 types of monomers have been synthesized in various\
microorganisms. The characteristics of thermoplastic PHAs range from rigid plastics to tough\
elastomers and depend on their molecular structure. Specifically, the properties of PHAs are\
highly dependent on the copolymer composition. Generally, thermoplastic PHAs are rigid but\
brittle, with poor impact resistance and flexibility, issues that restrict the applications for which\
PHAs can be used as alternatives to traditional petroleum-based plastics. Copolymers of 4-\
hydroxybutyrate and 3-hydroxybutyrate can be synthesized to produce bio-based polymers with\
different mechanical and thermal properties. Poly(3-hydroxybutyrate) is a brittle semicrystalline\
material with crystallinity ≥50% and Tg of approximately 4°C. However, poly(4-\
hydroxybutyrate) is more elastic with very low crystallinity and Tg  = −48°C. Most of the efforts\
aimed at improving the toughness of PHA have focused on blending PHA with other polymers\
such as poly(lactide) or thermoplastic starch.[19-22] The majority of reports regarding PHA\
blends focus on only a few aspects of their character, such as viscoelastic or rheological\
properties, instead of providing a comprehensive characterization of the material, and there have\
been no investigations evaluating the blending of poly(amide) with PHA to improve its\
flexibility and impact resistance for increased industrial application.\n"
    experimental = "EXPERIMENTAL"
    experimental_materials = "Materials\n"
    
    p3 = "\tPoly(hydroxyalkanoate) Mirel P1003 (compression molding grade resins) was supplied by\
Metabolix Inc., Cambridge, MA 02139. This PHA is made by fermentation of renewable biobased\
 feedstock, making it fully bio-based in neat form. Mirel P1003 is a blend of PHB and\
poly(3-hydroxybutyrate-co-4-hydroxybutyrate). The poly(amide) UNI-REZ™ 2651 was\
obtained from Arizona Chemical Inc., Jacksonville, FL, and is a fully bio-based resin derived\
from tall oil of pine tree.\n"

    experimental_molding = "Microcompounding and Compression Molding\n"

    p4 = "\tComplete drying of PHA and PA was accomplished by heating the material in a vacuum oven\
for 8 h at 60°C. The desired amounts of PHA and PA granules were fed into a twin-screw\
microcompounder (DACA Instrument, Santa Barbara, CA) set to 185°C and a rotation speed of\
100 rpm. The mixing time was controlled for 10 min to facilitate homogenous melt\
compounding. The extruded materials were then compression molded at 185°C to prepare the\
samples for dynamic mechanical analysis (DMA).\n"

    experimental_Measurements = "Measurements"

    measurements_microscopy = "Scanning Electron Microscopy\n"

    p5 = "\tThe fracture surface morphology of PHA/PA blends (wt % ratios of 20/80, 50/50, and 80/20)\
was examined using scanning electron microscopy (SEM). The tensile-fractured samples were\
fixed on the SEM holders after sputter coating with a thin gold layer. The prepared samples were\
characterized using a field-emission scanning electron microscope (FE-SEM, FEI Quanta 250)\
operating at 10 kV under high vacuum."

    example = TagTree()
    example.Cursor.get_tag().set_child("<H1>", data=introduction)
    example.Cursor.Down().get_tag().set_child("<P>", data=p1)
    example.Cursor.Down().get_tag().set_next("<P>", data=p2)
    example.Cursor.Up().get_tag().set_next("<H1>", data=experimental)
    example.Cursor.Next().get_tag().set_child("<H2>", data=experimental_materials)
    example.Cursor.Down().get_tag().set_child("<P>", data=p3)
    example.Cursor.get_tag().set_next("<H2>", data=experimental_molding)
    example.Cursor.Next().get_tag().set_child("<P>", data=p4)
    example.Cursor.Up().get_tag().set_next("<H1>", data=experimental_Measurements)
    example.Cursor.Next().get_tag().set_child("<H2>", data=measurements_microscopy)
    example.Cursor.Down().get_tag().set_child("<P>", data = p5)
    example.traverse_tree()
