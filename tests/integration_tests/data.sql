-- 插入用户数据
INSERT INTO `user` (`username`, `password_hash`, `mobile`, `email`) VALUES
('张三', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '13800138000', 'john@example.com'),
('李四', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', '13912345678', 'jane@test.com'),
('王五', '6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4', '13698765432', NULL);

-- 插入商品数据
INSERT INTO `product` (`product_name`, `description`, `price`, `stock`) VALUES
('iPhone 15', '6.1英寸 128GB 黑色', 6999.00, 100),
('小米电视65寸', '4K超高清智能电视', 3299.00, 50),
('华为MateBook X', '13英寸轻薄笔记本', 8999.00, 30),
('耐克运动鞋', 'Air Max 270 男款', 899.00, 200),
('《深入浅出MySQL》', '数据库技术书籍', 99.90, 500);

-- 插入用户地址（每个用户1个地址）
INSERT INTO `user_address` (`user_id`, `receiver`, `phone`, `province`, `city`, `district`, `detail_address`) VALUES
(1, '张三', '13800138000', '北京市', '市辖区', '朝阳区', '建国路88号'),
(2, '李四', '13912345678', '上海市', '市辖区', '浦东新区', '陆家嘴环路100号'),
(3, '王五', '13698765432', '广东省', '深圳市', '南山区', '科技园路1号');

-- 插入订单数据（3个订单）
INSERT INTO `order_info` (`user_id`, `order_no`, `total_amount`, `order_status`, `payment_method`, `address_id`, `payment_time`) VALUES
(1, 'ORDER202311011001', 13998.00, 1, 'ALIPAY', 1, '2023-11-01 10:05:00'),
(2, 'ORDER202311021002', 12197.00, 1, 'WECHAT', 2, '2023-11-02 14:30:00'),
(3, 'ORDER202311031003', 199.80, 0, NULL, 3, NULL);

-- 插入订单明细
INSERT INTO `order_item` (`order_id`, `product_id`, `quantity`, `unit_price`) VALUES
-- 订单1（购买2个iPhone）
(1, 1, 2, 6999.00),
-- 订单2（1台电视+1本书）
(2, 2, 1, 3299.00),
(2, 5, 2, 99.90),
-- 订单3（2双运动鞋）
(3, 4, 2, 899.00);

-- 插入支付信息（已完成支付的订单）
INSERT INTO `payment_info` (`order_id`, `transaction_no`, `payment_status`, `payment_amount`, `payment_method`, `payment_time`) VALUES
(1, 'PAY20231101123456', 'SUCCESS', 13998.00, 'ALIPAY', '2023-11-01 10:05:00'),
(2, 'PAY20231102567890', 'SUCCESS', 12197.00, 'WECHAT', '2023-11-02 14:30:00');