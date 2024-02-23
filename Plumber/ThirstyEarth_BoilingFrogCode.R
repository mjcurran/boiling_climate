################ Function for Boiling Frog Experiment ############################################################
#Lauren McGiven, February 2024

#This function is applied individually for a single player.

#rm(list=ls())  #clear environment
library(tidyverse)
library(ggplot2)

#######################################################################################################################################################################################
ThirstyEarth = function(round, crop, invest, minW, aF, max_income, WH, rain_mean, rain_var, dmean, dvar)
  
 #### Game Inputs #### UNCOMMENT TO TEST CODE, COMMENT TO RUN GAME ####
 ##Player game play inputs
 round = 1 #round number
 crop = 1  #player choice: 0 - fallow, 1 - crop
 invest = 0 #whether player has invested in the technology: 0 - no, 1 - yes
 
 ##Game design inputs
 #crop income parameters:
 minW = 50 #minimum water availability when the player has the technology 
 aF = 650 #fallow profit; equitable profit to W ~= 56
 max_income = 1000 #maximum possible profit per round
 WH = 30 #half-saturation  constant
 
 #climate distribution parameters:
 rain_mean = 85 #initial mean value for rainfall distribution 
 rain_var = 15 #initial variability of rainfall distribution 
 dvar = .40 #total % change in rainfall variability from round 1 to round 24 (implemented every 4 rounds)
 #different treatments affected by:
 dmean = .75 #total % change in rainfall mean from round 1 to round 24 (implemented every 4 rounds)
 
 #Initial Error Checks
 if (rain_mean == (rain_var+(rain_var*dvar))) stop('Minimum mean rainfall of 0 + maximum variability (no negative water)')
 if (minW<0) stop('Water availability cannot be negative')
 if (rain_mean<0) stop('Mean rainfall cannot be negative')
 
 
 #### CLIMATE CHANGE ####
 #start with same initial rainfall distribution mean and variance that change as the game progresses 
 
 if (round == 1 | round == 2 | round == 3 | round == 4 ) {
   rain_mean = rain_mean 
   rain_var = rain_var 
 }
 if (round == 5 | round == 6 | round == 7 | round == 8) {
   rain_mean = rain_mean - (rain_mean*(dmean*(1/5)))
   rain_var = rain_var + (rain_var*(dvar*(1/5)))
 }
 if (round == 9 | round == 10 | round == 11 | round == 12) {
   rain_mean = rain_mean - (rain_mean*(dmean*(2/5)))
   rain_var = rain_var + (rain_var*(dvar*(2/5)))
 }
 if (round == 13 | round == 14 | round == 15 | round == 16) {
   rain_mean = rain_mean - (rain_mean*(dmean*(3/5)))
   rain_var = rain_var + (rain_var*(dvar*(3/5)))
 }
 if (round == 17 | round == 18 | round == 19 | round == 20) {
   rain_mean = rain_mean - (rain_mean*(dmean*(4/5)))
   rain_var = rain_var + (rain_var*(dvar*(4/5)))
 }
 if (round == 21 | round == 22 | round == 23 | round == 24) {
   rain_mean = rain_mean - (rain_mean*(dmean))
   rain_var = rain_var + (rain_var*(dvar))
 }
 
 ##### WATER AVAILABILITY FROM RAINFALL DISTRIBUTION #####
 
 #convert mean and variance into gamma distribution scale and shape parameters
 theta = rain_var/rain_mean #gamma distribution scale parameter > 0; larger the scale parameter, more spread out distribution
 k = rain_mean/theta #gamma distribution shape parameter > 0
 
 #Water availability randomly drawn from rainfall distribution
 Water = rgamma(n=1, shape=k, scale=theta)  
 
 #whether player has opted into technology yet 
 W = -1 #initializing the variable with something illegal to ensure it gets replaced
 if (invest == 0) { #no technology
    W = Water 
 } else if (invest == 1) { #yes technology
    {if (Water < minW){ W = minW } #if water availability less than minimum set to minimum
      else if (Water >= minW) {W = Water}}
 }
 
 #checks
 if (theta <= 0) stop('Scale parameter cannot be below 0')
 if (k <= 0) stop('Shape parameter cannot be below 0')
 if (W < 0) stop('Water availability cannot be below 0')
 
 
 ##### PLAYER PROFITS #####
 #initializing the variables
 crop_income = 0
 fallow_income = 0

 if (crop == 0) {
   profit = aF #fallow annual profit
   fallow_income = aF
   crop_income = 0
 } else if (crop == 1) {
   crop_income = max_income*(W/(W+WH))
   profit = crop_income #crop annual profit
   fallow_income = 0
 }

 ############# SUMMARY DATA ##################
 
 summary = data.frame(W, crop_income, fallow_income, profit)
 names(summary)=c('Water Avail.', 'Crop Income', 'Fallow Income', 'Player Profit')

 summary
 
 
 
 
 #plot the rainfall gamma distribution
 x = seq(0,90,by=0.01)
 plot(x = x, y = dgamma(x, shape = k, scale = theta, log = FALSE), lwd = 1, xlab =('Water availability'), ylab =('Probability of W'))
 
 
 return(list(summary)) 
 
}



