#https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html

from numpy import array, arange, maximum, matrix, clip, asarray, zeros, append, concatenate, amax, full
from skfuzzy import trimf, trapmf, interp_membership, defuzz
import skfuzzy.control


from matplotlib.pyplot import plot, show, subplots, axis, pause, fill_between, grid, annotate, xlabel, ylabel
from matplotlib.axes import *


#input_size: amount of inputs
#inputs: array of inputs
#input_domain: array of arrays representing the domain (the x axis) of each input
#output_domain: array representing the domain (the x axis) of the output
#input_membership: array of membership arrays (order must match with inputs)
#output_mempership: membership arrays of output
#fam_table: matrix i_1 \times ... \times i_n relating each combination of inputs with an output
def control_signal(input_size, inputs, input_domain, output_domain, input_membership, output_membership, fam_table):
   membership_results = [] #array to record the membership of the i^{th} input in each set
   for i in range(0,input_size): #for each input...
      x = input_domain[i]
      mFunction = input_membership[i] 
      membership_results_temp = [] #array to record the membership of the i^{th} input in each set
      for m in mFunction: #for each membership function of the i^{th} input...
         membership_results_temp.append(interp_membership(x,m,inputs[i]))
      membership_results.append(membership_results_temp) 
   #Uncomment below to print the membership of the inputs
   #print("Membership results: ", membership_results) #membership of all the inputs   

   #definir a intersecção entre todas as variáveis
   output = zeros(len(output_membership)) #array to store the output
   for i in fam_table: #para cada registro na tabela
      lower = 1 #"lower" stores the lowest element
      for j in range(0,len(i)-1): #traverse each line in the table until the last but one element  - kind of an "and" operation among every elements
         if membership_results[j][i[j]] < lower:
            lower = membership_results[j][i[j]]           
      if lower > output[i[len(i)-1]]:
         output[i[len(i)-1]] = lower   
   #At this point, "output" stores the union of the result of all the "and" operations between the variables
   #print("Output: ", output)   

   #defuzzyfication 
   #pegar cada conjunto fuzzy de saída e limitá-lo pelo grau de pertinência obtido nos cálculos acima
   output_union = zeros(len(output_membership[0]))
   for i in range(0,len(output_membership)):
      output_union = maximum(output_union, clip(output_membership[i],0,output[i]))        
      #uncomment next 12 lines to plot the union of the outputs
      #if amax(output_union)<1 and amax(output_union)>0:
      #   plot(output_domain,full(len(output_domain),amax(output_union)),linestyle=':',linewidth=2)  
   #plot(output_domain,output_union)
   #fill_between(output_domain,0,output_union)
   #grid(True)
   #annotate('(6,0.6)', (6,0.6), xytext=(7,0.7),arrowprops=dict(arrowstyle="->"),ha='center') # horizontal alignment can be left, right or center
   #annotate('(14,0.6)', (14,0.6), xytext=(15,0.7),arrowprops=dict(arrowstyle="->"),ha='center') # horizontal alignment can be left, right or center
   #centroid = defuzz(output_domain,output_union,'centroid')
   #annotate('centroid = ' +   "%.4f" % centroid, (centroid,0.0), xytext=(centroid+2,0.05),arrowprops=dict(arrowstyle="->"),ha='center') # horizontal alignment can be left, right or center
   #xlabel('Force (lb)')
   #ylabel('Membership')
   #show()
   
   if sum(output_union) != 0: #if there is area to calculate centroid
      return defuzz(output_domain,output_union,'centroid')
   else: 
      return  0
   


###############



