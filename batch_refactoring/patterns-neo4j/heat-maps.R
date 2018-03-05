library(ggplot2) 

plotBatchNegative = function(csv_file, out_file) {
  patterns = read.csv(csv_file, sep=";")  
  p = qplot(y=smell, x=batch, data=patterns, fill=percentage, geom="tile", 
            , label=paste0(round(patterns$percentage, 1),"%")) + geom_text()
  
  p + theme_minimal(base_size=14) + theme(axis.title.x=element_blank(),
                                          axis.title.y=element_blank(),
                                          axis.text.x = element_text(angle = 45, hjust = 1)) + scale_fill_gradient2(limits=c(0, 100), mid="yellow", high="red") 
  ggsave(file=out_file, width = 70, limitsize=FALSE)
  
}

plotBatchPositive = function(csv_file, out_file) {
  patterns = read.csv(csv_file)  
  p = qplot(y=smell, x=batch, data=patterns, fill=percentage, geom="tile", 
            , label=paste0(round(patterns$percentage, 1),"%")) + geom_text()
  
  p + theme_minimal(base_size=14) + theme(axis.title.x=element_blank(),
                                          axis.title.y=element_blank(),
                                          axis.text.x = element_text(angle = 45, hjust = 1)) + scale_fill_gradient2(limits=c(0, 100), mid="yellow", high="dark green") 
  #ggsave(file="/Users/diego/selected-patterns.png",  width=7.5, height=2)
  ggsave(file=out_file, width = 70, limitsize=FALSE)
}

plotAllHeatMaps = function() {
  outdir = "/Users/diego/PycharmProjects/scripts_cedrim/batch_refactoring/patterns-neo4j/plots/"
  indir = "/Users/diego/PycharmProjects/scripts_cedrim/batch_refactoring/patterns-neo4j/summaries/"
  for (filename in list.files(indir)) {
    outfile = paste(outdir, substr(filename, 0, nchar(filename) - 4), ".pdf", sep = "")
    infile = paste(indir, filename, sep = "") 
    if (length(grep("introduced", filename)) > 0) {
      #print(paste(outfile, "introduced"))
      plotBatchNegative(infile, outfile)
    } else {
      #print(paste(outfile, "removed"))
      plotBatchPositive(infile, outfile)
    }
  }
}