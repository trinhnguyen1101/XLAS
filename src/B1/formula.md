# Công thức cần thiết cho Bài 1: Histogram

Nguồn nội dung chính: `c3_histogram.pptx` - Chương 3: Histogram.

---

## 1. Chuyển ảnh màu sang ảnh xám

Với ảnh màu RGB, ảnh xám có thể tính theo công thức:

$$
I_{gray}(x,y) = 0.299R(x,y) + 0.587G(x,y) + 0.114B(x,y)
$$

Nếu dùng OpenCV, ảnh đọc vào có thứ tự kênh là BGR, nên công thức tương đương là:

$$
I_{gray}(x,y) = 0.114B(x,y) + 0.587G(x,y) + 0.299R(x,y)
$$

---

## 2. Histogram của ảnh xám

Giả sử ảnh xám có $L$ mức xám:

$$
r_0, r_1, \dots, r_{L-1}
$$

Với ảnh $B$-bit:

$$
L = 2^B
$$

Ví dụ ảnh xám 8-bit:

$$
L = 2^8 = 256
$$

Histogram chưa chuẩn hóa:

$$
h(r_k) = n_k
$$

Trong đó:

- $r_k$: mức xám thứ $k$
- $n_k$: số pixel có mức xám $r_k$
- $n$: tổng số pixel của ảnh
- $0 \le k \le L-1$

Histogram chuẩn hóa:

$$
p(r_k) = \frac{n_k}{n}
$$

Histogram chuẩn hóa có thể xem như xác suất xuất hiện của mức xám $r_k$.

---

## 3. Hàm phân phối tích lũy CDF

CDF của histogram tại mức xám $r_k$:

$$
CDF(r_k) = \sum_{j=0}^{k} p(r_j)
$$

Hay viết theo số lượng pixel:

$$
CDF(r_k) = \sum_{j=0}^{k} \frac{n_j}{n}
$$

---

## 4. Cân bằng histogram

Mục tiêu của cân bằng histogram là tìm phép biến đổi $T(.)$ sao cho histogram chuẩn hóa của ảnh đầu ra phân bố gần đều hơn trong khoảng $[0,1]$.

Với ảnh rời rạc, biến đổi cân bằng histogram được tính bằng:

$$
s_k = T(r_k) = \sum_{j=0}^{k} p_{in}(r_j)
$$

Trong đó:

- $r_k$: mức xám đầu vào
- $s_k$: mức xám đầu ra sau biến đổi
- $p_{in}(r_j)$: histogram chuẩn hóa của ảnh đầu vào
- $0 \le k \le L-1$

Với ảnh 8-bit hoặc ảnh có $L$ mức xám, cần scale về khoảng $[0, L-1]$:

$$
s_k = \operatorname{round}\left((L-1) \sum_{j=0}^{k} p_{in}(r_j)\right)
$$

Tức là:

$$
s_k = \operatorname{round}\left((L-1) \cdot CDF(r_k)\right)
$$

Với ảnh 8-bit:

$$
s_k = \operatorname{round}\left(255 \cdot CDF(r_k)\right)
$$

---

## 5. Dịch chuyển histogram

Dịch chuyển histogram dùng để thay đổi độ sáng trung bình của ảnh.

Công thức tổng quát:

$$
s = r + c
$$

Trong đó:

- $r$: mức xám đầu vào
- $s$: mức xám đầu ra
- $c$: hằng số dịch chuyển

Nếu $c > 0$, ảnh sáng hơn.  
Nếu $c < 0$, ảnh tối hơn.

Với ảnh 8-bit cần chặn giá trị trong khoảng $[0,255]$:

$$
s = \operatorname{clip}(r+c, 0, 255)
$$

Tổng quát với ảnh $L$ mức xám:

$$
s = \operatorname{clip}(r+c, 0, L-1)
$$

---

## 6. Trải rộng histogram

Trải rộng histogram dùng để kéo dải mức xám hiện tại ra toàn bộ thang xám.

Công thức trong PPT:

$$
s = \frac{r-r_{min}}{r_{max}-r_{min}} \times (L-1)
$$

Trong đó:

- $r$: mức xám đầu vào
- $s$: mức xám đầu ra
- $r_{min}$: mức xám nhỏ nhất trong ảnh đầu vào
- $r_{max}$: mức xám lớn nhất trong ảnh đầu vào
- $L$: tổng số mức xám

Với ảnh 8-bit:

$$
s = \frac{r-r_{min}}{r_{max}-r_{min}} \times 255
$$

Khi cài đặt nên làm tròn và ép kiểu về ảnh 8-bit:

$$
s = \operatorname{round}\left(\frac{r-r_{min}}{r_{max}-r_{min}} \times 255\right)
$$

---

## 7. Thu hẹp histogram

Thu hẹp histogram dùng để đưa dải mức xám về một khoảng nhỏ hơn $[s_{min}, s_{max}]$.

Công thức trong PPT:

$$
s = \left[\frac{s_{max}-s_{min}}{r_{max}-r_{min}}\right](r-r_{min}) + s_{min}
$$

Trong đó:

- $r$: mức xám đầu vào
- $s$: mức xám đầu ra
- $r_{min}$: mức xám nhỏ nhất của ảnh đầu vào
- $r_{max}$: mức xám lớn nhất của ảnh đầu vào
- $s_{min}$: mức xám nhỏ nhất mong muốn ở ảnh đầu ra
- $s_{max}$: mức xám lớn nhất mong muốn ở ảnh đầu ra

Trong đề bài yêu cầu thu hẹp $H2$ vào khoảng $(30,120)$, nên lấy:

$$
s_{min} = 30
$$

$$
s_{max} = 120
$$

Thay vào công thức:

$$
s = \left[\frac{120-30}{r_{max}-r_{min}}\right](r-r_{min}) + 30
$$

Rút gọn:

$$
s = \frac{90}{r_{max}-r_{min}}(r-r_{min}) + 30
$$

Khi cài đặt:

$$
s = \operatorname{round}\left(\frac{90}{r_{max}-r_{min}}(r-r_{min}) + 30\right)
$$

---

## 8. Công thức độ sáng và độ tương phản

Độ sáng trung bình của ảnh xám:

$$
\mu = \frac{1}{n}\sum_{x,y} I(x,y)
$$

Độ tương phản theo khoảng mức xám:

$$
C = r_{max} - r_{min}
$$

Trong đó:

- $\mu$: độ sáng trung bình
- $C$: độ tương phản theo khoảng mức xám
- $I(x,y)$: giá trị mức xám tại pixel $(x,y)$

---

## 9. Pipeline cần dùng cho Bài 1

Với mỗi ảnh màu $I$:

1. Chuyển ảnh màu sang ảnh xám:

$$
I_{gray} = RGB2Gray(I)
$$

2. Tính histogram gốc:

$$
H1 = h(I_{gray})
$$

3. Cân bằng histogram:

$$
I_{eq}(x,y) = T(I_{gray}(x,y))
$$

4. Tính histogram của ảnh đã cân bằng:

$$
H2 = h(I_{eq})
$$

5. Thu hẹp ảnh đã cân bằng về khoảng $(30,120)$:

$$
I_{shrink}(x,y) = \frac{90}{r_{max}-r_{min}}(I_{eq}(x,y)-r_{min}) + 30
$$

6. Tính histogram sau khi thu hẹp:

$$
H_{shrink} = h(I_{shrink})
$$

---

## 10. Ghi chú khi code Python

Với ảnh 8-bit, các kết quả mức xám nên được ép về khoảng $[0,255]$:

$$
I_{out} = \operatorname{clip}(I_{out}, 0, 255)
$$

Sau đó chuyển về kiểu `uint8`.

Khi thu hẹp về khoảng $(30,120)$, kết quả nên nằm trong khoảng:

$$
30 \le I_{shrink}(x,y) \le 120
$$
