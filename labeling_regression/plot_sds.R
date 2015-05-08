library(ggplot2)

sds <- read.csv('mn_sds.csv', header=FALSE, row.names=1)[, 1]
ggplot(data.frame(sds=sds), aes(sds)) + geom_histogram(binwidth=0.23, col="#2c3e50", fill="#2980b9", alpha = .2) + ggtitle('Ranking Standard Deviations for Candidate Mnemonics (0-10)')
ggsave(file='mn_votes_sds.png', width=10, height=4)