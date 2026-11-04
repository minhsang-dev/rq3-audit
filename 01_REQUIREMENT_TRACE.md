# 01 — REQUIREMENT TRACE (G0)

- **STATUS:** G0 DRAFT — chờ NCS duyệt.
- **SOURCE ANCHORS:** `sources/outline_v14_3_RQ3_RQ4_verbatim.txt` — dòng nêu trong từng mục (L = số dòng của tệp này trong repo).
- **ASSUMPTIONS:** Trích dẫn dưới đây là nguyên văn (giữ nguyên ký hiệu pandoc như `E_(y ∼ …)`, `ℒ_(V)`). Phân loại theo thang của hồ sơ: ĐỀ CƯƠNG QUY ĐỊNH / BẰNG CHỨNG ĐÃ KIỂM / SUY LUẬN / GIẢ THUYẾT / CHƯA XÁC MINH / ĐỀ XUẤT SỬA (CHƯA DUYỆT). Ở G0 chỉ dùng "ĐỀ CƯƠNG QUY ĐỊNH" (trích) và "CHƯA XÁC MINH"; chưa có "BẰNG CHỨNG ĐÃ KIỂM" nào.
- **OPEN QUESTIONS:** các điểm đánh dấu ⚑ là chỗ có thể mơ hồ, chuyển sang G1 làm câu hỏi; **không tự quyết ở đây**.
- **DECISION:** Không sửa RQ/H/ε. H3 = NO CONCLUSION.

## A. Trích nguyên văn (ĐỀ CƯƠNG QUY ĐỊNH)

### A1. RQ3 (L8) và H3 (L10)
> RQ3: Khi mỗi ngày chỉ được gán b nhãn và nhãn đến sau độ trễ τ, chọn mẫu nào để gửi chuyên viên sẽ tối đa hóa chất lượng phát hiện?

> H3: Với b ∈ {100, 300, 1.000} nhãn/ngày và τ ∈{0; 1 ngày; 7 ngày}, chọn mẫu theo giảm lỗi kỳ vọng tính trên ngữ cảnh đạt F1-macro cao hơn chọn theo độ bất định ít nhất ε₃ và có chỉ số phơi nhiễm thấp hơn; phép so được thực hiện cả khi có và không có bộ lọc chống đầu độc.

### A2. Định nghĩa 4 (L27)
> Định nghĩa 4 – Ngân sách nhãn và độ trễ nhãn. Mỗi chu kỳ t, tối đa b dòng được gửi cho chuyên viên; nhãn của dòng gửi lúc s chỉ có từ thời điểm s + τ, với τ ∈ {0; 1 ngày; 7 ngày}. Chất lượng được đo cả bằng chỉ số phơi nhiễm: tổng thời gian các luồng tấn công không bị phát hiện kể từ khi họ tấn công đó xuất hiện [2].

### A3. Công thức (2-6) (L56–60)
> Điểm chọn mẫu là giảm lỗi kỳ vọng [31] tính trên ngữ cảnh:
>
> g(x) = E_(y ∼ p̂(⋅∣x))[ℒ_(V)(C)−ℒ_(V)(C∪{(x,y)})] (2-6)
>
> trong đó tập kiểm V_(t) gồm các dòng có nhãn chuyên viên, từ nguồn không bị gắn cờ, thuộc phần nhãn dành riêng η·b (mục 2.1), rời khỏi C_(t) và Dcal, trong cửa sổ W_(V) ngày gần nhất; độ cũ của V_(t) được báo cáo.

### A4. Nội dung 3 — toàn bộ (L54–64)
> Nội dung 3 – Chọn mẫu gán nhãn theo giảm lỗi kỳ vọng (RQ3)
>
> Điểm chọn mẫu là giảm lỗi kỳ vọng [31] tính trên ngữ cảnh:
>
> g(x) = E_(y ∼ p̂(⋅∣x))[ℒ_(V)(C)−ℒ_(V)(C∪{(x,y)})] (2-6)
>
> trong đó tập kiểm V_(t) gồm các dòng có nhãn chuyên viên, từ nguồn không bị gắn cờ, thuộc phần nhãn dành riêng η·b (mục 2.1), rời khỏi C_(t) và Dcal, trong cửa sổ W_(V) ngày gần nhất; độ cũ của V_(t) được báo cáo.
>
> Nhãn giả chỉ là một biến thể ablation: hạn mức ≤ 10% ngữ cảnh, không vào ngăn k_H và tập V, bị thay khi nhãn thật đến, và không áp dụng cho dòng dự đoán là bình thường thuộc vùng trôi dạt (để tránh nạp họ tấn công mới với nhãn bình thường). Rủi ro tự khẳng định sai được đo trực tiếp.
>
> Đối chứng: chọn ngẫu nhiên; chọn theo độ bất định (kiểu INSOMNIA [3]); chọn theo mật độ (NetGuard [1]); kích hoạt khi phát hiện thay đổi (STRAL [4]); chiến lược bất định có ngẫu nhiên hóa cho luồng trôi dạt [30]; và giảm lỗi kỳ vọng cho LightGBM ở cùng ngân sách để kiểm chứng H1a. Với LightGBM, g(x) được tính chính xác (huấn luyện lại với từng nhãn giả định) nếu tổng chi phí nằm trong ngân sách; nếu vượt, dùng xấp xỉ bằng refit của LightGBM (giữ cấu trúc cây, chỉ ước lượng lại giá trị lá), và báo cáo sai lệch của xấp xỉ so với cách tính chính xác trên một mẫu con.

### A5. Các đoạn liên quan trực tiếp (không nằm trong danh sách trích bắt buộc nhưng H3/g(x) dựa vào)
> Ngân sách nhãn cho V_(t) và D_(cal). Tập kiểm V_(t) (dùng cho g(x) ở Nội dung 3 và I_(i) ở Nội dung 4) và tập hiệu chỉnh D_(cal) đều cần nhãn chuyên viên, nên được trừ vào cùng ngân sách b. Mỗi ngày, η·b nhãn (η = 0,2) được dành riêng cho hai tập này; (1 − η)·b nhãn còn lại dùng cho chiến lược chọn mẫu đang đánh giá. Phần dành riêng được lấy ngẫu nhiên phân tầng theo điểm dự đoán của mô hình, lấy dư ở các tầng điểm cao để có đủ dòng tấn công, và mỗi dòng mang trọng số nghịch đảo xác suất được chọn để ước lượng trên V_(t) và D_(cal) không bị lệch. (L37)

> Ba câu hỏi RQ2–RQ4 không độc lập: chúng cùng tác động lên một tập dữ liệu có nhãn duy nhất theo thứ tự lọc → chọn → nạp. Vì vậy RQ2 và RQ3 được đánh giá cả khi có nhiễu nhãn, và RQ3, RQ4 được đánh giá khi ba cơ chế chạy chung (Nội dung 5). (L20)

> C_(t) = π(C_(t − 1), N_(t), U_(t)),  |C_(t)| ≤ k(B) (2-2) — "trong đó N_(t) là các dòng vừa có nhãn đã qua bộ lọc và U_(t) là luồng chưa nhãn." (L21–23)

> Biên hiệu ứng: "ε₃ = 0,02 F1-macro … Mỗi biên được chọn theo hai tiêu chí và giá trị chốt là giá trị lớn hơn: (i) ý nghĩa vận hành … (ii) vượt nhiễu – không nhỏ hơn 2 lần độ lệch chuẩn giữa các seed, ước lượng trên dữ liệu phát triển." (L53, rút gọn bằng dấu …)

> Định nghĩa 6 (L31–35): ngưỡng cảnh báo λ_t chọn sao cho tỷ lệ báo động nhầm ước lượng không vượt α_t = A_FP / N̂_t (2-3), hiệu chỉnh trên D_cal rời khỏi ngữ cảnh và V_t.

## B. Bảng truy vết yêu cầu RQ3

| ID | Yêu cầu (diễn đạt lại ngắn) | Neo | Phân loại | Gate xử lý | Ghi chú / ⚑ |
|---|---|---|---|---|---|
| R3-01 | b ∈ {100,300,1000}/ngày | L10, L27 | ĐỀ CƯƠNG QUY ĐỊNH | G2-A2, G4 | Probe G4 chỉ dùng b ∈ {100,300} (theo hồ sơ) — thu hẹp so với H3, ghi nhận. |
| R3-02 | τ ∈ {0; 1; 7 ngày}; nhãn của dòng gửi lúc s có từ s+τ | L10, L27 | ĐỀ CƯƠNG QUY ĐỊNH | G1 timeline, G2-A3 | ⚑ "ngày" vs "chu kỳ t" có cùng độ dài không? |
| R3-03 | So sánh chính: EER-trên-ngữ-cảnh vs bất định; F1-macro cao hơn ≥ ε₃ **VÀ** phơi nhiễm thấp hơn (hội của hai điều kiện) | L10 | ĐỀ CƯƠNG QUY ĐỊNH | G2-A1, G4 | ⚑ "thấp hơn" có biên không? Có nhất thiết ở **mọi** (b,τ) không? Chiều thống kê (trung bình/mọi ô) chưa nêu trong trích. |
| R3-04 | Phép so thực hiện cả khi có và không có bộ lọc chống đầu độc | L10 | ĐỀ CƯƠNG QUY ĐỊNH | G1 timeline | Phụ thuộc RQ4 + Nội dung 5 (thiếu). |
| R3-05 | Chỉ số phơi nhiễm = tổng thời gian luồng tấn công không bị phát hiện kể từ khi họ xuất hiện, tham chiếu [2] | L27 | ĐỀ CƯƠNG QUY ĐỊNH | G1 | ⚑ đơn vị; first-detection vs mọi luồng; ngưỡng phát hiện (Định nghĩa 6); censoring; [2] chưa mở. |
| R3-06 | g(x) = E_{y∼p̂(·|x)}[ℒ_V(C) − ℒ_V(C∪{(x,y)})] | L58 | ĐỀ CƯƠNG QUY ĐỊNH | G1, G2-A2 | ⚑ ℒ_V chưa xác định; p̂ lấy từ đâu; "kỳ vọng" lấy trên những y nào. |
| R3-07 | V_t: dòng có nhãn chuyên viên, nguồn không bị gắn cờ, thuộc phần dành riêng η·b, rời C_t và D_cal, cửa sổ W_V | L60 | ĐỀ CƯƠNG QUY ĐỊNH | G1, G2-A3 | ⚑ giá trị W_V không nêu; độ cũ "được báo cáo" nhưng không có ngưỡng. Nhãn trễ τ tác động V_t thế nào? |
| R3-08 | η = 0,2; (1−η)·b dùng cho chiến lược đang đánh giá; phần dành riêng lấy ngẫu nhiên phân tầng, lấy dư ở tầng điểm cao, trọng số nghịch đảo xác suất | L37 | ĐỀ CƯƠNG QUY ĐỊNH | G2-A2/A3 | Hệ quả (SUY LUẬN, G2): ngân sách hiệu dụng cho chọn mẫu là 80, 240, 800 nhãn/ngày. Chưa xác minh trong G0. ⚑ ngân sách η·b có bị τ làm trễ như nhãn khác không? |
| R3-09 | Nhãn giả: chỉ ablation, ≤10% ngữ cảnh, không vào k_H và V, bị thay khi nhãn thật đến, không áp cho dòng dự đoán bình thường thuộc vùng trôi dạt; đo trực tiếp rủi ro tự khẳng định sai | L62 | ĐỀ CƯƠNG QUY ĐỊNH | G2-A5 | ⚑ "k_H" (ngăn H) chưa định nghĩa trong trích; "vùng trôi dạt" xác định bởi gì? |
| R3-10 | Đối chứng 1: chọn ngẫu nhiên | L64 | ĐỀ CƯƠNG QUY ĐỊNH | G3 | Không cần nguồn ngoài. |
| R3-11 | Đối chứng 2: bất định kiểu INSOMNIA [3] | L64 | ĐỀ CƯƠNG QUY ĐỊNH | G1, G3 | [3] chưa mở → MENTIONED_ONLY. ⚑ entropy/margin/least-confidence. |
| R3-12 | Đối chứng 3: mật độ (NetGuard [1]) | L64 | ĐỀ CƯƠNG QUY ĐỊNH | G3 | [1] chưa mở → MENTIONED_ONLY. |
| R3-13 | Đối chứng 4: kích hoạt khi phát hiện thay đổi (STRAL [4]) | L64 | ĐỀ CƯƠNG QUY ĐỊNH | G3 | [4] chưa mở → MENTIONED_ONLY. |
| R3-14 | Đối chứng 5: bất định ngẫu nhiên hóa cho luồng trôi dạt [30] | L64 | ĐỀ CƯƠNG QUY ĐỊNH | G3 | [30] chưa mở → MENTIONED_ONLY. |
| R3-15 | Đối chứng 6: EER cho LightGBM cùng ngân sách (kiểm chứng H1a); chính xác (refit mỗi nhãn giả định) nếu chi phí trong ngân sách, ngược lại xấp xỉ refit lá; báo sai lệch trên mẫu con | L64 | ĐỀ CƯƠNG QUY ĐỊNH | G2-A2, G3, G4 | ⚑ "ngân sách" ở đây là ngân sách tính toán — định lượng không nêu trong trích. H1a không có trong tệp. |
| R3-16 | ε₃ = 0,02 F1-macro; giá trị chốt = max(quy đổi vận hành, 2×SD giữa seed) | L53 | ĐỀ CƯƠNG QUY ĐỊNH | G4 | Hai giá trị quy đổi "được tính và khóa khi đăng ký trước" — chưa tính; có thể làm ε₃ chốt > 0,02 (SUY LUẬN). Không sửa. |
| R3-17 | Chỉ số đánh giá mỗi ngày tính trên mẫu cố định phân tầng, giữ toàn bộ luồng họ hiếm; cùng mẫu cho mọi phương pháp/seed | L43 | ĐỀ CƯƠNG QUY ĐỊNH | G4 | Ràng buộc thiết kế probe. |
| R3-18 | Thống kê: mô hình hiệu ứng hỗn hợp, ngày gốc ngẫu nhiên; bootstrap phân cấp; công suất ≥ 0,8 tại ε; không nới biên | L51 | ĐỀ CƯƠNG QUY ĐỊNH | G4 | Probe DEV không phải kiểm định đăng ký trước. |
| R3-19 | Thứ tự "lọc → chọn → nạp"; RQ3 và RQ4 đánh giá khi ba cơ chế chạy chung (Nội dung 5) | L20 | ĐỀ CƯƠNG QUY ĐỊNH | G1 | Nội dung 5 SOURCE MISSING → HOLD. Khả năng INTERFACE_CONFLICT (nhãn trễ τ vs "lọc trước chọn"): CHƯA XÁC MINH, kiểm ở G1. |
| R3-20 | Nội dung 3 dùng V_t "rời khỏi C_t": g(x) tính trên C = ngữ cảnh do chính sách π (HB2 cho RQ2) quản lý | L60, L21 | ĐỀ CƯƠNG QUY ĐỊNH + hồ sơ giao việc | G2-A4 | HB2 SOURCE MISSING → HOLD. |

## C. Ràng buộc từ hồ sơ giao việc (không thuộc đề cương)

| ID | Ràng buộc | Phân loại |
|---|---|---|
| T-01 | Không sửa RQ/H, ε, mã, dữ liệu đã khóa; không chạy CPU/GPU; không tạo runner | Chỉ thị NCS |
| T-02 | Thiếu nguồn → "SOURCE MISSING" + HOLD | Chỉ thị NCS |
| T-03 | RQ2 dùng HB2 làm chính sách ngữ cảnh đã khóa; ThreeBin CLOSED_AT_DEV | Hồ sơ giao việc (CHƯA XÁC MINH bằng RQ2_DECISION_LOG) |
| T-04 | Không trộn ActiveLab × FS-FI với EER của đề cương | Chỉ thị NCS |
| T-05 | Hệ số TabFM "4,36 s + 5,25 s/1.000 hàng truy vấn mỗi ngày, k = 2.000" (Bài 1) | Số do NCS cung cấp; CHƯA XÁC MINH (báo cáo gốc thiếu) |
| T-06 | Xuất từng gate; dừng chờ duyệt sau G0 | Chỉ thị NCS |

## D. Ghi nhận cấu trúc (không phải kết luận)

1. Hồ sơ giao việc mô tả H3 gọn đúng như đề cương; không phát hiện sai khác giữa tóm tắt trong hồ sơ và nguyên văn đề cương ở các mục trích (kiểm tay, G0).
2. Đề cương gắn "(2-6)" cho EER và dùng cùng V_t cho I_i (2-7) của RQ4 — V_t là tài nguyên dùng chung giữa RQ3 và RQ4; ghi để G1 xét phụ thuộc vòng (V_t loại nguồn bị gắn cờ, mà gắn cờ nguồn là tầng của RQ4).
3. Số kết quả/ước lượng nào cũng chưa có: **H3 = NO CONCLUSION**.

## E. Ánh xạ số tham khảo ↔ khóa (bổ sung lần 2; nguồn gián tiếp)

Nguồn: bảng KT3 trong `sources/REVIEW_SKELETON.md` (dòng 74) và ghi chú `Outline ref` trong `REVIEW_REFS.bib`. **CHƯA XÁC MINH** với danh mục gốc của đề cương (thiếu `outline_v14_3_references.txt`).

| Số | Khóa | Công trình | Mức đọc theo bib/CSV | Ghi chú |
|---|---|---|---|---|
| [1] | gupta2025netguard | Generative active adaptation for drifting and imbalanced NID (arXiv:2503.03022) | "opened: arXiv abs page" | bib ghi `Outline ref [1]` |
| [2] | botacin2025 | Botacin & Gomes, Towards more realistic evaluations: label delays in malware detection pipelines, Comput. Secur. 148, 104122 (2025) | bib: "Abstract not read in full"; phiên này: chỉ bản ghi Crossref | **Đã phân giải bằng `outline_v14_3_references.txt` [2]**; nội dung chưa đọc |
| [3] | andresini2021 | INSOMNIA (AISec '21) | FIX applied (thư mục); "FIT OK (active learning / label estimation)" | Bib ghi "Bai1 ref [16]", không ghi Outline ref [3]; ánh xạ [3] chỉ từ bảng KT3 |
| [4] | ndichu2026stral | STRAL (arXiv:2605.22324) | bib ghi `Outline ref [4]` | |
| [30] | zliobaite2014active | Active learning with drifting streaming data (TNNLS 2014) | "Crossref record opened; content not read" | Ánh xạ [30] chỉ từ bảng KT3 |
| [31] | roy2001eer | Roy & McCallum, EER (ICML 2001) | "abstract page only; edition [VERIFY]" | Ánh xạ [31] chỉ từ bảng KT3 |

Lưu ý: không khóa nào trong bảng được đọc tới mức phương pháp theo bib/CSV, ngoại trừ ghi chú methods-read của `treerath2026tabaicl` (qua NOVELTY_AUDIT_2, không đính kèm). `cacciarelli2024` (survey) và `settles2010` (§ Expected Error Reduction, mục 3.4 theo bib) là nguồn bổ sung của nhóm RQ3 trước, cũng mới mở mức bìa/Crossref.

## F. Dữ kiện từ nguồn mới liên quan trực tiếp tới RQ3 (BẰNG CHỨNG ĐÃ KIỂM = có trong tệp đính kèm; chưa kiểm độc lập)

- `RQ2_DECISION_LOG.md` §2: giao thức Bài 1 replay L5 ("score first, learn after"), k = 2.000, LightGBM đã khóa, CPU-only cho DEV. §3: **không còn root DEV chưa dùng** → mọi probe G4 là DEV_REUSE (khớp hồ sơ giao việc). §8–9: HB2 = CBRS_FAMILY + H = 200 dòng benign chọn theo điểm tấn công (top-k); trạng thái GO CONTRIBUTION CANDIDATE phạm vi LightGBM, CIDDS-001; TabFM phase chưa làm.
- Bản thảo Bài 1: giao thức dùng b, η, k, τ; thiết lập chính τ = 0 ngày (dòng 178). Hệ số thời gian TabFM xem `00_SOURCE_MANIFEST.md` mục 3.
- `RQ2_DECISION_LOG.md` §10: novelty audit RQ2 = NARROW_REQUIRED; Tab-AICL nằm trong nhóm công trình gần nhất của RQ2 và cũng được `REVIEW_SKELETON.md` đánh dấu cần nhóm RQ3 đọc lại.

**Cập nhật v3:** đối chiếu với `sources/outline_v14_3_references.txt` (dòng 2–5, 31–32): [1] Gupta et al. arXiv:2503.03022; [2] Botacin & Gomes 2025; [3] INSOMNIA (Andresini et al. 2021); [4] STRAL arXiv:2605.22324; [30] Žliobaitė, Bifet, Pfahringer, Holmes, TNNLS 25(1) 2014; [31] Roy & McCallum, ICML 2001. **Ánh xạ số↔công trình VERIFIED** theo danh mục gốc của đề cương (không còn "gián tiếp"). Mức đọc nội dung các công trình vẫn như bảng trên.
