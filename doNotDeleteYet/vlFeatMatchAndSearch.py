import cv2
import numpy as np
import falconn
import math
import sys
import urllib
import json as m_json
from PIL import Image
import os

#Read path to search image from command line
searchImgPath = sys.argv[1]

#Variable to hold number of feature descriptors SIFT returns
numDesc = 10

vlFeat = "/home/maotouying/Code/LSDMProject/imagesAndKeyPoints/sturdy-potato/vlfeat-0.9.20/bin/glnxa64/sift "
params = "--edge-thresh 10 --peak-thresh 5"

searchImg = Image.open(searchImgPath).convert('L')
searchImg.save('searchIm.pgm')
searchImgName = 'searchIm.pgm'

cmmd = str(vlFeat + searchImgName + " --output=searchImg.sift" + " " + params)

os.system(cmmd)

searchImgDesc = np.loadtxt('searchImg.sift', dtype=np.float32)

'''
LSH
Most of these parameters I copied straight from the FALCONN website
The descriptors.npz file has the feature descriptors from the
reference images
'''
#dataset_file = 'descriptors.npz'
number_of_queries = numDesc
number_of_tables = 10

#print "Reading dataset..."

'''
Load data from .npz file
After loading, the data structure is a dictionary (key-value pair),
where the key is a string - 'laptop', 'notebook', 'pencil', 'printer'
and the value is a numpy array - the array of feature descriptor values
'''
laptop = np.loadtxt('laptop.sift', dtype=np.float32)
print laptop[0]
#print "Data type of laptop is ", laptop.dtype
#print "Shape of laptop is ", laptop.shape
notebook = np.loadtxt('notebook.sift', dtype=np.float32)
#print notebook[0]
#print "Data type of notebook is ", notebook.dtype
pencil = np.loadtxt('pencil.sift', dtype=np.float32)
#print "Data type of pencil is ", pencil.dtype
printer = np.loadtxt('printer.sift', dtype=np.float32)
#print "Data type of printer is ", printer.dtype

temp1 = np.append(laptop, notebook, axis=0)
temp2 = np.append(temp1, pencil, axis=0)
#dataset contains all of the feature descriptors from the reference images
dataset = np.append(temp2, printer, axis=0)
#print "dataset dtype is ", dataset.dtype

#Make sure the data type of the dataset are floats
assert dataset.dtype == np.float32

#Skipping this step for now

print "Normalizing dataset..."
normDataset = dataset/np.linalg.norm(dataset, axis=1).reshape(-1, 1)
normSearchImgDesc = searchImgDesc/np.linalg.norm(searchImgDesc, axis=1).reshape(-1, 1)
print "Done"

#center dataset
print "Centering the dataset..."
center = np.mean(dataset, axis=0)
normDataset -= center
normSearchImgDesc -= center
print "Done"


params_cp = falconn.LSHConstructionParameters()
params_cp.dimension = len(dataset[0])
params_cp.lsh_family = 'cross_polytope'
params_cp.distance_function = 'euclidean_squared'
params_cp.l = number_of_tables
params_cp.num_rotations = 2
params_cp.seed = 5721840
params_cp.num_setup_threads = 0
params_cp.storage_hash_table = 'bit_packed_flat_hash_table'
''' 
Modify params such that each hash table has 2^num_bits bins
The number of bins seems to be related to size of data set 
'''
falconn.compute_number_of_hash_functions(11, params_cp)

#print "Constructing the LSH table"
table = falconn.LSHIndex(params_cp)
table.setup(normDataset)
#The value chosen for number_of_probes is a guess right now
number_of_probes = 5

#skipping finding number of probes
nnKey = []
nearestNeighbor = []

'''
This is where the real work of FALCONN is done.
The loop goes through the descriptors from the search image,
and uses FALCONN's nearest neighbor function to find descriptors
that are similar to the reference descriptors.
The nearest neighbor is added to a Python list, which is like a Java ArrayList
'''
for i in range(normSearchImgDesc.shape[0]):
	nnKey.append(table.find_nearest_neighbor(normSearchImgDesc[i]))
	nearestNeighbor.append(dataset[nnKey[i]])

'''
counts is a dictionary used as a counter.
Since one feature descriptor from the search image won't be 
enough to match an image on, we need to use multiple
feature descriptors.  So my idea is to take the nearest neighbors 
returned by FALCONN, and then find which reference images
they came from.  Each match increments a counter for the relevant
reference image.  The matching image is the one with the
highest count.
'''
counts = {'laptop': 0, 'notebook': 0, 'pencil': 0, 'printer' : 0}

'''
Loop through the reference image descriptors for a count
NOTE: this is terribly inefficient
'''
for i in range(laptop.shape[0]):
	for j in range(len(nearestNeighbor)):
		if np.array_equal(laptop[i], nearestNeighbor[j]):
			counts['laptop'] += 1

for i in range(notebook.shape[0]):
	for j in range(len(nearestNeighbor)):
		if np.array_equal(notebook[i], nearestNeighbor[j]):
			counts['notebook'] += 1

for i in range(pencil.shape[0]):
	for j in range(len(nearestNeighbor)):
		if np.array_equal(pencil[i], nearestNeighbor[j]):
			counts['pencil'] += 1

for i in range(printer.shape[0]):
	for j in range(len(nearestNeighbor)):
		if np.array_equal(printer[i], nearestNeighbor[j]):
			counts['printer'] += 1

print counts
print max(counts, key=counts.get)

'''
I got the code below from here:
http://stackoverflow.com/questions/3898574/google-search-using-python-script
Not ideal, but probably enough for a prototype.
I'm retruning the search results as a JSON object.
I think that should be easy to work with on Daniel's side of the code
'''
#query = max(counts, key=counts.get)
#query = urllib.urlencode({'q' : query})
#response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query).read()
#json = m_json.loads(response)
#results = json['responseData']['results']
#printing out search results for testing 
#for result in results:
#	title = result['title']
#	url = result['url']
#	print title + "; " + url

#return results
