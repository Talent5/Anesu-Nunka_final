import re
p_content = '''<w:p w14:paraId="35FB6163" w14:textId="427AACB1" w:rsidR="00D05DB1" w:rsidRPr="00D05DB1" w:rsidRDefault="00D05DB1" w:rsidP="00D05DB1">
      <w:pPr>
        <w:widowControl/>
        <w:pBdr>
          <w:top w:val="nil"/>
          <w:left w:val="nil"/>
          <w:bottom w:val="nil"/>
          <w:right w:val="nil"/>
          <w:between w:val="nil"/>
        </w:pBdr>
        <w:spacing w:before="280" w:after="280" w:line="360" w:lineRule="auto"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:i/>
          <w:iCs/>
        </w:rPr>
        <w:t>Figure 3.1: CRISP-DM Methodology Lifecycle showing six phases with sequential flow and iterative feedback loops.</w:t>
      </w:r>
    </w:p>'''

match_t = re.search(r'(<w:t(?: [^>]+)?>)\s*(Figure\s+\d+(?:\.\d+)?)\s*:\s*(.*?)(</w:t>)', p_content, re.IGNORECASE | re.DOTALL)
t_open = match_t.group(1)
fig_text = match_t.group(2)
rest_text = match_t.group(3)
t_close = match_t.group(4)

if '<w:pStyle' in p_content:
    p_content = re.sub(r'<w:pStyle\s+w:val="[^"]+"\s*/>', '<w:pStyle w:val="Caption"/>', p_content)
elif '<w:pPr>' in p_content:
    p_content = p_content.replace('<w:pPr>', '<w:pPr>\n        <w:pStyle w:val="Caption"/>', 1)
else:
    p_content = re.sub(r'(<w:p(?: [^>]+)?>)', r'\1\n      <w:pPr>\n        <w:pStyle w:val="Caption"/>\n      </w:pPr>', p_content, count=1)

seq_xml = (
    f'{t_open}Figure {t_close}'
    f'</w:r>'
    f'<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
    f'<w:r><w:instrText xml:space="preserve"> SEQ Figure \* ARABIC </w:instrText></w:r>'
    f'<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
    f'<w:r><w:t>1</w:t></w:r>'
    f'<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    f'<w:r>{t_open}: {rest_text}{t_close}'
)

new_p_content = p_content[:match_t.start()] + seq_xml + p_content[match_t.end():]
print(new_p_content)
