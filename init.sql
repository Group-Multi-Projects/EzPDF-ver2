-- Chọn database mặc định
USE mysql;

-- Đổi plugin xác thực của user ezpdf_user thành mysql_native_password
ALTER USER 'ezpdf_user'@'%' IDENTIFIED WITH mysql_native_password BY 'ezpdf_password';

-- Gán quyền đầy đủ cho user này
GRANT ALL PRIVILEGES ON ezpdf.* TO 'ezpdf_user'@'%';

-- Xóa cache quyền
FLUSH PRIVILEGES;
