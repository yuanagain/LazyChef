"""
Generates 7 dummy nodes at ./tasks_out/

Usage:

python json_test_file.py
"""
import numpy as np
from tnode import TaskNode
import todoListGenerator as tdlg

def main():
  Tnode0 = TaskNode(0,0,0,np.array([1,2,3,4]), \
    'Put water on stove', \
    'Put water in pot. Put pot on stove')
  Tnode1 = TaskNode(1,30,0,np.array([5]), \
    'Put water on stove', \
    'Put water in pot. Put pot on stove')
  Tnode2 = TaskNode(2,0,300,np.array([]), \
    'Boil Water', \
    'Bring water to a boil')
  Tnode3 = TaskNode(3,15,0,np.array([]), \
    'Add salt', \
    'Add salt to water')
  Tnode4 = TaskNode(4,15,0,np.array([]), \
    'Put pasta in water', \
    'Add pasta to boiling water')
  Tnode5 = TaskNode(5,60,0,np.array([6]), \
    'Dice Tomatoes', \
    'Dice Tomatoes into small cubes')
  Tnode6 = TaskNode(6,20,0,np.array([7]), \
    'Drain pasta', \
    'Drain pasta using a strainer')
  Tnode7 = TaskNode(7,15,0,np.array([]), \
    'Put Tomatoes in pasta', \
    'Cover the pasta with Tomatoes')
  tnode_list = [Tnode0, Tnode1, Tnode2, Tnode3, Tnode4, Tnode5, Tnode6, Tnode7]
  tdlg.tnodelist_tojson(tnode_list)

if __name__ == "__main__":
  main()