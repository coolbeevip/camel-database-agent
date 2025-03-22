## 请列出所有已支付订单的详细信息。
SELECT o.order_no, o.total_amount, p.payment_status FROM order_info o JOIN payment_info p ON o.order_id = p.order_id WHERE o.order_status = 1;

## 哪些用户在最近一个月内下过订单？
SELECT DISTINCT u.username FROM user u JOIN order_info o ON u.user_id = o.user_id WHERE o.created_at >= DATE('now', '-1 month');

## 我想知道每种支付方式的订单数量。
SQL查询: SELECT payment_method, COUNT(*) AS order_count FROM order_info GROUP BY payment_method;