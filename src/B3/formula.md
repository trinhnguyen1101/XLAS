# Công thức cần thiết - Bài 3: Local Binary Patterns (LBP)

## 1. Mục tiêu của LBP

Local Binary Patterns (LBP) là toán tử mô tả **texture** của ảnh.

Ý tưởng chính:

- Xét một pixel trung tâm có mức xám `g_c`.
- Lấy `P` điểm lân cận nằm trên đường tròn bán kính `R` quanh pixel trung tâm.
- So sánh từng điểm lân cận với pixel trung tâm.
- Nếu điểm lân cận lớn hơn hoặc bằng pixel trung tâm thì gán bit `1`, ngược lại gán bit `0`.
- Ghép các bit lại thành một chuỗi nhị phân.
- Đổi chuỗi nhị phân đó sang số thập phân để tạo giá trị LBP tại pixel trung tâm.

---

## 2. Chuyển ảnh màu sang ảnh xám

Với ảnh màu RGB:

\[
I_{gray}(x,y) = 0.299R(x,y) + 0.587G(x,y) + 0.114B(x,y)
\]

Trong xử lý ảnh bằng OpenCV, ảnh đọc vào thường ở dạng BGR, nên khi code cần chú ý thứ tự kênh màu.

---

## 3. Vị trí các điểm lân cận trong LBP

Với pixel trung tâm tại tọa độ:

\[
(x_c, y_c)
\]

`P` điểm lân cận nằm trên đường tròn bán kính `R` được xác định bởi:

\[
x_p = x_c + R \cos\left(\frac{2\pi p}{P}\right)
\]

\[
y_p = y_c - R \sin\left(\frac{2\pi p}{P}\right)
\]

với:

\[
p = 0, 1, 2, ..., P-1
\]

Trong đó:

- `P`: số lượng điểm lân cận.
- `R`: bán kính lấy mẫu.
- `(x_c, y_c)`: tọa độ pixel trung tâm.
- `(x_p, y_p)`: tọa độ điểm lân cận thứ `p`.

Dấu `-` ở công thức `y_p` thường được dùng vì trong ảnh số, trục `y` tăng theo chiều từ trên xuống dưới.

---

## 4. Nội suy giá trị mức xám tại điểm lân cận

Khi `R = 1` và `P = 8`, nhiều điểm lân cận rơi đúng vào tọa độ pixel nguyên.

Nhưng với các trường hợp như:

\[
P = 16, R = 2
\]

hoặc:

\[
P = 24, R = 3
\]

các điểm lân cận có thể rơi vào tọa độ không nguyên. Khi đó cần nội suy để lấy giá trị mức xám `g_p`.

Có thể dùng nội suy song tuyến tính:

\[
g_p = (1-a)(1-b)I(x_1,y_1) + a(1-b)I(x_2,y_1) + (1-a)bI(x_1,y_2) + abI(x_2,y_2)
\]

Trong đó:

\[
x_1 = \lfloor x_p \rfloor, \quad x_2 = x_1 + 1
\]

\[
y_1 = \lfloor y_p \rfloor, \quad y_2 = y_1 + 1
\]

\[
a = x_p - x_1
\]

\[
b = y_p - y_1
\]

Nếu muốn làm đơn giản hơn trong bài thực hành, có thể làm tròn tọa độ:

\[
x_p' = round(x_p)
\]

\[
y_p' = round(y_p)
\]

rồi lấy:

\[
g_p = I(x_p', y_p')
\]

Tuy nhiên cách đúng hơn là dùng nội suy song tuyến tính.

---

## 5. Hàm so sánh nhị phân

Với pixel trung tâm có giá trị mức xám `g_c` và điểm lân cận có giá trị `g_p`, ta định nghĩa:

\[
s(g_p - g_c) =
\begin{cases}
1, & g_p \geq g_c \\
0, & g_p < g_c
\end{cases}
\]

Mỗi điểm lân cận sinh ra một bit nhị phân.

---

## 6. Công thức LBP chuẩn

Giá trị LBP tại pixel trung tâm được tính bằng:

\[
LBP_{P,R}(x_c,y_c) = \sum_{p=0}^{P-1} s(g_p - g_c)2^p
\]

Trong đó:

- `P`: số điểm lân cận.
- `R`: bán kính lân cận.
- `g_c`: mức xám của pixel trung tâm.
- `g_p`: mức xám của điểm lân cận thứ `p`.
- `s(g_p - g_c)`: bit nhị phân sau khi so sánh.

---

## 7. Ví dụ LBP với P = 8

Với `P = 8`, chuỗi nhị phân có 8 bit:

\[
b_0, b_1, b_2, b_3, b_4, b_5, b_6, b_7
\]

Trong đó:

\[
b_p = s(g_p - g_c)
\]

Giá trị LBP là:

\[
LBP_{8,R} = b_0 2^0 + b_1 2^1 + b_2 2^2 + b_3 2^3 + b_4 2^4 + b_5 2^5 + b_6 2^6 + b_7 2^7
\]

Hay:

\[
LBP_{8,R} = \sum_{p=0}^{7} b_p2^p
\]

Khoảng giá trị của ảnh LBP khi `P = 8` là:

\[
0 \leq LBP_{8,R} \leq 255
\]

---

## 8. Trường hợp P = 8, R = 1

Theo đề bài:

\[
P = 8, \quad R = 1
\]

Công thức:

\[
LBP_{8,1}(x,y) = \sum_{p=0}^{7} s(g_p - g_c)2^p
\]

Kết quả là ảnh LBP có giá trị trong khoảng:

\[
[0, 255]
\]

---

## 9. Trường hợp P = 8, R = 2

Theo đề bài:

\[
P = 8, \quad R = 2
\]

Công thức:

\[
LBP_{8,2}(x,y) = \sum_{p=0}^{7} s(g_p - g_c)2^p
\]

Khác với `R = 1`, các điểm lân cận được lấy trên vòng tròn bán kính lớn hơn nên mô tả texture ở phạm vi rộng hơn.

---

## 10. Trường hợp P = 16

Theo đề bài, khi:

\[
P = 16
\]

chuỗi nhị phân có 16 bit:

\[
b_0, b_1, ..., b_{15}
\]

Nhưng đề yêu cầu tách chuỗi 16 bit thành 2 phần, mỗi phần 8 bit:

Phần 1:

\[
B_1 = (b_0, b_1, ..., b_7)
\]

Phần 2:

\[
B_2 = (b_8, b_9, ..., b_{15})
\]

Giá trị thập phân của từng phần:

\[
V_1 = \sum_{p=0}^{7} b_p2^p
\]

\[
V_2 = \sum_{p=0}^{7} b_{p+8}2^p
\]

Giá trị LBP cuối cùng được gán cho pixel trung tâm là:

\[
LBP_{16,R}^{final}(x,y) = \max(V_1,V_2)
\]

Vì lấy giá trị lớn nhất của hai nhóm 8 bit, ảnh kết quả vẫn nằm trong khoảng:

\[
0 \leq LBP_{16,R}^{final} \leq 255
\]

---

## 11. Trường hợp P = 16, R = 2

Theo đề bài:

\[
P = 16, \quad R = 2
\]

Tạo 16 bit:

\[
b_p = s(g_p - g_c), \quad p = 0,1,...,15
\]

Tách thành 2 nhóm:

\[
V_1 = \sum_{p=0}^{7} b_p2^p
\]

\[
V_2 = \sum_{p=0}^{7} b_{p+8}2^p
\]

Gán:

\[
LBP_{16,2}^{final}(x,y) = \max(V_1,V_2)
\]

---

## 12. Trường hợp P = 16, R = 3

Theo đề bài:

\[
P = 16, \quad R = 3
\]

Công thức tương tự trường hợp `P = 16, R = 2`, chỉ khác bán kính lấy mẫu:

\[
LBP_{16,3}^{final}(x,y) = \max(V_1,V_2)
\]

Trong đó:

\[
V_1 = \sum_{p=0}^{7} b_p2^p
\]

\[
V_2 = \sum_{p=0}^{7} b_{p+8}2^p
\]

---

## 13. Trường hợp P = 24

Theo đề bài, khi:

\[
P = 24
\]

chuỗi nhị phân có 24 bit:

\[
b_0, b_1, ..., b_{23}
\]

Tách chuỗi 24 bit thành 3 phần, mỗi phần 8 bit:

Phần 1:

\[
B_1 = (b_0, b_1, ..., b_7)
\]

Phần 2:

\[
B_2 = (b_8, b_9, ..., b_{15})
\]

Phần 3:

\[
B_3 = (b_{16}, b_{17}, ..., b_{23})
\]

Giá trị thập phân của từng phần:

\[
V_1 = \sum_{p=0}^{7} b_p2^p
\]

\[
V_2 = \sum_{p=0}^{7} b_{p+8}2^p
\]

\[
V_3 = \sum_{p=0}^{7} b_{p+16}2^p
\]

Giá trị LBP cuối cùng được gán cho pixel trung tâm:

\[
LBP_{24,R}^{final}(x,y) = \max(V_1,V_2,V_3)
\]

Ảnh kết quả vẫn nằm trong khoảng:

\[
0 \leq LBP_{24,R}^{final} \leq 255
\]

---

## 14. Trường hợp P = 24, R = 3

Theo đề bài:

\[
P = 24, \quad R = 3
\]

Tạo 24 bit:

\[
b_p = s(g_p - g_c), \quad p = 0,1,...,23
\]

Tính 3 nhóm 8 bit:

\[
V_1 = \sum_{p=0}^{7} b_p2^p
\]

\[
V_2 = \sum_{p=0}^{7} b_{p+8}2^p
\]

\[
V_3 = \sum_{p=0}^{7} b_{p+16}2^p
\]

Gán:

\[
LBP_{24,3}^{final}(x,y) = \max(V_1,V_2,V_3)
\]

---

## 15. Xử lý biên ảnh

Vì LBP cần lấy lân cận bán kính `R`, các pixel gần biên có thể không đủ lân cận.

Có 2 cách thường dùng:

### Cách 1: Bỏ qua biên

Chỉ tính LBP cho các pixel thỏa mãn:

\[
R \leq x < W - R
\]

\[
R \leq y < H - R
\]

Các pixel biên có thể gán bằng `0`.

### Cách 2: Padding ảnh

Thêm padding quanh ảnh trước khi tính LBP.

Nếu bán kính lớn nhất là:

\[
R_{max} = 3
\]

thì có thể padding ảnh với kích thước:

\[
padding = 3
\]

Các kiểu padding thường dùng:

- zero padding
- replicate padding
- reflect padding

Trong bài thực hành, nên dùng `reflect padding` hoặc `replicate padding` để hạn chế tạo biên giả.

---

## 16. Histogram của ảnh LBP

Sau khi tạo ảnh LBP, có thể vẽ histogram để mô tả phân bố texture.

Histogram LBP được tính bởi:

\[
H(k) = \sum_{x,y} \mathbf{1}(LBP(x,y)=k)
\]

với:

\[
k = 0,1,2,...,255
\]

Histogram chuẩn hóa:

\[
p(k) = \frac{H(k)}{N}
\]

Trong đó:

- `H(k)`: số pixel có giá trị LBP bằng `k`.
- `N`: tổng số pixel của ảnh LBP.
- `p(k)`: histogram chuẩn hóa.

---

## 17. Pipeline xử lý cho bài 3

Với mỗi ảnh màu đầu vào `I_k`:

### Bước 1: Đọc ảnh màu

\[
I_k(x,y)
\]

### Bước 2: Chuyển sang ảnh xám

\[
Gray_k(x,y)
\]

### Bước 3: Tính các ảnh LBP theo yêu cầu

\[
LBP_{8,1}
\]

\[
LBP_{8,2}
\]

\[
LBP_{16,2}^{final}
\]

\[
LBP_{16,3}^{final}
\]

\[
LBP_{24,3}^{final}
\]

### Bước 4: Lưu kết quả

Với ảnh thứ `k`, có thể lưu các file:

```text
output/I_k/lbp_p8_r1.png
output/I_k/lbp_p8_r2.png
output/I_k/lbp_p16_r2.png
output/I_k/lbp_p16_r3.png
output/I_k/lbp_p24_r3.png
```

---

## 18. Tóm tắt công thức chính cần nhớ

### Công thức lấy điểm lân cận

\[
x_p = x_c + R \cos\left(\frac{2\pi p}{P}\right)
\]

\[
y_p = y_c - R \sin\left(\frac{2\pi p}{P}\right)
\]

### Hàm so sánh

\[
s(g_p - g_c) =
\begin{cases}
1, & g_p \geq g_c \\
0, & g_p < g_c
\end{cases}
\]

### LBP chuẩn

\[
LBP_{P,R}(x,y) = \sum_{p=0}^{P-1}s(g_p-g_c)2^p
\]

### P = 16 theo yêu cầu đề

\[
LBP_{16,R}^{final}(x,y) = \max\left(\sum_{p=0}^{7}b_p2^p, \sum_{p=0}^{7}b_{p+8}2^p\right)
\]

### P = 24 theo yêu cầu đề

\[
LBP_{24,R}^{final}(x,y) = \max\left(\sum_{p=0}^{7}b_p2^p, \sum_{p=0}^{7}b_{p+8}2^p, \sum_{p=0}^{7}b_{p+16}2^p\right)
\]
