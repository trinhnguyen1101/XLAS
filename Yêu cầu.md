Cho 1 ảnh màu I kích thước n x m, chuyển đổi ảnh I thành ảnh xám. 
Vẽ Histogram của I (H1)
Histogram cân bằng của I (H2)
Hiệu chỉnh thu hẹp H2 trong khoảng (30, 120)
Cho 1 ảnh màu I kích thước n x m, chuyển đổi ảnh I thành ảnh xám. 
Dùng phép tích chập (convolutional operator) để lọc ảnh I với các thông số sau:
Kernel 3x3, padding = 1 (I1)
Kernel 5x5, padding = 2 (I2)
Kernel 7x7, padding = 3 và stride = 2 (Dịch chuyển ngang và dọc) (I3)
Tìm ảnh I4 bằng cách lọc trung vị ảnh I3 với lân cận neighbors 3x3
Tìm ảnh I5 là bằng cách lọc trong bị mảnh I1 với lân cận lân cận neighbors 5x5.
Xây dựng ảnh I6 bằng cách lấy ngưỡng: Nếu I4(x,y)>I5(x,y) thì I6(x,y)=0, ngược lại I6(x,y)= I5(x,y). Trường hợp hai ảnh không bằng nhau về kích thước thì biến đổi (thêm padding) để các ảnh có cùng kích thước trước khi tính toán
Cho 1 ảnh màu I kích thước n x m, chuyển đổi ảnh I thành ảnh xám. Dùng toán tử LBP (Local Binary Patterns) để biến đổi ảnh I theo các yêu cầu sau:
Neighbors P = 8, R=1 và R=2;
Neighbors P = 16, R=2 và R=3;
Neighbors P = 24, R=3;
Ghi chú: Trường hợp P=16 (hoặc P=24) thì tách chuỗi nhị phân thành 2 phần (hoặc 3 phần). Tức là mỗi phần chuỗi có 8 bits. Sau đó, chỉ lấy phần có giá trị lớn nhất gán cho pixel đang xét (center pixel).
Cho 10 ảnh màu kích thước n x m. Thực hiện xử lý các bài 1, 2, 3 ở trên cho 10 ảnh này và báo cáo kết quả trong 1 file *.pdf. Lưu ý, trong file pdf, viết rõ tên nhóm, MSSV, Họ và Tên SV)
