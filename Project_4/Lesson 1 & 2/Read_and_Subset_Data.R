getwd()
setwd('~/Downloads')

statesInfo <- read.csv('stateData.csv')
# to view the dataframe
View(statesInfo)

# subset command pulls in specific views of the dataframe
stateSubset <- subset(statesInfo, state.region == 1)
head(stateSubset)

# another way to subset the dataframe is to use bracket notation
# to set conditions for data[ROWS, COLUMNS]
stateSubsetBracket <- statesInfo[statesInfo$state.region == 1, ]
head(stateSubsetBracket)