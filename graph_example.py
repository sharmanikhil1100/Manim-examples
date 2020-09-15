from manimlib.imports import *
import math

pi = math.pi

class Graphing(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 6,
        "y_min": -1,
        "y_max": 1,
        "graph_origin": 0*DOWN + 5*LEFT,
        "function_color": WHITE,
        "axes_color": BLUE
    }

    def construct(self):
        title_text = TextMobject("Plotting Sine and Cosine curve ", color="YELLOW").to_corner(ORIGIN)

        self.play(ShowCreation(title_text))
        self.wait()
        self.play(FadeOut(title_text))

        #Make graph
        self.setup_axes(animate=True)

        sine_graph=self.get_graph(self.sine_fn,self.function_color)
        graph_lab = self.get_graph_label(sine_graph, label = "sin")

        cose_graph=self.get_graph(self.cos_fn,self.function_color)
        graph_lab_2 = self.get_graph_label(cose_graph, label = "cos")

        #Display graph
        self.play(ShowCreation(sine_graph), Write(graph_lab))
        self.wait()
        self.play(FadeOut(sine_graph))
        self.wait()
        self.play(ShowCreation(cose_graph), Write(graph_lab_2))
        self.wait(2)


    def sine_fn(self, x):
        return (math.sin(pi*x))

    def cos_fn(self, x):
        return(math.cos(pi*x))