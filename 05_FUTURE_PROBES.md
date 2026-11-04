# 05 — FUTURE PROBES (G4) — chỉ thiết kế, KHÔNG chạy

- **STATUS:** G4 DRAFT — chờ NCS duyệt. Không chạy CPU/GPU, không tạo runner. Mọi kết quả sau này vẫn là **DEV (DEV_REUSE)**: không có root DEV chưa dùng (`RQ2_DECISION_LOG` §3). H3 = NO CONCLUSION.
- **SOURCE ANCHORS:** `sources/outline_v14_3_RQ3_RQ4_verbatim.txt` (H3 L10; ε₃ L53; (2-6) L58; V_t L60; đối chứng L64); `sources/outline_v14_3_noidung5.txt`; `sources/bai1_manuscript_v4_2_clean.md` §3.1, §3.2, §3.6, §4.1–4.3 (Bảng 2), §4.5; `sources/RQ2_DECISION_LOG.md` §2–3, §5 (bài học 2, 6, 7), §8–9 (HB2, LOCK_HB2); `sources/THESIS_AUDIT_LOG_RQ3_RQ4.md` §4 (Q1–Q18); `02_DEFINITIONS_AND_TIMELINE.md`; `03_ASSUMPTIONS_AND_COST.md` (A1–A6, bảng chi phí); `04_BASELINE_AND_NOVELTY.md`.
- **ASSUMPTIONS:** (1) Thời gian LightGBM 0,1 s/lần refit ở k = 2.000 và 0,0074 s/1.000 hàng dự đoán là số Bài 1 (phần cứng **[CXM]**); ước lượng CPU dưới đây là ngoại suy từ đó và sẽ được P3b thay bằng số đo. (2) Chuỗi "tái xuất hiện" như RQ2/Bài 1: 2 + d + 2 ngày, d = 3 (đề cương L49) → 7 ngày, ≈ 6–7 ngày đánh giá; ước lượng dùng 7 ngày chọn. (3) Khởi tạo ngữ cảnh/D_cal cho τ > 0 là PROPOSAL chờ Q23 (Bài 1 chỉ chạy τ = 0). (4) Mọi ngưỡng GO/HOLD/NO-GO bên dưới là **PROPOSAL, chốt trước khi chạy** (băm tệp, ghi `version_log.jsonl`), không phải kết quả.
- **OPEN QUESTIONS:** Q23–Q26 (mục 7). Q23 chặn P3a/P3c.
- **DECISION:** Thứ tự chạy đề nghị P3b → P3a → P3c (mục 6). Không có quyết định khoa học.

Cập nhật quyết định NCS (Q19–Q22, 04/11/2026) đã ghi ở `04_BASELINE_AND_NOVELTY.md` mục 8. Ràng buộc NCS cho G4 được tôn trọng: (i) mọi probe so sánh ở **cùng trần chi phí ≤ 1 CPU-giờ/ngày mô phỏng** và **cùng tổng số nhãn**; (ii) có kiểm thử độ đúng g(x) gồm (a)–(d) của §3 trong `04_…`; (iii) báo cáo **chỉ số nạp HB2** (Q17).

---

## 0. Thiết lập chung cho ba probe

| Mục | Quy định (PROPOSAL, chưa duyệt) |
|---|---|
| Mô hình / ngữ cảnh | LightGBM đã khóa (Bài 1 Bảng 2: `n_estimators=300, learning_rate=0.02162, num_leaves=15, min_child_samples=5, subsample=0.886, subsample_freq=1, colsample_bytree=0.983, reg_lambda=0.26711`) làm bộ chấm điểm **và** mô hình EER; ngữ cảnh k = 2.000 theo **HB2 đã khóa** (`rq2_hb2_lock_v1`, `LOCK_HB2.json` sha `9d8f6d49…1612`). Không chỉnh tham số |
| Replay | Scenario replay, vai EVAL/POLICY/CAL tách bạch (Q13); "score first, learn after"; nhãn đến cuối ngày s+τ, dùng từ ngày s+τ+1 cho cả chấm điểm lẫn chọn (Q8) |
| Chuỗi | Chuỗi tái xuất hiện: warm-up + họ rút d = 3 ngày rồi trở lại + 2 ngày sau; nếu τ > 0 thì thêm giai đoạn **làm nóng nhãn** (mục P3c) |
| Root | Các root DEV đã dùng của RQ2 (`DEV_REUSE`): ToN 2019-04-24, 25, 27, 28, 29 và CIC 2018-02-21 (6 root "informative" của DEV-CHECK). **Không mở** E1 (NF-UNSW-NB15-v3 2015-01-22/02-18), CIDDS-001, UGR'16 |
| Root "đủ thông tin" cho P3 (chốt trước) | Root được tính vào quyết định nếu nhánh Ngẫu nhiên có F1-macro trung bình < 0,95 (không chạm trần) ở mọi ô. Root chạm trần vẫn chạy và báo cáo nhưng không vào quyết định. Nếu còn < 4 root đủ thông tin → INCONCLUSIVE. (Lý do: RQ2 log bài học 5 — ToN 04-24, 04-27, 04-29 gần trần/hòa) |
| Nhánh so sánh | **R** ngẫu nhiên; **U** margin của chính mô hình (LightGBM), chọn trên toàn bộ POLICY chưa nhãn; **U_c** margin nhưng chỉ trên đúng N_c ứng viên mà EER thấy (tách tác dụng của tiêu chí khỏi tác dụng của việc lấy mẫu ứng viên); **EER_c** (2-6) dạng ngây thơ (Q17) trên N_c ứng viên |
| Ứng viên N_c | N_c = 10·b′ với b′ = (1−η)·b: b = 100 → N_c = 800; b = 300 → N_c = 2.400. Lấy ngẫu nhiên đều từ POLICY chưa nhãn, **cùng tập cho U_c và EER_c** (cùng seed). (Lý do: nếu N_c ≈ b′ thì không còn chọn lọc; tỷ lệ 10 chốt để giữ áp lực chọn 10%.) |
| Chọn | Một vòng, top-b′ theo điểm (không tham lam), vì tham lam nhân chi phí b′ lần (`03_…` A2) |
| Tổng nhãn | Mọi nhánh: đúng b′ nhãn chọn + ηb nhãn dành riêng mỗi ngày (assert theo ngày); báo cáo số nhãn thực tiêu |
| Chi phí | Trần chọn mẫu ≤ 1 CPU-giờ/ngày mô phỏng cho **mọi** nhánh (Q18). EER_c ở các ô trên dùng 0,044 giờ (b = 100) và 0,133 giờ (b = 300) mỗi ngày — dưới trần. R, U, U_c ≈ 0 so với EER_c; báo cáo tỉ lệ chi phí thực đo (không bắt các nhánh rẻ tiêu bằng nhau) → Q24 |
| g(x) | (2-6) như đề cương: ℒ_V = log-loss có trọng số 1/π trên V_t (PROPOSAL, vì Q-chưa-chốt ℒ_V; xem Q25); p̂ từ chính LightGBM dưới C; |Y| = 2; ngây thơ = cộng (x,y) vào C, không loại hàng (Q17). Refit **cùng seed bagging** cho mọi giả thuyết (số ngẫu nhiên chung) |
| V_t, D_cal | Q10/Q16: η·b chia 50/50 (seed); V_t theo ngày **đến** trong W_V = 3 ngày; hàng lấy từ CAL, phân tầng theo điểm của mô hình nhánh, lấy dư tầng cao, trọng số 1/π (Q11) |
| Ngưỡng λ_t | Định nghĩa 6 trên D_cal; sàn α_eff = max(α_t, 5/n_benign_cal) và **cờ ngày bị áp sàn** (A6) |
| Chỉ số chính | F1-macro 2 lớp tại λ_t (Q5); phơi nhiễm **E3** (Q1–Q4) và E1 phụ; chẩn đoán: độ cũ V_t (trung bình/tối đa theo ngày truy vấn, Q14/Q16), tỷ lệ ngày bị áp sàn, kích thước ngữ cảnh mỗi nhánh mỗi ngày |
| Chỉ số phụ không phụ thuộc ngưỡng | AUPRC_w (như RQ2) và recall tại số cảnh báo nhầm cố định — dùng khi A6 làm λ_t quá thô (b = 100) |
| Chỉ số nạp HB2 (Q17) | Với mỗi hàng được chọn ở ngày s (nhãn đến s+τ): **loaded@W** = hàng có mặt trong C ở ít nhất một ngày trong [s+τ+1, s+τ+W], W ∈ {3, 7}. Báo cáo tỷ lệ theo nhánh, theo (BASE | H), theo nhãn (benign | tấn công). Cần **ghi danh tính hàng trong BASE/H mỗi ngày** (RQ2 log §10 ghi lần kiểm toán trước không có telemetry này) |
| Quy tắc thực nghiệm (RQ2 log §5) | Băm tệp trước khi chạy; chạy **một lần**; `version_log.jsonl` chỉ nối thêm; báo cáo mọi root/seed/nhánh; bản sao runner với diff được ghi (runner khóa chỉ nhận k = 2.000 và 11 nhánh); I1–I3 dung sai 0; kiểm kích thước ngữ cảnh bằng nhau giữa các nhánh theo ngày (bài học 2) |
| Nhãn giả, bộ lọc RQ4 | **Không dùng** trong P3 (nhãn giả là ablation; bộ lọc thuộc RQ4, chưa thiết kế). P3 là nhánh "không có bộ lọc, nguồn sạch"; nhánh có bộ lọc để sau |

### Kiểm thử độ đúng của g(x) — chạy **trước** mọi probe (đáp ứng yêu cầu NCS (a)–(d))

Mỗi kiểm thử có tiêu chí đạt chốt trước; một kiểm thử không đạt = dừng P3a/P3c, sửa cài đặt, không đổi tiêu chí.

| # | Kiểm thử | Cách làm (CPU nhẹ) | Tiêu chí đạt |
|---|---|---|---|
| a | **Dấu và tổng quát** | Bài toán tổng hợp 2 lớp (Gaussian) với V rất lớn (10⁴), C nhỏ, ứng viên từ vùng thưa; p̂ = hậu nghiệm thật | ≥ 90% ứng viên có g > 0; trung bình g > 0. Không đạt → nghi ngờ cài đặt hoặc nhiễu bagging |
| b | **Thủy lực (plumbing)** | (i) thêm hàng trọng số 0: g phải bằng đúng 0; (ii) hàng giả định với p̂(y) = 0 không đóng góp; (iii) Σ_y p̂ = 1; (iv) hoán đổi thứ tự ứng viên: điểm không đổi | (i) |g| = 0 (cùng seed); (ii)–(iv) bằng nhau đến sai số số học 10⁻⁹ |
| c | **Xấp xỉ so với chính xác (trên mẫu con)** — theo yêu cầu đề cương L64 | 300 ứng viên × 3 ngày × 3 root: so g_chính xác (refit đầy đủ) với (1) g refit lá, nếu cài đặt được; (2) g trên N_c nhỏ hơn: Spearman ρ, độ trùng top-b′ (Jaccard), sai lệch trung bình | ρ ≥ 0,9 **và** Jaccard top-b′ ≥ 0,7; ngược lại xấp xỉ bị loại và báo cáo. (Ngưỡng là đề xuất; lý do: dưới 0,7 hơn 30% lựa chọn khác với chính xác, đủ làm mất ε₃ = 0,02) |
| d | **Tất định và tỉ số nhiễu/tín hiệu** | Hai lần refit cùng seed phải cho ℒ_V giống hệt; đo SD của g qua 10 seed bagging cho 200 ứng viên | Tất định đúng; SD(g qua seed) ≤ 0,5 × SD(g qua ứng viên). Không đạt → trung bình m lần refit (chi phí × m, tính lại cho cùng trần 1 CPU-giờ) |
| e | **Ước lượng V_t không lệch (IPW)** | Một ngày có đủ nhãn: lấy lại 200 lần mẫu η·b phân tầng + 1/π; so ℒ_V có trọng số với ℒ_V trên cả ngày | Trung bình trong ±2 SE của giá trị đầy đủ |

---

## P3b — Chi phí EER thực đo (LightGBM CPU) và ngoại suy TabFM — **chạy đầu tiên**

| Mục | Nội dung |
|---|---|
| Câu hỏi | Thời gian thực của EER trên LightGBM là bao nhiêu mỗi giả thuyết, mỗi ngày, theo b, N_c, |V_t|? Ngân sách ≤ 1 CPU-giờ/ngày giữ được ở N_c = 10b′ cho b ∈ {100, 300, 1.000} không? Với TabFM, N_c tối đa trong ≤ 1 GPU-giờ/ngày là bao nhiêu? |
| So sánh tối thiểu | (1) Refit đầy đủ; (2) refit lá (nếu cài đặt khả thi; API `refit` của LightGBM **[VERIFY — chưa mở tài liệu]**); (3) dự đoán V_t. Lưới: |V_t| ∈ {30, 90, 300}; N_c ∈ {200, 800, 2.400, 5.000, 8.000}; 20 lần lặp mỗi điểm |
| Root / seed | 2 root (1 ToN, 1 CIC), 3 seed; chỉ đo thời gian, không cần kết quả F1. Phần cứng ghi đủ (CPU, số luồng, phiên bản LightGBM) |
| Sản phẩm | Bảng t_giả-thuyết (trung vị, IQR) theo |V_t| và số luồng; công thức chi phí ngày C = 2·N_c·t_gt; N_c tối đa trong 1 CPU-giờ; **ngoại suy TabFM** bằng hệ số Bài 1 (4,36 + 5,25·|V|/1000 giây mỗi giả thuyết ở k = 2.000, nhãn *ngoại suy*) |
| Ngưỡng (chốt trước) | **GO** nếu t_gt đo ≤ 0,3 s (3 × ước lượng 0,1 s) và EER_c ở N_c = 10b′ cho b = 300 ≤ 1 CPU-giờ/ngày. **HOLD** nếu 0,3 s < t_gt ≤ 1 s: giảm N_c (ghi tỉ số N_c/b′ mới) hoặc bật refit lá. **NO-GO** (giả định chi phí A2 "LightGBM khả thi" bị bác) nếu t_gt > 1 s hoặc ngay cả refit lá không đưa ngày b = 300 dưới 1 CPU-giờ ở N_c ≥ 3b′ |
| Quy tắc dừng | Dừng nếu hai lần lặp liên tiếp lệch > 3× trung vị (máy nhiễu); dừng khi đã đo đủ lưới |
| Ước lượng CPU | ≈ 2 CPU-giờ (đo thời gian ≈ 200 giả thuyết × 0,1 s × 60 điểm ≈ 0,3 giờ; kiểm thử (a)–(e) ≈ 1–1,5 giờ) |
| Kết luận mẫu | ASSUMPTION FALSIFIED (A2 cho LightGBM) / INCONCLUSIVE / PROVISIONALLY SUPPORTED — vẫn DEV |

**Điều đã thấy trên giấy khi thiết kế (không phải kết quả) [SL, ngoại suy Bài 1 §4.5]:** mỗi giả thuyết TabFM mất ≈ 4,52 / 4,83 / 5,94 s (|V| = 30 / 90 / 300). Dưới trần 1 GPU-giờ, số ứng viên tối đa N_c ≈ 3600/(2·t) = **≈ 400 (b = 100), ≈ 370 (b = 300), ≈ 300 (b = 1.000)**. So với N_c = 10·b′ = 800 / 2.400 / 8.000: TabFM chỉ đạt 0,5× / 0,15× / 0,04× tỉ lệ cần. Ở b = 300, N_c ≈ 370 chỉ gấp 1,5 lần b′ = 240 (chọn 65% ứng viên) ⇒ **EER chính xác trên TabFM dưới trần của NCS gần như không còn tính chọn lọc ở b ≥ 300**. Đây là phát hiện cần đưa vào G5 (A2); P3b kiểm bằng số đo LightGBM nhưng **không thể** kiểm số TabFM trong DEV CPU.

---

## P3a — Khoảng cách (headroom): Ngẫu nhiên vs Bất định vs EER

| Mục | Nội dung |
|---|---|
| Câu hỏi | Ở b ∈ {100, 300}, τ ∈ {0, 1 ngày} (4 ô), nhánh EER_c có hơn U ít nhất ε₃ = 0,02 F1-macro **và** thấp hơn về phơi nhiễm E3 không? EER_c hơn U_c không (tách tác dụng tiêu chí)? |
| So sánh tối thiểu | Mỗi ô: EER_c − U; EER_c − U_c; EER_c − R; U − R (kiểm mốc: nếu U không hơn R thì ô không có áp lực chọn) |
| Root / seed | 6 root DEV_REUSE; 5 seed; chuỗi tái xuất hiện d = 3 (7 ngày chọn). Giai đoạn sơ bộ S1 (xem quy tắc dừng): 3 root × 2 seed ở ô (b = 100, τ = 0) để ước SD |
| Đơn vị suy luận | Root (n ≤ 6) — theo Q15 và Nội dung 1: ngày gốc là đơn vị độc lập; seed lấy trung vị trong root; **không** coi chuỗi/seed là đơn vị độc lập |
| Quyết định mỗi ô (theo Q15) | Δ_root = trung vị seed của (F1-macro nhánh A − nhánh B). Trung vị qua root; Wilcoxon một phía chính xác (n = 6: p nhỏ nhất = 1/64 ≈ 0,0156; p < 0,05 đạt khi tất cả dương hoặc chỉ một hiệu âm có hạng 1–2); ΔE3 < 0 một phía. **Lưu ý thiết kế:** Holm trên 4 ô yêu cầu p nhỏ nhất < 0,05/4 = 0,0125, mà với n = 6 root p nhỏ nhất là 0,0156 ⇒ **không ô nào có thể qua Holm**. Do đó trong probe DEV dùng p chưa hiệu chỉnh < 0,05 làm tiêu chí, báo cáo p-Holm chỉ để mô tả; (n = 7 root cho p nhỏ nhất 1/128 = 0,0078 < 0,0125 — phát hiện này đáng đưa vào kế hoạch công suất của nghiên cứu chính, G5). **Không gộp qua ô** |
| Ngưỡng ε dùng trong probe | ε₃ = max(0,02; 2 × SD giữa seed của ΔF1 ước từ S1) — theo tiêu chí (ii) của đề cương L53. Nếu 2×SD > 0,02, ngưỡng GO tăng theo, ghi rõ. Lý do: đề cương đã chốt giá trị lớn hơn của hai tiêu chí |
| GO / HOLD / NO-GO (chốt trước) | **PROVISIONALLY SUPPORTED (GO)** cho một ô: median_root(ΔF1 EER_c−U) ≥ ε₃, Wilcoxon p < 0,05 (chưa hiệu chỉnh; xem lưu ý Holm), median ΔE3 < 0 và ≥ 5/6 root cùng dấu ΔE3, **và** EER_c − U_c ≥ 0 (không do chỉ nhờ lấy mẫu ứng viên). **ASSUMPTION FALSIFIED (NO-GO)** nếu ở **cả 4 ô** cận trên 90% (bootstrap phân cấp qua root) của ΔF1(EER_c−U) < ε₃ **và** median < 0,01. **INCONCLUSIVE (HOLD)** mọi trường hợp còn lại, kể cả < 4 root đủ thông tin hoặc λ_t bị áp sàn trên ≥ 50% ngày (b = 100) mà chỉ số phụ thuộc ngưỡng không phân biệt được → khi đó phán quyết dựa AUPRC_w, nêu rõ. (0,01 = nửa ε₃: dưới mức đó ngay cả cận lạc quan cũng không chạm ε₃; chọn vì ε₃ chưa có giá trị chốt cuối) |
| Quy tắc dừng | (1) S1: nếu SD giữa seed của ΔF1 > 0,05 → dừng, HOLD, thiết kế lại số seed. (2) Vi phạm I1–I3, ngữ cảnh không đủ k, hoặc nhãn thực tiêu khác giữa nhánh → dừng ngay. (3) Thời gian mỗi chuỗi > 3× ước lượng → dừng và tính lại chi phí. (4) Dừng sớm vì vô ích: khi 4 root đủ thông tin đã xong ở cả 4 ô, nếu ≥ 3 ô có ΔF1(EER_c−U) < 0 trên ≥ 4/4 root → khai NO-GO sớm |
| Ước lượng CPU | EER_c: b = 100 → 800 ứng viên → 1.600 giả thuyết × 0,1 s = 160 s = 0,044 giờ/ngày; b = 300 → 4.800 × 0,1 = 480 s = 0,133 giờ/ngày. Một cặp (root, seed): 7 ngày × (0,044 + 0,133) × 2 giá trị τ = 2,5 giờ. × 6 root × 5 seed = **≈ 74 CPU-giờ** (R, U, U_c và đánh giá F1 mỗi ngày ≪ 0,01 giờ/ngày). Thời gian thực ≈ 74 / số lõi (8 lõi ≈ 9–10 giờ; số lõi thực **[CXM]**). Phụ thuộc số đo P3b |
| Kết luận mẫu | ASSUMPTION FALSIFIED / INCONCLUSIVE / PROVISIONALLY SUPPORTED — vẫn DEV |

**Báo cáo bắt buộc trong P3a** (ngoài chỉ số chính): chỉ số nạp HB2 loaded@3 và loaded@7 theo nhánh (Q17); độ cũ V_t; số ngày áp sàn α_eff; kích thước ngữ cảnh/ngày; thời gian thực mỗi nhánh; sai lệch xấp xỉ (kiểm thử c).

**Ngưỡng cho chỉ số nạp (PROPOSAL, chưa duyệt):** "thấp" nếu loaded@3 của EER_c < 25% hoặc < 50% của loaded@3 của U ở cùng ô. Lý do: dưới 25% thì ≥ 75% nhãn đã trả không từng ảnh hưởng ngữ cảnh trong 3 ngày. Khi "thấp", biến thể g nhận biết HB2 chỉ được thiết kế ở DEV (theo Q17), không thay đổi nhánh chính.

---

## P3c — Nhãn trễ τ = 7

| Mục | Nội dung |
|---|---|
| Câu hỏi | Ở một b (b = 300), τ = 7: EER_c có còn hơn U ≥ ε₃ không? V_t (cũ 8–10 ngày) có còn đại diện không? So với τ = 0 trên **cùng cấu trúc chuỗi** |
| Vấn đề thiết kế phát hiện được | Với chuỗi 7 ngày và τ = 7: nhãn hỏi ở cuối ngày s đến cuối ngày s+7, dùng từ ngày s+8 ⇒ **không nhãn nào kịp dùng trong chính chuỗi** ⇒ mọi nhánh chọn mẫu đồng nhất không thể khác nhau. Do đó P3c cần giai đoạn **làm nóng nhãn**: τ + 2 = 9 ngày trước khi họ bị rút (chuỗi ≈ 9 + 3 + 2 ≈ 14 ngày). Ngoài ra ngữ cảnh/D_cal ban đầu cho τ > 0 chưa được định nghĩa (Bài 1 chỉ τ = 0) ⇒ **Q23** |
| So sánh tối thiểu | R, U, U_c, EER_c ở (b = 300, τ = 7) **và** cùng bốn nhánh ở (b = 300, τ = 0) trên chuỗi dài 14 ngày (tham chiếu cùng cấu trúc) |
| Root / seed | Các root đủ thông tin từ P3a (≥ 4, tối đa 6) × 3 seed |
| Ngưỡng (chốt trước) | Hiệu ứng trễ ΔΔ = ΔF1(τ=0) − ΔF1(τ=7) của EER_c−U. **PROVISIONALLY SUPPORTED** (EER còn lợi thế khi trễ) nếu median_root ΔF1(τ=7) ≥ ε₃ (cùng quy tắc ô P3a, một ô nên không Holm) và ΔE3 < 0. **ASSUMPTION FALSIFIED** (A3) nếu median ΔF1(τ=7) < 0,01 và cận trên 90% < ε₃. **INCONCLUSIVE** còn lại. Báo cáo bắt buộc: độ cũ V_t (trung bình/tối đa theo ngày truy vấn), tỷ lệ ngày V_t rỗng, tỷ lệ họ tái xuất hiện không có hàng nào trong V_t (điểm mù A3), loaded@W |
| Quy tắc dừng | Không chạy nếu P3a là ASSUMPTION FALSIFIED (khi U ≈ R hoặc EER_c ≤ U ở mọi ô thì τ = 7 không đổi kết luận). Dừng nếu V_t rỗng > 50% ngày đánh giá ở τ = 7 (khi đó EER không xác định, ghi nhận như kết quả chứ không sửa) |
| Ước lượng CPU | 2 giá trị τ × 6 root × 3 seed × 14 ngày × 0,133 giờ = **≈ 67 CPU-giờ** (chỉ nhánh EER_c đắt) |
| Kết luận mẫu | ASSUMPTION FALSIFIED / INCONCLUSIVE / PROVISIONALLY SUPPORTED — vẫn DEV |

---

## 6. Thứ tự và tổng chi phí đề nghị

| Bước | Việc | CPU ước lượng |
|---|---|---|
| 0 | Kiểm thử độ đúng (a)–(e) | ≈ 1–1,5 giờ (gộp vào P3b) |
| 1 | **P3b** (đo thời gian; số đo thay các ước lượng 0,1 s) | ≈ 2 giờ |
| 2 | **P3a** giai đoạn S1 (3 root × 2 seed, ô b = 100, τ = 0) | ≈ 1,9 giờ (3 × 2 × 7 × 0,044) |
| 3 | **P3a** đầy đủ | ≈ 74 giờ |
| 4 | **P3c** (chỉ nếu P3a không FALSIFIED) | ≈ 67 giờ |
| Tổng | | **≈ 145 CPU-giờ trường hợp xấu nhất** (±2×, phụ thuộc phần cứng và P3b) |

Tổng ngân sách thực nghiệm chính thức **chốt sau P3b, trước tiền đăng ký** (Q18); số trên chỉ để NCS cân nhắc.

## 7. Câu hỏi mới cho NCS

| # | Câu hỏi | Mặc định tôi dùng nếu không trả lời |
|---|---|---|
| Q23 | **Khởi tạo** ngữ cảnh C₀ và D_cal₀ cho τ > 0: nhãn của những ngày đầu chưa đến. Cho phép một **lịch sử nhãn trước luồng** (ví dụ k hàng từ phần POLICY và một D_cal₀ từ CAL, giống nhau cho mọi nhánh, không tính vào b)? Giai đoạn làm nóng nhãn (τ+2 ngày) cho P3c có chấp nhận không? | Chặn P3a/P3c ở τ ≥ 1 cho tới khi có câu trả lời; P3a ô τ = 0 có thể chạy trước |
| Q24 | "Cùng chi phí" = mọi nhánh tuân **cùng trần ≤ 1 CPU-giờ/ngày** (cách tôi hiểu), hay phải **dùng gần bằng nhau** (khi đó R/U cần một dạng tiêu thêm tính toán, ví dụ ensemble nhiều seed)? | Cách hiểu thứ nhất; báo cáo tỉ lệ chi phí |
| Q25 | ℒ_V chính thức = log-loss có trọng số 1/π (đề xuất của tôi) hay 0-1? (Đề cương chưa nêu; Settles nêu cả hai.) Quy tắc N_c = 10·b′ và nhánh phân tách U_c có chấp nhận không? | log-loss; N_c = 10·b′; có U_c |
| Q26 | Root "đủ thông tin" cho P3 (F1-macro nhánh ngẫu nhiên < 0,95) và gộp quyết định theo root có chấp nhận không? Có muốn dùng cả root chạm trần làm kiểm tra phụ? | Như đề xuất ở §0 |
