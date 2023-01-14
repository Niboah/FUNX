from flask import Flask, render_template, request, redirect, url_for
from collections import OrderedDict

import antlr4

from antlr4 import *
from funxLexer import funxLexer
from funxParser import funxParser

app = Flask(__name__)

output = {}
llista_fun = {}


@app.route('/')
def root():
    return render_template('base.html', result=output)


@app.route('/cleanF', methods=['POST'])
def cleanF():
    global llista_fun
    llista_fun = {}
    return render_template(
        "base.html",
        result=OrderedDict(
            reversed(
                list(
                    output.items()))),
        fun=llista_fun,
        exception="")


@app.route('/cleanO', methods=['POST'])
def cleanO():
    global output
    output = {}
    return render_template(
        "base.html",
        result=OrderedDict(
            reversed(
                list(
                    output.items()))),
        fun=llista_fun,
        exception="")


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        num = str(int(len(output) / 2))
        input_stream = antlr4.InputStream(request.form['text'])
        error = ""
        try:
            output["Out" + num + ":"] = funx(input_stream)
            output["In" + num + ":"] = request.form['text']
        except Exception as e:
            error = "Error: " + str(e)

        return render_template(
            "base.html",
            result=OrderedDict(
                reversed(
                    list(
                        output.items()))),
            fun=llista_fun,
            exception=error)


def funx(input_stream):
    lexer = funxLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = funxParser(token_stream)
    funx = parser.root()
    global llista_fun
    evalua = EvalVisitor(llista_fun)
    r = evalua.visit(funx)
    llista_fun = r[1]
    return r[0]


if __name__ == '__main__':
    app.run()


if __name__ is not None and "." in __name__:
    from .funxParser import funxParser
    from .funxVisitor import funxVisitor
else:
    from funxParser import funxParser
    from funxVisitor import funxVisitor


class EvalVisitor(funxVisitor):

    def __init__(self, func={}):
        self.level = 0
        self.var = {}
        self.func = func

    def function(self, name, fun, args):
        if len(fun[0]) != len(args):
            raise Exception("'" +
                            name +
                            "'" +
                            " expected " +
                            str(len(fun[0])) +
                            " arg(s), " +
                            str(len(args)) +
                            " given.")

        backup = self.var.copy()

        for arg, valor in zip(fun[0], args):
            self.var[arg] = valor

        r = self.visit(fun[1])
        self.var = backup.copy()
        return r

    def visitRoot(self, ctx):
        v = None
        for l in ctx.getChildren():
            r = self.visit(l)
            if r is not None:
                v = r
        if isinstance(v, bool):
            return [1 if v else 0, self.func]
        return [v, self.func]

    def visitNUM(self, ctx):
        l = list(ctx.getChildren())
        return int(l[0].getText())

    def visitSUMRES(self, ctx):
        l = list(ctx.getChildren())
        self.level += 1
        if l[1].getText() == '+':
            result = self.visit(l[0]) + self.visit(l[2])
        if l[1].getText() == '-':
            result = self.visit(l[0]) - self.visit(l[2])
        return result

    def visitMULDIVMOD(self, ctx):
        l = list(ctx.getChildren())
        self.level += 1
        if l[1].getText() == '*':
            result = self.visit(l[0]) * self.visit(l[2])
        if l[1].getText() == '/':
            result = self.visit(l[0]) / self.visit(l[2])
        if l[1].getText() == '%':
            result = self.visit(l[0]) % self.visit(l[2])
        self.level -= 1
        return result

    def visitCALLFUN(self, ctx: funxParser.CALLFUNContext):
        return self.visitChildren(ctx)

    def visitPARENTESIS(self, ctx: funxParser.PARENTESISContext):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    def visitInstr(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0])

    def visitAsign(self, ctx):
        l = list(ctx.getChildren())
        result = self.visit(l[2])
        self.var[l[0].getText()] = result
        # return result

    def visitEXPRVAR(self, ctx):
        var = ctx.VAR().getText()
        if var in self.var:
            return self.var[var]
        return 0

    def visitBoolean(self, ctx):
        l = list(ctx.getChildren())
        if l[1].getText() == '=':
            return self.visit(l[0]) == self.visit(l[2])
        if l[1].getText() == '!=':
            return self.visit(l[0]) != self.visit(l[2])
        if l[1].getText() == '<':
            return self.visit(l[0]) < self.visit(l[2])
        if l[1].getText() == '>':
            return self.visit(l[0]) > self.visit(l[2])
        if l[1].getText() == '<=':
            return self.visit(l[0]) <= self.visit(l[2])
        if l[1].getText() == '>=':
            return self.visit(l[0]) >= self.visit(l[2])

    def visitBody(self, ctx):
        for l in list(ctx.getChildren()):
            r = self.visit(l)
            if r is not None:
                return r

        return None

    def visitCondi(self, ctx):
        l = list(ctx.getChildren())
        if (self.visit(l[1])):
            return self.visit(l[3])
        elif (len(l) > 5):
            return self.visit(l[7])

    def visitIter(self, ctx):
        l = list(ctx.getChildren())
        while (self.visit(l[1])):
            result = self.visit(l[3])
        return result

    def visitDef_fun(self, ctx):
        l = list(ctx.getChildren())
        args = self.visit(l[1])
        if args is None:
            args = {}
        name = l[0].getText()
        if name in self.func:
            raise Exception("'" + name + "'" + " already exist")
        self.func[name] = [args, l[len(l) - 2]]

    def visitArgs(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            return {l[0].getText(): ""}
        args = self.visit(l[0])
        newArgs = l[1].getText()
        if newArgs in args:
            raise Exception("'" + newArgs + "'" + " repeated")
        args[newArgs] = ""
        return args

    def visitCall_args(self, ctx: funxParser.Call_argsContext):
        l = list(ctx.getChildren())
        if len(l) == 1:
            return [self.visit(l[0])]
        args = self.visit(l[0])
        args.extend(self.visit(l[1]))
        return args

    def visitCall_fun(self, ctx):
        l = list(ctx.getChildren())
        name = l[0].getText()
        if name not in self.func:
            raise Exception("'" + name + "'" + " not exist")
        fun = self.func[name]
        args = {}
        if len(l) > 1:
            args = self.visit(l[1])

        return self.function(name, fun, args)
