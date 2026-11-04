# 04 — BASELINES AND NOVELTY (G3)

- **STATUS:** G3 **APPROVED** (NCS, 04/11/2026); Q19–Q22 đã trả lời (mục 8). H3 = NO CONCLUSION. Verdict tính mới: **GAP_NARROW** (không phải GAP_CONFIRMED).
- **SOURCE ANCHORS:** `sources/outline_v14_3_RQ3_RQ4_verbatim.txt` L64 (danh sách đối chứng); `sources/outline_v14_3_references.txt` [1] [3] [4] [30] [31]; `sources/REVIEW_SKELETON.md` KT3; `sources/RQ2_DECISION_LOG.md` §10 (novelty audit RQ2: NARROW_REQUIRED); NCS Q15–Q18 (04/11/2026); `sources/THESIS_AUDIT_LOG_RQ3_RQ4.md` (chưa lưu vào `sources/` — xem ghi chú dưới); `RQ3_REFS.bib` (chỉ nguồn đã mở, mỗi mục có `x-opened`, `x-depth`).
- **ASSUMPTIONS:** (1) "VERIFIED" = tôi đã mở trang/PDF và đọc phần được nêu; "MENTIONED_ONLY" = chỉ có tên/bản ghi/ảnh chụp kết quả tìm kiếm; "MISSING" = không tìm thấy hoặc không mở được. (2) Tìm kiếm tính mới giới hạn: ≈ 8 truy vấn chế độ standard + các bài đã tải; không phải rà soát hệ thống. Vắng kết quả không chứng minh khoảng trống. (3) Cập nhật quyết định: Q15–Q18 áp dụng (Q15 theo ô, Wilcoxon, Holm; Q16 thành viên V_t theo ngày đến; Q17 g(x) ngây thơ + chỉ số nạp HB2; Q18 nhãn giả cho hàng chờ nhãn, vùng trôi dạt = kNN-đặc-trưng > P95 của D_cal, ngân sách chọn ≤ 1 GPU-giờ TabFM / ≤ 1 CPU-giờ LightGBM mỗi ngày mô phỏng).
- **OPEN QUESTIONS:** Q19–Q22 (mục 7).
- **DECISION:** Không có kết luận H3. Đề xuất mục 5 và 7 chưa duyệt.

**Ghi chú nguồn:** `THESIS_AUDIT_LOG_RQ3_RQ4.md` (NCS đính kèm lần này) và `outline_v14_3_noidung5.txt` đã **đọc toàn bộ** (nội dung được dán trong hội thoại). Tôi lưu bản chính vào `sources/` ở lần commit này như bản tham chiếu của NCS. Nội dung 5 xác nhận: "ba cơ chế chạy chung theo thứ tự lọc → chọn → nạp … ablation bỏ từng cơ chế … bỏ bộ lọc thì ngăn mẫu khó và chọn mẫu theo độ bất định có làm tăng tỷ lệ nhãn độc trong ngữ cảnh không" → **gỡ HOLD cho Nội dung 5**; IC-1 giữ cách đọc chức năng (D3 của nhật ký: RQ3 chọn hàng chưa nhãn → nhãn đến sau τ → bộ lọc RQ4 → HB2 nạp).

---

## 1. Đặc tả sáu đối chứng

Nhãn nguồn: V = VERIFIED, M = MENTIONED_ONLY, X = MISSING. "Phần đã mở" nêu rõ.

### 1.1 Chọn ngẫu nhiên
| Mục | Nội dung |
|---|---|
| Vào | Tập ứng viên U_t (phần POLICY chưa nhãn, Q11/Q13), b' = (1−η)·b |
| Ra | b' hàng chọn đều không hoàn lại, seed cố định |
| Tham số | seed; không có siêu tham số |
| Nguồn/mã | Không cần nguồn ngoài; viết theo giao thức |
| Trạng thái | V (định nghĩa tầm thường); là mốc sàn cho A1 |

### 1.2 Bất định kiểu INSOMNIA [3] — **V**
| Mục | Nội dung |
|---|---|
| Nguồn | Andresini et al., AISec '21, DOI 10.1145/3474369.3486864 — mở full text https://s2lab.cs.ucl.ac.uk/downloads/insomnia.pdf (đọc §3 phương pháp, §5 thực nghiệm, §7) |
| Vào / Ra (đã đọc) | Mỗi cửa sổ X_i: DNN cho softmax; **chọn top σ% hàng có độ tin cậy softmax thấp nhất** (least confidence) → tập X_US; nhãn ước lượng bằng "oracle" NC (nearest-centroid/phân cụm) → thêm vào D → tinh chỉnh DNN. σ tham số người dùng; thực nghiệm σ ∈ {20, 50, 70}%. So sánh với Random Sampling (RS) |
| Điểm khác với đề cương/Q6 | (i) INSOMNIA dùng **nhãn ước lượng** (pseudo-label) thay nhãn người trong cập nhật; đề cương chỉ lấy tiêu chí chọn ("kiểu INSOMNIA"); (ii) tiêu chí gốc = least-confidence của DNN, còn Q6 chốt margin của mô hình nhánh — cho nhị phân hai xếp hạng như nhau nên tương đương trên giấy; (iii) bài **giả định nhãn đến ngay** (tác giả nêu thời gian chạy tính theo giả định nhãn người có sẵn "as soon as the model needs them") → khớp mô tả KT3 "đa số coi nhãn đến ngay" |
| Mã / giấy phép / phiên bản | Bài §7: mã tại http://www.di.uniba.it/~andresini/insomnia.html (**trang này tôi chưa mở**). Kết quả tìm kiếm ghi truy cập mã qua biểu mẫu xin quyền (https://docs.google.com/forms/…, **không mở**). Giấy phép/phiên bản: **[VERIFY / MISSING]** |
| Quyết định cần | Với RQ3 chỉ cần tái hiện luật chọn (top-b theo margin) — không cần mã INSOMNIA |

### 1.3 Mật độ NetGuard [1] — **V ở mức tổng quan phương pháp; mã MISSING**
| Mục | Nội dung |
|---|---|
| Nguồn | Gupta et al., arXiv:2503.03022 — mở trang abstract và PDF (https://arxiv.org/pdf/2503.03022); đọc phần tổng quan "density-aware dataset prior selection", thiết lập ngân sách; chưa đọc phụ lục/toàn bộ thực nghiệm |
| Vào / Ra (đã đọc) | Vào: tập có nhãn X_L (huấn luyện) và chưa nhãn X_UL (kiểm). Khớp GMM cho cả X_L và X_UL; điểm thông tin I_Score(x) = **chênh log-likelihood của x dưới GMM của X_UL so với GMM của X_L** (mô tả trong bài; công thức chính xác chưa trích); chọn lô X_P ⊆ X_UL có điểm cao trong ngân sách nhãn P ("prior labeling budget"); sau đó sinh dữ liệu có điều kiện cho lớp thiểu số (cắt ngưỡng lớp thiểu số 5%). Ngân sách thí nghiệm 0,1% / 0,5% / 1% |
| Điểm lệch | Là **thích nghi theo đợt (train/test)**, không phải luồng hằng ngày; luật chọn là một khâu của khung "chọn + sinh". Đối chứng RQ3 chỉ dùng khâu chọn theo mật độ (không sinh dữ liệu) → là phiên bản **rút gọn**, cần NCS xác nhận (Q19) |
| Mã / giấy phép | Không có liên kết mã trong trang abstract; PDF không chứa URL GitHub (grep) → **MISSING**. Giấy phép *bài báo*: CC BY 4.0 (trang abstract) — không phải giấy phép mã |
| Tham số cần khóa | số thành phần GMM, kiểu hiệp phương sai, cách tính I_Score, kích thước lô; bài có phân tích độ nhạy GMM ở phụ lục (chưa đọc) |

### 1.4 Kích hoạt theo thay đổi STRAL [4] — **V (một phần); mã MISSING**
| Mục | Nội dung |
|---|---|
| Nguồn | Ndichu et al., arXiv:2605.22324 **v2 (18/10/2026), bản đổi tên từ PACT v1** — mở https://arxiv.org/pdf/2605.22324; đọc tóm tắt, mô tả bộ điều khiển, §5.3, tuyên bố sẵn có dữ liệu/mã. Lưu ý: danh mục tham khảo của đề cương ghi "STRAL … arXiv:2605.22324, 2026" khớp v2; kết quả v1 (PACT) *không so sánh trực tiếp* theo chính ghi chú của tác giả |
| Vào / Ra (đã đọc) | Phát lại theo lô; mỗi sự kiện có điểm của mô hình triển khai; **điểm *trước cập nhật* đưa vào ADWIN (δ = 0,002) chỉ khi hết thời gian chờ 2.000 sự kiện**; cảnh báo ADWIN kích hoạt thu nhãn "lai" (gần ngưỡng + điểm cao; tỷ lệ bất định thử 0/50/100%), hạn mức theo mỗi lần kích hoạt; cập nhật có giới hạn (tối đa 500 cây XGBoost); biến thể "Guard" kiểm tra cập nhật trên tập nhãn quá khứ |
| Điểm lệch | STRAL **không có hạn mức b nhãn/ngày cố định**: lượng nhãn do kích hoạt quyết định (ví dụ tổng 2.000–3.550 nhãn tùy thiết lập). Đề cương RQ3 đặt b cố định mỗi ngày. Cần quy tắc thích nghi (Q20). STRAL không mô hình hóa nhãn trễ (không thấy từ khóa delay/latency trong văn bản) — khớp KT3. Tập nhãn quá khứ trong Guard cũng ký hiệu V_t nhưng **là khái niệm khác** với V_t của (2-6) (cùng tên, khác vai trò) |
| Mã / giấy phép | "Upon publication, we intend to release …" → **chưa phát hành → MISSING** |

### 1.5 Bất định ngẫu nhiên hóa [30] Žliobaitė et al. — **bài gốc M; triển khai V (tài liệu)**
| Mục | Nội dung |
|---|---|
| Nguồn bài | TNNLS 25(1):27–39, 2014. **Chưa mở được toàn văn**: chỉ có ảnh chụp kết quả tìm kiếm (trang ip-paris.fr) mô tả "ba chiến lược: bất định, phân bổ động ngân sách, ngẫu nhiên hóa không gian tìm kiếm" → M, [VERIFY] |
| Nguồn triển khai | MOA 2020.12.0 `moa.classifiers.active.ALUncertainty` — **đã mở** https://javadoc.io/static/nz.ac.waikato.cms.moa/moa/2020.12.0/moa/classifiers/active/ALUncertainty.html: bốn chiến lược `FixedUncertainty`, `VarUncertainty`, `RandVarUncertainty`, `SelSampling`; tham số `-b` ngân sách, `-u` ngưỡng cố định, `-s` bước ngân sách trôi, `-n` số mẫu đầu không dùng AL; trích dẫn bản ECML/PKDD 2011 (tiền thân) |
| Điểm lệch | Là quy tắc **quyết định từng mẫu theo ngưỡng** (stream-based), không xếp hạng top-b; mapping sang "đúng b nhãn mỗi ngày" cần quy tắc (Q20) |
| Mã / giấy phép / phiên bản | Phiên bản tài liệu 2020.12.0; giấy phép mã MOA **không mở → [VERIFY]** |

### 1.6 EER cho LightGBM cùng ngân sách [31] — **V (lý thuyết); mã tham chiếu X ở mức giấy phép**
| Mục | Nội dung |
|---|---|
| Nguồn | Roy & McCallum, ICML 2001 — mở trang abstract https://mlanthology.org/icml/2001/roy2001icml-optimal/ (không nêu hàm mất mát, không có PDF); công thức lấy từ **Settles 2010 §3.4** (đọc đầy đủ): EER 0/1: x* = argmin_x Σ_i P(y_i|x) Σ_u (1 − P_{θ+⟨x,y_i⟩}(ŷ|x^(u))); EER log-loss tương đương giảm entropy kỳ vọng; "gần tối ưu và không phụ thuộc lớp mô hình"; chi phí O(U·L·G) cho hồi quy logistic nhị phân; khuyến nghị lấy mẫu Monte Carlo từ pool hoặc huấn luyện xấp xỉ |
| Khác biệt với (2-6) | Settles dùng **U chưa nhãn làm tập kiểm với hậu nghiệm của chính mô hình**; (2-6) dùng **V_t có nhãn chuyên viên có trọng số IPW** và chỉ phần "rời C_t và D_cal". Đây là một biến đổi có chủ đích của đề cương (không sai) — phải được kiểm thử độ đúng (mục 3) |
| Triển khai tham chiếu | modAL `expected_error_reduction(learner, X, loss='binary'\|'log', p_subsample=1.0, n_instances=1)` — **đã mở** https://modal-python.readthedocs.io/en/latest/content/apireference/expected_error.html (chỉ chữ ký/tham số; không mô tả huấn luyện lại; kho mã và giấy phép **chưa mở → [VERIFY]**). `p_subsample` = xác suất giữ mỗi mẫu pool = lấy mẫu ứng viên |
| Xấp xỉ refit lá | Sharchilev et al. 2018 (arXiv:1802.06640) — **chỉ trang abstract**: huấn luyện lại bỏ-một cho GBDT với cấu trúc cây cố định, có xấp xỉ đánh đổi độ chính xác/tính toán. Tên "LeafRefit" thấy ở ảnh chụp tìm kiếm nhưng **không có trên trang đã mở → [VERIFY]**. Chưa có công trình đã mở dùng refit lá cho **EER** (chỉ cho ảnh hưởng mẫu/bỏ-một) |
| LightGBM | Ke et al. 2017 [11] (đề cương); API `Booster.refit` và giấy phép MIT: **chưa mở → [VERIFY]** |
| Ngân sách tính toán (Q18) | ≤ 1 CPU-giờ/ngày mô phỏng (LightGBM) ⇒ theo mục 4 của `03_…`, N_c ≲ 5.000 với refit đầy đủ (≈ 0,28 CPU-giờ/ngày) là vừa ngân sách; N_c = 50.000 (2,8 CPU-giờ/ngày) vượt |

**Bảng tổng:**
| Đối chứng | Bài | Mã | Giấy phép | Phiên bản | Trạng thái |
|---|---|---|---|---|---|
| Ngẫu nhiên | n/a | tự viết | n/a | n/a | V |
| Bất định [3] | V (toàn văn) | X/[VERIFY] (trang tác giả chưa mở; truy cập theo yêu cầu) | [VERIFY] | AISec '21 | V (luật chọn) |
| Mật độ [1] | V (tổng quan PP) | X | bài CC BY 4.0; mã MISSING | arXiv v3 (kết quả tìm kiếm nêu v3; **tôi chưa xác nhận bản tôi đọc là v3**) | V một phần |
| STRAL [4] | V (một phần) | X (chưa phát hành) | MISSING | v2 (18/10/2026) | V một phần |
| Bất định ngẫu nhiên [30] | M (bài); V (MOA doc) | MOA (mã chưa mở) | [VERIFY] | MOA 2020.12.0 | M/V |
| EER [31] | V (Settles); abstract Roy | modAL (chưa mở repo) | [VERIFY] | — | V (công thức) |

---

## 2. Tìm kiếm tính mới

**Phạm vi:** ≈ 8 truy vấn WebSearch (chế độ standard) + PDF đã tải: Tab-AICL, Cacciarelli & Kulahci, Castellani 2022, INSOMNIA, NetGuard, STRAL, Settles; trang abstract Sharchilev, Roy&McCallum, modAL, MOA. Không dùng cơ sở dữ liệu trích dẫn ngược.

| Hướng tìm | Tìm thấy (đã mở) | Không tìm thấy |
|---|---|---|
| EER cho học trong ngữ cảnh / mô hình nền dạng bảng | **Tab-AICL (Treerath & Pittorino 2026)** [V: tóm tắt, giới thiệu, phương pháp]: bốn luật thu nhãn cho TabPFN (margin, coreset, lai, proxy-lai); pool tĩnh; cold-start ≤ 100 nhãn; so với CatBoost/XGBoost-margin huấn luyện lại; giảm chi phí chấm pool bằng proxy tuyến tính. | **Không có EER**, nhãn trễ, luồng, trôi dạt, chỉ số phơi nhiễm. Truy vấn tìm "EER + TabPFN" không ra công trình nào |
| EER trong luồng / có trôi dạt | Cacciarelli & Kulahci (khảo sát) liệt EER vào nhóm "lỗi/phương sai kỳ vọng" (trích Cohn 1996, Roy 2001) [V: đoạn phân loại] | Không thấy phương pháp luồng nào dùng EER trong các đoạn đã đọc (chưa đọc toàn văn) |
| EER với nhãn trễ | **Castellani et al. 2022** [V: tóm tắt/giới thiệu]: PRopagate = bộ ước lượng tiện ích độc lập độ trễ *và dự đoán nhãn đã yêu cầu chưa tới*; ngân sách động sau phát hiện trôi dạt. **Pham et al. 2022 (FS)** [chỉ ảnh chụp tìm kiếm — M]: quên dữ liệu cũ + mô phỏng nhãn đang chờ khi ước lượng tiện ích. Cả hai là tiện ích kiểu bất định/không gian đặc trưng, **không phải EER** | EER có xét nhãn đang chờ: không thấy |
| Chọn mẫu trong IDS dưới trôi dạt | INSOMNIA (bất định + nhãn ước lượng), NetGuard (mật độ + sinh), STRAL (kích hoạt ADWIN + lai), CD-AHAL (theo ảnh chụp tìm kiếm — M) | Không có công trình dùng chỉ số phơi nhiễm [2] cho so sánh chiến lược chọn trong các nguồn đã mở |
| Xấp xỉ EER | modAL `p_subsample` (lấy mẫu pool); Settles: Monte Carlo/huấn luyện xấp xỉ; Tab-AICL proxy-shortlist (cho bất định) | EER + refit lá cho GBDT: không thấy (Sharchilev chỉ cho ảnh hưởng mẫu) |

---

## 3. Tách bốn trục (correctness / effectiveness / novelty / contribution)

| Trục | Câu hỏi | Trạng thái hiện tại |
|---|---|---|
| **Correctness** | g(x) của (2-6) được cài đặt đúng định nghĩa EER chưa? | Chưa có mã. Công thức có biến đổi so với Settles (V_t có nhãn + IPW thay cho U + hậu nghiệm). Cần thử trên giấy: (a) g(x) ≥ 0 kỳ vọng khi V_t đại diện; (b) g = 0 khi (x,y) trùng hàng đã có (nếu C đã đủ); (c) EER chính xác = xấp xỉ khi ứng viên nhỏ (so sánh trên mẫu con, đề cương yêu cầu báo sai lệch); (d) cùng seed → cùng điểm với LightGBM bagging (A2). Xếp **CHƯA KIỂM** |
| **Effectiveness** | EER có hơn bất định ≥ ε₃ và giảm phơi nhiễm? | **Không có bằng chứng.** A1 AT_RISK (`03_…`). Phụ thuộc probe P3a |
| **Novelty** | Chưa có công trình đã làm? | **GAP_NARROW** (mục 4) |
| **Contribution** | Theo chuẩn đóng góp NCS 01/11/2026 (RQ2 log §2): thay đổi kỹ thuật thật; lợi ích đo được; so sánh công bằng + ablation; phân biệt với tiền lệ; kiểm độc lập sau phát triển | Chưa đạt tiêu chí nào. EER-cho-LightGBM theo đề cương là *đối chứng* (không phải đóng góp). Đóng góp khả dĩ = "EER tính trên ngữ cảnh của mô hình học-trong-ngữ-cảnh, có nhãn trễ, trên nền HB2, đo bằng phơi nhiễm". Chỉ đáng tuyên bố nếu A1 qua và so sánh ngang chi phí (≤ 1 GPU-giờ/ngày) |

---

## 4. Verdict tính mới: **GAP_NARROW**

**Lý do (SUY LUẬN từ nguồn đã mở):**
1. Từng thành phần đã tồn tại riêng: EER (Roy–McCallum, Settles), lấy mẫu ứng viên (Roy; modAL), shortlist bằng proxy cho học chủ động với TabPFN (Tab-AICL), ước lượng tiện ích có nhãn chờ (Castellani; Pham — chưa mở), chọn mẫu bất định/mật độ/kích hoạt trong IDS (INSOMNIA, NetGuard, STRAL).
2. **Chưa thấy** trong phạm vi đã tìm: một công trình kết hợp (i) EER; (ii) mô hình học-trong-ngữ-cảnh mà "huấn luyện lại" = đổi ngữ cảnh; (iii) luồng có trôi dạt, mất cân bằng; (iv) nhãn trễ; (v) chỉ số phơi nhiễm.
3. Mệnh đề KT3 trong đề cương ("giảm lỗi kỳ vọng [31] chưa được khảo sát cho TFM") **nhất quán** với những gì tìm được nhưng là mệnh đề tuyệt đối; nên viết "chưa thấy trong phạm vi đã tìm" (cùng nguyên tắc với bản kiểm toán RQ2: không viết "chưa có tiền lệ").
4. Không nâng thành GAP_CONFIRMED vì: tìm kiếm hẹp; Pham 2022 và Žliobaitė 2014 (journal) chưa mở; Cacciarelli chưa đọc toàn văn; Tab-AICL là công trình *liền kề nhất* (cùng nhóm: học chủ động bằng ngữ cảnh của TabPFN) và khác ở: luật thu nhãn, pool tĩnh vs luồng, cold-start ≤ 100 nhãn vs ngân sách hằng ngày, không nhãn trễ.
5. Không GAP_CLOSED: không có nguồn đã mở nào làm đúng tổ hợp trên.

**Điểm phân biệt phải nêu rõ** khi viết đóng góp: (a) so với Tab-AICL; (b) so với Castellani/Pham (tiện ích kiểu không-EER xử lý nhãn chờ); (c) so với EER cổ điển (tập kiểm có nhãn + IPW + ngữ cảnh bị chặn k); (d) tính toán (xấp xỉ).

**Rủi ro tính mới** [SL]: một phản biện có thể coi "EER trên ngữ cảnh" là EER cổ điển với mô hình khác; điểm khác chỉ còn ở việc "huấn luyện lại = thêm hàng vào ngữ cảnh, không cập nhật tham số", nhưng Settles đã nêu trực tiếp các mô hình phi tham số làm EER "khá khả thi" (Gaussian random fields) vì huấn luyện lại tăng dần chính xác — ICL có tính chất tương tự (không huấn luyện) nhưng suy luận lại tốn kém (A2).

---

## 5. Đề xuất (CHƯA DUYỆT)

1. [ĐX] Hai biến thể bất định để làm độ nhạy ngoài biến thể chính (margin của mô hình nhánh): least-confidence (khớp INSOMNIA gốc; tương đương nhị phân) — không cần chạy thêm.
2. [ĐX] Với NetGuard: dùng riêng khâu "chọn theo mật độ GMM" (bỏ sinh dữ liệu), nêu rõ đây là bản rút gọn, ngân sách theo b.
3. [ĐX] Với STRAL: dùng riêng bộ kích hoạt ADWIN để quyết định *ngày nào được tiêu ngân sách*, với trần b nhãn/ngày và mức tối thiểu cố định cho phần dành riêng η·b để không phá V_t/D_cal.
4. [ĐX] Với [30]: dùng `RandVarUncertainty` như quy tắc ngưỡng ngẫu nhiên, điều chỉnh để dừng khi đủ b' nhãn trong ngày.
5. [ĐX] Mô tả tính mới theo lời lẽ hạn chế (mục 4), nêu Tab-AICL và Castellani/Pham như tiền lệ gần.
6. [ĐX] Trước khi phát biểu đóng góp, mở đủ: Pham et al. 2022 (Springer, bị chặn 429), Žliobaitė 2014 (toàn văn), Zhu et al. 2003 (EER bán giám sát — Settles dẫn "cải thiện đáng kể"), Guo & Greiner 2007 (EER biến thể lạc quan); đọc Cacciarelli đầy đủ mục chọn mẫu và nhãn trễ.

---

## 6. Nguồn chưa mở (không ghi VERIFIED, không đưa vào `RQ3_REFS.bib`)
- Žliobaitė, Bifet, Pfahringer, Holmes, TNNLS 25(1), 2014 [30] — chỉ ảnh chụp tìm kiếm (ip-paris.fr, MOA doc) → M.
- Pham, Kottke, Krempl, Sick, *Machine Learning* 2022, doi:10.1007/s10994-021-06099-z — Springer trả 429; trang Kassel bị Anubis chặn → M (nội dung chỉ qua tóm tắt kết quả tìm kiếm).
- Botacin & Gomes 2025 [2] — Crossref chỉ siêu dữ liệu; ScienceDirect 403; arXiv không có → **định nghĩa phơi nhiễm gốc chưa được đối chiếu (theo Q1: đối chiếu khi mở được)**.
- Zhu et al. 2003; Guo & Greiner 2007; Moskovitch 2007 — chỉ qua Settles §3.4 (tường thuật).
- CD-AHAL (J. Comput. Sci. Cybern. 2026) — chỉ ảnh chụp tìm kiếm.
- Kho mã/giấy phép: INSOMNIA, NetGuard, STRAL, MOA, modAL, LightGBM — chưa mở.

## 7. Câu hỏi mới cho NCS
| # | Câu hỏi |
|---|---|
| Q19 | Đối chứng "mật độ (NetGuard [1])" chỉ là khâu chọn GMM (không sinh dữ liệu) có chấp nhận được không? |
| Q20 | Quy tắc thích nghi STRAL và [30] sang "b nhãn cố định mỗi ngày": dùng mẫu §5 (2)–(4) hay quy tắc khác? |
| Q21 | Bản NetGuard cần trích là v1/v2/v3? (kết quả tìm kiếm nêu v3; tôi chưa xác nhận bản mình đọc.) |
| Q22 | Có chấp nhận lời lẽ tính mới "chưa thấy trong phạm vi đã tìm" (GAP_NARROW) cho KT3, hay NCS muốn mở rộng tìm kiếm (chế độ extended / thêm cơ sở dữ liệu) trước G5? |

---

## 8. Quyết định của NCS cho G3 (04/11/2026) và phiên bản đã đọc

| # | Quyết định |
|---|---|
| Q19 | Đối chứng mật độ chỉ dùng khâu chọn GMM của NetGuard. Tên gọi: **"NetGuard-style density selection (no generation)"**, ghi rõ là bản rút gọn, không phải NetGuard đầy đủ |
| Q20 | Quy tắc chung cho STRAL và [30] (áp dụng ở **thực nghiệm chính**, không dùng trong probe P3): ngân sách tích lũy — phần b′ chưa tiêu chuyển sang ngày sau, mỗi ngày tiêu tối đa 3b′, tổng nhãn cả lượt chạy bằng các nhánh khác; ηb dành riêng vẫn lấy đủ mỗi ngày; báo cáo số nhãn tiêu từng ngày. STRAL: ADWIN (δ = 0,002, chờ 2.000 sự kiện) quyết định ngày được tiêu; chọn lai (gần ngưỡng + điểm cao). [30]: `RandVarUncertainty`, tỷ lệ ngân sách = b′/|U_t|, duyệt theo thứ tự đến, dừng khi đủ b′. Không dùng phương án "chỉ tiêu vào ngày kích hoạt" vì STRAL sẽ dùng ít nhãn hơn |
| Q21 | Trích đúng phiên bản đã đọc (số phiên bản và ngày in ở lề trang 1 của PDF arXiv) |
| Q22 | Chấp nhận "chưa thấy trong phạm vi đã tìm" (GAP_NARROW). Tìm kiếm chế độ extended làm sau, trước khi viết bất kỳ tuyên bố đóng góp nào; không cần trước G5 |

**Phiên bản tôi đã đọc (lề trang 1 của PDF):** NetGuard (Gupta et al.) **arXiv:2503.03022v3, 14 Aug 2025**; STRAL **arXiv:2605.22324v2, 18 Oct 2026**; Tab-AICL **arXiv:2603.27385v1, 28 Mar 2026**; Castellani et al. **arXiv:2204.06822v2, 12 Sep 2022**; Cacciarelli & Kulahci **arXiv:2302.08893v4, 29 Nov 2023**. Danh mục tham khảo của đề cương: [1] ghi "arXiv:2503.03022, 2025" (không nêu phiên bản) — không mâu thuẫn, nhưng phiên bản đã đọc là v3 và cần ghi trong bài; [4] ghi "arXiv:2605.22324, 2026" — khớp v2 (tác giả nêu v2 là bản đổi tên từ PACT v1, kết quả hai bản không so sánh trực tiếp). Câu hỏi Q21 cũ ("v1/v2/v3?") đóng.
