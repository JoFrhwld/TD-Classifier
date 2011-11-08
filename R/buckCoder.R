b <- read.delim("Data/new_buckeye.txt")

b$Gram <- "mono"
b[grep("ed$", b$Word),]$Gram <- "past"
b[grep("n't$", b$Word),]$Gram <- "nt"
b[b$Word == "and",]$Gram <- "and"



semiweakT <- c("bereft", "cleft", "crept","dealt", "dreamt","felt", "heard", "kept", "knelt", "leapt", "left","lent","lost","meant","spelt", "slept", "swept", "wept")
semiweakD <- c("sold","heard", "told")
stemchange <- c("bound", "found", "ground","held","wound")
justT <- c("bent", "built", "sent", "spent")
nochange <- c("burst", "cast","cost", "spilt")
went <- "went"

semiweakTend <- paste(semiweakT, "$", sep = "")
semiweakDend <- paste(semiweakD, "$", sep = "")
stemchangeend <- paste(stemchange, "$", sep = "")
justTend <- paste(justT, "$", sep = "")
nochangeend <- paste(nochange, "$", sep = "")
went <- paste(went, "$", sep = "")

irregulars <- list(semiweakT = semiweakTend,semiweakD = semiweakDend, stemchange = stemchangeend, justT = justTend, nochange = nochangeend, went = went)

for(class in names(irregulars)){
	members <- irregulars[[class]]
	for(word in members){
		if(length(grep(word, b$Word)) > 0){
			b[grep(word, b$Word),]$Gram <- class
		}
	}
}

library(plyr)

##cleaning up errors
words_in_class <- dlply(b, .(Gram), with, unique(as.character(Word)))

## justT errors
words_in_class$justT
b$Gram[b$Word %in% c("present", "consent", "absent", "represent", "misrepresent")] <- "m"

#SemiweakT errors
words_in_class$semiweakT
b$Gram[b$Word %in% c("excellent", "violent", "talent", "equivalent", "prevalent")] <- "m"

#stem change errors
words_in_class$stemchange
b$Gram[b$Word %in% c("playground", "background", "underground", "ground", "rebound")] <- "m"


b$Gram2 <- b$Gram
b$Gram2 <- gsub("semiweak.", "semiweak", b$Gram2)


b$PreSeg <- b$PreSegTrans
dput(levels(b$PreSeg))
## c("b", "ch", "el", "en", "er", "f", "g", "jh", "k", "l", "m", 
## "n", "p", "r", "s", "sh", "th", "vowel", "z")

levels(b$PreSeg) <- c("stop", "affricate", "/l/", "/n/", "/r/", "fricative", "stop", "affricate", "stop", "/l/", "/m/", 
"/n/", "stop", "/r/", "sibilant", "sibilant", "fricative", "fricative", "sibilant")

b$FolSeg <- b$FolSegTrans
dput(levels(b$FolSeg))
## c("aa", "ae", "ah", "aw", "ay", "b", "B", "ch", "d", "dh", "E", 
## "eh", "er", "ey", "f", "g", "hh", "ih", "iy", "jh", "k", "l", 
## "m", "n", "null", "ow", "p", "r", "s", "S", "sh", "t", "th", 
## "U", "v", "w", "y", "z")


levels(b$FolSeg) <- c("vowel", "vowel", "vowel", "vowel", "vowel", "stop", "B", "apical", "apical", "apical", "E", 
"vowel", "vowel", "vowel", "fricative", "stop", "/h/", "vowel", "vowel", "apical", "stop", "/l/", 
"/m/", "/n/", "null", "vowel", "stop", "/r/", "sibilant", "S", "sibilant", "apical", "apical", 
"U", "fricative", "/w/", "/y/", "sibilant")
b$FolSeg <-as.character(b$FolSeg)

b$FolSeg[b$FolWord == "<SIL>"] <- "pause"


b$DepVar <- "del"
b$DepVar[b$SegTrans %in% c("t","d","dx")] <- "ret"
b$DepVar[b$SegTrans %in% c("tq")] <- "glot"
b$DepVar[b$SegTrans %in% c("ch","jh") & b$PreSegTrans %in% c("ch","jh")] <- "palat"


b$td <- (b$DepVar != "del") * 1




