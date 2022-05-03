setwd("C:/Users/yzz07/Desktop/DATA")

library(KoNLP)
library(stringr)
library(wordcloud)
useNIADic()


# 사전 추가
mergeUserDic(data.frame(readLines("ytube_dic.txt"), "ncn"))


# 형태소 분석
ytube <- readLines("youtube_all.txt", encoding = "UTF-8")
head(ytube, 5)
ytube_2 <- unique(ytube)
ytube_ext <- extractNoun(ytube_2)
ytube_ext_2 <- lapply(ytube_ext, unique)


# 불용어 제거
cdata <- unlist(ytube_ext_2)
ytube_un <- str_replace_all(cdata, "[^[:alpha:][:blank:][0-9]]", "")

wordcount <- table(unlist(ytube_un))
head(sort(wordcount, decreasing = T), 10)

ytube_un <- gsub("VLOG", "브이로그", ytube_un)
ytube_un <- gsub("vlog", "브이로그", ytube_un)
ytube_un <- gsub("Vlog", "브이로그", ytube_un)

# 불용어 사전
txt_gsub <- readLines("ytube_gsub.txt", encoding = "UTF-8")
(cnt_gsub <- length(txt_gsub))
for (i in 1:cnt_gsub) {
    ytube_un <- gsub((txt_gsub[i]), "", ytube_un)
}


# 글자수로 제거
ytube_un <- Filter(function(x) {
    nchar(x) >= 2 & nchar(x) <= 15
}, ytube_un)


# 확인
wordcount <- table(ytube_un)
head(sort(wordcount, decreasing = T), 100)


###

wordcount2 <- head(sort(wordcount, decreasing = T), 300)
palete <- brewer.pal(7, "Set1")
wordcloud(names(wordcount2),
    freq = wordcount2, scale = c(5, 1), rot.per = 0.25, min.freq = 4,
    random.order = F, random.color = T, colors = palete
)


#