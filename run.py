import pickle
import topsis

import graph_extraction

def candidate_search(substrate, vne_list,vne_list_rank,substrate_list_rank):

    # substrate candidate for each node of this req
    candidate_set = dict()

    # assume req is not rejected.
    rejected = False

    # traverse the req.
    mapped = [False] *  substrate.nodes
    for j in range(vne_list.nodes):
        # subs candidates of each node of this req.
        candidates = []
        j_index = vne_list_rank[j+1]
        
        # traverse the substrate n/w.
        for k in range(substrate.nodes):
          index = substrate_list_rank[k+1]
          if mapped[index] == False:
           if substrate.node_weights[index] >= vne_list.node_weights[j_index]:
            if substrate.node_level[index] >= vne_list.node_demand[j_index]:
              if substrate.node_demand[index] <= vne_list.node_level[j_index]:
                 mapped[index] = True
                 candidates.append(index)
                 break
                 

        # if candidate set is empty then reject the req.
        if len(candidates) == 0:
            rejected = True
            break
        else:
            candidate_set[j] = candidates
    # print(candidate_set)
    return candidate_set, rejected
def candidate_validation(substrate, vne_list,vne_list_rank,substrate_list_rank):
    Candidate = dict()
    
    

    # assume req is not rejected.
    rejected = False


    for j in range(vne_list.nodes):
        # subs candidates of each node of this req.
        Candidates = []
        j_index = vne_list_rank[j+1]
        
        # traverse the substrate n/w.
        for k in range(substrate.nodes):
          index = substrate_list_rank[k+1]
          
          if substrate.node_weights[index] >= vne_list.node_weights[j_index]:
            if substrate.node_level[index] >= vne_list.node_demand[j_index]:
              if substrate.node_demand[index] <= vne_list.node_level[j_index]:
                 Candidates.append(index)
                 

        # if candidate set is empty then reject the req.
        if len(Candidates) == 0:
            rejected = True
            break
        else:
            Candidate[j] = Candidates
    # print(candidate_set)
    return Candidate, rejected

x = graph_extraction.Extract()
substrate, vne_list= x.get_graphs()
v = []

print("***Physical Substrate Structure***")
print("Node\t weights \t demand \t level")

for i in range(substrate.nodes):
    print(i ,"\t",substrate.node_weights[i],"\t","\t",substrate.node_demand[i],"\t\t",substrate.node_level[i])
print("Edge weights of physical substrate")

for key, value in substrate.edge_weights.items():
    print(key, ' : ', value)
print("\n")

print("***Virtual Node request***")
print("Node\t weights \t demand \t level")
for i in range(vne_list.nodes):
    print(i ,"\t",vne_list.node_weights[i],"\t","\t",vne_list.node_demand[i],"\t\t",vne_list.node_level[i])

print("Edge weights of virtual reuquest")

for key, value in vne_list.edge_weights.items():
    print(key, ' : ', value)
print("\n")

for i in range(vne_list.nodes):
    tmp = []
    w = vne_list.node_weights[i]
    y = vne_list.node_demand[i]
    z = vne_list.node_level[i]
    tmp.append(w)
    tmp.append(y)
    tmp.append(z) 
    v.append(tmp)
# for x in matrix:
#  print(x)
t = topsis.Topsis(v)
t.calc()
#print(t.rank_to_best_similarity())
print("Implement Topsis on VNR for best order to map")
vne_rank_index = t.rank_to_best_similarity()
vne_list_rank = dict()

for i in range(vne_list.nodes):
   vne_list_rank[vne_rank_index[i]] = i;

print(vne_list_rank)  
#use topsis for substrate 
s = []
for i in range(substrate.nodes):
    tmp = []
    w = substrate.node_weights[i]
    y = substrate.node_demand[i]
    z = substrate.node_level[i]
    tmp.append(w)
    tmp.append(y)
    tmp.append(z) 
    s.append(tmp)
# for x in matrix:
#  print(x)
t = topsis.Topsis(s)
t.calc()
#print(t.rank_to_best_similarity())

substrate_rank_index = t.rank_to_best_similarity()
substrate_list_rank = dict()

for i in range(substrate.nodes):
   substrate_list_rank[substrate_rank_index[i]] = i;
print("\n")
print("Implement Topsis on physical Substrate for best order to map")
print(substrate_list_rank)  
print("\n\n")
print("Different way by which we can map every virtual node")
Candidate_Set,reject = candidate_validation(substrate, vne_list,vne_list_rank,substrate_list_rank)
print("virtual Node \t physical substrate Node")
for key, value in Candidate_Set.items():
    print(key, ' \t\t ', value)
print("\n")


candidate_set, rejected = candidate_search(substrate,vne_list,vne_list_rank,substrate_list_rank)

if rejected == True:
  print("***The request {} is rejected due to lack of resources***")
else: 
    print("***final Mapping *** ")
    print("virtual Node \t physical substrate Node")

for key, value in candidate_set.items():
    print(key, ' :\t\t ', value)
print("\n")


#print(Candidate_Set)

