## This is for excluding certain subsets of the data

b <- subset(b, !(FolSeg %in% c("apical")))
b <- subset(b, PreSeg != "/r/")
#b <- subset(b, !(Word == "kind" & FolWord == "of"))