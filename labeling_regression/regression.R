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

# Linear regression
control <- trainControl(method="repeatedcv", number=20, repeats=10)
model1 <- train(y~., df.scale, method="lm", trControl=control)
imp1 <- varImp(model1, scale=FALSE)
print(imp1)
plot(imp1)

# partial least squares
model1 <- train(y~., df.scale, method="kernelpls", trControl=control)
imp1 <- varImp(model1, scale=FALSE)
print(imp1)
plot(imp1)

fit.final <- lm(y ~ fam + syll + aoa + ph2, data=df.scale)