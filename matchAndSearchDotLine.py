import cv2
import numpy as np
import falconn
import math
import sys
import urllib
import json as m_json

#Read path to search image from command line
searchImg = sys.argv[1]

#Variable to hold number of feature descriptors SIFT returns
numDesc = 10

#Create OpenCV SIFT object used to detect and compute ffeture descriptors
sift = cv2.SIFT(numDesc)

#Get keypoints and feature descriptors from test image
img = cv2.imread(searchImg);
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kp, desc = sift.detectAndCompute(gray, None)

#Copy feature descriptor(s) of supplied image into an array
searchImgDesc = np.array([numDesc, 128])
searchImgDesc = desc[0:numDesc]

'''
LSH
Most of these parameters I copied straight from the FALCONN website
The descriptors.npz file has the feature descriptors from the
reference images
'''
dataset_file = 'dotLineDescriptors.npz'
number_of_queries = numDesc
number_of_tables = 10

#print "Reading dataset..."

'''
Load data from .npz file
After loading, the data structure is a dictionary (key-value pair),
where the key is a string - 'laptop', 'notebook', 'pencil', 'printer'
and the value is a numpy array - the array of feature descriptor values
'''
loadedDataset = np.load(dataset_file)
#need to get all the arrays from the dictionary into one large array
dot  = loadedDataset['dot']
line  = loadedDataset['line']
#pencil  = loadedDataset['pencil']
#rinter  = loadedDataset['printer']
#temp1 = np.append(laptop, notebook, axis=0)
#temp2 = np.append(temp1, loadedDataset['pencil'], axis=0)
#dataset contains all of the feature descriptors from the reference images
dataset = np.append(dot, line, axis=0)

print "Dataset shape:", dataset.shape
#print "Done"

#Make sure the data type of the dataset are floats
assert dataset.dtype == np.float32

#Skipping this step for now
'''
print "Normalizing dataset..."
dataset /= np.linalg.norm(dataset, axis=1).reshape(-1, 1)
print "Done"

#center dataset
print "Centering the dataset..."
center = np.mean(dataset, axis=0)
dataset -= center
testDesc -= center
print "Done"
'''

params_cp = falconn.LSHConstructionParameters()
params_cp.dimension = len(dataset[0])
params_cp.lsh_family = 'cross_polytope'
params_cp.distance_function = 'euclidean_squared'
params_cp.l = number_of_tables
params_cp.num_rotations = 1
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
table.setup(dataset)
#The value chosen for number_of_probes is a guess right now
number_of_probes = 5

#print "Consturcting the LSH table"
table = falconn.LSHIndex(params_cp)
table.setup(dataset)
#print "Done"


#skipping finding number of probes
#nnKey = []
nearestNeighbor = []

'''
This is where the real work of FALCONN is done.
The loop goes through the descriptors from the search image,
and uses FALCONN's nearest neighbor function to find descriptors
that are similar to the reference descriptors.
The nearest neighbor is added to a Python list, which is like a Java ArrayList
'''
for i in range(searchImgDesc.shape[0]):
	#nnKey.append(table.find_nearest_neighbor(testDesc[i]))
	nearestNeighbor.append(dataset[table.find_nearest_neighbor(searchImgDesc[i])])

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
counts = {'dot': 0, 'line': 0}

'''
Loop through the reference image descriptors for a count
NOTE: this is terribly inefficient
'''
for i in range(dot.shape[0]):
	for j in range(len(nearestNeighbor)):
		if np.array_equal(dot[i], nearestNeighbor[j]):
			counts['dot'] += 1

for i in range(line.shape[0]):
	for j in range(len(nearestNeighbor)):
		if np.array_equal(line[i], nearestNeighbor[j]):
			counts['line'] += 1
'''
for i in range(pencil.shape[0]):
	for j in range(len(nearestNeighbor)):
		if np.array_equal(pencil[i], nearestNeighbor[j]):
			counts['pencil'] += 1

for i in range(printer.shape[0]):
	for j in range(len(nearestNeighbor)):
		if np.array_equal(printer[i], nearestNeighbor[j]):
			counts['printer'] += 1
'''
print counts
print max(counts, key=counts.get)

'''
I got the code below from here:
http://stackoverflow.com/questions/3898574/google-search-using-python-script
Not ideal, but probably enough for a prototype.
I'm retruning the search results as a JSON object.
I think that should be easy to work with on Daniel's side of the code

query = max(counts, key=counts.get)
query = urllib.urlencode({'q' : query})
response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query).read()
json = m_json.loads(response)
results = json['responseData']['results']
'''
#printing out search results for testing 
#for result in results:
#	title = result['title']
#	url = result['url']
#	print title + "; " + url

#return results
