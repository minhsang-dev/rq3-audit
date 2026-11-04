# Khung tiểu luận tổng quan (v1)

**Đề tài:** Mô hình nền tảng dạng bảng, học trong ngữ cảnh và quản lý dữ liệu có nhãn cho phát hiện xâm nhập thích nghi.
**Phạm vi file này:** chỉ khung và thư mục tham khảo; không viết nội dung đầy đủ. Khóa tham khảo (`khóa`) tra trong `REVIEW_REFS.bib` / `REVIEW_REFS_STATUS.csv`.

**Quy ước trạng thái** (theo STATUS.csv): *OK / FIX applied* = đã kiểm ở REF_CHECK hoặc trang nguồn đã mở; *OK (bib from rq2_REFS_v2_1.bib; methods read)* = mục từ bản tìm RQ2, phần phương pháp đã đọc theo PRIOR_ART/NOVELTY_AUDIT; *provisional* = mới đọc tóm tắt, đoạn trích hoặc một phần. Không còn mục STUB.

**Đầu vào đã đủ (cập nhật):** `rq2_REFS_v2_1.bib`, `outline_v14_3_overview_KT.txt` và `outline_v14_3_references.txt` đã được dùng; 55 mục STUB cũ được thay bằng mục đầy đủ; 21 tài liệu của đề cương chưa có trong danh sách gộp đã được mở nguồn và thêm vào (xem `COVERAGE.md`). Bài 1 [9] là bản thảo của NCS chưa công bố (REF_CHECK: NOT_FOUND), không đưa vào danh sách tiểu luận và không trích kết quả của nó.

**Ràng buộc chung:** không nêu kết quả thực nghiệm của NCS (kể cả mức phát triển của HB2). Các mệnh đề "chưa thấy tiền lệ" chỉ phát biểu theo phạm vi tìm kiếm của các bản kiểm toán đính kèm.

---

## 1. IDS dưới trôi dạt và nhãn trễ: giao thức đánh giá theo thời gian, rò rỉ thông tin tương lai

**Mục đích.** Trình bày vì sao đánh giá IDS phải tôn trọng thứ tự thời gian và độ trễ nhãn, và các nguồn rò rỉ thông tin tương lai thường gặp (chia ngẫu nhiên, nhãn đến sau, lỗi nhãn của bộ dữ liệu). Làm nền cho các giao thức ở các mục sau.

**Tài liệu (15):** `gama2014survey`, `lu2019review`, `shyaa2024`, `pendlebury2019`, `barbero2022`, `arp2022`, `andresini2021`, `botacin2025`, `zliobaite2010`, `grzenda2020`, `gama2013`, `liu2022`, `engelen2021`, `goldschmidt2025`, `luay2025`. Mở rộng theo đề cương: `alahmadi2022`, `cantone2024`, `macia2018ugr16`, `lipton2018`, `gomes2017arf`.

**Ghi chú dùng tài liệu.** `engelen2021` chỉ về CIC-IDS-2017; lỗi nhãn của CSE-CIC-IDS2018 dùng `liu2022`. `gama2014survey`/`lu2019review` là khảo sát chung, không dùng để hỗ trợ tuyên bố định lượng về tỷ lệ luồng độc hại.

**Câu hỏi mở.** Giao thức nào vừa tách đúng "chấm điểm trước, học sau" vừa mô phỏng độ trễ nhãn thực tế cho dữ liệu luồng mạng, và đo mức chênh giữa đánh giá theo thời gian với chia ngẫu nhiên thế nào mà không rò thông tin?

## 2. Mô hình nền dạng bảng và học trong ngữ cảnh (TabPFN, TabICL, TabFM), chi phí

**Mục đích.** Tóm lược các mô hình nền dạng bảng hoạt động bằng đọc ngữ cảnh (không cập nhật tham số), điểm mạnh trên dữ liệu nhỏ, và chi phí tính toán/bộ nhớ khi ngữ cảnh lớn; đối chiếu với LightGBM huấn luyện lại.

**Tài liệu (15):** `hollmann2025`, `qu2025tabicl`, `qu2026tabiclv2`, `googletabfm2026`, `kong2026tabfm`, `gangwani2025`, `helli2024`, `garcia2025`, `ke2017`, `thomas2024localpfn`, `ma2024tabdpt`, `feuer2024tunetables`, `xu2024mixturepfn`, `priorlabs2025tabpfn25`, `aldahmani2026`. Mở rộng theo đề cương: `kurashkin2026`, `googleblog2026tabfm`.

**Ghi chú dùng tài liệu.** `gangwani2025` đo TabPFN-1.0 và TabICL-base, không phải TabFM. Với TabFM nêu rõ biến thể (TabFM / TabFM+ / TabFM-Auto) [VERIFY]. Giấy phép trọng số TabFM là non-commercial.

**Câu hỏi mở.** Chi phí suy luận theo kích thước ngữ cảnh k của TabFM thay đổi thế nào so với huấn luyện lại LightGBM, và ngữ cảnh nên lớn đến mức nào cho IDS theo ngày?

## 3. Quản lý ngữ cảnh/bộ nhớ: replay trong học liên tục, bộ đệm cân bằng lớp/họ, chọn theo độ khó, CURE/DualFIFO

**Mục đích.** Hệ thống hóa các chính sách giữ/loại mẫu trong bộ nhớ bị chặn (hồ chứa cân bằng lớp, FIFO hai ngăn, cổng entropy, chọn theo độ khó/bất định) và phân biệt "bao nhiêu mẫu mỗi lớp" với "mẫu nào của lớp".

**Tài liệu (15):** `lourenco2026dualfifo`, `lee2026cure`, `chrysakis2020cbrs`, `amalapuram2023ecbrs`, `ariffin2026`, `aljundi2019mir`, `shim2021aser`, `bang2021rainbow`, `serra2025uncertainty`, `felzenszwalb2010`, `shrivastava2016ohem`, `xuan2020hard`, `abdullah2026ctxsamp`, `zhang2025ssf`, `rebuffi2017icarl`. Mở rộng theo đề cương (KT2): `mai2022survey`, `gonzalez1985`. Gần-liên quan để đối chiếu khi viết: `xie2025ugsr`, `mei2022hcil`, `rahman2025madar`, `treerath2026tabaicl`, `harun2025grasp`, `zhang2025sclifd`, `yang2025baep` (từ NOVELTY_AUDIT_2; bib đã có).

**Ghi chú dùng tài liệu.** Trừ `chrysakis2020cbrs`, `lourenco2026dualfifo`, `lee2026cure` (REF_CHECK) và các mục đã đọc phương pháp (T) theo PRIOR_ART_1, phần lớn mới đọc tóm tắt (A) hoặc đoạn trích (S): xem cột status, xếp *provisional*, mở lại trước khi trích. Theo NOVELTY_AUDIT_2 (RQ2: NARROW_REQUIRED): không viết "chưa có tiền lệ trực tiếp"; phát biểu theo hướng "áp dụng khai thác mẫu âm khó vào bộ nhớ có ngân sách nhãn, chọn theo lớp"; không gọi chọn theo điểm mô hình là đối xứng giữa các lớp (MADAR, UGSR có thiên lệch theo lớp); không viết "đánh giá độc lập". `xuan2020hard` và `abdullah2026ctxsamp` là cảnh báo về chọn khó nhất/chọn có chủ đích.

**Câu hỏi mở.** Giữ riêng một ngăn các dòng benign khó trong bộ nhớ cân bằng theo họ có ích hơn lấy ngẫu nhiên cùng ngân sách hay không, và khó nhất có nên là tiêu chí khi nhãn có thể nhiễu? (Chỉ nêu như câu hỏi; không trích kết quả của NCS.)

## 4. Chọn mẫu gán nhãn có ngân sách (active learning cho luồng, giảm lỗi kỳ vọng)

> **Mục này cần được mở rộng bởi nhóm RQ3.** Hiện chỉ dựa vào file đính kèm và 4 công trình mới mở (≤10 cho phép): `zliobaite2014active`, `cacciarelli2024`, `settles2010`, `roy2001eer`. Hai công trình đầu mới mở bản ghi Crossref, chưa đọc nội dung; `settles2010` mới thấy trang bìa và mục lục; `roy2001eer` mới đọc trang tóm tắt.

**Mục đích.** Đặt bài toán chọn dòng nào để xin nhãn khi ngân sách nhãn hằng ngày hữu hạn và nhãn đến trễ, từ truyền thống chọn mẫu theo bất định đến giảm lỗi kỳ vọng, và điểm khác của bối cảnh luồng có trôi dạt.

**Tài liệu (15):** `settles2010`, `roy2001eer`, `zliobaite2014active`, `cacciarelli2024`, `andresini2021`, `botacin2025`, `grzenda2020`, `zliobaite2010`, `treerath2026tabaicl`, `faber2022active`, `amalapuram2024soul`, `gupta2025netguard`, `ndichu2026stral`, `nguyen2026cdahal`, `lee2026cure`. Mở rộng: `ipas2026lucos`, `faber2023lifelong`.

**Ghi chú dùng tài liệu.** `lee2026cure` dùng entropy tính lúc dự đoán, trước khi biết nhãn: là cổng nhận vào bộ nhớ, không phải chọn dòng để xin nhãn. `treerath2026tabaicl` (margin của TabPFN dưới ngân sách nhãn) cần mở lại.

**Câu hỏi mở.** Với mô hình đọc ngữ cảnh, tiêu chí chọn dòng để gán nhãn có nên khác tiêu chí chọn dòng đưa vào ngữ cảnh, và giảm lỗi kỳ vọng có xấp xỉ rẻ được khi "huấn luyện lại" chỉ là đổi ngữ cảnh?

## 5. Nhãn nhiễu và đầu độc nhãn: lọc dòng, kiểm toán nguồn, chứng nhận độ bền

**Mục đích.** Phân biệt nhãn nhiễu ngẫu nhiên với lật nhãn có chủ đích từ nguồn bị chiếm; tổng hợp các tầng phòng thủ (lọc dòng kiểu RONI/kNN/confident learning, kiểm toán nguồn, chứng nhận độ bền) và các tấn công biết cơ chế phòng thủ.

**Tài liệu (15):** `nelson2008`, `northcutt2021`, `paudice2018`, `koh2022`, `jia2022knn`, `rosenfeld2020`, `dawid1979`, `miao2018`, `ma2020`, `fang2021`, `vejling2025`, `xu2016`, `lan2025`, `bilos2026`, `korycki2020`. (Đã chuyển `liu2022`, `ariffin2026` sang mục 1 và 3.) Mở rộng khi cần: `levine2021dpa`, `steinhardt2017`, `cao2022fltrust`, `sameera2025`, `priorpoison2026`, `dolejs2026`, `hu2026`, `djilani2025`, `severi2021`, `taheri2020`, `vejling2025`, `xu2016`, `luong2023fedls`, `ha2024`.

**Ghi chú dùng tài liệu.** `rosenfeld2020`, `levine2021dpa`, `steinhardt2017`, `dawid1979`, `cao2022fltrust` đang ở mức *provisional* (tóm tắt). `priorpoison2026` là kho mã chưa bình duyệt, một bộ dữ liệu, một seed. Chi tiết xếp hạng ở `RQ4_PRIOR_ART.md` (không có công trình nào xếp "same").

**Câu hỏi mở.** Một kiểm toán nguồn ngang hàng trong ngày cộng một bộ lọc dòng theo ảnh hưởng và hạn mức mỗi nguồn có giữ được ngữ cảnh sạch mà không loại nhầm trôi dạt thật và nguồn trung thực có phân phối khác không, kể cả khi đối thủ biết cơ chế?

## 6. Tổng hợp khoảng trống

Nội dung KT1–KT4 và ánh xạ RQ/giả thuyết lấy **nguyên văn** từ `outline_v14_3_overview_KT.txt` (mục "Những hạn chế còn tồn tại" và Bảng 1.2); không diễn giải lại. Cột "Mục & khóa" là các mục/khóa của tiểu luận này; trong ngoặc vuông là số tài liệu của đề cương.

| KT | Nội dung (nguyên văn đề cương) | RQ / giả thuyết (Bảng 1.2) | Mục & khóa tiểu luận | Bản kiểm toán đính kèm | Kết quả kiểm toán |
|---|---|---|---|---|---|
| **KT1** | "Chưa rõ khi nào TFM có lợi trong IDS. Các đánh giá TFM cho IDS chia dữ liệu tĩnh [21, 22]; chưa có so sánh công bằng giữa TFM và mô hình nhẹ khi cả hai dùng cùng dữ liệu có nhãn đã chọn, dưới trôi dạt và ngân sách nhãn." | RQ1; H1a, H1b | §1, §2: `garcia2025` [21], `aldahmani2026` [22], `pendlebury2019`, `botacin2025`, `helli2024`, `gangwani2025`, `ke2017` | Không có bản kiểm toán độ mới; chỉ `REF_CHECK.csv` kiểm thư mục của Bài 1 | Chưa thu hẹp hay xác nhận bởi kiểm toán nào |
| **KT2** | "Quản lý ngữ cảnh và bộ đệm chưa xét điều kiện an ninh. CURE và bộ nhớ trượt [13, 14] không bảo vệ họ tấn công hiếm; các bộ đệm cân bằng lớp trong học liên tục [25, 26] không xét nhãn trễ, họ tấn công tái xuất hiện sau thời gian dài vắng mặt, và tương tác với nhãn độc." | RQ2; H2 | §3: `lourenco2026dualfifo` [13], `lee2026cure` [14], `rebuffi2017icarl` [25], `chrysakis2020cbrs` [26], `amalapuram2023ecbrs`, `felzenszwalb2010` | `NOVELTY_AUDIT_2.md`, `PRIOR_ART_1.md` (kiểm toán HB2) | **NARROW_REQUIRED**: đóng góp chỉ còn là điều chỉnh có hướng lớp (xếp hạng riêng benign bằng điểm tấn công trong ngữ cảnh cân bằng theo họ); không dùng "chưa có tiền lệ trực tiếp" |
| **KT3** | "Học chủ động chưa được thiết kế cho học trong ngữ cảnh với nhãn trễ. Các phương pháp chọn mẫu cho IDS [1, 3, 4] huấn luyện lại và đa số coi nhãn đến ngay; giảm lỗi kỳ vọng [31] chưa được khảo sát cho TFM." | RQ3; H3 | §4 (nhóm RQ3 mở rộng): `gupta2025netguard` [1], `andresini2021` [3], `ndichu2026stral` [4], `zliobaite2014active` [30], `roy2001eer` [31], `treerath2026tabaicl` | Không có bản kiểm toán đính kèm | Chưa đánh giá. Ghi chú: `PRIOR_ART_1`/`NOVELTY_AUDIT_2` nêu `treerath2026tabaicl` (TabPFN, chọn nhãn theo margin dưới ngân sách), cần nhóm RQ3 đọc lại đối chiếu với KT3 |
| **KT4** | "Chưa có phòng thủ đầu độc nhãn cho ngữ cảnh TFM. Các nghiên cứu độ bền TFM chỉ xét né tránh lúc suy luận hoặc nhiễu ngẫu nhiên [36, 37]; RONI và định giá dữ liệu [33] chưa được đánh giá cho ngữ cảnh TFM với đối thủ thích nghi." | RQ4; H4a, H4b | §5: `djilani2025` [36], `hu2026` [37], `nelson2008` [33], `vejling2025` [34], `xu2016` [35], `bilos2026`, `koh2022`, `miao2018`, `ma2020`, `jia2022knn` [49] | `RQ4_GAP.md`, `RQ4_PRIOR_ART.md` | **GAP_NARROW**: các thành phần tồn tại riêng lẻ; chưa thấy tổ hợp nguồn + dòng + hạn mức cho mô hình học trong ngữ cảnh dạng bảng, chưa thấy chặn trên kiểu Mệnh đề 2, chưa thấy đối thủ thích nghi trên cặp này. Kiểm soát FDR cho nguồn đã có ([34], [35]) |

**Điểm lệch giữa văn bản KT và bằng chứng kiểm toán (nêu để NCS quyết định, không sửa KT):**
- KT4 viết các nghiên cứu độ bền TFM "chỉ xét né tránh lúc suy luận hoặc nhiễu ngẫu nhiên [36, 37]". `RQ4_PRIOR_ART.md` có `bilos2026` (lật nhãn "hub" trong ngữ cảnh TabPFNv2/TabICLv2, không có phòng thủ) và `priorpoison2026` (kho mã chưa bình duyệt); hai công trình này xét thao túng ngữ cảnh nhưng không có phòng thủ, nên mệnh đề "chưa có phòng thủ" vẫn đứng.
- KT4 nêu "RONI và định giá dữ liệu [33]"; trong đề cương [33] là RONI (Nelson et al.), còn định giá dữ liệu (`ghorbani2019`, `jia2019knnshap`, `pruthi2020`) không có số riêng trong danh mục của đề cương.
- KT2 viết bộ đệm cân bằng lớp "không xét nhãn trễ"; `amalapuram2023ecbrs` (PRIOR_ART_1) xử lý riêng lớp benign theo hạn mức số lượng và `ariffin2026` neo benign trong bộ đệm: chúng đã nằm trong §3, cần đối chiếu khi viết.

**Câu hỏi mở tổng.** Sau khi thu hẹp, phần đóng góp còn lại của mỗi KT là gì và cách viết nào không vượt quá bằng chứng của các bản kiểm toán?
