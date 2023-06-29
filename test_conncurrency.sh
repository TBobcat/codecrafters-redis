#!/bin/bash
# Our custom function
cust_func(){
  x=1; while  [ $x -le 10 ]; do echo $i &&  redis-cli ping  $(( x++ )); done
}
# For loop 5 times
for i in {1..5}
do
	cust_func $i & # Put a function in the background
done
 
## Put all cust_func in the background and bash 
## would wait until those are completed 
## before displaying all done message
wait 
echo "All done"
