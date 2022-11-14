import os
import json

nodes = open('./nodes/math.json')
data = json.load(nodes)

for filename in os.scandir('proof-tex'):
    if not filename.is_file():
        continue
    ftex = open(filename.path, 'r')
    # make an auxiliary file
    faux = open('auxiliary.tex', 'w')
    template = open('latex/template_proof.tex', 'r').read()
    template = template.replace('{{ theorem }}', data[filename.name.replace('.tex', '')]['tex']).replace(
        '{{ proof }}', ftex.read())
    print(template)
    faux.write(template)
    faux.close()

    os.system("pdflatex auxiliary.tex")
    os.system("mv "+'auxiliary.pdf'+" proof-pdf/" +
              filename.name.replace('.tex', '.pdf'))
    os.system("rm -rf auxiliary.aux")
    os.system("rm -rf auxiliary.log")
    os.system("rm -rf auxiliary.tex")
