# HỒ SƠ GIAO VIỆC RQ3 — KIỂM TOÁN TRÊN GIẤY + THIẾT KẾ PROBE (Claude cloud) — v1, 04/11/2026

**Trạng thái:** `RQ3_PAPER_AUDIT = GO NOW`; `RQ3_DEV_PROBES = DESIGN NOW, RUN LOCALLY AFTER NCS APPROVAL`;
`H3 = NO CONCLUSION`. Mục đích: kiểm tra sớm các giả định nền của RQ3 trong đề cương v14.3, để kịp chuẩn bị nội dung sửa
đề cương nếu cần (bài học RQ2: ThreeBin thất bại vì giả định nền sai, phát hiện muộn).

## Cách giao (cho NCS)
- Repo private mới (ví dụ `rq3-audit`), đưa vào:
  1. `outline_v14_3_RQ3_RQ4_verbatim.txt` (RQ/H, Định nghĩa 4–6, biên ε, Nội dung 3–4, có công thức (2-6));
  2. `outline_v14_3_references.txt`;
  3. `REVIEW_SKELETON.md`, `REVIEW_REFS.bib`, `REVIEW_REFS_STATUS.csv` (khung tiểu luận, mục 4);
  4. `RQ2_DECISION_LOG.md` (bản mới nhất; HB2 là chính sách ngữ cảnh đã khóa cho RQ2);
  5. nếu có: báo cáo của nhóm RQ3 hiện tại (ActiveLab × FS-FI v0.1 NO-GO, v0.2 design) — chỉ để đối chiếu.
- claude.ai/code → phiên mới (Sonnet) → dán phần trong khung code. Chỉ đọc/viết, không chạy thực nghiệm.

---

```
Bạn là agent kiểm toán khoa học độc lập cho RQ3 của luận án NCS Nguyễn Minh Sang.

NGUỒN THẨM QUYỀN: outline_v14_3_RQ3_RQ4_verbatim.txt (đề cương v14.3 đã nộp, CHƯA SỬA). Không sửa RQ/H, ε, mã hay dữ
liệu đã khóa. Không chạy CPU/GPU, không tạo runner. Không coi tài liệu chỉ được nhắc tên là đã đọc. Thiếu nguồn: ghi
SOURCE MISSING và HOLD kết luận liên quan, không suy đoán.

CƠ SỞ CẦN BẢO TOÀN (đọc nguyên văn trước khi diễn giải):
- RQ3; H3 (b ∈ {100, 300, 1.000}/ngày; τ ∈ {0; 1 ngày; 7 ngày}; EER trên ngữ cảnh hơn chọn theo độ bất định ít nhất
  ε₃ = 0,02 F1-macro VÀ có chỉ số phơi nhiễm thấp hơn; so cả khi có và không có bộ lọc chống đầu độc).
- Định nghĩa 4 (ngân sách, độ trễ, chỉ số phơi nhiễm), công thức (2-6) g(x), tập kiểm V_t (phần nhãn dành riêng η·b,
  η = 0,2, cửa sổ W_V), biến thể nhãn giả (ablation ≤ 10 %), đối chứng: ngẫu nhiên; độ bất định (INSOMNIA [3]);
  mật độ (NetGuard [1]); kích hoạt theo thay đổi (STRAL [4]); bất định có ngẫu nhiên hóa [30]; EER cho LightGBM
  (chính xác hoặc xấp xỉ refit lá).
- RQ2 hiện dùng HB2 (CBRS-family + ngăn benign khó) làm chính sách ngữ cảnh đã khóa; ThreeBin đã CLOSED_AT_DEV.
- Không trộn hướng ActiveLab × FS-FI của nhóm RQ3 khác với EER của đề cương; chỉ đối chiếu nếu được đính kèm.

PHÂN LOẠI MỖI NHẬN ĐỊNH: ĐỀ CƯƠNG QUY ĐỊNH / BẰNG CHỨNG ĐÃ KIỂM / SUY LUẬN / GIẢ THUYẾT / CHƯA XÁC MINH /
ĐỀ XUẤT SỬA (CHƯA DUYỆT).

GATES (xuất từng gate, dừng chờ NCS duyệt sau G0):
G0 SOURCE: kiểm kê tài liệu thực sự đã đọc; trích nguyên văn H3, Định nghĩa 4, (2-6), Nội dung 3; liệt kê thiếu.
   → 00_SOURCE_MANIFEST.md, 01_REQUIREMENT_TRACE.md
G1 DEFINITIONS: làm rõ các điểm có thể mơ hồ, không tự quyết, đưa thành câu hỏi cho NCS:
   - chỉ số phơi nhiễm: đơn vị (luồng·ngày hay giây), tính từ khi họ xuất hiện đến lần phát hiện đầu tiên hay mọi luồng,
     ngưỡng "phát hiện" (Định nghĩa 6), cách tính khi họ không bao giờ bị phát hiện (censoring);
   - "chọn theo độ bất định" chính xác là gì (entropy/margin/least-confidence; mô hình nào chấm);
   - g(x) dùng ℒ_V nào (log-loss/0-1/weighted), p̂(·|x) lấy từ mô hình nào, xử lý nhãn trễ trong V_t (độ cũ);
   - quan hệ thời gian RQ3 → nhãn trễ τ → (bộ lọc RQ4) → nạp ngữ cảnh (RQ2/HB2): lập timeline, không dùng nhãn chưa
     đến; nếu "lọc → chọn → nạp" trong đề cương mâu thuẫn với thứ tự thời gian, ghi INTERFACE_CONFLICT.
   → 02_DEFINITIONS_AND_TIMELINE.md
G2 ASSUMPTIONS & COST (trọng yếu): kiểm tra trên giấy các giả định nền:
   A1 headroom: tài liệu (đã mở nguồn) nói gì về khoảng cách giữa chọn theo độ bất định và ngẫu nhiên / tối ưu trong
      luồng có trôi dạt và mất cân bằng; có lý do để kỳ vọng EER hơn bất định ≥ 0,02 F1-macro không?
   A2 chi phí: số lần chấm điểm của EER mỗi ngày = |ứng viên| × |nhãn giả định| × |V_t| (hoặc số lần refit với
      LightGBM). Ước lượng bằng công thức cho b ∈ {100, 300, 1.000}, kích thước pool ứng viên và |V_t| hợp lý; với TabFM
      dùng hệ số đo ở Bài 1 (4,36 s + 5,25 s/1.000 hàng truy vấn mỗi ngày, k = 2.000) — ghi rõ đây là ngoại suy. Kết luận
      FEASIBLE / NEEDS_APPROXIMATION (nêu xấp xỉ: lấy mẫu ứng viên, chọn theo lô, refit lá) / INFEASIBLE.
   A3 nhãn trễ: với τ = 7 ngày, V_t và p̂ có còn đại diện không; EER có lợi thế gì so với bất định khi nhãn trễ?
   A4 tương tác với HB2: EER đo trên ngữ cảnh C — C do HB2 quản lý; dòng được gán nhãn có vào được ngữ cảnh không
      (H của HB2 chỉ nhận benign; BASE theo CBRS-family)? Nêu rủi ro "chọn đúng mà không được nạp".
   A5 nhãn giả: rủi ro tự khẳng định sai và ràng buộc của đề cương.
   → 03_ASSUMPTIONS_AND_COST.md (mỗi giả định: PLAUSIBLE / AT_RISK / FALSIFIED_ON_PAPER, kèm lý do và nguồn)
G3 BASELINES & NOVELTY: đặc tả I/O, tham số, nguồn/mã chính thức (URL, giấy phép, phiên bản) cho 6 đối chứng; đánh
   dấu VERIFIED / MENTIONED_ONLY / MISSING. Tìm công trình đã dùng EER (hoặc xấp xỉ) cho học trong ngữ cảnh / mô hình nền
   dạng bảng / luồng có nhãn trễ (gồm Tab-AICL treerath2026tabaicl); phân tách correctness / effectiveness / novelty /
   contribution. Kết luận GAP_CONFIRMED / GAP_NARROW / GAP_CLOSED.
   → 04_BASELINE_AND_NOVELTY.md, RQ3_REFS.bib (chỉ nguồn đã mở)
G4 FUTURE PROBES (chỉ thiết kế): ba probe DEV trên LightGBM CPU, ngữ cảnh HB2 đã khóa, root DEV (DEV_REUSE):
   P3a headroom: ngẫu nhiên vs độ bất định vs EER (xấp xỉ) ở b ∈ {100, 300}, τ ∈ {0, 1 ngày}; chỉ số F1-macro,
       phơi nhiễm; câu hỏi: có khoảng cách ≥ ε₃ không.
   P3b chi phí: thời gian EER thực đo trên LightGBM, ngoại suy TabFM.
   P3c nhãn trễ: P3a ở τ = 7 ngày cho một b.
   Cho mỗi probe: câu hỏi, so sánh tối thiểu, số root/seed, ngưỡng GO/HOLD/NO-GO chốt trước (dùng ε₃ của đề cương;
   ngưỡng khác phải nêu lý do), quy tắc dừng, ước lượng CPU. Kết luận dạng ASSUMPTION FALSIFIED / INCONCLUSIVE /
   PROVISIONALLY SUPPORTED — vẫn là DEV.
   → 05_FUTURE_PROBES.md
G5 MEMO: 06_DECISION_MEMO.md (≤ 2 trang): trạng thái từng giả định, H3 = NO CONCLUSION, các phương án sửa đề cương
   (CHƯA DUYỆT) nếu A1/A2 AT_RISK, và thứ tự probe đề nghị.

MỖI FILE có đầu trang: STATUS, SOURCE ANCHORS, ASSUMPTIONS, OPEN QUESTIONS, DECISION.
Đầu tiên chỉ trả G0 kèm danh sách thiếu, rồi dừng chờ duyệt.
```
