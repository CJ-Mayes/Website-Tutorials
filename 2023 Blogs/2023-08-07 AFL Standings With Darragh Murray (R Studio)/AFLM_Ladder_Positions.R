# PREAMBLE -----

# This R script exists so we can determine the finishing position of each
# AFL team in each AFL season between 1990 and 2022.
#
# This script has been heavily OVER-COMMENTED as it is part of a basic tutorial
# on using the fitzRoy package and aimed at complete R newbies.

# PACKAGES -----

# R allows people to create and store useful and well-defined functions and 
# data in structures known as packages. We can install custom packages from a 
# variety of sources including the Comprehensive R Archive Network (or CRAN) or 
# packages built outside of CRAN (such as GitHub). Users typically only need to install
# a package once and then reference via a library call. They don't have to do this each time
# they run an R script.

# uncomment each line to install.

# install.packages("fitzRoy")
# install.packages("dplyr")

# LIBRARIES -----
# Packages are then stored in libraries. We load a package into our R session via making a call to the library. 

library("fitzRoy") # fitzRoy will do the heavy lifting when it comes to AFL stats
library("dplyr") # The ultimate data manipulation package!


# First step is that we'll create some empty data frames to store our afl season data.

all_afl_season = data.frame()
all_afl_grandfinal_results = data.frame()

# LOAD RELEVANT DATA FROM FITZROY() -----

# Next we'll create a loop between the seasons we're interested in - 1990 through to 2022

for (i in 1990:2022){
  
  # Retrieve the AFLladder from fitzRoy API for the end of the season/year 'i'
  # we use a handy fitzRoy function called 'fetch_ladder' to do this.
  
  afl_season <- fetch_ladder(season = i, source = "squiggle") %>%
    select(rank, name, pts, for., against, percentage) %>% #select relevant variables
    mutate(season = i) %>% # add the season/year variable into the dataset
    rename(ladder_finish = rank, team = name, points = pts, scores_for = for., 
           scores_against = against) # create nicer variable names
  
  # row bind (union) the afl data from season 'i' to the existing season data we've already stored
  all_afl_season <- rbind(all_afl_season, afl_season)
  
  # OK, we've got the final season ladders, but because AFL also has a final season, this
  # dataframe will not tell us the premiers (or those who won the 'flag').
  # However another handy fitzRoy function fetch_results_squiggle allows us to retrieve
  # match results and filter them for the 'grand final' for season/year 'i'
    
  afl_season_results <- fetch_results_squiggle(season = i, round_number = NULL) %>%
    # We have to specify the !is.na(winner) condition because the 2010 grand final ended 
    # in a draw and then was replayed.
    filter(is_grand_final == 1, !is.na(winner)) %>% 
    select(year, winner) %>%
    rename(season = year)
  
  # like before, we union the current grandfinal winner to existing list of winners.
  all_afl_grandfinal_results<- rbind(all_afl_grandfinal_results, afl_season_results) #row bind datasets together   
}

# DATA TRANSFORMATION/PREPARATION -----

# To get the data in the finalised format we want, we simply join the resultant data frames
# from the loop above - the final ladder positions + a 'premiership flag' boolean indicator
# to indicate which team ultimate won the premiership in the relevant season.

# Left join ladder results to premiership results
afl_ladder_with_flags <- left_join(all_afl_season, all_afl_grandfinal_results, by='season') %>%
  mutate(premiership_flag = ifelse(team == winner, TRUE, FALSE)) %>%  # use true false for winner variable rather than team name
  select(-winner) # do not need this field any more


# EXPORT DATA FOR ANALYIS IN TABLEAU -----

write.csv(afl_ladder_with_flags, "output/afl_ladder_with_flags.csv", row.names=FALSE)


# BONUS: PLOTTING IN R -----

# install the charting packages below if you don't already have them!
# install.packages("ggplot2")
# install.packages('devtools')
# devtools::install_github('bbc/bbplot') # install these BBC plot function from github cause they make a nicer plot than the default ggplot!

# Let's initialise these new packages!

library("ggplot2") # ggplot2 allows us to chart data
library("bbplot") # bbplot allows us a bit more functionality to pretty up our graphs BBC style!


# now we can chart using ggplot and facet_wrap by team (small multiples)
chart_seasons <- ggplot(all_afl_season, aes(x=season, y=ladder_finish, colour=team)) +
  labs(title="Pursuit of the Pennant", subtitle="AFL team ladder positions | 1990 - 2022") +
  geom_step() +
  facet_wrap(~team) +
  scale_y_reverse() +
  bbc_style() +
  theme(legend.position = "none") 

chart_seasons #output the seasons chart
  
