High-Level Synthesis - EE677 Course Project
By:
	OV Shashank		: shashankov[at]ee.iitb.ac.in
	Yogesh Mahajan	: y.mahajan456[at]gmail.com
	Avineil Jain	: avineil96[at]gmail.com
	
Contents:
	binding.py				: The code that contains the binding and scheduling 
							  (hereafter refered to as b and s) algorithm
	gen_binding_text.py		: The code that prints the b and s result in a plain text format
	generate_vhdl.py		: The code that contains the function to generate the VHDL Code
	infix2postfix.py		: Infix to Postfix Expression Converter
	plot_tree.py			: Used to create the dot files and the respective images
	postfix2bdt.py			: Postfix Expression to Binary Tree Converter
	README.txt				: You're reading this and from the previous README you know what this is all about
	stack.py				: An OOP implementation of a stack. Totally redundant but still retained
	vhdl.py					: OOP Classes for the VHDL Generation
	vlsi_2.0.py				: The MAIN EXECUTABLE CODE that runs the GUI and calls all of the above functions
	
Executing Instructions:
	For WINDOWS		: A direct ".exe" is available though Graphviz would still be required but 
					  due to its large size it is not inclulded in this distribution
	For Ubuntu		: Due to paucity of time a direct executable is unavailable
					  Though if all the dependencies are installed the code can be run by
					  executing in Python 3.5 the vlsi_2.0.py code as follows:
					  python3 vlsi_2.0.py
