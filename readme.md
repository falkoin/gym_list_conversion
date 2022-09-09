# Convert gymnastic result books to csv data

### Short description

A little script to convert trampolin result books to csv data tables.  
In trampolin sports results are reported through a result book. These can be found at [gymnastik.sport](https://www.gymnastics.sport/site/events/searchresults.php) or [europeangymnastics.com](https://www.europeangymnastics.com/events)

### Step by step  

- Download result book
- Find corresponding pages of event phase (e. g. qualification, final) and group (women, men)
- Edit data.csv
	- Association corresponds is dependant of where you got the resultbook from (the example above is world)
	- Event Phase is either qual, semi or final (qual has two routines, semi has one routine and a qualified column, final only has one routine and final ranks)
	- Ouput is the filename of the output table file
	- Input is the filename of the result book
	- First corresponds to the first page of the resultlist
	- Last corresponds to the last page of the resultlist (if there is only one page this is equal to first)
- Run full_processing.py

### Procedure	

The script will convert the PDF pages to a single txt file per entry in data.csv, which is then converted to a csv table containing the data.

### Dependencies

Python 3 with NumPy, Pandas  
Ghostscript available through shell