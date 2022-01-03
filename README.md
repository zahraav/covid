SARS-COVID-2

Setup/Execution:
 - Clone the git repository 
`  https://github.com/zahraav/covid.git`


Install libraries/packages:
 - install [biopython](https://biopython.org/wiki/Download):
   `pip install biopython`
 
 - install [pillow]():
   python3 -m pip install --upgrade pip
   python3 -m pip install --upgrade Pillow
 
 
Configure your config.cfg file

- There are some lines on the configuration file which are comments, 
   for using the pipeline on testing dataset it's better to put your data on test folders and comment the real files with same name.


input

   Put your input files on the related folder on
`files/input`


 - Execute pipeline
    from main folder of project in command prompt run this command:
    `python .\src\run.py`

 
**Result**:
you can find the result related to part of project that you run in the related folder in 
`files/output`  
