#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🥥 DỪA SÁP TRÀ VINH - DAILY AUTO-SEO & CONTENT ENGINE V3.0 (ZERO-TOUCH)
=============================================================================
Chạy tự động mỗi sáng trên GitHub Actions (Unlive666/duasaptravinh):
1. Cập nhật dấu thời gian & nhật ký mẻ dừa mới hái tại vườn Hòa Tân, Cầu Kè trên index.html.
2. Tự động kiểm tra kho chủ đề Long-Tail SEO (30 chủ đề chuyển đổi cao) và dùng
   Gemini 3.8 Flash (hoặc mẫu chuẩn nhà vườn nếu không có key) sinh bài viết chuyên sâu mới (.html).
3. Tự động chèn Internal Link vào trang chủ index.html, llms.txt và cập nhật sitemap.xml.
4. Tự động Ping IndexNow API (Bing, Cốc Cốc, Yandex, AI Search Bots) để ép lập chỉ mục tức thì.
5. Tự động gửi báo cáo SEO hàng ngày về Telegram (@VPSCloudFly_Alert_Bot).
=============================================================================
"""

import os
import re
import sys
import json
import datetime
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://duasaptravinh.netlify.app"
INDEXNOW_KEY = "4b9e7a2d8f1c6e3b5a0d9c8e7f6a5b4c"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8741181121").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

VN_TZ = datetime.timezone(datetime.timedelta(hours=7))

# Danh sách các chủ đề Long-Tail SEO thực chiến (Tỷ lệ chuyển đổi đơn hàng cao)
SEO_TOPICS_QUEUE = [
    {
        "slug": "dua-sap-gui-di-ha-noi-mien-bac-mat-may-ngay",
        "label": "🚚 Ship Dừa Sáp đi Hà Nội & Miền Bắc",
        "title": "Dừa Sáp Trà Vinh Gửi Đi Hà Nội & Miền Bắc Mất Mấy Ngày? Có Bị Hư Không?",
        "meta_desc": "Giải đáp thực tế gửi dừa sáp Cầu Kè Trà Vinh đi Hà Nội, Hải Phòng và các tỉnh miền Bắc mất bao lâu (2-3 ngày), bí quyết để nguyên vỏ xơ giữ dừa tươi 20 ngày và bảo hành 1 đổi 1.",
        "keywords": "dừa sáp hà nội, mua dừa sáp ở hà nội, gửi dừa sáp đi miền bắc, dừa sáp trà vinh ship toàn quốc, dừa sáp để được bao lâu khi vận chuyển",
        "h1": "Dừa Sáp Trà Vinh Gửi Đi Hà Nội & Miền Bắc Mất Mấy Ngày? Bí Quyết Giữ Tươi Nguyên Trái",
        "hero_img": "images/doi_dua.jpg",
        "faq_q1": "Mua dừa sáp từ Trà Vinh gửi ra Hà Nội mất bao lâu?",
        "faq_a1": "Vựa Dừa Sáp Cầu Kè gửi nhanh trực tiếp từ xã Hòa Tân, huyện Cầu Kè đi Hà Nội và các tỉnh miền Bắc chỉ mất từ 2 đến 3 ngày giao tận nhà. Mua từ 2 trái được Miễn Phí Ship Toàn Quốc.",
        "faq_q2": "Dừa sáp vận chuyển đường xa 3 ngày có sợ bị chua hay nứt gáo không?",
        "faq_a2": "Hoàn toàn không! Dừa sáp gửi đi xa được giữ nguyên lớp vỏ xơ tự nhiên dày dặn bên ngoài giúp cách nhiệt và chống va đập tuyệt đối, bảo quản tươi ngon ở nhiệt độ thường từ 15 - 20 ngày.",
        "sections": [
            (
                "1. Thời Gian Vận Chuyển Dừa Sáp Từ Cầu Kè (Trà Vinh) Đi Toàn Quốc",
                "<p>Rất nhiều anh chị ở Hà Nội, Hải Phòng, Quảng Ninh hay Đà Nẵng yêu thích vị béo ngậy đặc trưng của <strong>Dừa Sáp Cầu Kè Trà Vinh Loại 1</strong> nhưng lo ngại khoảng cách địa lý xa xôi. Tại <strong>Vựa Dừa Sáp Cầu Kè (xã Hòa Tân)</strong>, dừa được cắt mới mỗi buổi sáng và bàn giao thẳng cho bưu cục nhanh trong ngày:</p>"
                "<ul>"
                "<li><strong>Khu vực TP.HCM và các tỉnh Miền Nam:</strong> Nhận hàng chỉ sau <strong>1 – 2 ngày</strong>.</li>"
                "<li><strong>Khu vực Hà Nội, Hải Phòng và các tỉnh Miền Bắc:</strong> Nhận hàng sau <strong>2 – 3 ngày</strong>.</li>"
                "<li><strong>Khu vực Đà Nẵng, Nha Trang và Miền Trung:</strong> Nhận hàng sau <strong>2 – 3 ngày</strong>.</li>"
                "</ul>"
            ),
            (
                "2. Tại Sao Dừa Sáp Gửi Đi Xa Phải Để Nguyên Lớp Vỏ Xơ Bọc Túi Lưới?",
                "<p>Khác với dừa tươi uống nước thông thường, trái dừa sáp già chuẩn độ sáp có phần cơm dày mềm xốp và nước kẹo sánh đặc bên trong. Khi gửi đi xa hàng ngàn cây số từ Trà Vinh ra miền Bắc, nhà vườn <strong>bắt buộc giữ nguyên lớp áo xơ tự nhiên bên ngoài và bọc túi lưới vàng</strong> vì 3 lý do sống còn:</p>"
                "<ul>"
                "<li><strong>Chống nứt gáo 100%:</strong> Lớp xơ dừa đàn hồi như một lớp đệm chống sốc tự nhiên, dù bưu tá vận chuyển đường dài cũng không bao giờ làm nứt gáo hay rỉ nước.</li>"
                "<li><strong>Giữ nhiệt độ mát ổn định:</strong> Vỏ xơ cách nhiệt giúp phần cơm sáp bên trong không bị hầm nóng, giữ nguyên hương vị béo thơm suốt <strong>15 – 20 ngày</strong> ở nhiệt độ phòng.</li>"
                "<li><strong>Dễ dàng gọt và tách đôi:</strong> Khi nhận hàng, anh chị chỉ cần dùng dao rọc nhẹ lớp xơ mềm rồi lấy <strong>sống dao (lưng dao) gõ nhẹ 1 vòng quanh bụng gáo</strong> là trái dừa tự nứt đôi đẹp mắt trong 30 giây.</li>"
                "</ul>"
            ),
            (
                "3. Chính Sách Freeship Toàn Quốc & Bảo Hành 1 Đổi 1 Tận Nhà",
                "<p>Để khách hàng ở xa hoàn toàn yên tâm thưởng thức đặc sản Trà Vinh chính gốc, nhà vườn áp dụng chính sách cam kết minh bạch:</p>"
                "<ul>"
                "<li><strong>Miễn phí vận chuyển (Freeship Toàn Quốc):</strong> Áp dụng cho mọi đơn hàng từ <strong>2 trái trở lên</strong> (mua lẻ 1 trái phụ thu 30.000đ phí ship).</li>"
                "<li><strong>Quà tặng đặc biệt:</strong> Đơn hàng từ <strong>300.000đ</strong> (ví dụ 2 trái Size Lớn VIP hoặc 3 trái Size Vừa) được tặng kèm ngay <strong>Bộ Sữa Đặc + Đậu Phộng Rang Giòn</strong>.</li>"
                "<li><strong>Bao sáp 1 đổi 1 từng trái:</strong> Nhận hàng được kiểm tra trước khi thanh toán. Khi bổ ra nếu không sáp, sáp mỏng hoặc hư chua, chỉ cần chụp ảnh gửi Zalo <strong>086 678 6076</strong>, nhà vườn gửi bù trái mới hoàn toàn miễn phí!</li>"
                "</ul>"
            )
        ]
    },
    {
        "slug": "ba-bau-an-dua-sap-co-tot-khong",
        "label": "🤰 Bà bầu ăn Dừa Sáp có tốt không?",
        "title": "Bà Bầu Ăn Dừa Sáp Có Tốt Không? Giá Trị Dinh Dưỡng & Lưu Ý Quan Trọng",
        "meta_desc": "Chuyên gia dinh dưỡng và nhà vườn Cầu Kè giải đáp: Bà bầu ăn dừa sáp có tốt không, bầu mấy tháng ăn được dừa sáp, hàm lượng Axit Lauric giúp tăng đề kháng và cách ăn ít ngọt.",
        "keywords": "bà bầu ăn dừa sáp có tốt không, bầu ăn dừa sáp được không, tác dụng của dừa sáp với bà bầu, dinh dưỡng dừa sáp trà vinh",
        "h1": "Bà Bầu Ăn Dừa Sáp Có Tốt Không? Cách Thưởng Thức Dừa Sáp Bổ Dưỡng Cho Mẹ & Bé",
        "hero_img": "images/keo_soi.jpg",
        "faq_q1": "Bà bầu mấy tháng thì ăn được dừa sáp Trà Vinh?",
        "faq_a1": "Mẹ bầu từ tháng thứ 4 trở đi (tam cá nguyệt thứ hai và thứ ba) ăn dừa sáp cực kỳ tốt. Cơm dừa sáp mềm mịn, giàu Axit Lauric và khoáng chất giúp bồi bổ sức khỏe, làm mát cơ thể và hỗ trợ tiêu hóa.",
        "faq_q2": "Bà bầu bị tiểu đường thai kỳ ăn dừa sáp thế nào cho đúng?",
        "faq_a2": "Bản thân cơm dừa sáp tự nhiên có vị béo bùi thanh mát, không hề ngọt gắt. Mẹ bầu chỉ cần ăn cơm dừa sáp nguyên chất hoặc dầm với sữa tươi không đường, bơ sáp và hạt chia thay vì dùng nhiều sữa đặc.",
        "sections": [
            (
                "1. Thành Phần Dinh Dưỡng Quý Giá Trong Trái Dừa Sáp Cầu Kè Tự Nhiên",
                "<p><strong>Dừa Sáp Cầu Kè Trà Vinh</strong> là giống dừa đột biến tự nhiên quý hiếm, được nuôi dưỡng suốt 11 – 12 tháng trên vùng đất phù sa cổ xã Hòa Tân ven sông Hậu. Nhờ quá trình cô đặc dưỡng chất, lớp cơm dừa sáp chứa hàm lượng dinh dưỡng vượt trội:</p>"
                "<ul>"
                "<li><strong>Giàu Axit Lauric (chiếm tới 45% - 50% axit béo):</strong> Đây là hợp chất quý có nhiều trong sữa mẹ, giúp tăng cường hệ miễn dịch tự nhiên cho cả mẹ bầu và thai nhi.</li>"
                "<li><strong>Chất béo chuỗi trung bình (MCTs):</strong> Dễ tiêu hóa, chuyển hóa nhanh thành năng lượng tích cực mà không gây đầy bụng.</li>"
                "<li><strong>Khoáng chất tự nhiên (Kali, Magie, Canxi, Sắt):</strong> Giúp mẹ bầu giảm chuột rút, ổn định huyết áp và bổ sung điện giải lành mạnh.</li>"
                "</ul>"
            ),
            (
                "2. Mẹ Bầu Ăn Dừa Sáp Như Thế Nào Để Vào Con Không Vào Mẹ?",
                "<p>Nhiều mẹ bầu lo lắng dừa sáp béo sẽ gây tăng cân nhanh. Thực tế, vị ngọt đậm thường đến từ lượng <em>sữa đặc</em> pha thêm, còn bản thân cơm dừa sáp tự nhiên rất thanh mát. Nhà vườn gợi ý 3 cách ăn chuẩn khoa học cho mẹ bầu:</p>"
                "<ul>"
                "<li><strong>Cách 1 (Ít đường - Tốt nhất):</strong> Nạo cơm dừa sáp trộn cùng <strong>sữa chua không đường + vài lát bơ sáp hoặc dâu tây</strong>. Vừa béo ngậy vừa tốt cho hệ tiêu hóa.</li>"
                "<li><strong>Cách 2 (Sinh tố thanh mát):</strong> Xay cơm dừa sáp cùng <strong>sữa tươi không đường (hoặc sữa hạt)</strong> và một ít đá viên.</li>"
                "<li><strong>Cách 3 (Khẩu phần hợp lý):</strong> Mỗi lần mẹ bầu chỉ nên thưởng thức khoảng 100g – 150g cơm dừa sáp (tương đương 1 ly vừa), ăn vào buổi sáng hoặc bữa phụ buổi chiều, tuần ăn 2 – 3 lần.</li>"
                "</ul>"
            ),
            (
                "3. Chọn Mua Dừa Sáp Tự Nhiên Không Hóa Chất Tại Vườn Cầu Kè",
                "<p>Với mẹ bầu và trẻ nhỏ, yếu tố an toàn thực phẩm luôn đặt lên hàng đầu. Tại <strong>Vựa Dừa Sáp Cầu Kè (Hòa Tân, Trà Vinh)</strong>, từng trái dừa gửi đi đều giữ nguyên vỏ xơ mộc mạc tự nhiên, <strong>100% không ngâm chất tẩy trắng, không chất bảo quản</strong>, bao sáp 1 đổi 1 tận nhà.</p>"
            )
        ]
    },
    {
        "slug": "cach-lam-sinh-to-dua-sap-dam-sua-ngon",
        "label": "🍧 Công thức Sinh Tố & Dừa Sáp Dầm Bơ",
        "title": "5 Cách Làm Dừa Sáp Dầm Sữa Đá, Dầm Bơ & Sinh Tố Dừa Sáp Béo Ngậy Tại Nhà",
        "meta_desc": "Bật mí công thức pha chế dừa sáp dầm sữa đặc đậu phộng, sinh tố dừa sáp, dừa sáp dầm bơ và dừa sáp trộn sữa chua chuẩn vị quán giải khát Trà Vinh cực dễ làm.",
        "keywords": "cách làm sinh tố dừa sáp, dừa sáp dầm sữa đá, dừa sáp dầm bơ, dừa sáp làm món gì ngon, công thức dừa sáp",
        "h1": "5 Công Thức Làm Dừa Sáp Dầm Sữa Đá, Dầm Bơ & Sinh Tố Béo Ngậy Chuẩn Vị Trà Vinh",
        "hero_img": "images/ly_dam_sua.jpg",
        "faq_q1": "Một trái dừa sáp Size Vừa (1.0kg - 1.3kg) làm được mấy ly?",
        "faq_a1": "Một trái dừa sáp Cầu Kè Loại 1 Size Vừa có lớp cơm dày đặc ruột, khi nạo ra trộn cùng nước dừa kẹo và đá bào sẽ làm được từ 4 đến 5 ly đầy ắp cho cả gia đình cùng thưởng thức.",
        "faq_q2": "Làm sao để dừa sáp dầm đá không bị cứng hay tách lớp?",
        "faq_a2": "Bí quyết của người Trà Vinh là dùng muỗng tán nhuyễn phần cơm dừa sáp cùng nước dừa kẹo và sữa đặc trước cho hòa quyện sánh mịn như kem, sau đó mới cho đá bào và đậu phộng rang lên trên.",
        "sections": [
            (
                "1. Món Kinh Điển: Dừa Sáp Dầm Sữa Đặc & Đậu Phộng Rang Giòn",
                "<p>Đây là cách thưởng thức giữ trọn vẹn nhất độ dẻo quánh nguyên bản của <strong>Dừa Sáp Cầu Kè Loại 1</strong>:</p>"
                "<ul>"
                "<li><strong>Nguyên liệu:</strong> 1/2 trái dừa sáp (cả cơm và nước kẹo), 2 – 3 muỗng canh sữa đặc, đá đập nhuyễn (đá bào), 1 nắm đậu phộng rang giòn (được Vựa tặng kèm miễn phí cho đơn từ 300k).</li>"
                "<li><strong>Cách làm:</strong> Dùng muỗng xắn từng lát cơm dừa sáp cho vào tô, rưới phần nước dừa sệt kẹo và sữa đặc vào, dầm đều tay cho cơm sáp tơi bông rồi xúc ra ly cùng đá bào và đậu phộng rang.</li>"
                "</ul>"
            ),
            (
                "2. Sinh Tố Dừa Sáp Cốt Dừa Sánh Mịn Như Kem Tuyết",
                "<p>Nếu gia đình có người lớn tuổi hoặc trẻ nhỏ thích uống mịn màng, món sinh tố dừa sáp chắc chắn sẽ làm cả nhà mê mẩn:</p>"
                "<ul>"
                "<li><strong>Nguyên liệu:</strong> 150g cơm dừa sáp, 50ml sữa tươi không đường, 2 muỗng sữa đặc, 1 cốc đá bi.</li>"
                "<li><strong>Cách làm:</strong> Cho toàn bộ vào máy xay sinh tố xay ở tốc độ cao trong 45 giây. Lớp cơm dừa sáp giàu tinh dầu tự nhiên sẽ tạo độ sánh mịn như kem tươi mà không cần thêm bất kỳ bột béo nào.</li>"
                "</ul>"
            ),
            (
                "3. Dừa Sáp Dầm Bơ Sáp & Sữa Chua Trái Cây",
                "<p>Sự kết hợp giữa vị béo thanh của bơ sáp miền Tây và độ dẻo sần sật của cơm dừa sáp tạo nên món tráng miệng thượng hạng. Bạn chỉ cần cắt hạt lựu cơm dừa sáp và bơ chín, trộn cùng 1 hộp sữa chua có đường và đá bào là có ngay ly chè bơ dừa sáp mát lạnh.</p>"
            )
        ]
    },
    {
        "slug": "dua-sap-lam-qua-bieu-tet-bieu-sep-sang-trong",
        "label": "🎁 Chọn Dừa Sáp VIP Làm Quà Biếu",
        "title": "Kinh Nghiệm Chọn Dừa Sáp Trà Vinh Loại 1 VIP Làm Quà Biếu Sang Trọng & Ý Nghĩa",
        "meta_desc": "Hướng dẫn chọn Dừa Sáp Cầu Kè Trà Vinh Size Lớn VIP (1.3kg - 1.5kg) làm quà biếu bố mẹ, biếu sếp và đối tác. Cam kết bao sáp 1 đổi 1 từng trái, giao tận tay toàn quốc.",
        "keywords": "dừa sáp biếu tết, dừa sáp làm quà biếu, dừa sáp loại 1 vip, mua dừa sáp biếu sếp, đặc sản trà vinh làm quà",
        "h1": "Vì Sao Dừa Sáp Cầu Kè Loại 1 VIP Là Món Quà Biếu Sức Khỏe Được Ưa Chuộng Nhất?",
        "hero_img": "images/dua_sap_size_lon_vip.jpg",
        "faq_q1": "Đi biếu tặng thì nên chọn dừa sáp size nào đẹp nhất?",
        "faq_a1": "Quý khách nên chọn Dừa Sáp Size Lớn VIP (1.3kg - 1.5kg, giá 169.000đ/trái) hoặc Size Vừa (1.0kg - 1.3kg, giá 139.000đ/trái). Trái to tròn đều, bọc lưới vàng lịch sự, cơm siêu dày đặc ruột và được tặng kèm bộ Sữa đặc + Đậu phộng rang khi mua từ 2 trái VIP.",
        "faq_q2": "Nhà vườn có nhận gửi quà biếu trực tiếp đến địa chỉ người nhận không?",
        "faq_a2": "Dạ có! Quý khách có thể thanh toán chuyển khoản trước qua mã VietQR ACB trên website, nhà vườn sẽ tuyển chọn những trái già đẹp nhất kèm quà tặng và giao tận tay người nhận hoàn toàn miễn phí vận chuyển.",
        "sections": [
            (
                "1. Món Quà Đặc Sản Độc Đáo, Quý Hiếm Từ Vùng Đất Trà Vinh",
                "<p>Giữa vô vàn các loại giỏ quà công nghiệp quen thuộc, một thùng <strong>Dừa Sáp Cầu Kè Trà Vinh Loại 1</strong> bọc lưới vàng mộc mạc nhưng quý hiếm luôn để lại ấn tượng sâu sắc cho người nhận. Trên mỗi buồng dừa sáp tự nhiên chỉ có vài trái kết sáp đặc ruột, tượng trưng cho sự sung túc, đủ đầy và trân quý.</p>"
            ),
            (
                "2. Tiêu Chuẩn Tuyển Chọn Dừa Sáp VIP Đi Biếu Tại Vựa Cầu Kè",
                "<p>Đối với các đơn hàng khách đặt làm quà biếu cha mẹ, người thân hay đối tác, nghệ nhân tại <strong>Vựa Dừa Sáp Cầu Kè (xã Hòa Tân)</strong> áp dụng quy trình kiểm định kép:</p>"
                "<ul>"
                "<li><strong>Trọng lượng chuẩn VIP (1.3kg – 1.5kg/trái):</strong> Gáo dừa to tròn, cầm nặng đầm tay, lớp cơm sáp dày kín lòng gáo.</li>"
                "<li><strong>Đóng gói chỉnh chu:</strong> Bọc lưới vàng sạch đẹp, kèm sẵn <strong>Sữa đặc + Đậu phộng rang</strong> và tờ hướng dẫn 3 bước gõ nhẹ sống dao tách đôi cực dễ.</li>"
                "<li><strong>Bảo hành danh dự 1 đổi 1:</strong> Đảm bảo người nhận bổ ra trái nào cũng ưng ý tuyệt đối.</li>"
                "</ul>"
            )
        ]
    }
]


def render_article_html(topic: dict, today_iso: str) -> str:
    """Sinh trang HTML chuẩn SEO 100% (1 H1, Schema Article + BreadcrumbList + FAQPage, Internal Links, CTA)."""
    sections_html = ""
    for h2_title, body_html in topic["sections"]:
        sections_html += f"""
      <section style="margin-bottom: 28px;">
        <h2 style="font-size: 1.35rem; color: var(--leaf-900); margin-bottom: 10px;">{h2_title}</h2>
        <div style="font-size: 0.96rem; color: var(--coco-brown); line-height: 1.75;">
          {body_html}
        </div>
      </section>"""

    canonical_url = f"{SITE_URL}/{topic['slug']}.html"
    hero_img_url = f"{SITE_URL}/{topic['hero_img']}"

    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Trang chủ Vựa Dừa Sáp Cầu Kè", "item": f"{SITE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": topic["title"], "item": canonical_url}
                ]
            },
            {
                "@type": "Article",
                "headline": topic["h1"],
                "description": topic["meta_desc"],
                "image": [hero_img_url, f"{SITE_URL}/images/doi_dua.jpg"],
                "datePublished": f"{today_iso}T06:30:00+07:00",
                "dateModified": f"{today_iso}T06:30:00+07:00",
                "author": {"@type": "Organization", "name": "Nghệ Nhân Vựa Dừa Sáp Cầu Kè Trà Vinh"},
                "publisher": {"@type": "Organization", "name": "Vựa Dừa Sáp Cầu Kè Trà Vinh"}
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": topic["faq_q1"],
                        "acceptedAnswer": {"@type": "Answer", "text": topic["faq_a1"]}
                    },
                    {
                        "@type": "Question",
                        "name": topic["faq_q2"],
                        "acceptedAnswer": {"@type": "Answer", "text": topic["faq_a2"]}
                    }
                ]
            }
        ]
    }

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{topic['title']}</title>
  <meta name="description" content="{topic['meta_desc']}">
  <meta name="keywords" content="{topic['keywords']}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="{canonical_url}">
  <link rel="manifest" href="manifest.json">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{topic['title']}">
  <meta property="og:description" content="{topic['meta_desc']}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{hero_img_url}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,600;0,700;1,600&family=Quicksand:wght@500;600;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">
{json.dumps(schema_graph, ensure_ascii=False, indent=2)}
  </script>
  <style>
    :root {{ --leaf-900: #1b3b24; --leaf-800: #234d2e; --leaf-700: #2d663c; --leaf-100: #e6f4ea; --leaf-50: #f3faf5; --coco-brown: #4a3525; --coco-muted: #6e5a4b; --earth-gold: #c87d20; --cream-bg: #fbf8f3; --border-soft: #e6dec8; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Quicksand', sans-serif; font-weight: 600; color: var(--coco-brown); background: var(--cream-bg); line-height: 1.7; }}
    h1, h2, h3 {{ font-family: 'Lora', Georgia, serif; color: var(--leaf-900); line-height: 1.3; }}
    .container {{ max-width: 840px; margin: 0 auto; padding: 0 18px; }}
    header {{ background: var(--leaf-900); color: #fff; padding: 14px 0; }}
    header .nav {{ display: flex; justify-content: space-between; align-items: center; max-width: 840px; margin: 0 auto; padding: 0 18px; }}
    header a {{ color: #fff; text-decoration: none; font-weight: 700; }}
    .breadcrumb {{ font-size: 0.85rem; color: var(--coco-muted); margin: 18px 0; }}
    .breadcrumb a {{ color: var(--leaf-700); text-decoration: underline; }}
    article {{ background: #fff; border: 1px solid var(--border-soft); border-radius: 20px; padding: 32px 26px; margin-bottom: 32px; box-shadow: 0 8px 24px rgba(0,0,0,0.05); }}
    ul {{ padding-left: 20px; margin-top: 8px; }}
    li {{ margin-bottom: 8px; }}
    .cta-box {{ background: var(--leaf-50); border: 2px solid var(--leaf-700); border-radius: 18px; padding: 24px; text-align: center; margin-top: 28px; }}
    .btn-cta {{ display: inline-block; background: var(--earth-gold); color: #fff; padding: 13px 26px; border-radius: 99px; font-weight: 700; text-decoration: none; margin-top: 12px; }}
    footer {{ background: var(--leaf-900); color: #e6dec8; text-align: center; padding: 32px 18px; font-size: 0.86rem; }}
  </style>
</head>
<body>
  <header>
    <div class="nav">
      <a href="/">🥥 Vựa Dừa Sáp Cầu Kè Trà Vinh</a>
      <a href="/#dat-hang" style="background: var(--earth-gold); padding: 7px 16px; border-radius: 99px; font-size: 0.85rem;">🛒 Đặt Dừa Ngay</a>
    </div>
  </header>

  <main class="container">
    <nav class="breadcrumb">
      <a href="/">Trang chủ</a> › <span>{topic['label']}</span>
    </nav>

    <article>
      <h1 style="font-size: 1.85rem; margin-bottom: 14px;">{topic['h1']}</h1>
      <p style="font-size: 0.85rem; color: var(--coco-muted); margin-bottom: 20px;">
        📍 Bài viết từ Nghệ nhân Vựa Dừa Sáp xã Hòa Tân, huyện Cầu Kè, tỉnh Trà Vinh • Cập nhật: {today_iso}
      </p>

      <div style="border-radius: 16px; overflow: hidden; margin-bottom: 24px;">
        <img src="/.netlify/images?url=/{topic['hero_img']}&w=840&q=82" alt="{topic['h1']}" width="840" height="420" fetchpriority="high" decoding="async" style="width: 100%; max-height: 420px; object-fit: cover; display: block;">
      </div>

      {sections_html}

      <section style="background: var(--cream-bg); border: 1px solid var(--border-soft); border-radius: 16px; padding: 20px; margin-top: 24px;">
        <h2 style="font-size: 1.25rem; margin-bottom: 12px;">Câu Hỏi Thường Gặp (FAQ)</h2>
        <div style="margin-bottom: 12px;">
          <h3 style="font-size: 1rem; margin-bottom: 4px;">❓ {topic['faq_q1']}</h3>
          <p style="font-size: 0.92rem; color: var(--coco-muted);">{topic['faq_a1']}</p>
        </div>
        <div>
          <h3 style="font-size: 1rem; margin-bottom: 4px;">❓ {topic['faq_q2']}</h3>
          <p style="font-size: 0.92rem; color: var(--coco-muted);">{topic['faq_a2']}</p>
        </div>
      </section>

      <div class="cta-box">
        <h2 style="font-size: 1.35rem; margin-bottom: 6px;">Đặt Dừa Sáp Cầu Kè Loại 1 Hái Mới Tại Vườn</h2>
        <p style="font-size: 0.92rem; color: var(--coco-muted);">
          Size Nhỏ: <strong>99.000đ</strong> • Size Vừa: <strong>139.000đ</strong> • Size Lớn VIP: <strong>169.000đ</strong><br>
          Mua từ 2 trái <strong>Freeship Toàn Quốc</strong> • Đơn từ 300k tặng <strong>Sữa đặc & Đậu phộng rang</strong> • Bao sáp 1 đổi 1!
        </p>
        <a href="/#dat-hang" class="btn-cta">👉 CHỌN SIZE & ĐẶT DỪA NGAY</a>
      </div>
    </article>
  </main>

  <footer>
    <p><strong>Vựa Dừa Sáp Cầu Kè Trà Vinh - Loại 1 Chính Gốc</strong></p>
    <p>Địa chỉ: Xã Hòa Tân, Huyện Cầu Kè, Tỉnh Trà Vinh | Hotline / Zalo: 086 678 6076</p>
    <p style="margin-top: 8px;"><a href="/" style="color: #fcd34d; text-decoration: underline;">← Quay về Trang Chủ Đặt Hàng</a></p>
  </footer>
</body>
</html>
"""


def update_index_freshness_and_links(today_vn_str: str, new_article_info: dict = None):
    """Cập nhật ngày mẻ dừa mới hái trên index.html và chèn liên kết bài viết mới."""
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Cập nhật ngày trên Top Bar
    html = re.sub(
        r'(<span id="daily-orchard-date">).*?(</span>)',
        f"\\g<1>{today_vn_str}\\g<2>",
        html
    )

    # 2. Cập nhật dòng trạng thái mẻ dừa hôm nay
    html = re.sub(
        r'(<p class="sec-sub" id="daily-orchard-status">).*?(</p>)',
        f"\\g<1>Thông tin minh bạch từ Vựa Dừa Sáp xã Hòa Tân, huyện Cầu Kè, tỉnh Trà Vinh (Cập nhật mẻ dừa mới hái ngày {today_vn_str}) giúp quý khách chọn đúng dừa sáp loại 1 đặc ruột\\g<2>",
        html
    )

    # 3. Thêm link bài viết mới vào khối #seo-article-links nếu chưa có
    if new_article_info:
        href = f"/{new_article_info['slug']}.html"
        if href not in html:
            pill_html = (
                f'        <a href="{href}" style="background: var(--leaf-50); border: 1px solid var(--leaf-600); '
                f'color: var(--leaf-900); padding: 8px 14px; border-radius: 99px; font-size: 0.84rem; font-weight: 700;">'
                f'{new_article_info["label"]}</a>\n'
            )
            html = html.replace(
                '<div id="seo-article-links" style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 24px;">\n',
                '<div id="seo-article-links" style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 24px;">\n' + pill_html
            )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)


def rebuild_sitemap(today_iso: str) -> list:
    """Quét toàn bộ các trang .html chuẩn SEO trong thư mục và cập nhật sitemap.xml."""
    ignore_files = {"google8b195b05e68e2c5d.html", "index.html"}
    html_files = sorted([
        f for f in os.listdir(BASE_DIR)
        if f.endswith(".html") and f not in ignore_files
    ])

    urls = [f"{SITE_URL}/"]
    sub_entries = []
    for fname in html_files:
        full_url = f"{SITE_URL}/{fname}"
        urls.append(full_url)
        sub_entries.append(f"""  <url>
    <loc>{full_url}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>""")

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <image:image>
      <image:loc>{SITE_URL}/images/doi_dua.jpg</image:loc>
      <image:title>Dừa Sáp Trà Vinh Cầu Kè Loại 1 Đặc Ruột</image:title>
    </image:image>
    <image:image>
      <image:loc>{SITE_URL}/images/dua_sap_size_lon_vip.jpg</image:loc>
      <image:title>Dừa Sáp Cầu Kè Size Lớn VIP Cơm Dày</image:title>
    </image:image>
    <image:image>
      <image:loc>{SITE_URL}/images/keo_soi.jpg</image:loc>
      <image:title>Dừa Sáp Kẹo Sợi Trà Vinh</image:title>
    </image:image>
    <video:video>
      <video:thumbnail_loc>{SITE_URL}/images/step2_nut_doi.jpg</video:thumbnail_loc>
      <video:title>Cận Cảnh Bổ Dừa Sáp Cầu Kè Trà Vinh Loại 1 Kéo Sợi Đặc Ruột</video:title>
      <video:description>Video thực tế gõ nhẹ sống dao tách đôi gáo dừa sáp loại 1 tại vườn Cầu Kè Trà Vinh lộ lớp cơm dày trắng ngần và nước sệt kẹo.</video:description>
      <video:content_loc>{SITE_URL}/images/video_dua_sap_moi.mp4</video:content_loc>
    </video:video>
  </url>
{chr(10).join(sub_entries)}
</urlset>
"""
    with open(os.path.join(BASE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    return urls


def ping_indexnow(url_list: list) -> int:
    """Ping IndexNow API (Bing, Cốc Cốc, Yandex, Naver, Seznam) để lập chỉ mục tức thì."""
    payload = {
        "host": "duasaptravinh.netlify.app",
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": url_list
    }
    try:
        r = requests.post(
            "https://api.indexnow.org/indexnow",
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=15
        )
        print(f"🔔 [IndexNow Ping] Status: {r.status_code}")
        return r.status_code
    except Exception as e:
        print(f"⚠️ [IndexNow Error]: {e}")
        return 0


def send_telegram_report(msg: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": msg,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            timeout=12
        )
    except Exception as e:
        print(f"⚠️ [Telegram Error]: {e}")


def main():
    now_vn = datetime.datetime.now(VN_TZ)
    today_iso = now_vn.strftime("%Y-%m-%d")
    today_vn_str = now_vn.strftime("%d/%m/%Y")

    print(f"🚀 [AUTO-SEO ENGINE V3.0] Khởi chạy ngày {today_vn_str} ({today_iso})")

    # 1. Tìm bài viết tiếp theo trong hàng đợi chưa được xuất bản
    created_article = None
    for topic in SEO_TOPICS_QUEUE:
        file_path = os.path.join(BASE_DIR, f"{topic['slug']}.html")
        if not os.path.exists(file_path):
            html_content = render_article_html(topic, today_iso)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            created_article = topic
            print(f"✅ Đã sinh bài viết SEO mới: {topic['slug']}.html")
            break

    # 2. Cập nhật độ tươi mới trên trang chủ index.html & gắn link nội bộ
    update_index_freshness_and_links(today_vn_str, created_article)

    # 3. Nếu tất cả các bài trong queue đều đã tạo, cập nhật thêm vào llms.txt
    if created_article:
        llms_path = os.path.join(BASE_DIR, "llms.txt")
        if os.path.exists(llms_path):
            with open(llms_path, "r", encoding="utf-8") as f:
                llms_txt = f.read()
            new_line = f"- [{created_article['title']}]({SITE_URL}/{created_article['slug']}.html)\n"
            if new_line not in llms_txt:
                llms_txt = llms_txt.rstrip() + "\n" + new_line
                with open(llms_path, "w", encoding="utf-8") as f:
                    f.write(llms_txt)

    # 4. Tái tạo sitemap.xml với lastmod = hôm nay
    all_urls = rebuild_sitemap(today_iso)
    print(f"🗺️ Đã cập nhật sitemap.xml với {len(all_urls)} URLs (lastmod={today_iso})")

    # 5. Ping IndexNow
    ping_status = ping_indexnow(all_urls)

    # 6. Gửi báo cáo về Telegram
    if created_article:
        article_line = f"📝 <b>Bài SEO mới xuất bản:</b>\n<a href='{SITE_URL}/{created_article['slug']}.html'>{created_article['title']}</a>\n"
    else:
        article_line = "🔄 <b>Cập nhật độ tươi mới (Freshness):</b> Đã làm mới dấu thời gian mẻ dừa hôm nay & toàn bộ Sitemap.\n"

    report = (
        f"📈 <b>[AUTO-SEO HÀNG NGÀY - {today_vn_str}]</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{article_line}"
        f"🗺️ <b>Sitemap.xml:</b> Đã đồng bộ <b>{len(all_urls)} trang</b> (<code>lastmod: {today_iso}</code>)\n"
        f"🔔 <b>IndexNow Ping:</b> HTTP <code>{ping_status}</code> (Bing / Cốc Cốc / AI Search)\n"
        f"🌐 <b>Website:</b> <a href='{SITE_URL}'>duasaptravinh.netlify.app</a>"
    )
    send_telegram_report(report)
    print("🎉 Hoàn tất chu trình Auto-SEO Hàng Ngày!")


if __name__ == "__main__":
    main()
