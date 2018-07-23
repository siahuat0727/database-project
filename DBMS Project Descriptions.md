# DBMS Project Descriptions

## 系統架構與環境

### Ubuntu 17.10 + Python3.6.3 + mysql 5.7.22

![](https://i.imgur.com/6fhRD6W.png)

## 介面截圖與使用說明

提供 button 及 query 兩種操作界面，button 爲一些經過設計的功能，query 則可以按 mysql 的查詢方式進行查詢。
慾使用 query 進行查詢時，必須先將 tool 選擇爲 mysql

### 起始畫面

![](https://i.imgur.com/WxDZ73A.png)

### Button 功能

![](https://i.imgur.com/AgaTwtT.png)

### Query 查詢

![](https://i.imgur.com/MzozBJO.png)

## ER Diagram

![](https://i.imgur.com/jiVKPFX.png)

## Relation Schema

![](https://i.imgur.com/LulzI40.png)

## Project 簡介
一個 server 遍佈全球各地的大遊戲平臺爲了方便管理玩家資訊及伺服器維護人員聯絡資訊而設計的資料庫系統。

## Table 簡介
+ players - 記錄每個玩家的資訊
    + id - DB key constraint
    + name - 玩家名字(在遊戲中顯示)
    + age - 玩家年齡（限制遊戲類型）
    + sex - 性別（後續分析）
+ games - 記錄遊戲資訊
    + id - DB key constraint
    + name - 遊戲名字
    + develop year - 記錄開發年份
+ servers - 伺服器（玩家在玩該遊戲時使用的伺服器，不同伺服器可能有不同特性）
    + id - DB key constraint
    + name - server 名稱
    + location - server 地點，當發生問題時有助於知道該聯絡哪裡的工作人員維修
+ employees - server 維護人員，負責不定時維護系統
    + id - DB key constraint
    + name - server 名稱
    + phone - 電話號碼，方便聯絡
+ publisher - 遊戲開發商
    + id - DB key constraint
    + name - 公司名稱
    + num_employee - 該公司的員工數量

![](https://i.imgur.com/HxXmFEA.png)

## Relationship 簡介

+ play - 記錄玩家在玩哪個遊戲時登錄哪個 server
+ closed_play - 記錄遊戲的內測玩家
+ publish - 記錄遊戲由哪家公司開發
+ maintain - 記錄哪些 server 由哪些工程師維護

![](https://i.imgur.com/G2hhr9Q.png)