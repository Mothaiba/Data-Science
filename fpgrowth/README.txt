AUTHOR
	I'm Phung Minh Tung, and of course I'm not the author of this algorithm
	No copyright reserved, you can do anything with this!
	If this helps, or something wrong happens, feel free to message me: tungphung2907@gmail.com
	Best wishes for you!
	
DESCRIPTION
	This is an implementation of the FP-Growth algorithm for frequent pattern mining
	This is implemented in Python, so it will take you a little longer run time than if it were implemented in C/C++
	If the dataset is too big compared to your memory, this may crash!
	Comments included, so you maybe able to modify this easily
	
HOW TO USE
	I wrote this in fpgrowth.py, but let me copy it here:
		to use, just call the function:
		
					frequent_Pattern_fpGrowth(listOfTrans,min_sup,show_support)
					 
		type of 'transactions' is array of arrays ( e.g: [ [1,2,3],[1,2],[3,5,1] ] )
							   or array of tuples ( e.g: [ (1,2,3),(1,2),(3,5,1) ] )
							   
		min_sup can be an int (absolute minimum support)
					or a float ( relative minimum support) - in this case,
							it will be converted to absolute support
							
		show_support is a boolean variable, and be set to False by default
		
		this will return A GENERATOR of (pattern, support)   if show_support == True
										 pattern             otherwise
		