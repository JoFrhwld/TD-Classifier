## exclude preceding /r/

b <- subset(b, PreSeg != "/r/")
b <- subset(b, !(FolSeg %in% c("apical","B", "E","null","S","U")))
b <- subset(b, !Word %in% c("and","just","didn't"))


