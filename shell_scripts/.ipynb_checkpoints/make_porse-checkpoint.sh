posre_name=posre_DNA
cat ${posre_name}.itp | sed 's/1000  1000  1000/100  100  100/g' > ${posre_name}_100.itp
cat ${posre_name}.itp | sed 's/1000  1000  1000/1  1  1/g' > ${posre_name}_1.itp
posre_name=posre_DNA2
cat ${posre_name}.itp | sed 's/1000  1000  1000/100  100  100/g' > ${posre_name}_100.itp
cat ${posre_name}.itp | sed 's/1000  1000  1000/1  1  1/g' > ${posre_name}_1.itp