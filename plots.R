library(ggplot2)

labels_by_ref_type = function() {
  bows = read.csv("/Users/diego/PycharmProjects/issues_ref_base/data/labels_ret_types.csv", sep=",")
  p = qplot(x=refactoring, y=label, data=bows, fill=count, geom="tile", label=count) + geom_text() 
  #my_breaks = c(2, 10, 50, 250, 1250, 6000)
  p + theme_minimal(base_size=12) + scale_fill_gradient2(trans = "log", mid="yellow", high="red")
  ggsave(file="/Users/diego/PycharmProjects/issues_ref_base/data/labels_by_ref_type.png",  width=15, height = 10, limitsize=FALSE)
}

labels_by_ref_class = function() {
  bows = read.csv("/Users/diego/PycharmProjects/issues_ref_base/data/labels_by_ref_class.csv", sep=",")
  p = qplot(x=refactoring, y=label, data=bows, fill=count, geom="tile", label=count) + geom_text() 
  #my_breaks = c(2, 10, 50, 250, 1250, 6000)
  p + theme_minimal(base_size=12) + scale_fill_gradient2(trans = "log", mid="yellow", high="red")
  ggsave(file="/Users/diego/PycharmProjects/issues_ref_base/data/labels_by_ref_class.png",  width=5, height = 10, limitsize=FALSE)
}