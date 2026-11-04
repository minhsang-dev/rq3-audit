# 06 — DECISION MEMO (G5) — RQ3 / H3

- **STATUS:** G5 DRAFT, chờ NCS duyệt. Kiểm toán trên giấy; **chưa có thực nghiệm nào**. **H3 = NO CONCLUSION.**
- **SOURCE ANCHORS:** `03_ASSUMPTIONS_AND_COST.md` (A1–A6); `04_BASELINE_AND_NOVELTY.md`; `05_FUTURE_PROBES.md`; `sources/outline_v14_3_RQ3_RQ4_verbatim.txt` (H3 L10, ε₃ L53, Nội dung 1 L51); `sources/RQ2_DECISION_LOG.md` §3, §8–9 (số root); `sources/THESIS_AUDIT_LOG_RQ3_RQ4.md` §5.
- **ASSUMPTIONS:** Số TabFM là ngoại suy từ pilot Bài 1. Đề cương v14.3 đã nộp, **không sửa** trong ~6 tháng; mọi phương án sửa dưới đây là **ĐỀ XUẤT SỬA (CHƯA DUYỆT)**, chỉ để chuẩn bị.
- **OPEN QUESTIONS:** mục 5.
- **DECISION:** Không có kết luận khoa học. Thứ tự chạy NCS đã duyệt: **P3b → kiểm thử (a)–(e) → P3a (ô τ = 0 trước) → P3c**.

## 1. Trạng thái giả định
| ID | Giả định | Trạng thái | Lý do cốt lõi |
|---|---|---|---|
| A1 | EER hơn bất định ≥ ε₃ = 0,02 F1-macro | **AT_RISK** | Không nguồn đã mở định lượng khoảng cách trong luồng trôi dạt, mất cân bằng, nhãn trễ; chỉ 80/240/800 nhãn chọn/ngày so với k = 2.000; ε₃ cuối có thể > 0,02 |
| A2 | Chi phí EER chịu được | **NEEDS_APPROXIMATION**; chính xác toàn pool trên TabFM = FALSIFIED_ON_PAPER | ≥ 3,5 GPU-giờ/chuỗi ở N_c = 200; LightGBM khả thi nếu lấy mẫu ứng viên |
| A3 | Nhãn trễ τ = 7 | **AT_RISK** | V_t cũ 8–10 ngày, điểm mù với họ mới; đề cương không nêu cơ chế lợi thế |
| A4 | Tương tác HB2 | **AT_RISK** | Xác suất nạp < 1, thay thế, H chỉ benign, bộ lọc RQ4 chặn; g(x) ngây thơ |
| A5 | Nhãn giả | **PLAUSIBLE** (điều kiện) | Chỉ ablation; V_t không chứa nhãn giả; vùng trôi dạt đã định nghĩa (Q18) |
| A6 | Ngưỡng λ_t ở b nhỏ | **AT_RISK** (b = 100) | Sàn báo động nhầm 18–33% |
| Tính mới | | **GAP_NARROW** | Từng thành phần đã có; chưa thấy tổ hợp trong phạm vi đã tìm; tìm kiếm extended hoãn tới trước khi viết đóng góp |

Không giả định nào được xác nhận bằng thực nghiệm; "PLAUSIBLE" chỉ nghĩa là chưa thấy lý do bác trên giấy.

## 2. Rủi ro chính của H3 trên TabFM
Dưới trần NCS (≤ 1 GPU-giờ/ngày), số ứng viên tối đa ≈ **400 / 370 / 300** cho b = 100 / 300 / 1.000, trong khi cần N_c = 10·b′ = **800 / 2.400 / 8.000** để giữ áp lực chọn 10% (đạt 0,5× / 0,15× / 0,04×). Ở b = 300, EER chọn ≈ 65% ứng viên ⇒ gần như mất tính chọn lọc. *Ngoại suy từ Bài 1* (4,36 + 5,25·|V|/1000 s mỗi giả thuyết); **chưa quyết, chờ đo GPU thật chung lượt với P4d của RQ4.** Hai phương án NCS đã nêu: (i) nâng trần (phải báo cáo chi phí); (ii) EER hai tầng có danh sách rút gọn (LightGBM chấm rút gọn → TabFM chấm lại), dùng U_c để tách tác dụng của bước rút gọn.

## 3. Phương án sửa đề cương (CHƯA DUYỆT; xét sau 6 tháng)
| # | Nội dung | Kích hoạt khi | Ghi chú |
|---|---|---|---|
| S1 | Khai báo họ kiểm định chính nhỏ cho H3 (vài ô), ô còn lại chỉ mô tả; thay "mọi (b, τ)" của H3 | A1/A2/A6 AT_RISK và công suất | Gắn với phương án (a) mục 4 |
| S2 | Ghi rõ EER xấp xỉ bằng **lấy mẫu ứng viên** (N_c = 10·b′), không chỉ refit lá; và EER hai tầng cho TabFM | A2 | L64 chỉ nêu refit lá |
| S3 | Định nghĩa chính thức: phơi nhiễm E3, F1-macro 2 lớp tại λ_t, ℒ_V = log-loss 1/π, V_t theo ngày đến, nhãn dùng từ t+1 | Q1–Q16 | Đề cương không nêu; hiện chỉ là PROPOSAL |
| S4 | Ghi giai đoạn làm nóng nhãn τ + 2 ngày và lịch sử nhãn trước luồng, ngoài ngày đánh giá | τ > 0 | Q23 |
| S5 | Với b = 100: báo AUPRC_w và recall ở số cảnh báo nhầm cố định, hoặc đưa ô này khỏi họ chính | A6 | L35 chỉ dự phòng cho ngày ít lưu lượng bình thường |
| S6 | Cho g(x) nhận biết HB2 / nhãn đang chờ là nhánh DEV chứ không phải đối chứng | A3, A4 | Chỉ nếu loaded@3 thấp (< 25% hoặc < 50% của U) |
| — | **Không đề xuất** nới ε₃ (đề cương: "không nới biên") | | |

## 4. Công suất: Holm với số root hữu hạn (lỗi Q15, đã nhận)
Wilcoxon một phía chính xác trên n root có p nhỏ nhất 1/2ⁿ. Qua Holm với m ô cần 1/2ⁿ < 0,05/m. **Số root tối thiểu mỗi ô** (điều kiện cần, không phải đủ):

| m ô trong họ chính | 1 | 2 | 3 | 4 | 6 | 9 | 18 |
|---|---|---|---|---|---|---|---|
| n, mọi root cùng dấu | 5 | 6 | 6 | 7 | 7 | 8 | **9** |
| n, cho phép 1 root ngược (hạng 1) | 6 | 7 | 7 | 8 | 8 | 9 | 10 |

**Root thực có (nguồn: `RQ2_DECISION_LOG` §3, §8–9):** CIDDS-001-internal **7 root** (03-15, 16, 17, 20, 21, 23, 24; EXPOSED_OTHER, cùng một môi trường); NF-UNSW-NB15-v3 **2 root** (2015-01-22 EXPOSED_OTHER, gần trần: AP 0,974 ở mọi nhánh; 2015-02-18 EXPOSED_RQ2); UGR'16 không dùng được (HOLD_DATA, một cụm). Log ghi "≈ 2 cụm độc lập" cho cả hai tập. DEV: 6 root "informative" (DEV_REUSE, không dùng để xác nhận).

| Phương án | Họ chính | n cần | Đủ root? |
|---|---|---|---|
| **(a) Họ nhỏ khai báo trước** | m = 2–4 ô chính (ví dụ b = 300, τ ∈ {0, 1, 7}) | 6–7 (mọi cùng dấu) | **Về số lượng danh nghĩa: có** — CIDDS 7 root. Nhưng chúng cùng một môi trường (≈ 1 cụm), đã lộ với RQ2 (HB2), và m = 4 cần cả 7 root cùng dấu (không dư). Thực tế **sát giới hạn** |
| **(b) Đủ root cho 18 ô** | m = 18 | 9 (cùng dấu); 10 (một đảo) | **Không**: CIDDS 7 + UNSW 2 = 9 danh nghĩa, nhưng UNSW 01-22 gần trần, UNSW 02-18 đã lộ cho RQ2, và chỉ ≈ 2 cụm độc lập. Cần thêm ngày gốc (Nội dung 1: thêm bộ dữ liệu hoặc kéo dài giai đoạn) — **chưa có nguồn** |
| (c) (tôi nêu thêm) Tăng root bằng bộ dữ liệu mới | ≥ 9 root độc lập | 9 | Cần dữ liệu có nhãn chuẩn lược đồ Bài 1; UGR'16 hiện không dùng được |

Khuyến nghị (nêu ý kiến, NCS quyết): chốt trong tiền đăng ký **phương án (a)** với m ≤ 3 ô chính, vì (b) chưa khả thi với dữ liệu hiện có. Mục 3 ghi thêm: thư mục CIDDS đã được RQ2 dùng cho xác nhận HB2 (`THESIS_AUDIT_LOG` §5, mục 1 đề nghị bỏ CIDDS khỏi vai trò xác nhận phụ), nên số root còn lại **cho riêng RQ3** nhỏ hơn con số danh nghĩa.

## 5. Thứ tự probe và câu hỏi còn mở
1. **P3b** (≈ 2 CPU-giờ): thời gian thực LightGBM; chốt N_c và tỉ số N_c/b′.
2. **Kiểm thử (a)–(e)** của g(x) (≈ 1–1,5 CPU-giờ): không đạt thì dừng.
3. **P3a**, ô τ = 0 trước (S1: 3 root × 2 seed ≈ 1,9 giờ; rồi đủ 6 root × 5 seed; toàn P3a ≈ 74 giờ).
4. **P3c** (≈ 67 giờ), chỉ nếu P3a không FALSIFIED; chạy τ ≥ 1 sau khi Q23 đã đồng ý (đã duyệt).
5. Đo GPU TabFM thật chung P4d (RQ4) để quyết định trần/EER hai tầng.

Đã chốt: Q23 (lịch sử nhãn trước luồng, làm nóng τ + 2 ngày), Q24 (cùng trần, báo chi phí từng nhánh), Q25 (log-loss 1/π; 0-1 độ nhạy; N_c = 10·b′; U_c), Q26 (root "đủ thông tin" chỉ từ nhánh ngẫu nhiên, chốt trước khi xem EER, báo cáo root bị loại). **Còn mở:** (i) chọn (a) hay (b) cho tiền đăng ký; (ii) phần cứng CPU/số lõi cho P3b; (iii) định nghĩa phơi nhiễm gốc của [2] chưa đối chiếu được (chưa mở bài); (iv) tìm kiếm extended + đọc Pham 2022, Žliobaitė 2014 trước khi viết đóng góp.
