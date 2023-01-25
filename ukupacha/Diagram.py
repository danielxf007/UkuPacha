from ukupacha.Utils import is_dict
from blockdiag import parser, builder, drawer

_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
           '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']  # matplotlib TABLEAU_COLORS
# https://www.color-hex.com/color-palette/1017697
_colors += ['#56ba5a', '#0cc6b8', "#fdc0c7", "#8b9df2"]
# https://www.color-hex.com/color-palette/1017695
_colors += ["#0e8523", "#2b92eb", "#0911e0", "#7a00f9", "#b47ef4"]
# https://www.color-hex.com/color-palette/1017694
_colors += ["#960735", "#f8102a", "#ff9807", "#fff84c", "#75f708"]
# https://www.color-hex.com/color-palette/1017693
_colors += ["#986f42", "#50473f", "#554b50", "#423a28", "#8b7340"]
_colors += ['#00FFFF', '#7FFFD4', '#000000', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E', '#FF7F50', '#6495ED', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B', '#A9A9A9', '#006400', '#A9A9A9', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF', '#696969', '#696969', '#1E90FF', '#B22222', '#228B22', '#FF00FF', '#FFD700', '#DAA520', '#808080', '#008000', '#ADFF2F', '#808080', '#FF69B4', '#CD5C5C', '#4B0082', '#F0E68C', '#7CFC00', '#ADD8E6', '#F08080', '#90EE90', '#FFB6C1', '#FFA07A', '#20B2AA',
            '#87CEFA', '#778899', '#00FF00', '#32CD32', '#FF00FF', '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585', '#191970', '#FFE4B5', '#FFDEAD', '#000080', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA', '#98FB98', '#AFEEEE', '#DB7093', '#FFDAB9', '#CD853F', '#FFC0CB', '#DDA0DD', '#800080', '#663399', '#FF0000', '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460', '#2E8B57', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD', '#708090', '#00FF7F', '#4682B4', '#D2B48C', '#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#FFFF00', '#9ACD32']  # matplotlib ccs4 edited
_colors = list(dict.fromkeys(_colors))
colors = []


def graph2blockdiag(regs, pdb):
    """
    Recursive algorithm to parse the graph to a blockdiag structure.
    """
    global colors
    reg = regs[0]
    parent = list(reg.keys())[0]
    regs = reg.get(parent)
    if regs is None:
        if len(colors) == 0:
            colors = list(_colors[:])  # deep copy to start over
        color = colors.pop()
        return f"'{parent}\n{pdb}[color = \"{color}\"]';\n"
    output = ""
    for sub_reg in regs:
        db = sub_reg["DB"]
        for node in sub_reg["TABLES"]:
            out = graph2blockdiag([node], db)
            output += f" '{parent}\n{pdb}' -> {out}"
    return output


def model2diag(model: dict):
    """
    Given the model dict, takes the graph and the initial db to
    call grap2blockdiag
    """
    graph = model["GRAPH"]
    db = model["CHECKPOINT"]["DB"]
    out = graph2blockdiag(graph, db)
    output = "diagram { "+out+" }"
    return output


def diag2file(diag, filename, fmt):
    """
    Function to save the diagram in a file.

    Parameters
    ------------
    diag:str
        String with the diagram generated by model2diag
    filename:str
        file to save the diagram
    fmt:str
        format of the file, supported "SVG", "PNG" and "PDF"
    """
    tree = parser.parse_string(diag)
    diagram = builder.ScreenNodeBuilder.build(tree)
    draw = drawer.DiagramDraw(fmt, diagram, filename=filename)
    draw.draw()
    draw.save()