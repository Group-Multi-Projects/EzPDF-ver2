style_response = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }
        body {
            background-color: #f8f8f8;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .container {
            max-width: 600px;
        }
        h1 {
            font-size: 100px;
            color: #ff5252;
            animation: bounce 1s infinite alternate;
        }
        p {
            font-size: 20px;
            margin-bottom: 20px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            font-size: 18px;
            color: white;
            background-color: #007bff;
            text-decoration: none;
            border-radius: 5px;
            transition: 0.3s;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        @keyframes bounce {
            from {
                transform: translateY(0);
            }
            to {
                transform: translateY(-10px);
            }
        }
"""
body_response = """
    <div class="container">
        <h1>404</h1>
        <p>Xin lỗi, trang bạn tìm kiếm không tồn tại.</p>
        <a href="/" class="btn">Quay về trang chủ</a>
    </div>
    """