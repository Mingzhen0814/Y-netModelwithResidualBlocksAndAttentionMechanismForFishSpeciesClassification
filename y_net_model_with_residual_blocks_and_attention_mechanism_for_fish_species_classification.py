# -*- coding: utf-8 -*-
"""Y-net Model with Residual Blocks and Attention Mechanism for Fish Species Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Rhdj1UtaWAon6113POmyAr8P73fSkJ28

# 圖像標籤


*   0：康德鋸鱗魚Myripristis kuntee(450)-fish_07、mask_07
*   1：摩鹿加雀鯛Pomacentrus moluccensis(181)-fish_13、mask_13
*   2：黑緣擬金眼雕Pempheris vanicolensis(29)-fish_19、mask_19

數據來源：Fish4Knowledge

https://homepages.inf.ed.ac.uk/rbf/Fish4Knowledge/GROUNDTRUTH/RECOG/

# 1.匯入資料

## 1.1 連接google雲端硬碟
"""

!pip install scikit-learn

import os
from google.colab import drive
drive.mount('/content/gdrive/')  #掛載Google雲端硬碟

"""## 1.2 載入相關套件"""

import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
import cv2

"""## 1.3 設定檔案路徑"""

data_file = '/content/gdrive/My Drive/final_project/'
image_file = data_file + 'image/'
mask_file = data_file + 'mask/'

zero_img_file = image_file + 'fish_07/'
one_img_file = image_file + 'fish_13/'
two_img_file = image_file + 'fish_19/'

zero_mask_file = mask_file + 'mask_07/'
one_mask_file = mask_file + 'mask_13/'
two_mask_file = mask_file + 'mask_19/'

"""## 1.4 檢視圖像與遮罩的配對"""

# 確認圖像與遮罩配對
data_name = "_50.png" # 手動改圖像檔名
img_path = os.path.join(zero_img_file + str("fish") + data_name) # 設定圖檔路徑
img = cv2.imread(img_path)
img = cv2.resize(img, (64,64))
mask_path = os.path.join(zero_mask_file + str("mask") + data_name)
mask = cv2.imread(mask_path)
mask = cv2.resize(mask, (64,64))
plt.figure(figsize=(5, 8))
plt.subplot(1, 2, 1) # (rows, columns, index)
plt.imshow(cv2.cvtColor (img, cv2.COLOR_BGR2RGB))
plt.subplot(1, 2, 2)
plt.imshow(mask)

"""# 2.讀入資料

## 2.1 讀入image與相對的mask
"""

import numpy as np
import tensorflow as tf
def load_data(folder, image):
  File_List = os.listdir(folder)
  File_List.sort(key = str.lower)
  for filename in File_List:
    img = tf.keras.preprocessing.image.load_img(folder + filename,
        target_size = (64,64)) # 將照片讀進filename並將圖片大小正規化
    img_resize = np.array(img)
    image.append(img_resize)

"""## 2.2 建立標籤

### 康德鋸鱗魚(450)->label:0
"""

# 匯入康德鋸鱗魚(450)圖像資料夾的圖片->label:0
zeroimg = []
load_data(zero_img_file, zeroimg)
zeroimg = np.array(zeroimg)
print('Shape of Myripristis kuntee Images:', zeroimg.shape)
# Shape of Myripristis kuntee Images: (450, 64, 64, 3) # (張數,長,寬,RGB)
zeromask = []
load_data(zero_mask_file, zeromask)
zeromask = np.array(zeromask)
print('Shape of Myripristis kuntee Images:', zeromask.shape)
# Shape of Myripristis kuntee Images: (450, 64, 64, 3) # (張數,長,寬,RGB)
zero_label = np.zeros(zeroimg.shape[0]) # 建立450張正常的圖像標籤為0
print(zero_label)
zero_label = np.reshape(zero_label, (zero_label.shape[0], 1))

"""### 摩鹿加雀鯛(181)->label:1"""

# 匯入摩鹿加雀鯛(181)圖像資料夾的圖片->label:1
oneimg = []
load_data(one_img_file, oneimg)
oneimg = np.array(oneimg)
print('Shape of Pomacentrus moluccensis Images:', oneimg.shape)
# Shape of Pomacentrus moluccensis Images: (181, 64, 64, 3) # (張數,長,寬,RGB)
onemask = []
load_data(one_mask_file, onemask)
onemask = np.array(onemask)
print('Shape of Pomacentrus moluccensis Images:', onemask.shape)
# Shape of Pomacentrus moluccensis Images: (181, 64, 64, 3) # (張數,長,寬,RGB)
one_label = np.ones(oneimg.shape[0]) # 建立181張正常的圖像標籤為1
print(one_label)
one_label = np.reshape(one_label, (one_label.shape[0], 1))

"""### 黑緣擬金眼鯛(29)->label:2"""

# 匯入黑緣擬金眼鯛(29)圖像資料夾的圖片->label:2
twoimg = []
load_data(two_img_file, twoimg)
twoimg = np.array(twoimg)
print('Shape of Pempheris vanicolensis Images:', twoimg.shape)
# Shape of normal Images: (29, 64, 64, 3) # (張數,長,寬,RGB)
twomask = []
load_data(two_mask_file, twomask)
twomask = np.array(twomask)
print('Shape of Pempheris vanicolensis Images:', twomask.shape)
# Shape of normal Images: (29, 64, 64, 3) # (張數,長,寬,RGB)
two_label = np.full((twoimg.shape[0]),2) # 建立450張正常的圖像標籤為0
print(two_label)
two_label = np.reshape(two_label, (two_label.shape[0], 1))

# 將三種資料集合在一起，為同一欄位
Total_img = []
Total_img = np.concatenate((zeroimg, oneimg, twoimg), axis=0) # 將三種圖像合在一起，為同一欄位
print('Total_Image: ',Total_img.shape)
Total_mask = []
Total_mask = np.concatenate((zeromask, onemask, twomask), axis=0) # 將三種遮罩合在一起，為同一欄位
print('Total_Mask: ',Total_mask.shape)
Total_label = []
Total_label = np.concatenate((zero_label, one_label, two_label)) # 將三種標題合在一起，為同一欄位
print('Total_label: ',Total_label.shape)

"""## 2.3 影像正規化與標籤處理"""

# one-hot encoding->loss函數改為'classification':'categorical_crossentropy'
# from keras.utils import to_categorical
# Total_label = to_categorical(Total_label, num_classes = 3)

# 影像正規化
image_norm = Total_img / 255 # 255:最大像素質
mask_norm = Total_mask / 255 # 255:最大像素質

# 確認圖像img、遮罩mask與標籤label配對
i = 500
plt.figure(figsize=(5, 8))
plt.subplot(1, 2, 1)# (rows, columns, index)
plt.imshow(Total_img[i])
plt.subplot(1, 2, 2)# (rows, columns, index)
plt.imshow(Total_mask[i])
print("label:",Total_label[i])

"""# 3.將資料分成Train,Valid與Test資料集"""

from sklearn.model_selection import train_test_split
# 任務一: 影像切割 -> 資料: 圖像 & 遮罩
# 區分 x 資料 (image) 與 y 資料 (mask) 的訓練集、測試集與預測集
x_train_val, x_test, y_train_val_mask, y_test_mask = train_test_split(image_norm, mask_norm, test_size=0.1, random_state=11)
x_train, x_val, y_train_mask, y_val_mask = train_test_split(x_train_val, y_train_val_mask, test_size=0.1, random_state=11)
# 任務二: 影像分類 -> 資料: 圖像 & 標籤
# 區分 x 資料 (image) 與 y 資料 (label) 的訓練集、測試集與預測集
_, _, y_train_val_label, y_test_label = train_test_split(image_norm, Total_label, test_size=0.1, random_state=11)
# _, _, y_train_val_label, y_test_label=x_train_val, x_test, y_train_val_label, y_test_label
_, _, y_train_label, y_val_label = train_test_split(x_train_val, y_train_val_label, test_size=0.1,random_state=11)
# _, _, y_train_label, y_val_label=x_train, x_val, y_train_label, y_val_label
# 確認數量
print(x_train.shape)
print(y_train_mask.shape)
print(y_train_label.shape)
print(x_val.shape)
print(y_val_mask.shape)
print(y_val_label.shape)
print(x_test.shape)
print(y_test_mask.shape)
print(y_test_label.shape)

"""# 4. 建立模型

### attention模塊
"""

# attention模塊
def attention(g, s, num_filters):
  att_g = Conv2D(num_filters, 1, padding = "same")(g)
  att_g = BatchNormalization()(att_g)

  att_s = Conv2D(num_filters, 1, padding = "same")(s)
  att_s = BatchNormalization()(att_s)

  out = Activation("relu")(att_g + att_s)
  out = Conv2D(num_filters, 1, padding = "same")(out)
  out = Activation("sigmoid")(out)
  return out * s

"""### residual模塊"""

# residual模塊
def residual(inputs, filters, kernel_size = 3):
  x = Conv2D(filters, kernel_size, padding = 'same')(inputs)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  x = Conv2D(filters, kernel_size, padding = 'same')(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  x = Add()([x,inputs])
  return x

"""## 4.2 建立Y-net

"""

from tensorflow import keras
import tensorflow as tf
from keras import Model
from tensorflow. keras import backend as K
from tensorflow. keras. layers import Input, Conv2D, Conv2DTranspose, Dropout, Concatenate, MaxPooling2D, BatchNormalization, Activation, Flatten, Dense, Add

from keras.api._v2.keras import activations
def build_model():
  inputs = Input((x_train.shape[1], x_train.shape[2],x_train.shape[3],),name = 'input')
#下採樣

  conv1 = Conv2D(64,(3,3),activation = 'relu',padding = 'same')(inputs)
  resi1 = residual(conv1, 64)
  pool1 = MaxPooling2D((2,2),strides = 2,padding = 'same')(resi1)
  drop1 = Dropout(0.2)(pool1)


  conv2 = Conv2D(128,(3,3),activation = 'relu',padding = 'same')(drop1)
  resi2 = residual(conv2, 128)
  pool2 = MaxPooling2D((2,2),strides = 2,padding = 'same')(resi2)
  drop2 = Dropout(0.2)(pool2)


  conv3 = Conv2D(256,(3,3),activation = 'relu',padding = 'same')(drop2)
  resi3 = residual(conv3, 256)
  pool3 = MaxPooling2D((2,2),strides = 2,padding = 'same')(resi3)
  drop3 = Dropout(0.2)(pool3)


  conv4 = Conv2D(512,(3,3),activation = 'relu',padding = 'same')(drop3)
  resi4 = residual(conv4, 512)
  pool4 = MaxPooling2D((2,2),strides = 2,padding = 'same')(resi4)
  drop4 = Dropout(0.2)(pool4)


  convm = Conv2D(1024,(3,3),activation = 'relu',padding = 'same')(drop4)
  convm = Conv2D(1024,(3,3),activation = 'relu',padding = 'same')(convm)
# 上採樣
  tran5 = Conv2DTranspose(512,(2,2),strides =(2,2) ,padding = 'valid',activation = 'relu')(convm)
  att1 = attention(tran5, resi4, 512)
  conc5 = Concatenate()([tran5, att1])# 保留下採樣的訓練特徵
  conv5 = Conv2D(512,(3,3),activation = 'relu',padding = 'same')(conc5)
  resi5 = residual(conv5, 512)
  drop5 = Dropout(0.1)(resi5)


  tran6 = Conv2DTranspose(256,(2,2),strides =(2,2),padding = 'valid',activation = 'relu')(drop5)
  att2 = attention(tran6, resi3, 256)
  conc6 = Concatenate()([tran6, att2])# 保留下採樣的訓練特徵
  conv6 = Conv2D(256,(3,3),activation = 'relu',padding = 'same')(conc6)
  resi6 = residual(conv6, 256)
  drop6 = Dropout(0.1)(resi6)


  tran7 = Conv2DTranspose(128,(2,2),strides = 2,padding = 'valid',activation = 'relu')(drop6)
  att3 = attention(tran7, resi2, 128)
  conc7 = Concatenate()([tran7,att3])# 保留下採樣的訓練特徵
  conv7 = Conv2D(128,(3,3),activation = 'relu',padding = 'same')(conc7)
  resi7 = residual(conv7, 128)
  drop7 = Dropout(0.1)(resi7)

  tran8 = Conv2DTranspose(64,(2,2),strides = 2,padding = 'valid',activation = 'relu')(drop7)
  att4 = attention(tran8, resi1, 64)
  conc8 = Concatenate()([att4, tran8])# 保留下採樣的訓練特徵
  conv8 = Conv2D(64,(3,3),name="Attention",activation = 'tanh',padding = 'same')(conc8)
  resi8 = residual(conv8, 64)
  drop8 = Dropout(0.1)(resi8)
  # 任務一: 影像切割 -> 資料: 圖像 & 遮罩
  # 區分 x 資料 (image) 與 y 資料 (mask) 的訓練集、測試集與預測集
  segmentation_output = Conv2D(3,(1,1), activation='sigmoid',name='segmentation')(drop8)
  # 任務二: 影像分類 -> 資料: 圖像 & 標籤
  # 區分 x 資料 (image) 與 y 資料 (label) 的訓練集、測試集與預測集
  dense_classification=Flatten()(convm)
  dense_classification=Dense(64, activation='tanh')(dense_classification)
  classification_output = Dense(3, activation='softmax', name='classification')(dense_classification)


  model = Model(inputs = inputs, outputs = [classification_output, segmentation_output])
  return model

model = build_model()
model.summary()

"""# 5.建立Metrics(量化指標)"""

# 設定損失函數->dice:圖像分割
def dice_coef(y_true, y_pred):
  smooth = 1
  y_true_f = K.flatten(y_true)
  y_pred_f = K.flatten(y_pred)
  intersection = K.sum(y_true_f * y_pred_f)
  return (2. * intersection + smooth) / (K.sum(y_true_f * y_true_f) + K.sum(y_pred_f) + smooth)

"""# 6.模型編譯"""

# 模型編譯
model.compile(
    optimizer = keras.optimizers.Adam(learning_rate = 0.0003),
    loss = {'classification':'sparse_categorical_crossentropy',
            'segmentation':'binary_crossentropy'},
    loss_weights = {'classification':0.5,'segmentation':0.5},
    metrics = [{'classification':'accuracy'},{'segmentation':dice_coef}]
)

# Total loss = classification loss + segmentation loss = sparse_categorical_crossentropy + binary_crossentropy

"""# 7.訓練模型"""

from sklearn.utils import validation
history = model.fit(
    {'input':x_train},
    {'classification':y_train_label, 'segmentation':y_train_mask},
    epochs = 50,
    batch_size = 32,
    validation_data = ({'input':x_val},{'classification':y_val_label,'segmentation':y_val_mask})
                    )

"""# 8.繪製訓練中的Loss與Dice變化"""

import matplotlib.pyplot as plt

# Total loss = classification loss + segmentation loss = sparse_categorical_crossentropy + binary_crossentropy
plt.figure(figsize=(22, 12))
plt.subplot(2, 3, 1) # (rows, columns, index)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Total Loss')
plt.xlabel('Epoch')
plt.legend(['train','val'],loc = 'upper right')

plt.subplot(2, 3, 2)# (rows, columns, index)
plt.plot(history.history['classification_loss'])
plt.plot(history.history['val_segmentation_loss'])
plt.title('Classification Loss')
plt.xlabel('Epoch')
plt.legend(['train','val'],loc = 'upper right')

plt.subplot(2, 3, 3)# (rows, columns, index)
plt.plot(history.history['segmentation_loss'])
plt.plot(history.history['val_segmentation_loss'])
plt.title('Segmentaton Loss')
plt.xlabel('Epoch')
plt.legend(['train','val'],loc = 'upper right')

plt.subplot(2, 3, 5)# (rows, columns, index)
plt.plot(history.history['classification_accuracy'])
plt.plot(history.history['val_classification_accuracy'])
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train','val'],loc = 'upper right')

plt.subplot(2, 3, 6)# (rows, columns, index)
plt.plot(history.history['segmentation_dice_coef'])
plt.plot(history.history['val_segmentation_dice_coef'])
plt.title('Dice')
plt.xlabel('Epoch')
plt.legend(['train','val'],loc = 'upper left')

"""# 9.評估模型

*   test：loss
*   classification：accuracy
*   segmentation：dice
"""

score = model.evaluate(
    {'input':x_test},
    {'classification':y_test_label,'segmentation':y_test_mask}
    )
print('Test loss:',score[0])
print('Test classification accuracy:',score[3])
print('Test segmentation dice:',score[4])
# Total loss = classification loss + segmentation loss = sparse_categorical_crossentropy + binary_crossentropy

"""## 9.2 分類結果與混淆矩陣"""

from sklearn.metrics import confusion_matrix, classification_report

pred = model.predict({'input': x_test})
pred_c = np.around(pred[0],0)
pred_c = tf.argmax(pred_c, axis = 1)
print(classification_report(y_test_label, pred_c))

from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import pandas as pd

conf = confusion_matrix(y_test_label, pred_c)
class_name = ["zero","one","two"]
cm_df = pd.DataFrame(
    conf,
    index = class_name,
    columns = class_name
)

# 繪製混淆矩陣
sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.ylabel("Actual Values")
plt.xlabel("Predicted Values")
plt.show()

"""### 康德鋸鱗魚特異性與敏感性"""

# 康德鋸鱗魚特異性與敏感性->label:0
def zero_specificity_sensitivity(y_test, y_pred):
  P00,P10,P20,P01,P11,P21,P02,P12,P22 = confusion_matrix(y_test, y_pred).ravel()

  # P00, P10, P20,
  # P01, P11, P21,
  # P02, P12, P22

  TP = P00
  FP = P01 + P02
  FN = P10 + P20
  TN = confusion_matrix(y_test, y_pred).sum() - TP - FP - FN
  specificity = TN / (TN + FP) # 特異性
  sensitivity = TP / (TP + FN) # 敏感性
  return specificity, sensitivity
specificity, sensitivity = zero_specificity_sensitivity(y_test_label, pred_c)

print("\t zero")
print("specificity: ",specificity)
print("sensitivity: ",sensitivity)

"""### 摩鹿加雀鯛特異性與敏感性"""

# 摩鹿加雀鯛特異性與敏感性->label:1
def one_specificity_sensitivity(y_test, y_pred):
  P00, P10, P20, P01, P11, P21, P02, P12, P22 = confusion_matrix(y_test, y_pred).ravel()

  # P00, P10, P20,
  # P01, P11, P21,
  # P02, P12, P22

  TP = P11
  FP = P10 + P12
  FN = P01 + P21
  TN = confusion_matrix(y_test, y_pred).sum() - TP - FP - FN
  specificity = TN / (TN + FP) # 特異性
  sensitivity = TP / (TP + FN) # 敏感性
  return specificity, sensitivity
specificity, sensitivity = one_specificity_sensitivity(y_test_label, pred_c)

print("\t one")
print("specificity: ",specificity)
print("sensitivity: ",sensitivity)

"""### 黑緣擬金眼鯛特異性與敏感性"""

# 黑緣擬金眼鯛特異性與敏感性->label:2
def two_specificity_sensitivity(y_test, y_pred):
  P00, P10, P20, P01, P11, P21, P02, P12, P22 = confusion_matrix(y_test, y_pred).ravel()

  # P00, P10, P20,
  # P01, P11, P21,
  # P02, P12, P22

  TP = P22
  FP = P20 + P21
  FN = P02 + P12
  TN = confusion_matrix(y_test, y_pred).sum() - TP - FP - FN
  specificity = TN / (TN + FP) # 特異性
  sensitivity = TP / (TP + FN) # 敏感性
  return specificity, sensitivity
specificity, sensitivity = two_specificity_sensitivity(y_test_label, pred_c)

print("\t two")
print("specificity: ",specificity)
print("sensitivity: ",sensitivity)

"""### 分割結果"""

pred_s = pred[1]

pred_s[pred_s >= 0.5] = 1
pred_s[pred_s < 0.5] = 0

i = 55
plt.figure(figsize = (5, 8))
plt.subplot(1, 2, 1)# (rows, columns, index)
plt.imshow(pred_s[i])
plt.subplot(1, 2, 2)# (rows, columns, index)
plt.imshow(y_test_mask[i])

y_test_8bit = y_test_mask.astype(np.uint8) # cv2.Canny只能輸入uint8
pred_8bit = pred_s.astype(np.uint8)
x_test_32 = x_test.astype(np.float32) # 64位浮點opencv只適用float32

for i in range(x_test.shape[0]):
  plt.figure(figsize = (8, 4))
  plt.subplot(2, 3, 1)# (rows, columns, index)
  plt.title("original image")# 原始圖像
  plt.imshow(cv2.cvtColor(x_test_32[i],cv2.COLOR_BGR2RGB))
  plt.subplot(2, 3, 2)# (rows, columns, index)
  plt.title("ground truth")# 基本事實(專家畫的外框)
  plt.imshow(cv2.Canny(y_test_8bit[i], 0, 1),cmap = "gray")
  # plt.subplot(2, 3, 5)
  # plt.imshow(cv2.cvtColor(x_test_32[i] + convertToThreeChennel(cv2.Canny(y_test_8bit[i], 0, 1)), cv2.COLOR_BGR2RGB))
  plt.subplot(2, 3, 3)# (rows, columns, index)
  plt.title("pred")# 預測
  plt.imshow(cv2.Canny(pred_8bit[i], 0, 1),cmap = "gray")
  # plt.subplot(2, 3, 6)
  # plt.imshow(cv2.cvtColor(x_test_32[i] + convertToThreeChennel(cv2.Canny(y_test_8bit[i], 0, 1)), cv2.COLOR_BGR2RGB))
  plt.show()