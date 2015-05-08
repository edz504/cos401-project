

df <- read.delim('results.txt', row.names=1, header=FALSE)
colnames(df) <- c('sem_dist', 'fam', 'image', 'concr', 'syll', 'logfreq', 'aoa', 'ph1', 'ph2')
df.scale <- data.frame(scale(df))
df.scale$y <- read.csv('borda_y.csv', header=FALSE, row.names=1)[, 1]

### ANOVA
anova.fit <- aov(y ~ ., data=df.scale)
summary(anova.fit)

### stepwise regression
lm.fit.null <- lm(y ~ 1, data=df.scale)
lm.fit.full <- lm(y ~ ., data=df.scale)
stepreg <- step(lm.fit.null, scope=list(upper=lm.fit.full), direction="both")

### Feature importance
library(mlbench)
library(caret)
control <- trainControl(method="repeatedcv", number=10, repeats=5)

# Linear regression
model1 <- train(y~., data=df.scale, method="lm", trControl=control)
imp1 <- varImp(model1, scale=FALSE)
print(imp1)
plot(imp1)
