# Spam-Classifier

## INTRODUCTION

Chương trình phân loại tin nhắn là có phải là thư rác (spam) hay không với hai nhãn spam và ham bằng các mô hình học máy SVM, BNN, BACKPROPAGATION

## ACCURACY
| Text Preprocessing Type              | SVM                 | BAYESIAN BELIEF NETWORK  | BACKPROPAGATION      |
|--------------------------------------|---------------------|--------------------------|----------------------|
| Stemmer_countvectorizer              | 96.68%              | 97.30%                   | 98.47%               |
| Stemmer_tfidf                        | 98.65%              | 98.56%                   | 98.74%               | 
| Lemmatization_countvectorizer        | 98.56%              | 98.29%                   | 98.38%               |
| Lemmatization_tfidf                  | 96.41%              | 97.48%                   | 98.47%               |

## REQUIERMENTS
+ Flask
+ BeautyfulSoup
+ Joblib
+ requests
+ pandas
+ numpy

## DATASET
* Bộ dữ liệu train từ Kaggle: SMS Spam Collection là một tập hợp các tin nhắn được gắn thẻ SMS đã được thu thập để nghiên cứu SMS Spam. Nó chứa một bộ tin nhắn SMS bằng tiếng Anh gồm 5.574 tin nhắn, được gắn thẻ là ham (hợp pháp) hoặc spam. [link](https://www.kaggle.com/uciml/sms-spam-collection-dataset/download).
* Bộ dữ liệu test từ UCI Irvine mã 228
  
##  USAGE
1.Chạy app:
``` python serverNumber.py ```

2. http://127.0.0.1:5000
