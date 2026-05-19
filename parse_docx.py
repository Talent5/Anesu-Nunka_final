import xml.etree.ElementTree as ET
import os

xml_path = r'C:\Users\Takunda Mundwa\Desktop\School Projects\Anesu Nunka_final\unpacked_docx\word\document.xml'
rels_path = r'C:\Users\Takunda Mundwa\Desktop\School Projects\Anesu Nunka_final\unpacked_docx\word\_rels\document.xml.rels'

ns = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
}

# Parse rels to map rId to image files
rels_tree = ET.parse(rels_path)
rels_root = rels_tree.getroot()
rid_to_target = {}
for rel in rels_root:
    rid = rel.get('Id')
    target = rel.get('Target')
    rid_to_target[rid] = target

tree = ET.parse(xml_path)
root = tree.getroot()

for p in root.findall('.//w:p', ns):
    text = ''.join(t.text for t in p.findall('.//w:t', ns) if t.text)
    if 'Figure' in text:
        print(f'Text: {text.strip()}')
    for drawing in p.findall('.//w:drawing', ns):
        for blip in drawing.findall('.//a:blip', ns):
            embed_id = blip.get(f'{{{ns["r"]}}}embed')
            target = rid_to_target.get(embed_id, "UNKNOWN")
            print(f'  --> Image: {target} (rId: {embed_id})')
