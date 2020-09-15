from manimlib.imports import *
from sklearn import datasets
from sklearn import decomposition
import numpy as np
import math

class Regression(GraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 10,
        "x_axis_width": 8,
        "x_tick_frequency": 1,
        "x_leftmost_tick": 0, # Change if different from x_min
        "x_labeled_nums": None,
        "x_axis_label": "$x$",
        "y_min": 0,
        "y_max": 30,
        "y_axis_height": 4,
        "y_tick_frequency": 1,
        "y_bottom_tick": 0, # Change if different from y_min
        "y_labeled_nums": None,
        "y_axis_label": "$y$",
        "graph_origin" : 2*DOWN + 6*LEFT,
        "function_color": WHITE,
        "axes_color": BLUE
    }
    def construct(self):
        red = "RED"
        green = "GREEN"
        orange = "ORANGE"
        features_ =["Sepal Length", "Sepal Width", "Petal Length","Petal Width"]

        iris = datasets.load_iris()
        X = iris["data"]
        y = iris["target"]

        #Plotting each of the features on the graph
        self.x_max = 150+2
        self.y_min = np.array([data_column.min() for data_column in X]).min() -1
        self.y_max = np.array([data_column.max() for data_column in X]).max() +1
        self.x_tick_frequency = self.x_max/10
        self.y_tick_frequency = self.y_max/2
        self.x_labeled_nums = [i*self.x_tick_frequency for i in range(1,math.ceil(self.x_max/self.x_tick_frequency))]
        self.y_labeled_nums = [2,4,6,8]

        title = TextMobject("The features of Iris dataset:")
        title.to_edge(UP, buff= 0.1)
        class_label1 = TextMobject("Setosa", color=red)
        class_label1.to_corner(UR)
        class_label2 = TextMobject("Versiocolor", color=green)
        class_label2.next_to(class_label1, direction=DOWN, aligned_edge=RIGHT)
        class_label3 = TextMobject("Virginica", color=orange)
        class_label3.next_to(class_label2, direction=DOWN, aligned_edge=RIGHT)

        self.play(ShowCreation(title))
        self.setup_axes(animate=True)
        self.play(ShowCreation(class_label1), ShowCreation(class_label2), ShowCreation(class_label3))
        
        _, total_features = X.shape
        points = []
        features = [0 for i in range(len(X))]
        feature_labels = [0 for i in range(len(X))]
        col_points = []
        
        for i in range(total_features):
            features[i] = self.get_graph(self.plain)
            features[i].graph_origin = ORIGIN
            feature_labels[i] = self.get_graph_label(features[i], label = features_[i], color=BLUE).shift(RIGHT)
            #Points -
            points = VGroup(*[ Dot(self.coords_to_point(j, X[j, i]), color = red if y[j]==0 else green if y[j]==1 else orange) for j in range(len(X)) ])
            col_points.append(points)

        # Adding animations
        for i in range(total_features):
            self.play(ShowCreation(features[i]), Write(feature_labels[i]))
            self.play(FadeIn(col_points[i]))
            self.wait(2)
            self.play(FadeOut(features[i]))
            self.play(FadeOut(feature_labels[i]))
            self.play(FadeOut(col_points[i]))
            
    
    def plain(self, index):
        return 0

class PCA(GraphScene):
    CONFIG = {
        "x_min": -10,
        "x_max": 10,
        "x_axis_width": 9,
        #"x_tick_frequency": 1,
        #"x_labeled_nums": None,
        #"x_axis_label": "$x$",
        "y_min": -10,
        "y_max": 10,
        "y_axis_height": 4,
        #"y_tick_frequency": 1,
        #"y_labeled_nums": None,
        #"y_axis_label": "$y$",
        "graph_origin" : ORIGIN,
        "function_color": BLACK,
        "axes_color": BLACK
    }

    def construct(self):
        red = "RED"
        green = "GREEN"
        orange = "ORANGE"
        features_ =["Sepal Length", "Sepal Width", "Petal Length","Petal Width"]

        iris = datasets.load_iris()
        X = iris["data"]
        y = iris["target"]

        row = 6
        col = 4
        matrix = [["" for j in range(col)] for i in range(row)] #Just For Display
        for j in range(col):
            for i in range(row):
                if i>3:
                    matrix[i][j]="."
                else:
                    matrix[i][j]=X[i][j]


        ########### Matrix ########### 
        matrix_title1 = TextMobject("Dataset (Before PCA) ")
        matrix_title1.to_edge(UP, buff=0.1)
        mat1 = Matrix(matrix)
        #mat = mat.get_columns()
        self.play(ShowCreation(matrix_title1))
        self.wait()
        self.play(ShowCreation(mat1))
        self.wait()

        # PCA
        pca = decomposition.PCA(n_components=2)
        pca.fit(X)
        X = pca.transform(X)

        row = 6
        col = 2
        matrix = [["" for j in range(col)] for i in range(row)] #Just For Display
        for j in range(col):
            for i in range(row):
                if i>3:
                    matrix[i][j]="."
                else:
                    matrix[i][j]=round(X[i][j], 2)
        
        ########### Matrix ########### 
        matrix_title2 = TextMobject("Dataset (After PCA) ")
        matrix_title2.to_edge(UP, buff=0.1)
        mat2 = Matrix(matrix)
        #mat = mat.get_columns()
        self.play(Transform(matrix_title1, matrix_title2))
        self.wait()
        self.play(Transform(mat1, mat2))
        self.wait()
        self.play(FadeOut(matrix_title2), FadeOut(mat2), FadeOut(matrix_title1), FadeOut(mat1))
        self.wait()

        plt_message1 = TextMobject("The 2 components are now plotted ", color="YELLOW").to_edge(ORIGIN)
        plt_message2 = TextMobject("that represent the whole dataset :", color="YELLOW").next_to(plt_message1, DOWN)
        self.play(ShowCreation(plt_message1), ShowCreation(plt_message2))
        self.wait(2)
        self.play(FadeOutAndShiftDown(plt_message1), FadeOutAndShiftDown(plt_message2))
        self.wait()

        #Plotting each of the features on the graph
        #Graph property Updates -
        self.x_min = int(np.array(X[:,0]).min())-1
        self.x_max = int(np.array(X[:,0]).max())+1
        self.y_min = int(np.array(X[:,1]).min())-1
        self.y_max = int(np.array(X[:,1]).max())+1
        self.x_tick_frequency = self.x_max/5
        self.y_tick_frequency = self.y_max/5
        # These are Doubtful (labeling the axes)
        #self.x_labeled_nums = [i*self.x_tick_frequency for i in range(1,int(self.x_max/self.x_tick_frequency))]
        #self.y_labeled_nums = [i*self.y_tick_frequency for i in range(1,int(self.y_max/self.y_tick_frequency))]
        
        #These remaining are important, as it changes the whole perspective of the graph
        self.graph_origin = ORIGIN
        self.function_color = WHITE
        self.axes_color = BLUE
        self.setup_axes(animate=True)

        class_label1 = TextMobject("Setosa", color=red)
        class_label1.to_corner(UR)
        class_label2 = TextMobject("Versiocolor", color=green)
        class_label2.next_to(class_label1, direction=DOWN, aligned_edge=RIGHT)
        class_label3 = TextMobject("Virginica", color=orange)
        class_label3.next_to(class_label2, direction=DOWN, aligned_edge=RIGHT)

        self.play(ShowCreation(class_label1), ShowCreation(class_label2), ShowCreation(class_label3))
        self.wait(2)

        features_ =["Sepal Length", "Sepal Width"]
        _, total_features = X.shape
        col_points = []
        
        features = self.get_graph(self.plainfn)
        feature_labels = self.get_graph_label(features, label = "Combined Features").to_corner(DR)

        ########### Points ###########
        points = VGroup(*[ Dot(self.coords_to_point(X[j, 0], X[j, 1]), color = red if y[j]==0 else green if y[j]==1 else orange) for j in range(len(X)) ])

        self.play(ShowCreation(features), Write(feature_labels))
        self.play(FadeIn(points))
        self.wait(3)

    def plainfn(self, index):
        return 0
