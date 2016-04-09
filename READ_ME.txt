I thought I'd write this to explain the purpose of some of the files in this folder.

pyExtractDesc.py extracts the feature descriptors of the reference images and saves them in the descriptors.npz file.  It only needs to be run once, and I've already run it.  So you can ignore it, but don't delete it.

The images WITHOUT "test_" in the name are the "reference images."  I ran the pyExtractDesc.py program on them to produce the descriptors.npz file.

The descriptors.npz file contains the feature descriptors returned by running SIFT on the reference images.  This file is loaded when matchAndSearch.py is ran.  It is kind of like a database.

The images WITH "test_" in the name were images I was using to test out my program.

matchAndSearch.py is the program that:
	1) runs SIFT on the search image,
	2) uses FALCONN to find the nearest neighbors among the the reference feature descriptors, 
	3) attempts to find a match of the nearest neighbors in the reference feature descriptors, 
	4) keeps track of where matches are found, i.e. in the "pencil" reference feature descriptors, and increments a counter for each match,
	5) chooses the counter with the highest value as the matched image
	6) does a web search on the name of the matched image
	7) saves it as a JSON object
	8) and returns the object

You can ignore, but please don't delete both the compileCommand, and extractDesc.cpp files.

***Daniel** - when your code calls matchAndSearch.py it needs to provide the path to the search image.  matchAndSearch.py returns a JSON object that contains the web search results.

So, you'll need to do something like this in your code:
	1) Create a variable of type JSON, like 'myJSON'
	2) call my program as follows: myJSON = matchAndSearch.py /absolute/path/to/search/image
	3) then parse the JSON object and display it
