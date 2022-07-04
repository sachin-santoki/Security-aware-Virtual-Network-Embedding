import os
import pickle
import sys
import graph
from vne import create_vne


class Extract:
    # def get_graphs(self, req_no = 5):     # USE THIS DEFINATION FOR AUTOMATION & comment line no 10
    def get_graphs(self):
        #current = os.path.dirname(os.path.realpath(__file__))
        #sys.path.append(os.path.join(os.path.dirname(current), "cloud_alib"))
        current = os.path.join(
            os.getcwd(),
            "input",
            "input.pickle",
          )
        with open(current, "rb") as f:
            data = pickle.load(f)
            
        para = graph.Parameters(100, 300 , 50,100 , 50, 100, 100, 200)  # Parameters for subsrate graph BW ,CRB, Location,Delay
        substrate = graph.Graph(
           7,
            [('5','4'),('4','5'),('0','1'),('1','0'),('4','3'),('3','4'),('2','6'),('6','2'),('5','2'),('2','5'),('1','3'),('3','1')],
            para,
        )
        vne_list = create_vne()
        return substrate, vne_list


if __name__ == "__main__":
    x = Extract()
    substrate, vne_list = x.get_graphs()
    output = {"substrate": substrate, "vne_list" : vne_list}
    pickle_file = open("input/graph.pickle", "wb")
    pickle.dump(output, pickle_file)