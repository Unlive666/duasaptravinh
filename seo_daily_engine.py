#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🥥 DỪA SÁP TRÀ VINH - DAILY AUTO-SEO & CONVERSION ENGINE V4.0 (UNSTOPPABLE)
=============================================================================
Chạy tự động mỗi sáng trên GitHub Actions (Unlive666/duasaptravinh):
1. Cập nhật dấu thời gian & nhật ký mẻ dừa mới hái tại vườn Hòa Tân, Cầu Kè trên index.html.
2. Kho 16 chủ đề Buyer-Intent SEO thực chiến (Tỷ lệ chuyển đổi đơn hàng cao nhất)
   + Cơ chế AI Autonomous Generator (Gemini 3.8 Flash / 3.6 Flash) tự động sinh chủ đề mới
   khi hàng đợi tĩnh đã xuất bản hết -> Không bao giờ cạn bài mới!
3. Trang bài viết chuẩn CRO: Tích hợp Bảng chọn nhanh 3 Size (Deep-link tự điền giỏ hàng),
   Sticky Mobile Conversion Bar (Zalo + Gọi + Đặt 2 Trái Freeship) & Topic Cluster Links.
4. Tự động chèn Internal Link vào index.html, llms.txt, cập nhật sitemap.xml và Ping IndexNow.
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
SITE_URL = "https://duasaptravinh.vercel.app"
INDEXNOW_KEY = "4b9e7a2d8f1c6e3b5a0d9c8e7f6a5b4c"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8741181121").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

VN_TZ = datetime.timezone(datetime.timedelta(hours=7))

# =============================================================================
# KHO 16 CHỦ ĐỀ BUYER-INTENT SEO CHUYỂN ĐỔI ĐƠN HÀNG TRỰC TIẾP
# =============================================================================
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
    },
    {
        "slug": "mua-dua-sap-tra-vinh-o-tphcm-sai-gon-giao-nhanh",
        "label": "🏙️ Mua Dừa Sáp tại TP.HCM Giao 1 Ngày",
        "title": "Mua Dừa Sáp Trà Vinh Ở TP.HCM Ở Đâu Uy Tín? Giá Gốc Tại Vườn Giao Nhanh 1 Ngày",
        "meta_desc": "Địa chỉ đặt mua Dừa Sáp Cầu Kè Trà Vinh Loại 1 chính gốc giao tận nhà TP.HCM (Sài Gòn), Bình Dương, Đồng Nai chỉ 1 ngày. Giá gốc tại vườn từ 99k, Freeship từ 2 trái, bao sáp 1 đổi 1.",
        "keywords": "mua dừa sáp ở tphcm, dừa sáp trà vinh tại sài gòn, mua dừa sáp cầu kè ở đâu uy tín, dừa sáp giao nhanh tphcm, giá dừa sáp tphcm",
        "h1": "Mua Dừa Sáp Trà Vinh Ở TP.HCM Ở Đâu Ngon Chuẩn Cầu Kè? Giá Gốc Nhà Vườn Giao 1 Ngày",
        "hero_img": "images/doi_dua.jpg",
        "faq_q1": "Đặt dừa sáp từ vườn Cầu Kè gửi lên TP.HCM mất bao lâu?",
        "faq_a1": "Vựa cắt dừa mới mỗi sáng tại Hòa Tân (Cầu Kè, Trà Vinh) gửi tuyến nhanh lên TP.HCM, Thủ Đức, Bình Dương và Đồng Nai chỉ mất 1 - 2 ngày là giao tận tay. Mua từ 2 trái được Miễn Phí Ship 100%.",
        "faq_q2": "Nhận dừa tại TP.HCM có được kiểm tra hàng và bảo hành không sáp không?",
        "faq_a2": "Dạ có! Anh chị nhận hàng được kiểm tra trước khi thanh toán COD. Khi bổ ra nếu lỡ gặp trái không sáp hoặc sáp mỏng, chỉ cần chụp hình gửi Zalo 086 678 6076 là nhà vườn gửi bù trái mới tận nơi miễn phí.",
        "sections": [
            (
                "1. Vì Sao Khách Hàng TP.HCM Chọn Đặt Trực Tiếp Từ Vựa Cầu Kè Thay Vì Mua Trôi Nổi?",
                "<p>Tại TP.HCM, không ít nơi rao bán dừa sáp giá rẻ nhưng thực chất là <em>dừa sáp lai loại 2, loại 3</em> (cơm mỏng dính, nhiều nước lỏng) hoặc dừa tồn kho lâu ngày bị gắt dầu. Khi đặt trực tiếp từ <strong>Vựa Dừa Sáp Cầu Kè (xã Hòa Tân, Trà Vinh)</strong>, anh chị nhận được 3 lợi ích vượt trội:</p>"
                "<ul>"
                "<li><strong>Dừa mới rọc trong ngày:</strong> Cắt tại vườn sáng sớm, chiều lên xe gửi thẳng lên Sài Gòn nên cơm dừa giữ nguyên vị ngọt thanh và mùi thơm sữa dừa tươi mới.</li>"
                "<li><strong>Giá gốc nhà vườn không qua trung gian:</strong> Size Nhỏ <strong>99.000đ</strong>, Size Vừa bán chạy <strong>139.000đ</strong>, Size Lớn VIP <strong>169.000đ</strong> (rẻ hơn 30% – 40% so với cửa hàng trái cây nhập lại).</li>"
                "<li><strong>Thợ vườn lắc tuyển loại 1:</strong> Từng trái đều đạt độ sáp đặc chiếm 75% – 85% lòng gáo, nước dừa kẹo sánh kéo sợi.</li>"
                "</ul>"
            ),
            (
                "2. Lịch Giao Hàng & Chính Sách Freeship Tận Nhà Các Quận TP.HCM",
                "<p>Nhà vườn giao tận cửa tất cả các quận nội ngoại thành TP.HCM (Quận 1, Quận 3, Quận 7, Bình Thạnh, Gò Vấp, Tân Bình, Phú Nhuận, TP. Thủ Đức, Quận 12, Bình Tân...) và Bình Dương, Biên Hòa:</p>"
                "<ul>"
                "<li><strong>Mua từ 2 trái trở lên:</strong> <strong>Miễn Phí Ship Toàn Bộ</strong> (0đ phí vận chuyển).</li>"
                "<li><strong>Đơn từ 300.000đ:</strong> Tặng kèm ngay <strong>Combo Sữa Đặc + Đậu Phộng Rang Giòn</strong> để anh chị bổ ra là dầm đá ăn liền.</li>"
                "<li><strong>Thanh toán linh hoạt:</strong> Nhận hàng kiểm tra mới trả tiền mặt (COD) hoặc quét VietQR ACB tiện lợi.</li>"
                "</ul>"
            )
        ]
    },
    {
        "slug": "cach-bo-dua-sap-cuc-de-khong-can-dao-to",
        "label": "🔪 Mẹo Bổ Dừa Sáp 30 Giây Cực Nhàn",
        "title": "Cách Bổ Dừa Sáp Cực Dễ Chỉ 30 Giây Bằng Sống Dao (Không Cần Chặt Mạnh, Không Đổ Nước)",
        "meta_desc": "Hướng dẫn chi tiết cách gọt vỏ xơ và dùng sống dao gõ nhẹ tách đôi trái dừa sáp Trà Vinh chỉ trong 30 giây cực kỳ an toàn cho chị em phụ nữ, giữ trọn 100% nước dừa kẹo.",
        "keywords": "cách bổ dừa sáp, cách đập dừa sáp, cách khui dừa sáp dễ nhất, dừa sáp vỏ xơ bổ sao, hướng dẫn gọt dừa sáp",
        "h1": "Mẹo Bổ Dừa Sáp Chỉ Mất 30 Giây Bằng Sống Dao: Nhẹ Nhàng, An Toàn, Không Mất Giọt Nước Nào!",
        "hero_img": "images/step2_nut_doi.jpg",
        "faq_q1": "Chị em phụ nữ ở nhà không có dao chặt xương to có bổ được dừa sáp không?",
        "faq_a1": "Hoàn toàn được! Gáo dừa sáp già rất giòn. Bạn không cần chặt mạnh, chỉ cần rọc lớp vỏ xơ mềm bên ngoài rồi dùng sống lưng của con dao bếp bình thường (hoặc chiếc búa nhỏ/chày đâm tiêu) gõ nhẹ 1 vòng quanh bụng gáo là dừa tự nứt đôi.",
        "faq_q2": "Có cần đục lỗ lấy nước trước khi tách đôi trái dừa sáp không?",
        "faq_a2": "Không cần đục lỗ! Nước dừa sáp Loại 1 rất sệt kẹo chứ không nhiều nước loãng như dừa tươi. Bạn chỉ cần kê 1 chiếc tô sạch bên dưới lúc gõ sống dao, khi gáo nứt hé ra thì hứng phần nước kẹo vào tô rồi tách đôi trái dừa.",
        "sections": [
            (
                "1. Tại Sao Không Nên Dùng Dao Chặt Mạnh Trái Dừa Sáp?",
                "<p>Nhiều anh chị lần đầu mua <strong>Dừa Sáp Trà Vinh nguyên vỏ xơ</strong> thường lấy dao phay chặt thẳng từ trên xuống giống như chặt dừa tươi uống nước. Cách này vừa tốn sức, nguy hiểm, lại dễ làm nát vụn gáo dừa rơi vào lớp cơm sáp trắng muốt bên trong.</p>"
            ),
            (
                "2. Quy Trình 3 Bước Tách Đôi Gáo Dừa Sáp Đẹp Như Ngoài Hàng",
                "<ul>"
                "<li><strong>Bước 1 – Rọc lớp áo xơ mềm:</strong> Đặt trái dừa lên thớt, dùng dao rọc từ trên xuống dưới thành 4 – 5 múi rồi lột bỏ lớp vỏ xơ bảo vệ bên ngoài cho lộ ra chiếc gáo tròn màu nâu sẫm.</li>"
                "<li><strong>Bước 2 – Gõ nhẹ sống dao quanh đường xích đạo:</strong> Cầm trái dừa trên lòng bàn tay (kê tô sạch phía dưới), quay ngược <strong>sống dao (lưng dao)</strong> gõ nhẹ đều tay một vòng tròn quanh giữa bụng gáo. Chỉ sau 5 – 7 nhịp gõ nhẹ, gáo dừa già sẽ tự động nứt một đường thẳng tắp!</li>"
                "<li><strong>Bước 3 – Tách đôi & thưởng thức:</strong> Dùng mũi dao cạy nhẹ theo vết nứt để mở đôi hai nửa trái dừa trắng ngần, rưới sữa đặc và đá bào vào thưởng thức.</li>"
                "</ul>"
            )
        ]
    },
    {
        "slug": "dua-sap-bao-nhieu-calo-an-co-beo-khong",
        "label": "🥗 Dừa Sáp Bao Nhiêu Calo? Ăn Có Mập Không?",
        "title": "Dừa Sáp Bao Nhiêu Calo? Ăn Dừa Sáp Có Béo (Mập) Không? Cách Ăn Giữ Dáng Đẹp Da",
        "meta_desc": "Giải đáp chuẩn dinh dưỡng: 100g cơm dừa sáp bao nhiêu calo, chất béo tốt MCTs trong dừa sáp Cầu Kè và 3 công thức ăn dừa sáp healthy không lo tăng cân.",
        "keywords": "dừa sáp bao nhiêu calo, ăn dừa sáp có mập không, ăn dừa sáp có béo không, dừa sáp giảm cân, dinh dưỡng dừa sáp",
        "h1": "100g Dừa Sáp Bao Nhiêu Calo? Bí Quyết Ăn Dừa Sáp Ngon Miệng Mà Vẫn Giữ Dáng Thon Gọn",
        "hero_img": "images/muong_com_sap.jpg",
        "faq_q1": "Trong 100g cơm dừa sáp nguyên chất chứa bao nhiêu calo?",
        "faq_a1": "100g cơm dừa sáp tự nhiên cung cấp khoảng 280 - 320 kcal, chủ yếu đến từ axit béo chuỗi trung bình (MCTs) và chất xơ tự nhiên giúp no lâu và chuyển hóa năng lượng nhanh.",
        "faq_q2": "Người đang ăn kiêng hoặc tập gym ăn dừa sáp thế nào không sợ tăng cân?",
        "faq_a2": "Thay vì pha nhiều sữa đặc có đường, bạn hãy trộn 80g - 100g cơm dừa sáp với sữa chua Hy Lạp không đường, hạt chia và trái cây tươi làm bữa phụ trước buổi tập 60 phút.",
        "sections": [
            (
                "1. Hiểu Đúng Về Lượng Calo & Chất Béo Tốt Trong Dừa Sáp",
                "<p>Trong 100g cơm <strong>Dừa Sáp Cầu Kè nguyên bản</strong> chứa khoảng 280 – 320 kcal. Khác với chất béo bão hòa từ đồ chiên rán hay trà sữa kem cheese, chất béo trong dừa sáp là <strong>MCTs (Medium-Chain Triglycerides)</strong> — loại axit béo lành mạnh đi thẳng đến gan để tạo năng lượng tức thì, hạn chế tích tụ mỡ thừa.</p>"
            ),
            (
                "2. 3 Công Thức Dừa Sáp Healthy Ít Đường Cho Chị Em Giữ Dáng",
                "<ul>"
                "<li><strong>Dừa sáp dầm sữa chua Hy Lạp & Việt quất:</strong> Vị chua thanh của sữa chua quyện cùng độ béo dẻo của cơm sáp tạo cảm giác no lâu suốt cả buổi chiều.</li>"
                "<li><strong>Sinh tố dừa sáp sữa hạnh nhân (Almond Milk):</strong> Thay thế hoàn toàn sữa đặc bằng sữa hạt không đường và đá xay.</li>"
                "<li><strong>Chia nhỏ khẩu phần thông minh:</strong> Một trái dừa sáp Size Vừa có thể chia thành 4 – 5 phần ăn, phần chưa dùng hết đóng hộp kín cất ngăn mát dùng dần trong tuần.</li>"
                "</ul>"
            )
        ]
    },
    {
        "slug": "so-sanh-dua-sap-cau-ke-tra-vinh-va-dua-sap-khac",
        "label": "🌴 Dừa Sáp Cầu Kè Khác Gì Nơi Khác?",
        "title": "Tại Sao Dừa Sáp Hòa Tân Cầu Kè (Trà Vinh) Ngon Bậc Nhất? Khác Gì Dừa Sáp Vùng Khác?",
        "meta_desc": "Khám phá bí mật thổ nhưỡng xã Hòa Tân, huyện Cầu Kè, tỉnh Trà Vinh tạo nên trái dừa sáp chính gốc cơm dày 80% gáo, béo ngậy kéo sợi vượt trội hơn hẳn dừa sáp trồng nơi khác.",
        "keywords": "dừa sáp cầu kè khác gì bến tre, dừa sáp hòa tân cầu kè, tại sao dừa sáp trà vinh ngon nhất, dừa sáp cấy phôi và dừa sáp tự nhiên",
        "h1": "Vì Sao Chỉ Vùng Đất Hòa Tân (Cầu Kè, Trà Vinh) Mới Cho Ra Trái Dừa Sáp Kẹo Sợi Đỉnh Cao?",
        "hero_img": "images/vuon_dua.jpg",
        "faq_q1": "Mang giống dừa sáp Cầu Kè đi tỉnh khác trồng có cho cơm sáp ngon giống vậy không?",
        "faq_a1": "Thực tế nhiều nơi từng mang giống đi trồng thử nhưng tỷ lệ lên sáp giảm mạnh hoặc cơm dừa bị xơ, kém béo. Thổ nhưỡng phù sa pha cát cổ và nguồn nước lợ nhẹ đặc thù ven sông Hậu tại Cầu Kè quyết định hương vị béo ngậy độc nhất vô nhị.",
        "faq_q2": "Dừa sáp truyền thống tại vườn khác gì dừa sáp cấy phôi?",
        "faq_a2": "Dừa sáp truyền thống tại các vườn lâu năm ở Hòa Tân (Cầu Kè) có hương thơm tự nhiên rất đậm, cơm sáp dẻo quánh hai tầng (ngoài giòn dẻo, trong mềm kem) và nước kẹo sánh ngọt thanh.",
        "sections": [
            (
                "1. Bí Mật Thổ Nhưỡng Phù Sa Ven Sông Hậu Tại Xã Hòa Tân, Cầu Kè",
                "<p>Không phải ngẫu nhiên mà suốt gần 100 năm qua kể từ khi cây dừa sáp đầu tiên bén rễ tại <strong>huyện Cầu Kè, tỉnh Trà Vinh</strong>, vùng đất này vẫn giữ ngôi vương tuyệt đối. Sự giao thoa giữa dòng phù sa ngọt sông Hậu, độ khoáng vi lượng trong đất thịt pha cát và nắng gió miền Tây giúp trái dừa tích tụ lớp tinh dầu thơm ngậy mà không vùng đất nào sao chép trọn vẹn được.</p>"
            ),
            (
                "2. Bảng So Sánh Dừa Sáp Cầu Kè Loại 1 Tuyển Chọn Với Hàng Chợ Trôi Nổi",
                "<ul>"
                "<li><strong>Độ dày cơm dừa:</strong> Dừa Sáp Cầu Kè Loại 1 chiếm <strong>75% – 85% thể tích gáo</strong>; hàng loại 2/3 trôi nổi chỉ có lớp cơm mỏng 1cm kèm rất nhiều nước loãng.</li>"
                "<li><strong>Độ dẻo & hương vị:</strong> Cơm sáp Cầu Kè chính gốc trắng phau, xắn muỗng vào dẻo quánh như kem bơ, nước kẹo kéo sợi óng ánh.</li>"
                "<li><strong>Cam kết minh bạch:</strong> Mua trực tiếp tại Vựa Cầu Kè được <strong>bao sáp 1 đổi 1 từng trái</strong> tận nhà toàn quốc.</li>"
                "</ul>"
            )
        ]
    },
    {
        "slug": "gia-si-dua-sap-tra-vinh-cho-quan-sinh-to-cafe",
        "label": "📦 Bảng Giá Sỉ Dừa Sáp Cho Quán & Đại Lý",
        "title": "Nguồn Bỏ Sỉ Dừa Sáp Cầu Kè Trà Vinh Giá Gốc Tận Vườn Cho Quán Chè, Sinh Tố & CTV",
        "meta_desc": "Vựa Dừa Sáp Cầu Kè (Hòa Tân, Trà Vinh) chuyên cung cấp sỉ dừa sáp loại 1 từ 10 - 100 trái/ngày cho quán sinh tố, quán chè, nhà hàng và đại lý toàn quốc. Bao sáp 100% từng trái.",
        "keywords": "sỉ dừa sáp trà vinh, lấy sỉ dừa sáp cầu kè, nguồn hàng dừa sáp giá gốc, vựa dừa sáp trà vinh, dừa sáp cho quán sinh tố",
        "h1": "Bỏ Sỉ Dừa Sáp Cầu Kè Trà Vinh Tận Gốc Nhà Vườn: Nguồn Hàng Ổn Định, Bao Sáp 100%",
        "hero_img": "images/luoi_vang_4_trai.jpg",
        "faq_q1": "Lấy bao nhiêu trái thì được tính giá sỉ nhà vườn Cầu Kè?",
        "faq_a1": "Nhà vườn hỗ trợ chính sách ưu đãi riêng ngay từ đơn 5 - 10 trái (quà biếu/nhóm mua chung) và bảng giá sỉ tận gốc cho quán chè, quán sinh tố, đại lý nhập từ 10 - 20 trái trở lên mỗi chuyến. Liên hệ trực tiếp Zalo 086 678 6076.",
        "faq_q2": "Quán nhập sỉ lỡ khui trúng trái sáp yếu thì vựa có đổi bù không?",
        "faq_a2": "Chắc chắn 100%! Toàn bộ đơn sỉ cho quán và đại lý đều được Vựa bao sáp 1 đổi 1 (khấu trừ hoặc gửi bù ngay trong chuyến kế tiếp) để chủ quán tính cost ly sinh tố luôn có lãi ổn định.",
        "sections": [
            (
                "1. Món 'Hái Ra Tiền' Cho Quán Giải Khát, Quán Chè & Cafe Sân Vườn",
                "<p>Một trái <strong>Dừa Sáp Cầu Kè Size Vừa – Lớn</strong> khi nạo ra dầm sữa đá hoặc xay sinh tố cốt dừa bơ sáp cho ra từ <strong>5 – 6 ly thành phẩm</strong>. Với giá bán lẻ mỗi ly dừa sáp dầm tại các thành phố từ 35.000đ – 55.000đ/ly, biên lợi nhuận của quán đạt trên 50% mà khách ăn một lần là quay lại thường xuyên.</p>"
            ),
            (
                "2. Quyền Lợi Khi Nhập Sỉ Trực Tiếp Từ Vựa Dừa Sáp Cầu Kè (Zalo 086 678 6076)",
                "<ul>"
                "<li><strong>Phân loại chuẩn xác theo cân nặng:</strong> Đủ các size Nhỏ (800g-1kg), Vừa (1kg-1.3kg), Lớn VIP (1.3kg-1.5kg) đồng đều.</li>"
                "<li><strong>Đóng bao dứa / gửi chành xe tốc hành:</strong> Hỗ trợ gửi chành xe miền Tây – TP.HCM nhận ngay trong ngày hoặc bưu cục nhanh đi Hà Nội, Đà Nẵng, các tỉnh.</li>"
                "<li><strong>Bảo hành sáp 100%:</strong> Không lo hao hụt vốn nguyên liệu.</li>"
                "</ul>"
            )
        ]
    },
    {
        "slug": "cach-lam-kem-dua-sap-che-dua-sap-tai-nha",
        "label": "🍨 Cách Làm Kem Dừa Sáp & Chè Dừa Sáp",
        "title": "Cách Làm Kem Dừa Sáp & Chè Dừa Sáp Trân Châu Cốt Dừa Mát Lạnh Không Bị Dăm Đá",
        "meta_desc": "Công thức làm kem dừa sáp dẻo mịn không cần máy làm kem và món chè dừa sáp trân châu cốt dừa béo ngậy giải nhiệt mùa hè cho cả gia đình.",
        "keywords": "cách làm kem dừa sáp, chè dừa sáp, kem dừa sáp trà vinh, món ngon từ dừa sáp, dừa sáp trân châu cốt dừa",
        "h1": "Bí Quyết Làm Kem Dừa Sáp Mịn Mượt Không Dăm Đá & Chè Dừa Sáp Trân Châu Tại Nhà",
        "hero_img": "images/gao_dua_trai_cay.jpg",
        "faq_q1": "Làm kem dừa sáp tại nhà không có máy làm kem có bị cứng đá không?",
        "faq_a1": "Không hề bị dăm đá! Do bản thân cơm dừa sáp Cầu Kè chứa hàm lượng tinh dầu béo tự nhiên rất cao, khi xay nhuyễn cùng whipping cream (hoặc sữa đặc + cốt dừa) rồi cấp đông vẫn giữ được độ dẻo xốp mịn màng.",
        "faq_q2": "Nên chọn dừa sáp size nào để làm kem và nấu chè kinh tế nhất?",
        "faq_a2": "Gia đình 4 - 6 người nên chọn cặp 2 trái Size Vừa (1.0kg - 1.3kg, giá 278.000đ Freeship) sẽ thu được lượng cơm sáp dày dặn nhất.",
        "sections": [
            (
                "1. Công Thức Kem Dừa Sáp Đựng Trong Gáo Dừa Mịn Như Ngoài Tiệm",
                "<p>Chỉ với 1 trái <strong>Dừa Sáp Cầu Kè Loại 1</strong>, 150ml kem tươi (whipping cream) và 60g sữa đặc, bạn xay mịn hỗn hợp cơm dừa sáp rồi trộn nhẹ (fold) với kem tươi đánh bông, cho ngược vào hai nửa gáo dừa sạch rồi để ngăn đá 5 tiếng. Khi ăn rắc thêm dừa khô và đậu phộng rang giòn rụm.</p>"
            ),
            (
                "2. Chè Dừa Sáp Sương Sáo Hạt Đác Ngọt Thanh Giải Nhiệt",
                "<p>Thái sợi hoặc xắn miếng vuông cơm dừa sáp, kết hợp cùng hạt đác rim dứa, thạch sương sáo đen và nước dừa kẹo pha sữa tươi mát lạnh — món tráng miệng thanh nhiệt tuyệt vời cho cả ông bà và các bé nhỏ.</p>"
            )
        ]
    },
    {
        "slug": "dua-sap-bi-chua-hay-hu-cach-nhan-biet",
        "label": "🔍 Nhận Biết Dừa Sáp Ngon vs Dừa Hư Chua",
        "title": "Dừa Sáp Có Vị Hơi Chua Hay Bị Hư? Cách Nhận Biết Dừa Sáp Tươi Ngon Chuẩn Loại 1",
        "meta_desc": "Phân biệt mùi thơm lên men nhẹ tự nhiên hay dấu hiệu dừa sáp bị hư chua, gắt dầu do nứt gáo, cùng chính sách bảo hành 1 đổi 1 trong 15 phút tại Vựa Cầu Kè.",
        "keywords": "dừa sáp bị chua, cách nhận biết dừa sáp bị hư, mùi vị dừa sáp chuẩn, dừa sáp để lâu bị gắt dầu, bảo hành dừa sáp",
        "h1": "Cách Nhận Biết Dừa Sáp Tươi Ngon Chuẩn Vị Và Dấu Hiệu Dừa Sáp Bị Hư Do Nứt Gáo",
        "hero_img": "images/dac_ruot.jpg",
        "faq_q1": "Mùi vị chuẩn của trái dừa sáp Cầu Kè tươi ngon là như thế nào?",
        "faq_a1": "Trái dừa sáp chuẩn khi mới bổ ra có màu trắng phau như bông gòn, mùi thơm dịu đặc trưng của cùi dừa già quyện sữa, nước dừa sệt trong hơi đục nhẹ và có vị ngọt thanh bùi béo (hoàn toàn không chua gắt hay hắc mùi dầu).",
        "faq_q2": "Nếu bổ ra thấy nước dừa có mùi chua hoặc ngả màu vàng thì xử lý sao?",
        "faq_a2": "Quý khách tuyệt đối không sử dụng mà hãy chụp ngay 1 tấm hình bên trong gáo dừa gửi qua Zalo 086 678 6076. Vựa Dừa Sáp Cầu Kè sẽ gửi bù ngay 1 trái mới hoàn toàn miễn phí hoặc hoàn tiền 100% trong 15 phút!",
        "sections": [
            (
                "1. 3 Dấu Hiệu Của Trái Dừa Sáp Tươi Ngon Đạt Đỉnh Độ Sáp",
                "<ul>"
                "<li><strong>Màu sắc:</strong> Cơm dừa trắng tinh khôi, bề mặt bông xốp mềm mịn như kem tuyết.</li>"
                "<li><strong>Hương thơm:</strong> Thơm thoang thoảng mùi dừa non pha cốt dừa béo dịu ngay khi vừa tách gáo.</li>"
                "<li><strong>Vị giác:</strong> Nhai thử miếng cơm sáp nguyên chất thấy dẻo sần sật bên ngoài, tan mềm bên trong, hậu vị ngọt thanh tự nhiên.</li>"
                "</ul>"
            ),
            (
                "2. Nguyên Nhân Khiến Dừa Bị Chua & Cam Kết Bảo Hành Vàng 1 Đổi 1",
                "<p>Trong hàng trăm trái dừa tự nhiên, đôi khi có 1 – 2% trái bị rạn mắt mầm li ti bên dưới lớp xơ làm không khí lọt vào gây chua nước. Hiểu rõ điều đó, <strong>Vựa Dừa Sáp Cầu Kè</strong> luôn đứng ra chịu trách nhiệm 100%: <strong>bổ ra lỗi trái nào, nhà vườn đền bù ngay trái mới trái đó tận nhà</strong>, không bao giờ để khách hàng chịu thiệt!</p>"
            )
        ]
    },
    {
        "slug": "mua-dua-sap-da-nang-mien-trung-giao-tan-noi",
        "label": "🌊 Ship Dừa Sáp đi Đà Nẵng & Miền Trung",
        "title": "Đặt Mua Dừa Sáp Trà Vinh Gửi Đi Đà Nẵng, Huế, Nha Trang & Miền Trung Mất Bao Lâu?",
        "meta_desc": "Dịch vụ gửi Dừa Sáp Cầu Kè Trà Vinh Loại 1 đi Đà Nẵng, Hội An, Huế, Quy Nhơn, Nha Trang chỉ 2 ngày nhận hàng. Mua 2 trái Freeship tận nơi, bao sáp đặc từng trái.",
        "keywords": "mua dừa sáp ở đà nẵng, dừa sáp trà vinh tại nha trang, gửi dừa sáp đi miền trung, mua dừa sáp huế, dừa sáp freeship toàn quốc",
        "h1": "Mua Dừa Sáp Cầu Kè Trà Vinh Tại Đà Nẵng, Nha Trang & Miền Trung: Giao Tận Nhà 2 Ngày",
        "hero_img": "images/boc_luoi.jpg",
        "faq_q1": "Khách ở Đà Nẵng và Nha Trang đặt 2 trái dừa sáp có được miễn phí ship không?",
        "faq_a1": "Dạ được Miễn Phí Ship 100%! Chỉ cần đặt từ 2 trái bất kỳ (Size Nhỏ, Vừa hoặc Lớn VIP), nhà vườn bao trọn phí vận chuyển giao tận nhà tại Đà Nẵng, Huế, Quảng Nam, Quy Nhơn, Nha Trang.",
        "faq_q2": "Trời nắng miền Trung gửi dừa sáp đi 2 - 3 ngày có cần bỏ thùng đá không?",
        "faq_a2": "Không cần thùng đá (vì hơi nước đá làm ẩm mốc mắt dừa). Giữ nguyên lớp vỏ xơ dày tự nhiên bên ngoài và bọc túi lưới thoáng khí chính là cách bảo quản truyền thống tốt nhất giúp dừa tươi nguyên suốt 2 tuần.",
        "sections": [
            (
                "1. Thưởng Thức Đặc Sản Trà Vinh Chính Gốc Ngay Tại Miền Trung",
                "<p>Không cần phải đi du lịch miền Tây xa xôi, giờ đây anh chị tại <strong>Đà Nẵng, Huế, Quảng Nam, Quảng Ngãi, Bình Định, Phú Yên, Khánh Hòa (Nha Trang)</strong> chỉ cần đặt hàng trực tuyến tại website nhà vườn, thợ vườn Hòa Tân sẽ lắc tuyển những trái dừa già đanh cắt mới trong sáng và gửi thẳng tận cửa chỉ sau <strong>2 – 3 ngày</strong>.</p>"
            ),
            (
                "2. Combo Gia Đình Được Khách Đà Nẵng & Nha Trang Ưa Chuộng Nhất",
                "<ul>"
                "<li><strong>Combo Ăn Thử Gia Đình (278.000đ):</strong> 2 trái Size Vừa (1.0kg – 1.3kg/trái) + <strong>Miễn Phí Ship</strong> — làm được 8 đến 10 ly dừa sáp dầm sữa đá mát lạnh.</li>"
                "<li><strong>Combo Quà Tặng Đủ Đầy (338.000đ):</strong> 2 trái Size Lớn VIP (1.3kg – 1.5kg/trái) + <strong>Miễn Phí Ship</strong> + <strong>Tặng Bộ Sữa Đặc & Đậu Phộng Rang</strong>.</li>"
                "</ul>"
            )
        ]
    }
]


def generate_ai_seo_topic_gemini(existing_slugs: set) -> dict:
    """Khi hàng đợi tĩnh đã xuất bản hết, tự động gọi Gemini 3.8 Flash / 3.6 Flash sinh chủ đề Long-Tail mới."""
    if not GEMINI_API_KEY:
        return None
    prompt = (
        "Bạn là chuyên gia SEO Thương mại điện tử cho thương hiệu 'Vựa Dừa Sáp Cầu Kè Trà Vinh' "
        "(xã Hòa Tân, huyện Cầu Kè, tỉnh Trà Vinh; bảng giá: Size Nhỏ 800g-1kg 99.000đ, Size Vừa 1-1.3kg 139.000đ, "
        "Size Lớn VIP 1.3-1.5kg 169.000đ; mua từ 2 trái Freeship toàn quốc; đơn từ 300k tặng Sữa đặc + Đậu phộng; "
        "bao sáp 1 đổi 1 qua Zalo 086 678 6076).\n"
        f"Các slug đã viết (TUYỆT ĐỐI KHÔNG TRÙNG): {sorted(list(existing_slugs))}\n"
        "Hãy tạo 1 bài viết Long-Tail SEO mới tinh có ý định mua hàng cao (ví dụ: trẻ em ăn dừa sáp, người già tiểu đường ăn dừa sáp, "
        "dừa sáp làm bánh/rau câu, mua dừa sáp Hải Phòng/Cần Thơ/Bình Dương, tại sao dừa sáp hiếm...).\n"
        "Trả về DUY NHẤT 1 JSON hợp lệ (không markdown fence) theo cấu trúc:\n"
        '{"slug":"slug-khong-dau","label":"🥥 Tiêu đề ngắn 5 từ","title":"Tiêu đề chuẩn SEO 55-65 ký tự",'
        '"meta_desc":"Mô tả 140-155 ký tự","keywords":"từ khóa 1, từ khóa 2","h1":"Tiêu đề H1 hấp dẫn",'
        '"hero_img":"images/doi_dua.jpg","faq_q1":"Câu hỏi 1?","faq_a1":"Trả lời 1","faq_q2":"Câu hỏi 2?","faq_a2":"Trả lời 2",'
        '"sections":[["1. Tiêu đề H2 mục 1","<p>Nội dung HTML chi tiết...</p>"],["2. Tiêu đề H2 mục 2","<p>Nội dung HTML chi tiết...</p>"]]}'
    )
    for model in ["gemini-3.8-flash", "gemini-3.6-flash"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            r = requests.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.6, "maxOutputTokens": 1800, "responseMimeType": "application/json", "thinkingConfig": {"thinkingBudget": 0}}
                },
                timeout=25
            )
            if r.status_code == 200:
                txt = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                txt = re.sub(r"^```(?:json)?|```$", "", txt, flags=re.MULTILINE).strip()
                data = json.loads(txt)
                slug = re.sub(r"[^a-z0-9\-]", "", data.get("slug", "").lower())
                if slug and slug not in existing_slugs and data.get("sections"):
                    data["slug"] = slug
                    if data.get("hero_img") not in ("images/doi_dua.jpg", "images/keo_soi.jpg", "images/ly_dam_sua.jpg", "images/dua_sap_size_lon_vip.jpg"):
                        data["hero_img"] = "images/doi_dua.jpg"
                    return data
        except Exception as e:
            print(f"⚠️ Gemini SEO topic gen ({model}) warning: {e}")
    return None


def render_article_html(topic: dict, today_iso: str) -> str:
    """Sinh trang HTML chuẩn SEO & CRO 100% (Schema @graph, Quick Size Picker Deep-Links, Related Cluster, Sticky Mobile Bar)."""
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

    related_items = [t for t in SEO_TOPICS_QUEUE if t["slug"] != topic["slug"]][:4]
    related_links_html = "".join([
        f'<li><a href="/{r["slug"]}.html" style="color: var(--leaf-700); font-weight: 700; text-decoration: underline;">{r["title"]}</a></li>'
        for r in related_items
    ])

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
                "publisher": {
                    "@type": "Organization",
                    "name": "Vựa Dừa Sáp Cầu Kè Trà Vinh",
                    "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/images/brand/icon-512.png"}
                }
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
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="32x32" href="images/brand/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="images/brand/apple-touch-icon.png">
  <meta name="theme-color" content="#163822">
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
    :root {{ --leaf-950: #102818; --leaf-900: #163822; --leaf-800: #1f4c2f; --leaf-700: #2b663f; --leaf-100: #e7f3eb; --leaf-50: #f4faf6; --coco-brown: #3e2b1d; --coco-muted: #654f3f; --earth-gold: #9d5b0d; --earth-gold-dark: #7e4708; --gold-ring: #d4942a; --gold-foil: #f5d078; --cream-bg: #faf6ee; --border-soft: #e2d7c2; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Quicksand', sans-serif; font-weight: 600; color: var(--coco-brown); background: var(--cream-bg); line-height: 1.7; padding-bottom: 68px; }}
    h1, h2, h3 {{ font-family: 'Lora', Georgia, serif; color: var(--leaf-900); line-height: 1.3; }}
    a:focus-visible, button:focus-visible {{ outline: 3px solid var(--gold-ring); outline-offset: 2px; }}
    .container {{ max-width: 840px; margin: 0 auto; padding: 0 18px; }}
    header {{ background: rgba(250, 246, 238, 0.96); backdrop-filter: blur(10px); border-bottom: 1.5px solid var(--border-soft); padding: 10px 0; position: sticky; top: 0; z-index: 100; }}
    header .nav {{ display: flex; justify-content: space-between; align-items: center; max-width: 840px; margin: 0 auto; padding: 0 18px; gap: 10px; }}
    .brand {{ display: flex; align-items: center; gap: 10px; text-decoration: none; min-width: 0; }}
    .brand > div {{ min-width: 0; }}
    .brand svg {{ width: 38px; height: 38px; flex-shrink: 0; border-radius: 50%; box-shadow: 0 3px 10px rgba(22, 56, 34, 0.2); }}
    .brand-title {{ font-family: 'Lora', serif; font-weight: 700; font-size: 1.08rem; color: var(--leaf-900); display: block; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .brand-sub {{ font-size: 0.72rem; color: var(--coco-muted); display: block; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .nav-cta {{ display: flex; align-items: center; gap: 8px; flex-shrink: 0; }}
    .btn-phone {{ padding: 8px 13px; border-radius: 99px; background: var(--leaf-100); color: var(--leaf-800); font-weight: 700; font-size: 0.82rem; white-space: nowrap; text-decoration: none; }}
    .btn-order-top {{ background: var(--earth-gold); color: #fff; padding: 8px 16px; border-radius: 99px; font-size: 0.84rem; font-weight: 700; white-space: nowrap; text-decoration: none; }}
    .btn-order-top:hover {{ background: var(--earth-gold-dark); }}
    .breadcrumb {{ font-size: 0.85rem; color: var(--coco-muted); margin: 18px 0; }}
    .breadcrumb a {{ color: var(--leaf-700); text-decoration: underline; }}
    article {{ background: #fff; border: 1px solid var(--border-soft); border-radius: 20px; padding: 32px 26px; margin-bottom: 32px; box-shadow: 0 8px 24px rgba(62,43,29,0.06); }}
    ul {{ padding-left: 20px; margin-top: 8px; }}
    li {{ margin-bottom: 8px; }}
    .quick-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-top: 16px; text-align: left; }}
    .q-card {{ background: #fff; border: 1.5px solid var(--border-soft); border-radius: 14px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; }}
    .q-card.featured {{ border: 2px solid var(--gold-ring); background: #fffdf9; }}
    .q-btn {{ display: block; text-align: center; background: var(--leaf-800); color: #fff; padding: 10px 12px; border-radius: 99px; font-weight: 700; font-size: 0.85rem; text-decoration: none; margin-top: 10px; }}
    .q-card.featured .q-btn {{ background: var(--earth-gold); }}
    .cta-box {{ background: var(--leaf-50); border: 2px solid var(--leaf-700); border-radius: 18px; padding: 24px 20px; text-align: center; margin-top: 28px; }}
    .sticky-bar {{ position: fixed; bottom: 0; left: 0; right: 0; background: rgba(255,255,255,0.98); border-top: 1px solid var(--border-soft); padding: 8px 12px; display: flex; gap: 8px; justify-content: center; z-index: 200; box-shadow: 0 -4px 16px rgba(0,0,0,0.07); }}
    .s-btn {{ flex: 1; max-width: 220px; padding: 11px 8px; border-radius: 99px; font-weight: 700; font-size: 0.82rem; text-align: center; text-decoration: none; white-space: nowrap; }}
    footer {{ background: var(--leaf-900); border-top: 2px solid var(--gold-ring); color: #e2d7c2; text-align: center; padding: 34px 18px; font-size: 0.86rem; }}
    @media (max-width: 600px) {{ header .nav {{ padding: 0 12px; gap: 8px; }} article {{ padding: 22px 16px; }} h1 {{ font-size: 1.55rem !important; }} .btn-phone {{ display: none; }} .brand svg {{ width: 34px; height: 34px; }} .brand-title {{ font-size: 0.94rem; }} .brand-sub {{ font-size: 0.66rem; }} .btn-order-top {{ padding: 7px 12px; font-size: 0.78rem; }} }}
  </style>
</head>
<body>
  <header>
    <div class="nav">
      <a href="/" class="brand">
        <svg viewBox="0 0 64 64" width="38" height="38" fill="none" aria-hidden="true">
          <circle cx="32" cy="32" r="30" fill="#163822"/>
          <circle cx="32" cy="32" r="27" stroke="#D4942A" stroke-width="1.6"/>
          <path d="M15 24C12 18 15 12 22 10C18 14 17 19 18 24Z" fill="#D4942A" opacity="0.9"/>
          <path d="M49 24C52 18 49 12 42 10C46 14 47 19 46 24Z" fill="#D4942A" opacity="0.9"/>
          <circle cx="32" cy="34" r="16.5" fill="#5E3C23" stroke="#D4942A" stroke-width="1.4"/>
          <circle cx="32" cy="34" r="13" fill="#FAF6EE"/>
          <circle cx="32" cy="34.5" r="5.5" fill="#163822" opacity="0.14"/>
          <path d="M32 29.5C32 29.5 35.8 33.8 35.8 36.4C35.8 38.5 34.1 40.2 32 40.2C29.9 40.2 28.2 38.5 28.2 36.4C28.2 33.8 32 29.5 32 29.5Z" fill="#D4942A"/>
          <circle cx="30.8" cy="35.6" r="1" fill="#FFFDF8" opacity="0.85"/>
          <circle cx="32" cy="9.5" r="1.5" fill="#F5D078"/>
        </svg>
        <div>
          <span class="brand-title">Vựa Dừa Sáp Cầu Kè</span>
          <span class="brand-sub">Đặc Sản Trà Vinh Loại 1</span>
        </div>
      </a>
      <div class="nav-cta">
        <a href="tel:0866786076" class="btn-phone">📞 086 678 6076</a>
        <a href="/?size=size_vua&qty=2#dat-hang" class="btn-order-top">🛒 Đặt 2 Trái Freeship</a>
      </div>
    </div>
  </header>

  <main class="container">
    <nav class="breadcrumb" aria-label="Phân cấp trang">
      <a href="/">Trang chủ</a> › <span>{topic['label']}</span>
    </nav>

    <article>
      <h1 style="font-size: 1.85rem; margin-bottom: 14px;">{topic['h1']}</h1>
      <p style="font-size: 0.85rem; color: var(--coco-muted); margin-bottom: 20px;">
        📍 Bài viết từ Nghệ nhân Vựa Dừa Sáp xã Hòa Tân, huyện Cầu Kè, tỉnh Trà Vinh • Cập nhật: {today_iso}
      </p>

      <div style="border-radius: 16px; overflow: hidden; margin-bottom: 24px;">
        <img src="/{topic['hero_img']}" alt="{topic['h1']}" width="840" height="420" fetchpriority="high" decoding="async" style="width: 100%; max-height: 420px; object-fit: cover; display: block;">
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
        <h2 style="font-size: 1.35rem; margin-bottom: 6px;">Chọn Size Dừa Sáp Cầu Kè Loại 1 (Hái Mới Sáng Nay)</h2>
        <p style="font-size: 0.9rem; color: var(--coco-muted);">
          Mua từ 2 trái <strong>Freeship Toàn Quốc</strong> • Đơn từ 300k tặng <strong>Sữa đặc & Đậu phộng rang</strong> • Bao sáp 1 đổi 1 tận nhà!
        </p>

        <div class="quick-grid">
          <div class="q-card">
            <div>
              <div style="font-size: 0.78rem; color: var(--coco-muted);">800g - 1.0kg (Ăn thử)</div>
              <strong style="font-size: 1.05rem; color: var(--leaf-900);">Size Nhỏ • 99.000đ</strong>
              <div style="font-size: 0.8rem; margin-top: 4px;">Cặp 2 trái: <strong>198.000đ</strong> (Freeship)</div>
            </div>
            <a href="/?size=size_nho&qty=2#dat-hang" class="q-btn">Chọn 2 Trái Nhỏ</a>
          </div>

          <div class="q-card featured">
            <div>
              <div style="font-size: 0.76rem; color: var(--earth-gold); font-weight: 700;">🔥 BÁN CHẠY NHẤT</div>
              <strong style="font-size: 1.05rem; color: var(--leaf-900);">Size Vừa • 139.000đ</strong>
              <div style="font-size: 0.8rem; margin-top: 4px;">Cặp 2 trái: <strong>278.000đ</strong> (Freeship)</div>
            </div>
            <a href="/?size=size_vua&qty=2#dat-hang" class="q-btn">👉 Đặt 2 Trái Vừa Ngay</a>
          </div>

          <div class="q-card">
            <div>
              <div style="font-size: 0.78rem; color: var(--leaf-700);">1.3kg - 1.5kg (Biếu VIP)</div>
              <strong style="font-size: 1.05rem; color: var(--leaf-900);">Size Lớn • 169.000đ</strong>
              <div style="font-size: 0.8rem; margin-top: 4px;">Cặp 2 trái: <strong>338k</strong> (Freeship + Quà)</div>
            </div>
            <a href="/?size=size_lon&qty=2#dat-hang" class="q-btn">Chọn 2 Trái VIP + Quà</a>
          </div>
        </div>
      </div>

      <section style="margin-top: 26px; padding-top: 18px; border-top: 1px dashed var(--border-soft);">
        <h3 style="font-size: 1.08rem; margin-bottom: 8px;">📖 Cẩm Nang Dừa Sáp Cầu Kè Liên Quan:</h3>
        <ul style="font-size: 0.9rem;">
          {related_links_html}
          <li><a href="/cach-phan-biet-dua-sap-that-gia.html" style="color: var(--leaf-700); font-weight: 700; text-decoration: underline;">4 Tuyệt kỹ lắc & phân biệt Dừa Sáp thật giả chuẩn nhà vườn</a></li>
          <li><a href="/gia-dua-sap-tra-vinh.html" style="color: var(--leaf-700); font-weight: 700; text-decoration: underline;">Bảng giá Dừa Sáp Trà Vinh Loại 1 cập nhật mới nhất</a></li>
        </ul>
      </section>
    </article>
  </main>

  <div class="sticky-bar">
    <a href="https://zalo.me/0866786076" target="_blank" rel="noopener" class="s-btn" style="background: #eff6ff; color: #0068ff; border: 1px solid #bfdbfe;">💬 Chat Zalo</a>
    <a href="tel:0866786076" class="s-btn" style="background: var(--leaf-100); color: var(--leaf-900);">📞 086.678.6076</a>
    <a href="/?size=size_vua&qty=2#dat-hang" class="s-btn" style="background: var(--earth-gold); color: #fff;">🛒 Đặt 2 Trái Freeship</a>
  </div>

  <footer>
    <div style="display: inline-flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 8px;">
      <svg viewBox="0 0 64 64" width="32" height="32" fill="none" aria-hidden="true">
        <circle cx="32" cy="32" r="30" fill="#102818"/>
        <circle cx="32" cy="32" r="27" stroke="#D4942A" stroke-width="1.6"/>
        <path d="M15 24C12 18 15 12 22 10C18 14 17 19 18 24Z" fill="#D4942A" opacity="0.9"/>
        <path d="M49 24C52 18 49 12 42 10C46 14 47 19 46 24Z" fill="#D4942A" opacity="0.9"/>
        <circle cx="32" cy="34" r="16.5" fill="#5E3C23" stroke="#D4942A" stroke-width="1.4"/>
        <circle cx="32" cy="34" r="13" fill="#FAF6EE"/>
        <path d="M32 29.5C32 29.5 35.8 33.8 35.8 36.4C35.8 38.5 34.1 40.2 32 40.2C29.9 40.2 28.2 38.5 28.2 36.4C28.2 33.8 32 29.5 32 29.5Z" fill="#D4942A"/>
      </svg>
      <p style="font-family: 'Lora', serif; font-size: 1rem; color: #fff;"><strong>Vựa Dừa Sáp Cầu Kè Trà Vinh - Loại 1 Chính Gốc</strong></p>
    </div>
    <p>Địa chỉ: Xã Hòa Tân, Huyện Cầu Kè, Tỉnh Trà Vinh | Hotline / Zalo: 086 678 6076</p>
    <p style="margin-top: 8px;"><a href="/" style="color: #f5d078; text-decoration: underline;">← Quay về Trang Chủ Đặt Hàng</a> • <a href="https://www.facebook.com/duasaptravinhbaosap/" target="_blank" rel="noopener" style="color: #f5d078; text-decoration: underline;">Fanpage Chính Thức</a></p>
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
      <video:thumbnail_loc>{SITE_URL}/images/doi_dua.jpg</video:thumbnail_loc>
      <video:title>ASMR Bổ Dừa Sáp Cầu Kè Trà Vinh Loại 1 Kéo Sợi Đặc Ruột</video:title>
      <video:description>Cận cảnh tách đôi gáo dừa sáp Cầu Kè Trà Vinh trắng muốt, múc muỗng cơm sáp dẻo quánh kéo sợi óng ánh.</video:description>
      <video:content_loc>{SITE_URL}/images/asmr_bo_dua_keo_soi.mp4</video:content_loc>
    </video:video>
    <video:video>
      <video:thumbnail_loc>{SITE_URL}/images/ly_dam_sua.jpg</video:thumbnail_loc>
      <video:title>Cách Làm Ly Dừa Sáp Dầm Sữa Đá Đậu Phộng Rang Chuẩn Vị Trà Vinh</video:title>
      <video:description>Cơm dừa sáp dẻo quánh dầm sữa đặc đá bào và đậu phộng rang giòn rụm mát lạnh.</video:description>
      <video:content_loc>{SITE_URL}/images/asmr_dam_sua_dau_phong.mp4</video:content_loc>
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
        "host": "duasaptravinh.vercel.app",
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
    upgrade_existing = ("--upgrade-existing" in sys.argv)

    print(f"🚀 [AUTO-SEO ENGINE V4.0] Khởi chạy ngày {today_vn_str} ({today_iso})")

    if upgrade_existing:
        for t in SEO_TOPICS_QUEUE:
            fp = os.path.join(BASE_DIR, f"{t['slug']}.html")
            if os.path.exists(fp):
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(render_article_html(t, today_iso))
                print(f"♻️ Đã nâng cấp giao diện CRO cho bài cũ: {t['slug']}.html")

    # 1. Tìm bài viết tiếp theo trong hàng đợi chưa được xuất bản
    created_article = None
    existing_slugs = {
        f[:-5] for f in os.listdir(BASE_DIR) if f.endswith(".html")
    }

    for topic in SEO_TOPICS_QUEUE:
        file_path = os.path.join(BASE_DIR, f"{topic['slug']}.html")
        if not os.path.exists(file_path):
            html_content = render_article_html(topic, today_iso)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            created_article = topic
            print(f"✅ Đã sinh bài viết SEO mới từ Queue: {topic['slug']}.html")
            break

    # 1b. Nếu hàng đợi tĩnh đã xuất bản hết -> dùng Gemini sinh bài mới tự động
    if not created_article:
        ai_topic = generate_ai_seo_topic_gemini(existing_slugs)
        if ai_topic:
            file_path = os.path.join(BASE_DIR, f"{ai_topic['slug']}.html")
            html_content = render_article_html(ai_topic, today_iso)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            created_article = ai_topic
            print(f"🤖 Đã sinh bài viết SEO mới bằng Gemini AI: {ai_topic['slug']}.html")

    # 2. Cập nhật độ tươi mới trên trang chủ index.html & gắn link nội bộ
    update_index_freshness_and_links(today_vn_str, created_article)

    # 3. Đồng bộ bài viết mới vào llms.txt cho AI Search (ChatGPT, Perplexity, Google AI Overviews)
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

    # 6. Gửi báo cáo về Telegram (khi chạy trên GitHub Actions có secret)
    if created_article:
        article_line = f"📝 <b>Bài SEO mới xuất bản:</b>\n<a href='{SITE_URL}/{created_article['slug']}.html'>{created_article['title']}</a>\n"
    else:
        article_line = "🔄 <b>Cập nhật độ tươi mới (Freshness):</b> Đã làm mới dấu thời gian mẻ dừa hôm nay & toàn bộ Sitemap.\n"

    report = (
        f"📈 <b>[AUTO-SEO HÀNG NGÀY V4.0 - {today_vn_str}]</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{article_line}"
        f"🗺️ <b>Sitemap.xml:</b> Đã đồng bộ <b>{len(all_urls)} trang</b> (<code>lastmod: {today_iso}</code>)\n"
        f"🔔 <b>IndexNow Ping:</b> HTTP <code>{ping_status}</code> (Bing / Cốc Cốc / AI Search)\n"
        f"🌐 <b>Website:</b> <a href='{SITE_URL}'>duasaptravinh.vercel.app</a>"
    )
    send_telegram_report(report)
    print("🎉 Hoàn tất chu trình Auto-SEO Hàng Ngày V4.0!")


if __name__ == "__main__":
    main()
