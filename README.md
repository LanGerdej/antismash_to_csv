I made this simple script, in a bit of a rush, to summarize a large number of antismash results and store them in a single CSV spreadsheet.

How to use:

1. If you haven't yet installed beautifulsoup4 and pandas, you can do that in your terminal by running: pip install beautifulsoup4 pandas

2. Click on "Code" button in the upper right corner of this github page, click "download zip" and save into a desired directory.

3. Extract downloaded file.

4. Give file execute permissions by opening your terminal and running: chmod +x "path to extracted antismash_to_csv.py file"

5. Run the script by running: "path to the extracted antismash_to_csv.py file" -in "path to the directory containing multiple (exclusively) antismash output files" -out "desired existing output directory" -name "desired name of .csv output file"

Output is a CSV spreadsheet containing metabolite, region and known similar cluster information for each genome analyzed with antismash. If you need help you can use "--help" flag
