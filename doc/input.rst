Add  input data in the Exchange project directory
-------------------------------------------------

At first, MetaGenSense directory (here called MGS) needs to be created in Galaxy import directory. The user must create in his MetaGenSense directory (“links/’yourLogin’/MGS”) a folder named as the project to store input data that will be analyzed. This way, Galaxy will be able to copy the files to analyse within the user’s library, just before the analysis will start.
This step is the only one, not automated at all. Indeed, the user will need to do those steps manually. To be clear, here are the steps to follow:

1. Go to your Galaxy transfert directory: /links/’*yourLogin*’

2. Create a directory called MGS, if it doesn’t exist.

3. Create in MGS, a sub-directory named like the projec (same case).

4. Copy the file to analyse in the sub-directory

Example with user Jake Sully and the project named PanDora:
---------------------------
::

  # go in the galaxy transfer directory:
  cd galaxy/links/jake.sully/
  #Create the MGS directory:
  mkdir MGS
  #Create the project directory:
  mkdir MGS/PanDora
  cd MGS/PanDora

Copy a fastq file to the project directory::

  cp path/to/myfile.fastq monfichier.fastq   

Remark: This is the only task which needs to be made outside MetaGenSense interface, the rest can be followed on the Galaxy instance but is executed from MetaGenSense.


