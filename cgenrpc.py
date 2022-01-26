# Using pycparser
# Based on files in the examples directory of the repo https://github.com/eliben/pycparser
# See https://github.com/eliben/pycparser/tree/master/examples

import sys
from pycparser import c_ast, c_generator, parse_file

class FuncArgVisitor(c_ast.NodeVisitor):
    def visit_FuncDecl(self, node):
        if node.args:
            print("The args of func")
            print(node.args.params)
        else:
            print("No args")

def show_add_func(filename):
    # Do we need to use_cpp? 
    # based on https://github.com/eliben/pycparser/blob/master/examples/c-to-c.py
    ast = parse_file(filename, use_cpp=True)

    #v = FuncDefVisitor()
    #v.visit(ast)

    v2 = FuncArgVisitor()
    v2.visit(ast)

    new_func_ret_type = c_ast.TypeDecl(
        declname='new_invoke',
        quals=[],
        align=None,
        type=c_ast.IdentifierType(names=['void']))

    new_func_args_ret = c_ast.FuncDecl(
        args=None,
        type=new_func_ret_type)

    new_func_decl = c_ast.Decl(
        name = "new_invoke",
        quals = [],
        align = [],
        storage=[],
        funcspec=[],
        type=new_func_args_ret,
        init=None,
        bitsize=None)

    new_func_body = c_ast.Compound(
        block_items=[])

    new_func_node = c_ast.FuncDef(
        decl = new_func_decl,
        param_decls=None,
        body=new_func_body)

    # This example is to just add an empty new_invoke function

    ast.ext.append(new_func_node)
    generator = c_generator.CGenerator()
    print(generator.visit(ast))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename  = sys.argv[1]
    else:
        print("Usage: %s c_filename" % sys.argv[0])
        exit(0)

    show_add_func(filename)
