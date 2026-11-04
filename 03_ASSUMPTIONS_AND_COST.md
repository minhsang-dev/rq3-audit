# 03 — ASSUMPTIONS AND COST (G2)

- **STATUS:** G2 DRAFT — chờ NCS duyệt. Kiểm tra trên giấy; không chạy gì. H3 = NO CONCLUSION.
- **SOURCE ANCHORS:** `sources/outline_v14_3_RQ3_RQ4_verbatim.txt` (H3 L10; L27; L37; L53; L58–64); `02_DEFINITIONS_AND_TIMELINE.md` (+ quyết định Q1–Q14, mục 7 của tệp đó); `sources/bai1_manuscript_v4_2_clean.md` §3.1, §3.4 (CBRS), §3.6, §4.1–4.2, §4.3 (Bảng 2), §4.5, §4.8; `sources/RQ2_DECISION_LOG.md` §5, §8–9. Web (đã mở thật, mức đọc ghi ở từng chỗ): Settles 2010 (PDF https://burrsettles.com/pub/settles.activelearning.pdf, **đọc §3.4 đầy đủ**); Tab-AICL (https://arxiv.org/pdf/2603.27385, **đọc tóm tắt + phương pháp + phần thảo luận chi phí/kết quả tóm lược**, không đọc từng bảng); Cacciarelli & Kulahci (https://arxiv.org/pdf/2302.08893, **chỉ các đoạn phân loại chiến lược và nhãn trễ**, không đọc toàn văn); STRAL (https://arxiv.org/pdf/2605.22324 — **phiên bản v2 đổi tên từ PACT**; đọc mục 5.3 về chính sách thu nhãn, không đọc toàn văn).
- **ASSUMPTIONS:** (1) Mọi con số thời gian TabFM là **ngoại suy** từ pilot Bài 1 §4.5 (L4 GPU, 3 ngày pilot, hồi quy tuyến tính 2 điểm 1.000/10.000 hàng truy vấn; k = 2.000); không có đo trực tiếp cho EER. (2) Quyết định Q1–Q14 của NCS được dùng như đã chốt (PROPOSAL cho prereg). (3) Không dùng kết quả Bài 1 (H1a, AUPRC) làm bằng chứng cho giả định (chỉ số đo thời gian là ngoại lệ NCS cho phép). (4) Số hàng trong V_t / D_cal giả định mọi hàng dành riêng còn nằm trong cửa sổ W_V = 3 ngày, chia 50/50 (Q10).
- **OPEN QUESTIONS:** Q15–Q18 (mục 8).
- **DECISION:** Không có kết luận khoa học về H3. Trạng thái giả định: A1 AT_RISK · A2 NEEDS_APPROXIMATION (EER chính xác trên TabFM = FALSIFIED_ON_PAPER) · A3 AT_RISK · A4 AT_RISK · A5 PLAUSIBLE (có điều kiện) · A6 AT_RISK (b = 100). Không giả định nào bị xác nhận bằng thực nghiệm.

**SOURCE MISSING mới:** NCS ghi đã đính kèm `outline_v14_3_noidung5.txt` (Q7) nhưng **tệp không có** trong thư mục tải lên của phiên (chỉ có 8 tệp, không có tệp tên đó). Nội dung 5 vẫn chưa đọc → phần "chạy chung RQ3+RQ4" và xác minh IC-1 vẫn **HOLD**; Q7 vẫn được ghi là quyết định đọc ở mức tập dữ liệu.

Nhãn: **[ĐC]** đề cương · **[BC]** bằng chứng đã kiểm (nguồn đã mở / tệp đính kèm) · **[SL]** suy luận · **[GT]** giả thuyết · **[CXM]** chưa xác minh · **[ĐX]** đề xuất (CHƯA DUYỆT).

---

## A1 — Headroom: EER có hơn độ bất định ≥ ε₃ = 0,02 F1-macro không? → **AT_RISK**

**Ghi chú về ε₃ [ĐC L53]:** biên chốt = max(quy đổi vận hành, 2×SD giữa seed). Hai giá trị quy đổi chưa tính → ε₃ cuối có thể > 0,02 [SL].

**Bằng chứng trong nguồn đã mở:**
- Settles 2010 §3.4 [BC, đọc đầy đủ mục]: EER định nghĩa bằng mất mát 0/1 hoặc log-loss (công thức nêu rõ); khung "gần tối ưu và không phụ thuộc lớp mô hình"; Zhu et al. 2003 được thuật lại là "cải thiện đáng kể so với ngẫu nhiên hoặc bất định" (**tường thuật lại của khảo sát, chưa mở Zhu 2003**); nhưng EER là khung "đắt nhất về tính toán", và tập chưa nhãn U được *giả định đại diện phân phối kiểm* để làm tập kiểm. Khảo sát nêu EER chủ yếu được xét ở bài toán nhị phân đơn giản; ứng dụng thực tế phải lấy mẫu Monte Carlo từ pool hoặc huấn luyện xấp xỉ. Khảo sát **không** nêu độ lớn khoảng cách F1-macro so với bất định, **không** xét luồng/trôi dạt/mất cân bằng.
- Tab-AICL [BC, tóm tắt + phương pháp]: pool tĩnh, cold-start ≤ 100 nhãn, 20 bộ benchmark; "không luật nào chiếm ưu thế" (margin mạnh trên dữ liệu sạch, lai tốt trên hình học cụm, proxy-lai vững hơn khi bất định "cố định vào ngoại lai"); nêu "bất định có thể giòn trên pool nhiễu/mất cân bằng". **Không có EER, nhãn trễ, trôi dạt.** Gợi ý rằng khoảng cách giữa các luật chọn phụ thuộc chế độ dữ liệu.
- STRAL v2 §5.3 [BC, một đoạn]: "không hỗn hợp thu nhãn nào chiếm ưu thế" trên recall/FP/1M; tác giả tự nhận đây là độ nhạy chính sách, không xếp hạng. Không có EER.
- Cacciarelli & Kulahci [BC, đoạn phân loại]: EER nằm trong nhóm "kỳ vọng lỗi/phương sai"; không đọc số liệu so sánh.

**Không tìm thấy** (trong phạm vi các nguồn đã mở và lần tìm hạn chế của phiên này) bất kỳ nguồn nào định lượng EER − bất định trong luồng có trôi dạt, mất cân bằng và nhãn trễ. Vắng bằng chứng **không** nghĩa là bị bác bỏ [SL].

**Suy luận cấu trúc (SL):**
1. Ngân sách chọn hiệu dụng = (1−η)·b = 80 / 240 / 800 nhãn/ngày so với ngữ cảnh k = 2.000: mỗi ngày chỉ thay 4–40% ngữ cảnh bằng nhãn mới; khoảng cách giữa hai quy tắc chọn bị chặn bởi những gì 80–800 nhãn có thể thay đổi.
2. Giá trị g(x) ~ thay đổi ℒ_V khi thêm 1 hàng vào ngữ cảnh 2.000 hàng: rất nhỏ; xếp hạng dựa vào chênh lệch nhỏ trên V_t (30 / 90 / 300 hàng, mục A6) → nhiễu xếp hạng (SL).
3. Mất mát ℒ_V (log-loss/0-1) ≠ F1-macro tại λ_t; tối ưu proxy không bảo đảm tối ưu chỉ số (Settles nêu EER có thể tối ưu chỉ số bất kỳ nhưng đây là lý thuyết, không phải kết quả) [SL].
4. H3 là hội hai điều kiện (F1-macro ≥ ε₃ **và** phơi nhiễm thấp hơn) tại mọi ô? — chưa định (→ Q15).
5. Có lý do ngược lại (ủng hộ headroom): bất định có thể chọn các hàng nhiễu/ngoại lai và trùng lặp (Tab-AICL) và không biết ngữ cảnh đã chứa gì; EER thì biết [GT].

**Kết luận:** có lý do hợp lý để kỳ vọng **một** khoảng cách, nhưng **không có lý do nguồn** để kỳ vọng ≥ 0,02 F1-macro. Probe P3a (G4) là cách duy nhất kiểm.

---

## A2 — Chi phí EER → **NEEDS_APPROXIMATION** (EER chính xác toàn pool trên TabFM = **FALSIFIED_ON_PAPER**)

### Công thức
- Số giả thuyết mỗi ngày: **H = N_c × |Y|**, N_c = số ứng viên, |Y| = 2 (nhãn nhị phân [ĐC L58, Q5]).
- Mỗi giả thuyết (x,y): một ngữ cảnh mới C∪{(x,y)} và chấm |V_t| hàng.
- Chi phí chấm điểm EER mỗi ngày = **N_c × |Y| × |V_t|** lượt chấm hàng, nhưng với TabFM chi phí chủ yếu theo *số ngữ cảnh* (cố định 4,36 s mỗi ngữ cảnh), không theo số hàng truy vấn.
- Thêm: một lượt chấm N_c hàng bằng ngữ cảnh C để lấy p̂ (4,36 + 5,25·N_c/1000 s).

### Hệ số (BC từ Bài 1, được NCS cho phép) và ngoại suy (SL)
- TabFM L4: t = 4,36 + 5,25 · (hàng truy vấn/1000) s, k = 2.000 [BC, §4.5; kiểm số học: 9,61 và 56,86 s khớp hai điểm đo 9,6 / 56,8].
- "Chấm lại sau khi bỏ một hàng ngữ cảnh = tính lại toàn bộ ngữ cảnh": **9,61 s** ở k = 2.000, 1.000 hàng truy vấn [BC, §4.5] → xác nhận không có tái dùng ngữ cảnh (không có cache) trong cấu hình đã đo.
- Bảng 11 của Bài 1 ghi 5,84 s/1.000 hàng (median, lần chạy chính, L4) khác 9,6 s của pilot [BC]; dùng hệ số pilot (bảo thủ), nêu rõ hệ số chính có thể thấp hơn ≈ 40% → kết luận dưới đây không đổi nhóm.
- LightGBM CPU: huấn luyện lại 2.000 hàng ≈ 0,1 s; dự đoán 0,0074 s/1.000 hàng [BC §4.5, Bảng 11; phần cứng CPU của số đo: **[CXM]**]. Tham số đã khóa có `subsample = 0,886` và `colsample_bytree = 0,983` [BC Bảng 2] → mỗi lần refit là ngẫu nhiên; so g(x) giữa các ứng viên cần cùng seed (số ngẫu nhiên chung) kẻo nhiễu bagging lớn hơn hiệu ứng thật [SL].
- Quy mô pool ứng viên: ngày gốc có 329.487–6.373.074 luồng [BC §4.1] → pool thật 10⁵–10⁶ ≫ mọi N_c dưới đây.
- Cỡ V_t theo Q10 (50/50, W_V = 3): b = 100 → 30 hàng; 300 → 90; 1.000 → 300 [SL].
- Tham chiếu ngân sách Bài 1: toàn bộ lần chạy chính = 6,2 GPU-giờ, trần 12 CU ≈ 7,4 giờ [BC §4.8]; chỉ dùng làm thước đo quy mô.

### Kết quả tính (GPU-giờ/ngày TabFM; CPU-giờ/ngày LightGBM), mỗi chuỗi một ô (b,τ), một seed — **ngoại suy**
| b | |V_t| | t/giả thuyết TabFM | N_c = 200 | N_c = 1.000 | N_c = 5.000 | N_c = 50.000 |
|---|---|---|---|---|---|---|
| 100 | 30 | 4,52 s | 0,50 h (7 ngày: 3,5 h) | 2,51 h (17,6 h) | 12,6 h (88 h) | 125 h (878 h) |
| 300 | 90 | 4,83 s | 0,54 h (3,8 h) | 2,68 h (18,8 h) | 13,4 h (94 h) | 134 h (940 h) |
| 1.000 | 300 | 5,94 s | 0,66 h (4,6 h) | 3,30 h (23,1 h) | 16,5 h (115 h) | 165 h (1.154 h) |

LightGBM (EER chính xác, refit đầy đủ, một luồng): N_c = 200: 0,011 h/ngày (0,08 h/7 ngày); N_c = 1.000: 0,056 h (0,39 h); N_c = 5.000: 0,28 h (1,95 h); N_c = 50.000: 2,8 h (19,5 h) — gần như không đổi theo b.

(Chuỗi 7 ngày đánh giá = trung bình chuỗi tái xuất hiện của Bài 1 §4.2; chuỗi đặc trưng/tiên nghiệm = 4 ngày.)

### Hệ quả cho lưới H3
- Lưới H3 = 3 b × 3 τ × 2 (có/không bộ lọc) = **18 ô**, chưa kể seed, bộ dữ liệu, ngày gốc.
- **TabFM, ngay cả N_c = 200:** ≈ 3,5–4,6 GPU-giờ cho *một* chuỗi 7 ngày của *một* ô → 18 ô ≈ 63–83 GPU-giờ cho đúng một chuỗi mỗi ô; so với 6,2 GPU-giờ cho toàn bộ lần chạy chính Bài 1. N_c = 1.000 → ≈ 320–415 GPU-giờ. **EER chính xác trên toàn pool (10⁵–10⁶): FALSIFIED_ON_PAPER.**
- **LightGBM:** với N_c ≤ 5.000 ứng viên: ≈ 2 CPU-giờ/chuỗi 7 ngày → 18 ô ≈ 35 CPU-giờ/một chuỗi mỗi ô: **FEASIBLE nhưng chỉ nhờ lấy mẫu ứng viên** (bản thân lấy mẫu là một xấp xỉ, [ĐC L64] chỉ nêu xấp xỉ refit lá, không nêu lấy mẫu ứng viên). Toàn pool: không khả thi (19,5 CPU-giờ/chuỗi ở N_c = 50.000).
- Chưa tính: chọn *theo lô* — chọn tham lam cập nhật C sau mỗi hàng nhân chi phí với (1−η)·b = 80–800 vòng → vô hiệu; chọn top-(1−η)b theo g (một vòng) rẻ nhưng chọn hàng gần giống nhau [SL].
- Cho p̂ và chấm D_cal hằng ngày (Q4 yêu cầu λ_t mỗi ngày): D_cal chỉ 30–300 hàng → ≈ 4,5–5,9 s/ngày; không đáng kể (khác với ≈ 1 GPU-giờ Bài 1 từ chối vì D_cal ≈ 1.200 hàng ở b = 2.000) [SL].

### Xấp xỉ khả dĩ (không chọn, không quyết định)
| Xấp xỉ | Giảm gì | Ghi chú/rủi ro | Trạng thái |
|---|---|---|---|
| Lấy mẫu ứng viên (N_c ≪ pool) | N_c | Settles nêu Monte Carlo từ pool là kỹ thuật chuẩn (Roy & McCallum 2001); cần chọn mẫu ứng viên thế nào để vẫn thấy họ hiếm | [ĐX], chưa duyệt |
| Danh sách rút gọn bằng proxy rẻ (kiểu Tab-AICL Proxy-Hybrid: proxy tuyến tính lọc N_proxy hàng rồi mới dùng TabPFN) | N_c | Tab-AICL [BC] dùng đúng mục đích giảm chi phí chấm pool; tiền lệ cho TabFM | [ĐX] |
| Refit lá (LightGBM, giữ cấu trúc cây) | chi phí mỗi giả thuyết | Đề cương đã nêu [ĐC L64]. API `Booster.refit` của LightGBM: **[VERIFY, chưa mở tài liệu]**; tác dụng thực lên thời gian: chưa đo | [ĐC] |
| Dùng LightGBM làm mô hình chấm EER cho cả nhánh TabFM (kiểu CURE Bài 1) | 40–70× | Chọn bằng mô hình A, đánh giá trên mô hình B → xếp hạng sai lệch; chỉ như độ nhạy | [ĐX] |
| Dùng lại ngữ cảnh đã mã hóa (KV-cache) cho giả thuyết | t/giả thuyết | **[GT]**: pilot Bài 1 cho thấy chấm lại = tính lại toàn bộ; không có đo về cache; không biết `tabfm` hỗ trợ | [GT] |
| Chọn theo lô một vòng (top-k theo g) | vòng lặp | rủi ro trùng lặp (xem A3) | [ĐX] |

**Kết luận A2:** NEEDS_APPROXIMATION. Với TabFM, mọi phương án có N_c đủ lớn để thấy họ hiếm trong pool hàng triệu hàng vượt xa ngân sách Bài 1; P3b (G4) cần đo thật trên LightGBM CPU.

---

## A3 — Nhãn trễ τ = 7: V_t và p̂ còn đại diện không? EER có lợi thế gì? → **AT_RISK**

**Độ cũ của V_t tại thời điểm chọn [SL, suy từ Q8, Q10 và Bài 1 §3.1]:** nhãn đến cuối ngày s+τ, dùng từ s+τ+1. V_t = nhãn dành riêng đến trong 3 ngày trước đó (W_V = 3):

| τ | tuổi theo ngày *truy vấn* (= ngày của luồng) | trung bình | tối đa |
|---|---|---|---|
| 0 | 1–3 ngày | 2 | 3 |
| 1 | 2–4 | 3 | 4 |
| 7 | 8–10 | 9 | 10 |

(Q14: báo cáo trung bình và tối đa, không loại. Tuổi theo ngày *đến* luôn 1–3 ngày, vì vậy cần báo cả hai định nghĩa tuổi → Q16.)

**Rủi ro đại diện [SL]:**
1. Với τ = 7, V_t chỉ chứa luồng của 8–10 ngày trước. Họ tấn công mới xuất hiện hoặc tái xuất hiện trong 7 ngày gần nhất (đúng kịch bản RQ2/H3: vắng ≥ 3 ngày rồi quay lại) **không có hàng nào trong V_t** → ℒ_V không thể thưởng cho việc gán nhãn họ đó; g(x) ≈ 0 cho đúng loại hàng cần gán nhãn nhất. Bất định không phụ thuộc V_t nên không có điểm mù này. Đây là bất lợi cấu trúc của EER, mạnh dần theo τ.
2. p̂(·|x) từ mô hình với ngữ cảnh C cũng cũ ≥ τ ngày → hiệu chỉnh xác suất kém dưới trôi dạt.
3. V_t nhỏ (30/90/300 hàng): sau khi sắp xếp theo điểm cao (lấy dư) vẫn ít hàng tấn công (xem A6).
4. Settles: EER dùng pool chưa nhãn "đại diện cho phân phối kiểm" làm tập kiểm [BC]; V_t cũ vi phạm điều kiện lý thuyết này khi có trôi dạt.

**Lợi thế khả dĩ của EER khi nhãn trễ (GT):** Cacciarelli & Kulahci nêu rằng nếu bỏ qua nhãn trễ thì có thể có yêu cầu nhãn dư thừa cho các mẫu giống nhau [BC, đoạn đã đọc]; nếu g(x) được tính trên ngữ cảnh *đã gồm các hàng đang chờ nhãn* (với nhãn kỳ vọng) thì EER có thể tránh trùng lặp mà bất định thuần không làm được. Phiên bản "chấp nhận dòng chờ" này **không có** trong đề cương (g(x) tính trên C hiện tại) → [ĐX], CHƯA DUYỆT. Không nguồn nào đã mở chứng minh lợi thế này.

**Kết luận:** không có cơ chế được đề cương nêu để EER hơn bất định khi τ = 7; có cơ chế gây bất lợi (điểm 1). AT_RISK. P3c kiểm.

---

## A4 — Tương tác với HB2: "chọn đúng mà không được nạp" → **AT_RISK**

**Cơ sở [BC, RQ2_DECISION_LOG §8–9; Bài 1 §3.4]:** HB2 = CBRS_FAMILY (reservoir cân bằng theo họ; benign là một lớp riêng) cộng ngăn H = 200 hàng benign chọn theo điểm tấn công của mô hình (top-k độ khó, không k-center); k tổng = 2.000; trạng thái GO CONTRIBUTION CANDIDATE phạm vi LightGBM, CIDDS-001; TabFM chưa chạy. **Không có** mô tả mã-mức về pool mà H chọn và thời điểm nạp ([CXM]).

**Quy tắc nạp CBRS (Bài 1 §3.4) [BC]:** hàng của lớp chưa đầy ghi đè một hàng ngẫu nhiên của lớp lớn nhất; hàng của lớp đã đầy thay một hàng cùng lớp với xác suất m_c/n_c, còn lại bị bỏ. Hệ quả:
1. **R1 — xác suất nạp < 1:** hàng thuộc lớp đã đầy (thường là benign, hoặc họ tấn công lớn) được nạp với xác suất m_c/n_c ≪ 1. Một dòng được EER chọn và gán nhãn vẫn có thể bị bỏ ngay khi nạp → g(x) giả định C∪{(x,y)} (nạp chắc chắn) lệch với thực tế [SL].
2. **R2 — thay thế:** |C| ≤ k = 2.000 nên mỗi lần nạp loại một hàng khác (hàng ngẫu nhiên của lớp lớn nhất/cùng lớp). (2-6) cộng hàng vào mà không loại → bỏ qua tác dụng loại [SL].
3. **R3 — H chỉ nhận benign và xếp theo điểm tấn công:** hàng benign được gán nhãn vào H chỉ khi nằm trong top-k điểm của HB2, không phải do EER xếp hạng; hàng tấn công không bao giờ vào H [BC log §8]. Giá trị của một hàng benign "khó" (điểm cao) có thể đã được HB2 thu qua kênh riêng.
4. **R4 — trùng lặp vai trò:** bất định (margin) ưu tiên hàng gần ngưỡng — nhóm benign điểm cao chính là thứ H cần. Bất định + HB2 có thể bổ trợ nhau; khoảng cách EER − bất định *trên nền HB2* có thể nhỏ hơn khoảng cách trên nền chính sách khác. **[GT]**, không có bằng chứng.
5. **R5 — trễ τ:** hàng chọn ở ngày s vào C ở s+τ+1; HB2 đã thay đổi C trong thời gian đó.
6. **R6 — Q12:** nhãn giả chỉ vào BASE (CBRS-family), không vào H (giữ phù hợp với "H chỉ benign nhận từ nhãn thật").
7. **R7 — bộ lọc RQ4 chặn hàng:** hàng bị giữ chờ xác minh (tầng nguồn/dòng) bị bỏ khỏi N_t nhưng đã tiêu hao 1 nhãn trong ngân sách → "chọn đúng, không nạp" (bộ lọc loại, không phải HB2).

**Điều cần quyết (Q17):** g(x) có phải *nhận biết π* (tính kỳ vọng theo xác suất nạp/thay thế của HB2) hay giữ dạng ngây thơ (2-6) như đề cương? Dạng nhận biết π tốn thêm tính toán và mô phỏng reservoir ngẫu nhiên.

**Kết luận:** AT_RISK. Đề cương không đặt ràng buộc để g(x) phản ánh thực tế nạp. Mức độ thật chỉ đo được bằng probe (tỷ lệ hàng chọn thực sự vào C).

---

## A5 — Nhãn giả → **PLAUSIBLE (có điều kiện)**

**Ràng buộc đề cương [ĐC L62] + Q12:** chỉ là ablation; ≤ 10% ngữ cảnh (≤ 200 hàng); BASE (CBRS-family) chỉ, không vào H, không vào V_t (đề cương: "không vào ngăn k_H và tập V"); bị thay khi nhãn thật đến; không áp cho hàng dự đoán benign thuộc vùng trôi dạt; "rủi ro tự khẳng định sai được đo trực tiếp".

**Rủi ro [SL]:**
1. *Tự khẳng định:* nhãn giả là chính dự đoán của mô hình → thêm vào ngữ cảnh chỉ củng cố dự đoán; mô hình sai ở họ mới (dự đoán benign) sẽ nạp họ đó với nhãn benign — đề cương chặn bằng điều kiện "vùng trôi dạt", nhưng **"vùng trôi dạt" chưa định nghĩa** (xác định bằng tín hiệu nào? BBSE + kiểm định hai mẫu theo Định nghĩa 3?) [CXM].
2. *Tác động lên reservoir:* CBRS có thể loại hàng thật của lớp lớn nhất để nhường chỗ cho hàng giả.
3. *Thời gian sống:* với τ = 0, nhãn thật đến ngay hôm sau, nhãn giả gần như vô nghĩa; chỉ đáng đo với τ = 1, 7. Với τ = 7, hàng giả sống ≥ 8 ngày, đúng vùng rủi ro.
4. *V_t an toàn:* V_t không chứa nhãn giả [ĐC] → ℒ_V không bị ô nhiễm trực tiếp bởi chính nhãn giả → không có vòng "tự thưởng" trực tiếp trong g(x). 
5. *Ngữ nghĩa:* nhãn giả áp cho hàng *đã gửi chờ nhãn* (sẽ có nhãn thật) hay hàng *chưa gửi*? Câu "bị thay khi nhãn thật đến" gợi ý hàng đã gửi → Q18.

**Kết luận:** vì chỉ là ablation (không thuộc H3 chính) và đã bị chặn nhiều tầng, A5 không đe dọa H3; rủi ro được đề cương đo trực tiếp. PLAUSIBLE nếu định nghĩa "vùng trôi dạt" được khóa trước.

---

## A6 — (NCS thêm) Độ phân giải ngưỡng λ_t ở b nhỏ → **AT_RISK (b = 100), AT_RISK nhẹ (b = 300), PLAUSIBLE (b = 1.000)**

**Cơ sở [BC]:** Q4/Q5 buộc phát hiện và F1-macro tại λ_t của Định nghĩa 6, được hiệu chỉnh trên D_cal bằng quy tắc Bài 1 §3.6: α_eff = max(α_t, 5/n_benign_cal) [BC]. Q10: η·b chia 50/50 cho V_t và D_cal; W_V = 3 ngày.

**Tính số học [SL]:** D_cal ≈ 30 / 90 / 300 hàng (b = 100 / 300 / 1.000). Phần benign của D_cal chưa biết (phần dành riêng lấy dư ở tầng điểm cao nên tỷ lệ tấn công cao hơn quần thể); giả định benign 50% / 80% / 95%:

| b | D_cal | n_benign (50 / 80 / 95%) | sàn α_eff = 5/n_benign |
|---|---|---|---|
| 100 | 30 | 15 / 24 / 28 | **33% / 21% / 18%** |
| 300 | 90 | 45 / 72 / 86 | 11% / 7% / 6% |
| 1.000 | 300 | 150 / 240 / 285 | 3,3% / 2,1% / 1,8% |

(So với Bài 1: D_cal ≈ 1.200 hàng, sàn vẫn gây ràng buộc ở A_FP = 1.000 [BC §3.6].)

**Hệ quả [SL]:** ở b = 100 ngưỡng λ_t sẽ chấp nhận ~20–33% báo động nhầm trên benign — không phải ngân sách cảnh báo của một SOC; F1-macro (Q5) tại ngưỡng đó bị chi phối bởi quy tắc sàn, và "phát hiện" (Q4) rất dễ (ngưỡng thấp) nên chỉ số phơi nhiễm E3 ít nhạy với chiến lược chọn. Phương sai của phân vị với 15–28 điểm benign lớn. Có thể che khuất khoảng cách 0,02. Đề cương có nhánh dự phòng "báo cáo trực tiếp số cảnh báo nhầm và recall tại ngưỡng cố định" [ĐC L35] nhưng nhánh này nêu cho ngày "lưu lượng bình thường quá ít", không phải cho D_cal nhỏ.

**Lưu ý:** các tỷ lệ benign là giả định, chưa đo. P3a/P3b nên ghi n_benign_cal thực và số ngày bị áp sàn.

---

## Tổng hợp trạng thái

| ID | Giả định | Trạng thái | Lý do ngắn |
|---|---|---|---|
| A1 | EER hơn bất định ≥ 0,02 | AT_RISK | Không có nguồn nào cho độ lớn; ε₃ có thể tăng; hiệu ứng mỗi ngày nhỏ |
| A2 | Chi phí EER chịu được | NEEDS_APPROXIMATION; chính xác toàn pool trên TabFM = FALSIFIED_ON_PAPER | ≥ 3,5 GPU-giờ/chuỗi ở N_c = 200; LightGBM khả thi nếu lấy mẫu ứng viên |
| A3 | Nhãn trễ τ = 7 | AT_RISK | V_t 8–10 ngày tuổi; điểm mù với họ mới; không có cơ chế lợi thế trong đề cương |
| A4 | Tương tác HB2 | AT_RISK | Xác suất nạp < 1, thay thế, H chỉ benign, bộ lọc RQ4; g(x) ngây thơ |
| A5 | Nhãn giả | PLAUSIBLE (điều kiện) | Chỉ ablation; V_t sạch; cần định nghĩa vùng trôi dạt |
| A6 | Ngưỡng ở b nhỏ | AT_RISK (b=100) | sàn 18–33% báo động nhầm |

Các phương án sửa đề cương (CHƯA DUYỆT) sẽ gom ở G5; không đề xuất sửa nào ở đây.

---

## 8. Câu hỏi mới cho NCS

| # | Câu hỏi |
|---|---|
| Q15 | H3 yêu cầu "F1-macro hơn ≥ ε₃ **và** phơi nhiễm thấp hơn" ở **mọi** ô (b,τ), trung bình qua ô, hay theo mô hình hỗn hợp trên ô như hiệu ứng cố định? Phơi nhiễm "thấp hơn" có biên không? |
| Q16 | Tuổi của V_t tính theo ngày truy vấn (ngày của luồng) hay ngày đến? (Q14 chưa nêu.) |
| Q17 | g(x) giữ dạng ngây thơ (2-6) hay nhận biết π/HB2 (xác suất nạp, thay thế)? |
| Q18 | Nhãn giả áp cho hàng đã gửi chờ nhãn hay hàng chưa gửi? "Vùng trôi dạt" xác định bằng tín hiệu nào? Ngân sách tính toán ("nếu tổng chi phí nằm trong ngân sách", L64) bằng bao nhiêu GPU/CPU-giờ? |
