# 02 — DEFINITIONS AND TIMELINE (G1)

- **STATUS:** G1 DRAFT — chờ NCS trả lời các câu hỏi Q1–Q14. Không có điểm nào được tự quyết. G2–G5 chưa làm.
- **SOURCE ANCHORS:** `sources/outline_v14_3_RQ3_RQ4_verbatim.txt` (H3 L10; Định nghĩa 4 L27; Định nghĩa 6 L31–35; ngân sách η·b L37; Nội dung 3 L54–64; (2-6) L58; V_t L60; thứ tự lọc→chọn→nạp L20; (2-2) L21–23); `sources/bai1_manuscript_v4_2_clean.md` §3.1, §3.2, §3.4, §3.6, §4.3, §4.5, Bảng 2 (hash khác bản NCS nêu, xem `00_SOURCE_MANIFEST.md` §5); `sources/RQ2_DECISION_LOG.md` §8–9 (HB2); `sources/outline_v14_3_references.txt`.
- **ASSUMPTIONS:** (a) Giao thức Bài 1 (§3.1) là *triển khai tham chiếu* của "score first, learn after", không phải điều khoản của đề cương; dùng làm khung lập timeline, mỗi chỗ lệch với đề cương được nêu. (b) Chưa đọc nội dung [2], [3], [30], [31] → mọi nhận định về "các công trình đó định nghĩa gì" là **CHƯA XÁC MINH**. (c) Không dùng kết quả Bài 1 làm bằng chứng cho RQ3 (theo chỉ thị NCS).
- **OPEN QUESTIONS:** Q1–Q14 (mục 6).
- **DECISION:** Không có. H3 = NO CONCLUSION. Hai mục INTERFACE_CONFLICT (IC-1, IC-2) và ba mục lệch triển khai (IC-3…IC-5) được ghi nhận, chờ NCS.

Nhãn phân loại: **[ĐC]** đề cương quy định · **[BC]** bằng chứng đã kiểm (có trong tệp đính kèm hoặc trang đã mở; chưa kiểm độc lập) · **[SL]** suy luận · **[GT]** giả thuyết · **[CXM]** chưa xác minh · **[ĐX]** đề xuất sửa (chưa duyệt).

---

## 1. Chỉ số phơi nhiễm (Định nghĩa 4)

**Nguyên văn [ĐC]:** "Chất lượng được đo cả bằng chỉ số phơi nhiễm: tổng thời gian các luồng tấn công không bị phát hiện kể từ khi họ tấn công đó xuất hiện [2]." [2] = Botacin & Gomes 2025 (xác nhận bằng danh mục tham khảo của đề cương). Nội dung [2]: **chưa đọc** (chỉ có bản ghi Crossref) → định nghĩa gốc của "exposure" **[CXM]**.

**Những điều văn bản không xác định [SL]:** câu có ít nhất ba cách đọc.

| Cách đọc | Công thức (đề xuất để NCS chọn, KHÔNG phải quyết định) | Đơn vị | Ghi chú |
|---|---|---|---|
| E1 — cấp họ, thời gian đến lần phát hiện đầu | Σ_họ f (d_phát-hiện-đầu(f) − d_xuất-hiện(f)) | ngày (họ·ngày) | Một số mỗi họ; nhỏ gọn; không phụ thuộc số luồng |
| E2 — cấp luồng, mọi luồng chưa bị phát hiện | Σ_ngày Σ_họ đã xuất hiện Σ_luồng tấn công chưa bị phát hiện (trọng số 1/π) × (độ dài ngày) | luồng·ngày | Khớp nghĩa đen "tổng thời gian các luồng … không bị phát hiện"; nhạy với khối lượng luồng của họ |
| E3 — E2 chuẩn hóa | E2 / số luồng tấn công đã xuất hiện | ngày/luồng | So sánh được giữa b, τ, bộ dữ liệu |

**Các điểm cần quyết (→ Q1–Q4):**
1. *Đơn vị:* replay của Bài 1 chấm theo **ngày** (§3.1: mỗi ngày được chấm một lần với ngữ cảnh dựng từ nhãn đến trước cuối ngày t−1) [BC]. Với bước thời gian là ngày, đơn vị "giây" không có nghĩa trừ khi dùng mốc thời gian trong luồng; E1/E2 theo ngày là phù hợp tự nhiên với lưới replay [SL].
2. *"Họ xuất hiện":* ngày đầu tiên họ có mặt trong luồng, hay mỗi lần tái xuất hiện sau ≥ d = 3 ngày vắng (Nội dung 1, L49) [ĐC cho định nghĩa tái xuất hiện]? Với họ tái xuất hiện, đồng hồ có reset không? [CXM]
3. *"Bị phát hiện":* Định nghĩa 6 chỉ định ngưỡng λ_t từ ngân sách cảnh báo nhầm α_t = A_FP/N̂_t hiệu chỉnh trên D_cal [ĐC]. Nếu "phát hiện" = điểm ≥ λ_t thì: (i) phát hiện ở cấp *luồng* hay cấp *họ* (≥ 1 luồng của họ vượt ngưỡng trong ngày? ≥ x% luồng?); (ii) đo trên mẫu đánh giá cố định phân tầng có trọng số 1/π (Nội dung 1, L43) [ĐC]. Cả hai chưa được nêu [CXM].
4. *Kiểm duyệt (censoring):* họ không bao giờ bị phát hiện trong cửa sổ replay → phơi nhiễm = ∞ nếu cộng thẳng. Cần quy ước (chặn trên theo độ dài cửa sổ; báo cáo riêng số họ bị kiểm duyệt; hoặc dùng thống kê sống-sót) [CXM]. Đây không được đề cương nêu.
5. *Phụ thuộc vào hiệu chỉnh D_cal ở b nhỏ [SL, tính số học từ công thức Bài 1 §3.6 + η = 0,2 của đề cương]:* η·b = 20 / 60 / 200 nhãn mỗi ngày cho b = 100 / 300 / 1.000. Nếu toàn bộ η·b vào D_cal (Bài 1: `split_vt = False`) và cửa sổ 3 ngày thì D_cal ≤ 60 / 180 / 600 hàng, trong đó chỉ phần benign dùng cho phân vị. Quy tắc Bài 1 α_eff = max(α_t, 5 / n_benign_cal) khiến sàn tỷ lệ báo động nhầm ≥ ~8% khi n_benign_cal ≈ 60 [SL]. Nếu η·b còn phải chia cho cả V_t (Định nghĩa 4 mục "Ngân sách nhãn cho V_t và D_cal"), D_cal còn nhỏ hơn. → ngưỡng "phát hiện" ở b = 100 rất thô; mọi chỉ số phụ thuộc ngưỡng (F1-macro, phơi nhiễm) bị ảnh hưởng. Ghi để G2/G4; chưa kết luận.
6. *Chi phí đo:* Bài 1 không báo cáo chỉ số phụ thuộc ngưỡng cho so sánh TabFM–LightGBM vì chấm D_cal bằng TabFM tốn thêm ≈ 1 GPU-giờ (DEV-010, §3.6) [BC]. RQ3 cần ngưỡng mỗi ngày cho phơi nhiễm và F1-macro → chấm D_cal hằng ngày là chi phí bổ sung [SL] (tính ở G2-A2).

**Mục tiêu "F1-macro" trong H3** [ĐC]: chưa nêu (a) macro trên 2 lớp nhị phân hay trên họ tấn công; (b) tại ngưỡng nào (λ_t của Định nghĩa 6?). Bài 1 dùng AUPRC_w làm chỉ số chính, F1-macro không có ở đó [BC] → **không có tiền lệ giao thức** cho F1-macro (→ Q5).

---

## 2. "Chọn theo độ bất định" (đối chứng chính của H3)

**Nguyên văn [ĐC]:** "chọn theo độ bất định (kiểu INSOMNIA [3])" (L64); H3: "…cao hơn chọn theo độ bất định ít nhất ε₃".

- Văn bản **không** nêu: entropy / margin / least-confidence; mô hình chấm điểm (TabFM, LightGBM hay mô hình thay thế); có ngẫu nhiên hóa hay không (đã tách thành đối chứng riêng [30]).
- INSOMNIA [3]: **chưa mở** (bib: "FIT OK (active learning / label estimation)" là nhãn thư mục của Bài 1, không phải mô tả thuật toán) → tiêu chí chọn gốc **[CXM]**. Không suy đoán.
- Tab-AICL (abstract đã mở): một luật bất định là *TabPFN-Margin*, tức margin chấm bằng chính mô hình đọc ngữ cảnh [BC: abstract, https://arxiv.org/abs/2603.27385] — đây là tiền lệ cho "mô hình chấm = mô hình nền" nhưng **không phải** căn cứ cho cách đề cương định nghĩa đối chứng.
- Tiền lệ trong chính dự án: Bài 1 dùng LightGBM đã khóa để tính entropy cho **cả hai** nhánh TabFM/LightGBM của CURE (DEV-005, §3.4) [BC] → khả năng đối chứng bất định cũng dùng LightGBM để chấm cho cả hai nhánh (một lựa chọn *có thể*, chưa phải quy định).
- Hệ quả [SL]: "chọn theo độ bất định" có ≥ 3 biến thể × ≥ 2 mô hình chấm = ≥ 6 đối chứng khả dĩ; chọn biến thể nào cho phép so H3 là quyết định có ảnh hưởng kết quả (ε₃ = 0,02). Cần khóa trước (→ Q6).

---

## 3. g(x), ℒ_V, p̂ và độ cũ của V_t

**Nguyên văn [ĐC]:** g(x) = E_{y∼p̂(·|x)}[ℒ_V(C) − ℒ_V(C∪{(x,y)})] (2-6); V_t = "các dòng có nhãn chuyên viên, từ nguồn không bị gắn cờ, thuộc phần nhãn dành riêng η·b (mục 2.1), rời khỏi C_t và D_cal, trong cửa sổ W_V ngày gần nhất; độ cũ của V_t được báo cáo".

**Điều chưa xác định [CXM] / lưu ý [SL]:**

| Mục | Văn bản nêu gì | Chưa nêu | Rủi ro/ghi chú |
|---|---|---|---|
| ℒ_V | "ℒ_V" là mất mát trên V_t; V_t dùng chung với I_i (2-7) | log-loss / 0-1 / có trọng số / Brier / mất mát cảm ứng F1 | H3 đo bằng F1-macro; ℒ_V là proxy. Roy & McCallum: trang abstract đã mở **không** nêu hàm mất mát → **[VERIFY]**. Mất mát 0-1 cho khác biệt rời rạc, nhiễu lớn trên V_t nhỏ (xem dưới) [SL] |
| Trọng số | Hàng dành riêng có trọng số nghịch đảo xác suất chọn (L37) | ℒ_V có dùng trọng số IPW không | Đề cương nói ước lượng "không bị lệch" nhờ trọng số → ℒ_V phải có trọng số [SL] |
| p̂(·\|x) | "p̂" xuất hiện trong (2-6) | mô hình nào sinh p̂ (TabFM với ngữ cảnh C? LightGBM? có hiệu chỉnh xác suất?) | p̂ sai hiệu chỉnh → kỳ vọng sai → xếp hạng sai [SL] |
| Tập y | y ∼ p̂ | với nhãn nhị phân |y| = 2; với nhãn họ thì nhiều hơn | quyết định số lần chấm điểm (G2-A2) |
| Cỡ V_t | η·b nhãn/ngày, cửa sổ W_V | W_V; tỷ lệ chia η·b giữa V_t và D_cal | Bài 1: W_V = 3 ngày, toàn bộ η·b vào D_cal, V_t **chưa được hiện thực** (`split_vt = False`) [BC]. Với b = 100, η·b = 20/ngày: V_t ≤ 60 hàng sau 3 ngày nếu không chia với D_cal, ít hàng tấn công (phần dư ở tầng điểm cao giúp một phần) [SL] |
| Độ cũ | "được báo cáo" | định nghĩa (tuổi trung bình? tuổi hàng cũ nhất?) và ngưỡng chấp nhận | với τ = 7, độ cũ tối thiểu ≈ τ + 1 ngày (mục 4) |
| Chọn y∈batch | g(x) tính cho từng x riêng lẻ | chọn *theo lô* (b−ηb hàng cùng lúc) xử lý trùng lặp thế nào: top-(1−η)b theo g, hay tham lam cập nhật C? | top-k theo g dễ chọn các hàng gần giống nhau (thiếu đa dạng) [SL]; tham lam đắt gấp ~(1−η)b lần [SL] |
| C | "tính trên ngữ cảnh" C = C_t | C là ngữ cảnh *hiện tại lúc chọn*, nhưng nhãn mới chỉ vào C sau τ ngày và qua chính sách π (HB2) | g(x) là *myopic*: bỏ qua việc (x,y) có được nạp hay không và khi nào (→ A3/A4 ở G2) [SL] |

Lưu ý nhạy cảm: V_t loại "nguồn bị gắn cờ" (RQ4 tầng nguồn) nên V_t của **RQ3 phụ thuộc đầu ra của RQ4** (xem IC-2).

---

## 4. Timeline: RQ3 → nhãn trễ τ → (bộ lọc RQ4) → nạp ngữ cảnh (π/HB2)

**Cơ sở [BC, Bài 1 §3.1, phát biểu là *triển khai*]:** với ngày t: (1) Chấm điểm ngày t bằng ngữ cảnh và D_cal dựng từ nhãn đến *trước cuối ngày t−1*. (2) Cuối ngày t, hỏi *b* nhãn từ ngày t. (3) Dành η cho D_cal. (4) Mọi nhãn đã hỏi **đến cuối ngày t+τ** và dùng được **từ ngày t+τ+1**; hàng chính sách đi qua `policy.update(context, new_labelled_rows, unlabelled_stream)`.

Ghép với đề cương [ĐC: (2-2): C_t = π(C_{t−1}, N_t, U_t), N_t = "dòng vừa có nhãn đã qua bộ lọc"]:

| | τ = 0 | τ = 1 ngày | τ = 7 ngày |
|---|---|---|---|
| Chọn (cuối ngày s) | cuối ngày s | cuối ngày s | cuối ngày s |
| Nhãn đến / lọc / nạp | cuối ngày s | cuối ngày s+1 | cuối ngày s+7 |
| Chấm điểm đầu tiên dùng nhãn | ngày s+1 | ngày s+2 | ngày s+8 |
| Tuổi tối thiểu của nhãn mới nhất mà phép *chọn* ở ngày t nhìn thấy trong C | 0 hoặc 1 ngày* | 1 hoặc 2 ngày* | 7 hoặc 8 ngày* |
| V_t (W_V gần nhất) tại ngày t | nhãn hỏi ở t−W_V…t (đến trong cửa sổ) | t−1−W_V…t−1 | t−7−W_V…t−7 |

\* tuỳ việc nhãn *đến cùng thời điểm* cuối ngày t có được dùng cho phép chọn cuối ngày t không (Bài 1 chưa nói thứ tự bên trong bước cuối ngày) → Q8.

**Quy tắc "không dùng nhãn chưa đến" [ĐC suy từ Định nghĩa 4: "nhãn … chỉ có từ thời điểm s + τ"]:** phép chọn ở cuối ngày t chỉ được thấy nhãn của các dòng gửi ở s ≤ t − τ (hoặc s ≤ t − τ − 1 tùy Q8). Có một ngoại lệ có chủ đích: **nhãn giả** (ablation) không phải nhãn chuyên viên và được thay khi nhãn thật đến [ĐC, L62] — nhưng nó thêm một kênh thông tin từ dự đoán, làm rủi ro tự khẳng định sai (G2-A5).

**Hệ quả [SL]:** (i) Tuổi của V_t và C trong lúc chọn ≥ τ ngày; với τ = 7 và W_V = 3 (nếu giữ giá trị Bài 1), V_t phản ánh các dòng được hỏi cách đây 7–10 ngày. (ii) Giá trị của một dòng được chọn ở ngày s chỉ bắt đầu ở ngày s+τ+1 — trong lúc đó C có thể đã bị π thay đổi (đẩy ra/đưa vào) nhiều lần; g(x) tính trên C của ngày s không phản ánh C của ngày s+τ+1.

### INTERFACE_CONFLICT / lệch cần NCS xác nhận

**IC-1 (thứ tự "lọc → chọn → nạp" vs thứ tự thời gian theo hàng) — INTERFACE_CONFLICT mềm.**
- Đề cương [ĐC L20]: "cùng tác động lên một tập dữ liệu có nhãn duy nhất theo thứ tự lọc → chọn → nạp".
- Theo timeline (Định nghĩa 4 + Bài 1 §3.1): với *một dòng cụ thể*, thứ tự thật là **chọn (ngày s) → [trễ τ] → lọc (ngày s+τ) → nạp (s+τ, dùng từ s+τ+1)**. Bộ lọc (RQ4: tầng nguồn + tầng dòng) chỉ có thể tác động lên dòng *sau khi nhãn đến*, tức sau khi chọn. [SL, từ hai nguồn trên]
- Chỉ nhất quán nếu đọc "lọc → chọn → nạp" ở mức *tập dữ liệu có nhãn* (bộ lọc làm sạch V_t và C, rồi phép chọn *tiếp theo* dùng chúng, rồi nạp). Với cách đọc đó, "lọc" chưa bao giờ ảnh hưởng *lựa chọn chính dòng đó*, chỉ ảnh hưởng gián tiếp qua V_t và C.
- Nội dung 5 (nơi quy định chạy chung) **bị cắt** → không xác minh được. **HOLD**. → Q7.

**IC-2 (V_t phụ thuộc cờ nguồn của RQ4; vòng phụ thuộc):** V_t "từ nguồn không bị gắn cờ" [ĐC]; cờ nguồn là kết quả tầng nguồn của RQ4 (so sánh ngang hàng theo ngày) dùng nhãn *đã đến*; tầng dòng I_i (2-7) lại dùng chính V_t. Hai hệ quả: (a) *không có bộ lọc* (nhánh còn lại của H3) thì "không bị gắn cờ" không xác định → V_t = mọi nguồn, kể cả nguồn bị chiếm ⇒ ℒ_V có thể bị đầu độc; (b) có bộ lọc: cờ nguồn trễ τ ngày, nên trong cửa sổ đó nguồn bị chiếm chưa bị gắn cờ vẫn nằm trong V_t. [SL] → Q9.

**IC-3 (V_t chưa hiện thực trong giao thức tham chiếu):** đề cương chia η·b cho *cả* V_t và D_cal (L37); Bài 1 dành toàn bộ cho D_cal (`split_vt = False`) và có W_V = 3 áp cho D_cal [BC]. Tỷ lệ chia, W_V thật, và việc V_t và D_cal có *rời nhau* hay chung hàng là chưa rõ (đề cương nói V_t "rời khỏi C_t và Dcal") → Q10.

**IC-4 (cách lấy phần dành riêng):** đề cương: lấy phân tầng theo điểm dự đoán, lấy dư ở tầng điểm cao, trọng số nghịch đảo xác suất (L37) [ĐC]. Bài 1: hỏi nhãn *ngẫu nhiên đều* trong ngày ở chế độ real-day (§3.2a) [BC]; chế độ scenario có nhãn chính sách chỉ lấy từ phần POLICY và D_cal chỉ từ phần CAL [BC]. Chưa rõ trong RQ3: (a) mô hình nào cho "điểm dự đoán" để phân tầng; (b) phần dành riêng lấy trước hay sau khi chiến lược chọn mẫu chọn (tránh chọn trùng) → Q11.

**IC-5 (ký hiệu "ngăn k_H" vs HB2):** Nhãn giả "không vào ngăn k_H và tập V" [ĐC L62] dùng ký hiệu của chính sách *ba ngăn*; RQ2 hiện dùng HB2 (CBRS_FAMILY + H = 200 dòng benign xếp theo điểm tấn công; ThreeBin đã CLOSED_AT_DEV) [BC, RQ2_DECISION_LOG §1, §8]. Chưa rõ ràng buộc nhãn giả được ánh xạ sang HB2 thế nào (H của HB2 *chỉ nhận benign* — nhãn giả "benign" là đúng loại hàng H nhận!). Đây chính là tương tác trọng yếu của A4/A5 (G2). → Q12.

**IC-6 (tách vai trò đánh giá/chọn):** Bài 1 scenario replay: mỗi hàng gốc có đúng một vai (EVAL/POLICY/CAL), hàng đánh giá không bao giờ được gán nhãn [BC]. Với chọn mẫu chủ động, tập ứng viên phải nằm trong luồng POLICY+CAL chưa nhãn; nếu chiến lược được chấm trên hàng EVAL thì rò rỉ. Ở chế độ real-day, mẫu đánh giá *không bị loại khỏi* kho hỏi nhãn (§3.2a) và giữ trọn họ hiếm — nên chiến lược ưu tiên họ hiếm sẽ chọn đúng các hàng đã được chấm ở ngày đó (hợp lệ theo "score first, learn after", nhưng từ ngày sau). Không phải mâu thuẫn; ghi để G4 chọn chế độ replay. → Q13.

---

## 5. Hệ quả đã thấy cho các gate sau (chưa kết luận)

- **G2-A2:** số lần chấm điểm EER phụ thuộc trực tiếp |y| (§3), batch/tham lam, và việc chấm D_cal hằng ngày cho ngưỡng (§1.6).
- **G2-A3:** tuổi tối thiểu của V_t ≥ τ+1 (bảng §4) và cỡ V_t = 20–200 nhãn/ngày × W_V.
- **G2-A4/A5:** IC-5.
- **G4:** F1-macro chưa có tiền lệ giao thức (Q5); phơi nhiễm cần E1/E2 và censoring (Q1–Q4).

---

## 6. Câu hỏi cho NCS (KHÔNG tự quyết)

| # | Câu hỏi | Lựa chọn tôi thấy (không khuyến nghị bắt buộc) |
|---|---|---|
| Q1 | Chỉ số phơi nhiễm: cấp họ (E1) hay cấp luồng (E2/E3)? | E1 / E2 / E3 / khác. [2] chưa được đọc nên không có tiền lệ nguồn |
| Q2 | Đơn vị: ngày (khớp replay) hay giây (cần mốc thời gian trong ngày)? | ngày / giây |
| Q3 | "Họ xuất hiện": lần đầu trong luồng hay mỗi lần tái xuất hiện (≥ d = 3 ngày vắng)? | lần đầu / mỗi lần |
| Q4 | Quy tắc "phát hiện": điểm ≥ λ_t (Định nghĩa 6) ở cấp luồng hay cấp họ; ngưỡng bao nhiêu; kiểm duyệt (không bao giờ phát hiện) tính thế nào? | chặn bằng độ dài cửa sổ + báo cáo số họ bị kiểm duyệt / thống kê sống-sót |
| Q5 | F1-macro: macro trên 2 lớp hay trên họ; tại ngưỡng λ_t của Định nghĩa 6? (Bài 1 không có F1-macro) | — |
| Q6 | "Chọn theo độ bất định": entropy / margin / least-confidence; mô hình chấm là TabFM, LightGBM hay cả hai? (INSOMNIA [3] chưa mở) | khóa một biến thể trước, các biến thể khác là phân tích độ nhạy |
| Q7 | Thứ tự "lọc → chọn → nạp" có nghĩa ở mức tập dữ liệu (IC-1)? Nội dung 5 có thể đính kèm không? | — |
| Q8 | Trong bước cuối ngày t, nhãn đến cùng thời điểm có được dùng cho phép chọn của ngày t không? | có / không |
| Q9 | Nhánh "không có bộ lọc" của H3: V_t gồm mọi nguồn (kể cả bị chiếm) hay nguồn tin cậy giả định? (IC-2) | — |
| Q10 | η·b chia thế nào giữa V_t và D_cal; W_V = 3 như Bài 1 hay giá trị khác; V_t có rời D_cal không? | — |
| Q11 | Phân tầng phần dành riêng theo điểm của mô hình nào; lấy trước hay sau lượt chọn? | — |
| Q12 | Nhãn giả ánh xạ sang HB2 thế nào (H chỉ nhận benign; "không vào ngăn k_H")? | — |
| Q13 | Chế độ replay dùng cho probe: scenario (EVAL/POLICY/CAL tách vai) hay real-day (§3.2a)? | — |
| Q14 | Độ cũ của V_t: định nghĩa (trung bình/tối đa) và có ngưỡng loại trừ không? | — |

Ngoài ra, nhắc lại một lệch nguồn (không thuộc G1 nhưng chặn mọi trích Bài 1): hash của bản thảo Bài 1 NCS nêu (`438d5b44…989c7`) ≠ hash tệp đính kèm (`e25f39ee…`).
