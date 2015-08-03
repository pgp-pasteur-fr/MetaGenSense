Add  input data in the Exchange project directory
-------------------------------------------------

At first, MetaGenSense directory (called MGS) needs to be created in the user's Galaxy import directory (“links/’yourLogin’/MGS”). When created, the user must create in it, a folder named as the project to store input raw data that will be analyzed. This way, Galaxy will be able to copy those files within the user’s library and then to a history, just before the workflow execution.

This step is the only one, not automated at all. Indeed, the user will need to do those steps manually. To be clear, here are the steps to follow:

1. Go to your Galaxy transfert directory: /links/’*yourLogin*’

2. Create a directory called MGS, if it doesn’t exist.

3. Create in MGS, a sub-directory named like the project (respect even the case).

4. Copy the file(s) to analyse in the sub-directory

Example with user Jake Sully and the project named PanDora:
---------------------------
.. code-block:: shell

  # go in the galaxy transfer directory:
  cd galaxy/links/jsully/
  #Create the MGS directory:
  mkdir MGS
  #Create the project directory:
  mkdir MGS/PanDora
  cd MGS/PanDora

Copy a fastq file(s) to the project directory::

  cp path/to/myfile.fastq .    

Remark: This task is the only one which needs to be made outside MetaGenSense.


