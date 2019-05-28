# Finding all the distinct words
uniqueWords <- unique(all2$Words, ,encoding="UTF-8")
write.csv(uniqueWords, file ="distinctwords.csv", row.names=FALSE)

# Most popular words in the whole database
mostPopularWords <- subset(all2, select = c("Words", "Usage"))
mostPopularWords <- aggregate(. ~ Words, data=mostPopularWords, FUN=sum)
mostPopularWords <- mostPopularWords[order(-mostPopularWords$Usage),]
write.csv(mostPopularWords, file ="mostpopularwords.csv", row.names=FALSE)
#edited later in python
library(readr)
MostCommonWords <- read_csv("MostCommonWords.csv")
top20 <- head(MostCommonWords, 20)
write.csv(top20, file ="top20.csv", row.names=FALSE)

# Sorting
sorting <- all2[all2[,"Ratio"]=="1",] 
sorting

# Distinct words to only <5 communities
cVals <- data.frame(table(all2$Words))
Rows <- all2$Words %in% cVals[cVals$Freq < 5,1]
wordsInOnlyLessThan5Communities <- all2[Rows,]
wordsInOnlyLessThan5Communities <- wordsInOnlyLessThan5Communities[order(-wordsInOnlyLessThan5Communities$"Total Usage"),]
wordsInOnlyLessThan5Communities <- subset(wordsInOnlyLessThan5Communities, as.numeric(wordsInOnlyLessThan5Communities$Ratio)>0.8)
wordsInOnlyLessThan5Communities <- subset(wordsInOnlyLessThan5Communities, wordsInOnlyLessThan5Communities$Subreddits!=c("PewdiepieSubmissions"))
headWordsInOnlyLessThan5Communities <- head(wordsInOnlyLessThan5Communities, 500)
aggregatevalue<-aggregate(. ~ Subreddits, data = headWordsInOnlyLessThan5Communities, FUN = function(x){NROW(x)})
aggregatevalue<-subset(aggregatevalue, select = c("Subreddits", "Words"))
aggregatevalue<-aggregatevalue[order(-aggregatevalue$Words),]
others <-aggregatevalue[as.numeric(aggregatevalue$"Words")<10,]
others <- sum(others$Words)
aggregatevalue <-aggregatevalue[as.numeric(aggregatevalue$"Words")>=10,]
aggregatevalue[nrow(aggregateValue),] = list("other",others)
headWordsInOnlyLessThan5Communities <- head(wordsInOnlyLessThan5Communities, 20)
write.csv(headWordsInOnlyLessThan5Communities, file ="top20Distinct.csv", row.names=FALSE)
write.csv(aggregatevalue, file ="top500aggregate.csv", row.names=FALSE)

# Distinct words by highest ratio coefficients for one community
distinctValues <- data.frame(all2$Ratio) 
Rows2 <- as.numeric(all2$Ratio) %in% distinctValues[distinctValues >= 0.93]
wordsInOnlyLessThan4CommunitiesAndPoint88Ratio <- all2[Rows2,]$Words
abc <- all2[is.element(all2$Words,wordsInOnlyLessThan4CommunitiesAndPoint88Ratio),]
abc <- abc[order(-abc$"Total Usage"),]
abc <- subset(abc, select = c("Words", "Usage"))
abc <- aggregate(. ~ Words, data=abc, FUN=sum)
#

# Measuring swear words
df <- data.frame(x = character(), y = numeric())
names(df) <-c("swear word", "usage")
for (word in c("arse",
               "ass",
               "asshole",
               "bastard",
               "bitch",
               "bollocks",
               "crap",
               "cunt",
               "damn",
               "dyke",
               "fag",
               "faggot",
               "fuck",
               "hell",
               "motherfucker",
               "nigga",
               "nigger",
               "prick",
               "shit",
               "slut",
               "sonofabitch",
               "thot")){
  temp <- sum(all2[all2[, "Words"]==word,]$Usage)
  df <- rbind(df, data.frame(x = word, y = temp))
}
df
write.csv(df, file ="swearwords.csv", row.names=FALSE)

# Submission Times
temp = list.files(pattern="*.csv")
myfiles = do.call(rbind, lapply(temp, function(x) read.csv(x, stringsAsFactors = FALSE)))
daysandtimes <- aggregate(. ~ hour+weekday, data=myfiles, FUN=sum)
times <- aggregate(. ~ hour, data=daysandtimes, FUN=sum)
times <- subset(times, select = -c(weekday) )
timesblocks4hours <- rowsum(times, (1:nrow(times) - 1) %/% 4)
timesblocks4hours$hour <- c("0:00-3:59", "4:00-7:59", "8:00-11:59", "12:00-15:59", "16:00-19:59", "20:00-23:59")
write.csv(timesblocks4hours, file ="timesblocks4hours.csv", row.names=FALSE)

# Emotions on Subreddits
mean_sentiments <- read_csv("mean_sentiments.csv")
mean_emotions <- aggregate(. ~ weekday, data=mean_sentiments, mean)
mean_emotions <- aggregate(. ~ hour, data=mean_emotions, mean)
mean_emotions$hour = NULL

mean_emotions <- as.data.frame(t(mean_emotions[,-1]))
colnames(mean_emotions) <- "Positivity Factor"
mean_emotions[sapply(mean_emotions, is.numeric)]  <- mean_emotions[sapply(mean_emotions, is.numeric)] * -1
mean_emotions <- as.data.frame(mean_emotions)
mean_emotions$"Subreddit Names" <- rownames(mean_emotions)
mean_emotions <- mean_emotions[order(-mean_emotions$"Positivity Factor"),]
mean_emotions <- mean_emotions[,c(2, 1)]
mean_emotions
write.csv(mean_emotions, file ="meanemotions.csv", row.names=FALSE)

# Submission Days
days <- aggregate(. ~ weekday, data=daysandtimes, FUN=sum)
days <- subset(days, select = -c(hour) )
days$weekday <- c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
write.csv(days, file ="timesblocksdays.csv", row.names=FALSE)

# Hillary Clinton vs Donald Trump
clinton <- read_csv("clinton_be_2.csv")
trump <- read_csv("trump_be_2.csv")
clinton <- clinton[order(-clinton$count),]
trump <- trump[order(-trump$count),]

# Want to
want_to <- read_csv("want_to_2.csv")
want_to <- head(want_to[order(-want_to$count),], 20)
write.csv(want_to, file ="wantto.csv", row.names=FALSE)

# Feelings
feel <- read_csv("feel_1.csv")
feel <- feel[order(-feel$count),]
test_strings <- c("bad", "well", "good", "guilty", "sorry", "comfortable", "great", "pretty", "sad", "old", "weird", "depressed")
feel <- feel[feel$followup %in% test_strings,]
write.csv(feel, file ="feel.csv", row.names=FALSE)
