# Packages

Here are the test packages for the Rion Client. The content and everything else in connection with the packages is freely invented and is in no conflict with preexisting licenses. 

# Syntax 
## Overview
Basically, we do not care what is in the packages. The main thing is that there is a ``deps.txt`` file.

Here is an overview from a sample package. 

```
packages
|
+---buddy
|       cute.modul
|       deps.txt
|       love.modul
|
+---futternapf
|       bestnapfever.napf
|       deps.txt
|       futternapf3000.napf
...
```
## Build
The packages are simply formed using the "tar" command. Alternatively, you can also use the script for this. [Script](/package/extract/makepacs.sh)
```shell
tar czvf buddy-v100_0_3.tar.gz buddy/
```

## Dependencies
The dependencies list is kept pretty close to pythons pip requirements. 
Strictly speaking it is just a txt list with all values. These can be refined by operators. 

### Example
```txt
katzenfutter>=43
```

### Flags
The separation operator is a =.  Nevertheless, there are other options.

- hallo==0.1: The package hallo version 0.1 is installed.
- hallo>=:0.1 The package hallo with the minimum version 0.1 is installed.
- hallo: The latest version of the hallo package is installed.  
