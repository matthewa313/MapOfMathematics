#!/usr/bin/env python3
"""
render.py

Read LaTeX code from stdin and render a SVG using LaTeX + dvisvgm.
"""
__version__ = '0.1.0'
__author__ = 'Matthew Anderson'
__email__ = 'umatthew@umich.edu'
__license__ = 'MIT'
__copyright__ = '(c) 2022, Matthew Anderson'

import os
import sys
import subprocess
import shlex
import re
from tempfile import TemporaryDirectory
from ctypes.util import find_library
import json
import os
import glob
from latex2svg import latex2svg
from jsonmerge import merge
from tqdm import tqdm

FONT_SIZE = 12
COLORING_STYLE = 'type'  # 'subject', 'class', 'author' -- not supported
FORCE_NODE_RENDER = False
COLOR_ON = False


def identify_target_map() -> str:
    # return target map key from config-file.json
    try:
        with open('config-file.json') as f:
            config = json.load(f)
    except:
        print('Error: config-file.json not found')
        sys.exit(1)
    return config['target-map']


def collect_logs(target_map: str) -> None:
    global rendered_logs_old
    rendered_logs_old_file = open('.logs/' + target_map +
                                  '/rendered_nodes.json', 'r')
    rendered_logs_old = json.load(rendered_logs_old_file)
    global rendered_logs_json
    rendered_logs_json = {}


def node_color(node: dict) -> str:
    # return node color based on its type
    if not COLOR_ON:
        return "white"
    if "type" not in node:
        return "white"
    type = node["type"]
    if type == "definition":
        return "blue!20"
    if type == "theorem":
        return "yellow!20"
    if type == "corollary":
        return "yellow!10"
    if type == "axiomatic":
        return "red!20"
    return "white"


def already_rendered(name: str, data: dict) -> bool:
    if name not in rendered_logs_old:
        return False
    if name + '.svg' not in os.listdir('./nodes-svgs'):
        return False
    if 'height' not in data or 'width' not in data:
        return False
    return data["tex"] == rendered_logs_old[name]["tex"]


def render_node(name: str, data: dict) -> None:
    # if node already rendered, skip
    if not FORCE_NODE_RENDER and already_rendered(name, data):
        return
    # compute tex of node
    tex = '\\textbf{' + data['type'].capitalize() + '.} ' + data['tex']
    # try rendering node
    try:
        output = latex2svg(tex, color=node_color(data))
    except:
        print("LaTeX error while rendering: " + name)
    # write output to nodes-svgs file
    with open('nodes-svgs/' + name + '.svg', 'w') as f_read:
        print('rendering ' + name)
        f_read.writelines(output["svg"])
        data["width"] = round(output["width"] * FONT_SIZE, 2)
        data["height"] = round(output["height"] * FONT_SIZE, 2)


def render_nodes_from_file(filename: str) -> None:
    with open(filename, 'r') as file:
        data = json.load(file)
    for node in data:
        render_node(node, data[node])
        rendered_logs_json[node] = data[node]
    json.dump(data, open(filename, 'w'))


def render_nodes(target_map: str) -> None:
    for filename in glob.glob("./nodes/math/*.json"):
        render_nodes_from_file(filename)
    # write rendered nodes to log file
    rendered_logs_write = open(
        '.logs/' + target_map + '/rendered_nodes.json', 'w')
    json.dump(rendered_logs_json, rendered_logs_write)


def clear_map_directory() -> None:
    # clear map directory of files beginning with .
    # objective is to clear out files stored to my iCloud drive
    for f in glob.glob('map/.*'):
        os.remove(f)


def read_graphml_template_code() -> None:
    global graphml_preamble
    with open('graphml/preamble.txt', 'r') as file:
        graphml_preamble = file.read()
    global graphml_node
    with open('graphml/node.txt', 'r') as file:
        graphml_node = file.read()
    global graphml_proof
    with open('graphml/proof.txt', 'r') as file:
        graphml_proof = file.read()
    global graphml_def
    with open('graphml/def.txt', 'r') as file:
        graphml_def = file.read()
    global graphml_edge
    with open('graphml/edge.txt', 'r') as file:
        graphml_edge = file.read()


def write_preamble(fout) -> None:
    fout.write(graphml_preamble)


def write_node(fout, name: str, data: dict, id: int) -> None:
    fout.write(graphml_node.format(node=name, id=id,
               height=data['height'], width=data['width']))


def write_nodes(fout) -> None:
    id = 1
    for node in rendered_logs_json:
        write_node(fout, node, rendered_logs_json[node], id)
        id += 1


def write_proof(fout, name: str) -> None:
    link = os.getcwd() + '/proof-pdf/' + name + '.pdf'
    fout.write(graphml_proof.format(name=name, link=link))


def write_proofs(fout) -> None:
    for node in rendered_logs_json:
        if 'proofs' not in rendered_logs_json[node]:
            continue
        for proof in rendered_logs_json[node]['proofs']:
            write_proof(fout, proof['name'])


def write_defs(fout) -> None:
    for node in rendered_logs_json:
        if 'defs' not in rendered_logs_json[node]:
            continue
        for defn in rendered_logs_json[node]['defs']:
            name = node + str(defn['id'])
            fout.write(graphml_def.format(name=name))


def write_proof_edges(fout, node, name, src, id) -> int:
    for thm in src:
        fout.write(graphml_edge.format(
            id=id, source=thm, target=name+'_proof', style='t_shape'))
        id += 1
    fout.write(graphml_edge.format(id=id, source=name +
               '_proof', target=node, style='standard'))
    id += 1
    return id


def write_def_edges(fout, node, name, src, id) -> int:
    name = node + str(name)
    for arg in src:
        fout.write(graphml_edge.format(id=id, source=arg,
                   target=name+'_def', style='t_shape'))
        id += 1
    fout.write(graphml_edge.format(id=id, source=name +
               '_def', target=node, style='standard'))
    id += 1
    return id


def write_edges(fout) -> None:
    edge_id = 0
    for node in rendered_logs_json:
        # write proof edges
        if 'proofs' in rendered_logs_json[node]:
            for proof in rendered_logs_json[node]['proofs']:
                edge_id = write_proof_edges(
                    fout, node, proof['name'], proof['src'], edge_id)
        # write def edges
        if 'defs' in rendered_logs_json[node]:
            for defn in rendered_logs_json[node]['defs']:
                edge_id = write_def_edges(
                    fout, node, defn['id'], defn['src'], edge_id)


def write_svgs(fout) -> None:
    svg_text = '\n<y:Resource id="{id}" xml:space="preserve">{svg}</y:Resource>'
    id = 1
    for node in rendered_logs_json:
        svg = open('nodes-svgs/'+node+'.svg').read()
        fout.write(svg_text.format(
            id=id, svg=svg.replace("<", "&lt;").replace(">", "&gt;")))
        id += 1


def draw_map(target_map: str) -> None:
    clear_map_directory()
    fout = open('map/' + target_map + '/map.graphml', 'w')
    read_graphml_template_code()
    write_preamble(fout)
    write_nodes(fout)
    write_proofs(fout)
    write_defs(fout)
    write_edges(fout)
    fout.write('\n</graph>\n<data key="d7">\n<y:Resources>')
    write_svgs(fout)
    fout.write("\n</y:Resources>\n</data>\n</graphml>")
    fout.close()


def main() -> None:
    # args: force rerender of all nodes
    # if force rerender, clear rendered_nodes.json
    # args: render pdfs
    # which map are we rendering?
    target_map = identify_target_map()
    collect_logs(target_map)
    render_nodes(target_map)
    draw_map(target_map)


if __name__ == "__main__":
    main()
