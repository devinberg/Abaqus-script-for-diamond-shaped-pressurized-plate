# READ OUTPUT FROM ODB RESULTS FILES
import odbAccess

maxStress=[] # Initialize the variable of interest.
for j in range(1):  # Just need to edit this with actual number of Job output files.
    jindex=j+1  # Adjust index to match job name convention used in parametric study.
    jobname='Job-%s.odb' %jindex
    stressField=session.openOdb(name=jobname).steps['Step-1'].frames[-1].fieldOutputs['S'] # Define path to stored data.
    stressVector=[] # Initialize a temporary variable.
    for i in range(len(stressField.values)): # Loop through all the elements in the model.
        vonMises=stressField.values[i].mises # Extract variable of interest (von Mises stress in this case).
        stressVector.insert(i,vonMises) # Put that variable in a the temporary list.
    maxS=max(stressVector) # Looking for max value in this case.
    maxStress.insert(jindex,maxS) # Store that max value in a list.
# end for loop

output=file('/some/path/Results.txt','w') # Once all of the job files are processed, write max stress list to text file.
for item in maxStress:
    print>>output, item
# end output for loop
output.close() # Close the text file.
