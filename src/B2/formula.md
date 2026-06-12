# Công thức cần thiết - Bài 2: Xử lý miền không gian

Nguồn nội dung chính: `c4_xu-ly-mien-khong-gian(1).pptx` - Chương 4: Xử lý miền không gian.

---

## 1. Ảnh đầu vào và chuyển ảnh xám

Với ảnh màu đầu vào:

\[
I(x,y) = [R(x,y), G(x,y), B(x,y)]
\]

Có thể chuyển sang ảnh xám bằng công thức phổ biến:

\[
I_{gray}(x,y) = 0.299R(x,y) + 0.587G(x,y) + 0.114B(x,y)
\]

Trong OpenCV, nếu ảnh đọc bằng `cv2.imread()` thì thứ tự kênh là `BGR`, nên thường dùng:

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

Ký hiệu ảnh xám sau khi chuyển:

\[
f(x,y)
\]

---

## 2. Phép toán điểm

Phép toán điểm xử lý từng pixel độc lập:

\[
s = T(r)
\]

Trong đó:

- \(r\): mức xám đầu vào.
- \(s\): mức xám đầu ra.
- \(T\): hàm biến đổi mức xám.

---

## 3. Ảnh âm bản

Công thức ảnh âm bản:

\[
s = L - 1 - r
\]

Với ảnh 8-bit:

\[
s = 255 - r
\]

Trong đó:

- \(r\): mức xám đầu vào.
- \(s\): mức xám đầu ra.
- \(L\): số mức xám, thường \(L = 256\).

---

## 4. Lấy ngưỡng

Công thức lấy ngưỡng nhị phân:

\[
s =
\begin{cases}
0, & r \leq T \\
1, & r > T
\end{cases}
\]

Nếu dùng ảnh 8-bit, thường viết:

\[
s =
\begin{cases}
0, & r \leq T \\
255, & r > T
\end{cases}
\]

Trong đó:

- \(T\): giá trị ngưỡng.
- \(r\): mức xám đầu vào.
- \(s\): mức xám đầu ra.

---

## 5. Biến đổi logarithm

Công thức:

\[
s = c \log(1 + r)
\]

Trong đó:

- \(r\): mức xám đầu vào.
- \(s\): mức xám đầu ra.
- \(c\): hằng số tỉ lệ.

Công dụng:

- Làm nổi bật chi tiết vùng tối.
- Nén vùng mức xám lớn.
- Phù hợp khi ảnh có khoảng cường độ rất rộng.

---

## 6. Biến đổi lũy thừa / Gamma correction

Công thức:

\[
s = c r^\gamma
\]

Trong đó:

- \(c\): hằng số tỉ lệ.
- \(\gamma\): hệ số gamma.
- \(r\): mức xám đầu vào.
- \(s\): mức xám đầu ra.

Ý nghĩa:

- \(\gamma < 1\): làm sáng ảnh, tăng chi tiết vùng tối.
- \(\gamma = 1\): biến đổi tuyến tính.
- \(\gamma > 1\): làm tối ảnh.

---

## 7. Lọc không gian

Lọc không gian thay thế giá trị pixel tại \((x,y)\) dựa trên vùng lân cận của pixel đó.

Công thức tổng quát:

\[
g(x,y) = T\{f(x,y)\}
\]

Trong đó:

- \(f(x,y)\): ảnh đầu vào.
- \(g(x,y)\): ảnh đầu ra.
- \(T\): phép toán áp dụng trên lân cận của \((x,y)\).

---

## 8. Kích thước ảnh sau convolution

Với ảnh đầu vào kích thước:

\[
H \times W
\]

Kernel kích thước:

\[
K \times K
\]

Padding:

\[
P
\]

Stride:

\[
S
\]

Kích thước ảnh đầu ra:

\[
H_{out} = \left\lfloor \frac{H + 2P - K}{S} \right\rfloor + 1
\]

\[
W_{out} = \left\lfloor \frac{W + 2P - K}{S} \right\rfloor + 1
\]

---

## 9. Các trường hợp trong đề bài

### 9.1. Kernel 3x3, padding = 1, stride = 1

\[
K = 3,\quad P = 1,\quad S = 1
\]

\[
H_{out} = \left\lfloor \frac{H + 2 - 3}{1} \right\rfloor + 1 = H
\]

\[
W_{out} = \left\lfloor \frac{W + 2 - 3}{1} \right\rfloor + 1 = W
\]

Vậy ảnh \(I_1\) có cùng kích thước với ảnh xám ban đầu:

\[
I_1 \in \mathbb{R}^{H \times W}
\]

---

### 9.2. Kernel 5x5, padding = 2, stride = 1

\[
K = 5,\quad P = 2,\quad S = 1
\]

\[
H_{out} = \left\lfloor \frac{H + 4 - 5}{1} \right\rfloor + 1 = H
\]

\[
W_{out} = \left\lfloor \frac{W + 4 - 5}{1} \right\rfloor + 1 = W
\]

Vậy ảnh \(I_2\) có cùng kích thước với ảnh xám ban đầu:

\[
I_2 \in \mathbb{R}^{H \times W}
\]

---

### 9.3. Kernel 7x7, padding = 3, stride = 2

\[
K = 7,\quad P = 3,\quad S = 2
\]

\[
H_{out} = \left\lfloor \frac{H + 6 - 7}{2} \right\rfloor + 1
= \left\lfloor \frac{H - 1}{2} \right\rfloor + 1
\]

\[
W_{out} = \left\lfloor \frac{W + 6 - 7}{2} \right\rfloor + 1
= \left\lfloor \frac{W - 1}{2} \right\rfloor + 1
\]

Vậy ảnh \(I_3\) nhỏ hơn ảnh ban đầu vì stride = 2.

---

## 10. Padding

Một số cách xử lý biên ảnh:

### 10.1. Zero padding

Thêm giá trị 0 vào vùng biên:

\[
f_{pad}(x,y) = 0
\]

với các vị trí nằm ngoài ảnh gốc.

### 10.2. Copy padding / replicate padding

Lặp lại giá trị biên gần nhất:

\[
f_{n+1} = f_n
\]

### 10.3. Flipping padding / symmetric padding

Lấy đối xứng qua biên:

\[
f_{n+1} = f_{n-1}
\]

---

## 11. Tương quan không gian

Tương quan áp dụng trực tiếp kernel lên vùng ảnh lân cận:

\[
g(x,y) = \sum_{s=-a}^{a}\sum_{t=-b}^{b} w(s,t) f(x+s, y+t)
\]

Trong đó:

- \(w(s,t)\): kernel hoặc mask.
- \(f(x+s,y+t)\): pixel trong vùng lân cận.
- \(g(x,y)\): pixel đầu ra.
- Kernel có kích thước \((2a+1) \times (2b+1)\).

---

## 12. Tích chập / Convolution

Tích chập tương tự tương quan nhưng kernel được lật 180 độ trước khi tính.

Công thức:

\[
g(x,y) = \sum_{s=-a}^{a}\sum_{t=-b}^{b} w(s,t) f(x-s, y-t)
\]

Tương đương:

\[
g(x,y) = \sum_{s=-a}^{a}\sum_{t=-b}^{b} w(-s,-t) f(x+s, y+t)
\]

Trong đó kernel sau khi lật 180 độ là:

\[
w_{conv}(s,t) = w(-s,-t)
\]

Nếu kernel đối xứng:

\[
w(s,t) = w(-s,-t)
\]

thì:

\[
\text{convolution} = \text{correlation}
\]

---

## 13. Ví dụ lật kernel 180 độ

Kernel ban đầu:

\[
W =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{bmatrix}
\]

Kernel sau khi lật 180 độ:

\[
W_{rot180} =
\begin{bmatrix}
9 & 8 & 7 \\
6 & 5 & 4 \\
3 & 2 & 1
\end{bmatrix}
\]

---

## 14. Lọc trung bình số học

Công thức trung bình số học trong cửa sổ \(m \times n\):

\[
g(x,y) = \frac{1}{mn} \sum_{(s,t) \in S_{xy}} f(s,t)
\]

Trong đó:

- \(S_{xy}\): vùng lân cận của pixel \((x,y)\).
- \(m \times n\): kích thước cửa sổ lọc.

Ví dụ kernel trung bình 3x3:

\[
W =
\frac{1}{9}
\begin{bmatrix}
1 & 1 & 1 \\
1 & 1 & 1 \\
1 & 1 & 1
\end{bmatrix}
\]

---

## 15. Lọc trung bình có trọng số

Công thức tổng quát:

\[
g(x,y) = \sum_{s=-a}^{a}\sum_{t=-b}^{b} w(s,t) f(x+s, y+t)
\]

Với điều kiện thường dùng cho lọc làm trơn:

\[
\sum_{s=-a}^{a}\sum_{t=-b}^{b} w(s,t) = 1
\]

Ví dụ kernel trung bình có trọng số 3x3:

\[
W =
\frac{1}{16}
\begin{bmatrix}
1 & 2 & 1 \\
2 & 4 & 2 \\
1 & 2 & 1
\end{bmatrix}
\]

---

## 16. Lọc trung vị / Median filter

Lọc trung vị thay thế giá trị pixel trung tâm bằng giá trị trung vị của các pixel trong vùng lân cận.

Công thức:

\[
g(x,y) = \operatorname{median}\{f(s,t) \mid (s,t) \in S_{xy}\}
\]

Trong đó:

- \(S_{xy}\): vùng lân cận quanh pixel \((x,y)\).
- `median`: giá trị đứng giữa sau khi sắp xếp tăng dần hoặc giảm dần.

Với cửa sổ 3x3:

\[
S_{xy} =
\begin{bmatrix}
p_1 & p_2 & p_3 \\
p_4 & p_5 & p_6 \\
p_7 & p_8 & p_9
\end{bmatrix}
\]

Sắp xếp:

\[
p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(9)}
\]

Giá trị trung vị:

\[
g(x,y) = p_{(5)}
\]

---

## 17. Lọc tối đa

Lọc tối đa thay thế pixel trung tâm bằng giá trị lớn nhất trong vùng lân cận:

\[
g(x,y) = \max \{ f(s,t) \mid (s,t) \in S_{xy} \}
\]

---

## 18. Lọc tối thiểu

Lọc tối thiểu thay thế pixel trung tâm bằng giá trị nhỏ nhất trong vùng lân cận:

\[
g(x,y) = \min \{ f(s,t) \mid (s,t) \in S_{xy} \}
\]

---

## 19. Lọc điểm giữa / Midpoint filter

Công thức:

\[
g(x,y) = \frac{1}{2}
\left[
\max_{(s,t)\in S_{xy}} f(s,t)
+
\min_{(s,t)\in S_{xy}} f(s,t)
\right]
\]

---

## 20. Alpha-trimmed mean filter

Sắp xếp các pixel trong vùng lân cận, loại bỏ \(d/2\) pixel nhỏ nhất và \(d/2\) pixel lớn nhất.

Công thức:

\[
g(x,y) =
\frac{1}{mn - d}
\sum_{k=\frac{d}{2}+1}^{mn-\frac{d}{2}} p_{(k)}
\]

Trong đó:

- \(m \times n\): kích thước cửa sổ.
- \(d\): số phần tử bị loại bỏ.
- \(p_{(k)}\): phần tử thứ \(k\) sau khi sắp xếp tăng dần.

---

## 21. Công thức tạo các ảnh trong bài 2

### 21.1. Ảnh I1

\[
I_1 = f * W_{3 \times 3}
\]

với:

\[
K = 3,\quad P = 1,\quad S = 1
\]

---

### 21.2. Ảnh I2

\[
I_2 = f * W_{5 \times 5}
\]

với:

\[
K = 5,\quad P = 2,\quad S = 1
\]

---

### 21.3. Ảnh I3

\[
I_3 = f * W_{7 \times 7}
\]

với:

\[
K = 7,\quad P = 3,\quad S = 2
\]

---

### 21.4. Ảnh I4

Lọc trung vị ảnh \(I_3\) với lân cận 3x3:

\[
I_4(x,y) = \operatorname{median}\{I_3(s,t) \mid (s,t) \in S_{xy}^{3 \times 3}\}
\]

---

### 21.5. Ảnh I5

Lọc ảnh \(I_1\) với lân cận 5x5:

\[
I_5(x,y) = \operatorname{filter}_{5 \times 5}\{I_1(s,t)\}
\]

Nếu dùng lọc trung vị 5x5:

\[
I_5(x,y) = \operatorname{median}\{I_1(s,t) \mid (s,t) \in S_{xy}^{5 \times 5}\}
\]

Nếu dùng lọc trung bình 5x5:

\[
I_5(x,y) = \frac{1}{25}\sum_{(s,t)\in S_{xy}^{5 \times 5}} I_1(s,t)
\]

---

### 21.6. Ảnh I6

Theo đề bài:

\[
I_6(x,y) =
\begin{cases}
0, & I_4(x,y) > I_5(x,y) \\
I_5(x,y), & I_4(x,y) \leq I_5(x,y)
\end{cases}
\]

Nếu \(I_4\) và \(I_5\) khác kích thước, cần padding hoặc resize/pad để đưa về cùng kích thước trước khi so sánh.

---

## 22. Laplacian

Toán tử Laplacian là đạo hàm bậc hai trong không gian 2D:

\[
\nabla^2 f =
\frac{\partial^2 f}{\partial x^2}
+
\frac{\partial^2 f}{\partial y^2}
\]

Xấp xỉ rời rạc 4-neighbor:

\[
\nabla^2 f(x,y)
=
f(x+1,y) + f(x-1,y) + f(x,y+1) + f(x,y-1) - 4f(x,y)
\]

Kernel Laplacian 4-neighbor:

\[
\begin{bmatrix}
0 & 1 & 0 \\
1 & -4 & 1 \\
0 & 1 & 0
\end{bmatrix}
\]

Kernel Laplacian 8-neighbor:

\[
\begin{bmatrix}
1 & 1 & 1 \\
1 & -8 & 1 \\
1 & 1 & 1
\end{bmatrix}
\]

---

## 23. MSE và PSNR

Nếu cần so sánh ảnh sau lọc với ảnh gốc, dùng MSE và PSNR.

### 23.1. MSE

\[
MSE =
\frac{1}{MN}
\sum_{x=0}^{M-1}
\sum_{y=0}^{N-1}
[f(x,y) - g(x,y)]^2
\]

Trong đó:

- \(f(x,y)\): ảnh gốc.
- \(g(x,y)\): ảnh sau xử lý.
- \(M \times N\): kích thước ảnh.

### 23.2. PSNR

\[
PSNR = 10 \log_{10}
\left(
\frac{MAX_I^2}{MSE}
\right)
\]

Với ảnh 8-bit:

\[
MAX_I = 255
\]

nên:

\[
PSNR = 10 \log_{10}
\left(
\frac{255^2}{MSE}
\right)
\]

---

## 24. Pipeline xử lý cho bài 2

Với mỗi ảnh màu đầu vào \(I_k\):

\[
I_k \rightarrow I_{gray}
\]

Sau đó:

\[
I_1 = I_{gray} * W_{3 \times 3},\quad P=1,\quad S=1
\]

\[
I_2 = I_{gray} * W_{5 \times 5},\quad P=2,\quad S=1
\]

\[
I_3 = I_{gray} * W_{7 \times 7},\quad P=3,\quad S=2
\]

\[
I_4 = \operatorname{median}_{3 \times 3}(I_3)
\]

\[
I_5 = \operatorname{filter}_{5 \times 5}(I_1)
\]

\[
I_6(x,y) =
\begin{cases}
0, & I_4(x,y) > I_5(x,y) \\
I_5(x,y), & I_4(x,y) \leq I_5(x,y)
\end{cases}
\]

---

## 25. Ghi chú khi code Python

Nên tự viết các hàm chính:

```python
def convolution2d(gray, kernel, padding=0, stride=1):
    pass

def median_filter(gray, ksize=3, padding=1):
    pass

def pad_to_same_size(img_a, img_b):
    pass

def create_I6(I4, I5):
    pass
```

Với OpenCV, chỉ nên dùng cho:

```python
cv2.imread()
cv2.cvtColor()
cv2.imwrite()
```

Nếu muốn code đúng tinh thần bài học, convolution, padding, stride và median filter nên tự cài đặt bằng NumPy.
