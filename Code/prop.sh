# Initiation
 ncpu=$1 



../Code/get_geom.x t.0 #  reads in the geometries and places them inside a file called t.0 (t holds for trajectory)

 echo '$molecule' > f.inp # f.inp is the name of all the input files for qchem (f holds for forces)
 cat geom.in >> f.inp # copy the geometry into the qchem file
 echo '$end' >> f.inp
 cat sf_diis >> f.inp # cat means copy in bash and this just copies the template of a qchem submission
    echo 'CIS_N_ROOTS' 1 >>f.inp
    echo 'CIS_STATE_DERIV' 1 >>f.inp
    echo '$end' >>f.inp

    qchem -save -nt $ncpu f.inp f.out wf # submit the qchem job

    if ! grep -q "Calculating analytic gradient of the CIS energy" f.out; then # if the qchem job fails then resubmit under a different style
     echo '$molecule' >f.inp
     cat geom.in >>f.inp
     echo '$end' >>f.inp
     cat sf_gmd >>f.inp
     echo 'CIS_N_ROOTS' 1 >>f.inp
     echo 'CIS_STATE_DERIV' 1 >>f.inp
     echo '$end' >>f.inp

     qchem -save -nt $ncpu f.inp f.out wf # retry the submission
    fi
if ! grep -q "Calculating analytic gradient of the CIS energy" f.out; then # if both methods fail then just say error and call it quits
cat error >ERROR
pwd >>../ERROR
exit 1
fi
cat  f.out >>  f.all # copy over the output from qchem to a list that tracks all outputs.
../Code/q_to_prop.x >>t.0 # translates from angstroms to bohr or vice versa ? need to check again 

mv t.0 t.1 # renames t.0 to t.1 by literally moving the whole file and deletes the old one?
 cat t.1 > t1.all # copies the data from t.1 to an overall tracker file
 echo '---------------------------------------------------' >>t1.all # adds a separator



#Propagation
for i in {1..2500};do

 mv t.1 t.0 # rename the current t.1 to t.0 to begin to take a new timestep.

../Code/stop.x # option for restarting to ensure total time is not exceeded, makes a file called stop.

if [ -f stop ]; then
  break
fi




 ../Code/prop_prelim.x t # I don't yet know why this takes an input of t but i guess it gives an output of t.p?

 ../Code/get_geom.x t.p # translates units to bohr to be used with qchem. 

 echo '$molecule' > f.inp # Exact same qchem setup as before
 cat geom.in >> f.inp
 echo '$end' >> f.inp
 cat sf_diis >> f.inp
    if [ -d wf ]; then
      echo 'SCF_GUESS           Read' >>f.inp
    fi
    echo 'CIS_N_ROOTS' 1 >>f.inp
    echo 'CIS_STATE_DERIV' 1 >>f.inp
    echo '$end' >>f.inp

     qchem -save -nt $ncpu f.inp f.out wf 

    if ! grep -q "Calculating analytic gradient of the CIS energy" f.out; then
     echo '$molecule' >f.inp
     cat geom.in >>f.inp
     echo '$end' >>f.inp
     cat sf_gmd >>f.inp
     if [ -d wf ]; then
       echo 'SCF_GUESS           Read' >>f.inp 
     fi
     echo 'CIS_N_ROOTS' 1 >>f.inp
     echo 'CIS_STATE_DERIV' 1 >>f.inp
     echo '$end' >>f.inp

      qchem -save -nt $ncpu f.inp f.out wf
    fi
if ! grep -q "Calculating analytic gradient of the CIS energy" f.out; then
cat error >ERROR
pwd >>../ERROR
exit 1
fi



    cat  f.out >>  f.all # same tranfer as always



 ../Code/q_to_prop.x >>t.p # translates back to angstroms for nuclear dynamics
 ../Code/prop_corr.x t # recalculates the momentum using the forces from both sides of the timestep 
 cat t.1 >> t1.all #  tracking transfer
 echo '---------------------------------------------------' >>t1.all #  separator 
 cat t.te>>te.all #  energies stuff - maybe not important

if [ "$(head -1 t.1)" != "$(head -1 t.p)" ]; then # if a molecule is removed because the forces are removed but records when it happens.
  rm -r wf
  echo $i>>t.diss1
fi




done




