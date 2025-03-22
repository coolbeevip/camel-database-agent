-- 用户表
CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- 用户ID
  username TEXT NOT NULL UNIQUE, -- 用户名
  password_hash TEXT NOT NULL, -- 密码哈希值
  mobile TEXT NOT NULL UNIQUE, -- 手机号
  email TEXT, -- 邮箱
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP -- 更新时间
); -- 用户信息表

-- 商品表
CREATE TABLE product (
  product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- 商品ID
  product_name TEXT NOT NULL, -- 商品名称
  description TEXT, -- 商品描述
  price REAL NOT NULL, -- 商品单价
  stock INTEGER NOT NULL DEFAULT 0, -- 库存数量
  status INTEGER NOT NULL DEFAULT 1, -- 状态(1:上架 0:下架)
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP -- 更新时间
); -- 商品信息表

-- 订单表
CREATE TABLE order_info (
  order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- 订单ID
  user_id INTEGER NOT NULL, -- 用户ID
  order_no TEXT NOT NULL UNIQUE, -- 订单编号（业务唯一）
  total_amount REAL NOT NULL, -- 订单总金额
  order_status INTEGER NOT NULL DEFAULT 0, -- 订单状态(0:待支付 1:已支付 2:已发货 3:已完成 4:已取消)
  payment_method TEXT, -- 支付方式
  address_id INTEGER NOT NULL, -- 收货地址ID
  payment_time DATETIME, -- 支付时间
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 更新时间
  FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (address_id) REFERENCES user_address (address_id) ON DELETE RESTRICT ON UPDATE CASCADE
); -- 订单主表

-- 订单明细表
CREATE TABLE order_item (
  item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- 明细ID
  order_id INTEGER NOT NULL, -- 订单ID
  product_id INTEGER NOT NULL, -- 商品ID
  quantity INTEGER NOT NULL, -- 购买数量
  unit_price REAL NOT NULL, -- 成交单价
  total_price REAL AS (quantity * unit_price) STORED, -- 明细总价
  FOREIGN KEY (order_id) REFERENCES order_info (order_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (product_id) REFERENCES product (product_id) ON DELETE RESTRICT ON UPDATE CASCADE
); -- 订单明细表

-- 用户地址表
CREATE TABLE user_address (
  address_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- 地址ID
  user_id INTEGER NOT NULL, -- 用户ID
  receiver TEXT NOT NULL, -- 收货人
  phone TEXT NOT NULL, -- 联系电话
  province TEXT NOT NULL, -- 省
  city TEXT NOT NULL, -- 市
  district TEXT NOT NULL, -- 区
  detail_address TEXT NOT NULL, -- 详细地址
  is_default INTEGER NOT NULL DEFAULT 0, -- 是否默认地址
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 更新时间
  FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE ON UPDATE CASCADE
); -- 用户地址表

-- 支付信息表
CREATE TABLE payment_info (
  payment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- 支付ID
  order_id INTEGER NOT NULL, -- 订单ID
  transaction_no TEXT NOT NULL UNIQUE, -- 第三方交易号
  payment_status TEXT NOT NULL, -- 支付状态
  payment_amount REAL NOT NULL, -- 实际支付金额
  payment_method TEXT NOT NULL, -- 支付方式
  payment_time DATETIME NOT NULL, -- 支付时间
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
  FOREIGN KEY (order_id) REFERENCES order_info (order_id) ON DELETE RESTRICT ON UPDATE CASCADE
); -- 支付信息表