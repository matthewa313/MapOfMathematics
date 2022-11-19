import networkx as nx
import json
import os
import glob

G = nx.Graph()

fin = open('./nodes/math.json')
data = json.load(fin)

for f in glob.glob('map/.*'):
    os.remove(f)

fout = open('map/map.graphml', 'w')


fout.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
fout.write('\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:java="http://www.yworks.com/xml/yfiles-common/1.0/java" xmlns:sys="http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0" xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:y="http://www.yworks.com/xml/graphml" xmlns:yed="http://www.yworks.com/xml/yed/3" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">')
fout.write('''\n<!--Created by yEd 3.21.1-->
<key attr.name="Description" attr.type="string" for="graph" id="d0"/>
<key for="port" id="d1" yfiles.type="portgraphics"/>
<key for="port" id="d2" yfiles.type="portgeometry"/>
<key for="port" id="d3" yfiles.type="portuserdata"/>
<key attr.name="url" attr.type="string" for="node" id="d4"/>
<key attr.name="description" attr.type="string" for="node" id="d5"/>
<key for="node" id="d6" yfiles.type="nodegraphics"/>
<key for="graphml" id="d7" yfiles.type="resources"/>
<key attr.name="url" attr.type="string" for="edge" id="d8"/>
<key attr.name="description" attr.type="string" for="edge" id="d9"/>
<key for="edge" id="d10" yfiles.type="edgegraphics"/>
<graph edgedefault="directed" id="G">
<data key="d0" xml:space="preserve"/>''')

node_text = """\n<node id="{node}">
<data key="d5"/>
<data key="d6">
<y:SVGNode>
<y:Geometry height="{height}" width="{width}"/>
<y:Fill color="#CCCCCC" transparent="false"/>
<y:BorderStyle color="#000" type="line" width="1.0"/>
<y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" hasText="false" height="4.0" horizontalTextPosition="center" iconTextGap="4" modelName="sandwich" modelPosition="s" textColor="#000000" verticalTextPosition="bottom" visible="true" width="4.0" x="49.598968505859375" y="21.7762508392334"/>
<y:SVGNodeProperties usingVisualBounds="true"/>
<y:SVGModel svgBoundsPolicy="0">
<y:SVGContent refid="{id}"/>
</y:SVGModel>
</y:SVGNode>
</data>
</node>"""

proof_node_text = """<node id="{name}_proof">
<data key="d4" xml:space="preserve"><![CDATA[{link}]]></data>
<data key="d5"/>
<data key="d6">
<y:ShapeNode>
<y:Geometry height="12.0" width="12.0"/>
<y:Fill color="#000" transparent="false"/>
<y:BorderStyle color="#000" raised="false" type="line" width="1.0"/>
<y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" hasText="false" height="4.0" horizontalTextPosition="center" iconTextGap="4" modelName="custom" textColor="#000000" verticalTextPosition="bottom" visible="true" width="4.0" x="4.0" y="4.0">
<y:LabelModel>
<y:SmartNodeLabelModel distance="4.0"/>
</y:LabelModel>
<y:ModelParameter>
<y:SmartNodeLabelModelParameter labelRatioX="0.0" labelRatioY="0.0" nodeRatioX="0.0" nodeRatioY="0.0" offsetX="0.0" offsetY="0.0" upX="0.0" upY="-1.0"/>
</y:ModelParameter>
</y:NodeLabel>
<y:Shape type="ellipse"/>
</y:ShapeNode>
</data>
</node>"""

def_node_text = """<node id="{name}_def">
<data key="d5"/>
<data key="d6">
<y:ShapeNode>
<y:Geometry height="0" width="0"/>
<y:Fill color="#000" transparent="false"/>
<y:BorderStyle color="#000" raised="false" type="line" width="1.0"/>
<y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" hasText="false" height="4.0" horizontalTextPosition="center" iconTextGap="4" modelName="custom" textColor="#000000" verticalTextPosition="bottom" visible="true" width="4.0" x="4.0" y="4.0">
<y:LabelModel>
<y:SmartNodeLabelModel distance="4.0"/>
</y:LabelModel>
<y:ModelParameter>
<y:SmartNodeLabelModelParameter labelRatioX="0.0" labelRatioY="0.0" nodeRatioX="0.0" nodeRatioY="0.0" offsetX="0.0" offsetY="0.0" upX="0.0" upY="-1.0"/>
</y:ModelParameter>
</y:NodeLabel>
<y:Shape type="rectangle"/>
</y:ShapeNode>
</data>
</node>"""

edge_text = """\n<edge id="e{id}" source="{source}" target="{target}">
<data key="d9"/>
<data key="d10">
<y:PolyLineEdge>
<y:Path sx="0.0" sy="0.0" tx="0.0" ty="0.0"/>
<y:LineStyle color="#000" type="line" width="1.0"/>
<y:Arrows source="none" target="standard"/>
<y:BendStyle smoothed="false"/>
</y:PolyLineEdge>
</data>
</edge>"""

id = 1
for node in data:
    if 'hide' in data[node] and data[node]['hide']:
        continue
    fout.write(node_text.format(
        node=node, height=data[node]["height"]*12, width=32.5*12, id=id))
    id += 1

for node in data:
    if 'hide' in data[node] and data[node]['hide']:
        continue
    if ('proofs' not in data[node]):
        continue
    for proof in data[node]['proofs']:
        # proof node
        name = proof['name']
        link = './proof-pdf/' + name + '.pdf'
        fout.write(proof_node_text.format(name=name, link=link))

for node in data:
    if 'hide' in data[node] and data[node]['hide']:
        continue
    if ('defs' not in data[node]):
        continue
    for defin in data[node]['defs']:
        # proof node
        name = node + str(defin['id'])
        fout.write(def_node_text.format(name=name))


id = 0
for node in data:
    if 'hide' in data[node] and data[node]['hide']:
        continue
    if ('proofs' not in data[node]):
        continue
    for proof in data[node]['proofs']:
        name = proof['name']
        # proof edges
        for thm in proof['src']:
            fout.write(edge_text.format(
                id=id, source=thm, target=name+'_proof'))
            id += 1
        fout.write(edge_text.format(
            id=id, source=name+'_proof', target=node))
        id += 1

for node in data:
    if 'hide' in data[node] and data[node]['hide']:
        continue
    if ('defs' not in data[node]):
        continue
    for defin in data[node]['defs']:
        name = node + str(defin['id'])
        # proof edges
        for arg in defin['src']:
            fout.write(edge_text.format(
                id=id, source=arg, target=name+'_def'))
            id += 1
        fout.write(edge_text.format(
            id=id, source=name+'_def', target=node))
        id += 1

fout.write('\n</graph>\n<data key="d7">\n<y:Resources>')
svg_text = '\n<y:Resource id="{id}" xml:space="preserve">{svg}</y:Resource>'

id = 1
for node in data:
    svg = open('nodes-svgs/'+node+'.svg').read()
    fout.write(svg_text.format(
        id=id, svg=svg.replace("<", "&lt;").replace(">", "&gt;")))
    id += 1

fout.write("\n</y:Resources>\n</data>\n</graphml>")

fin.close()
fout.close()
