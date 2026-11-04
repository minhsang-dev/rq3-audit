# 00 — SOURCE MANIFEST (G0)

- **STATUS:** G0 DRAFT v2 — chờ NCS duyệt. Chưa làm G1–G5.
- **SOURCE ANCHORS:** `sources/outline_v14_3_RQ3_RQ4_verbatim.txt` (dòng 1–82); `sources/RQ3_CLOUD_PAPER_AUDIT_TASK_v1.md` (dòng 1–80); các tệp khác trong `sources/`.
- **ASSUMPTIONS:** (1) Hai tệp trong repo là bản sao nguyên trạng của hai tệp NCS tải lên (sha256 khớp, xem dưới). (2) "Đã đọc" chỉ nghĩa là nội dung tệp đã được mở trong phiên này; tài liệu chỉ được nhắc tên thì không tính.
- **OPEN QUESTIONS:** xem mục 3 (danh sách thiếu) và mục 4.
- **DECISION:** Không có quyết định khoa học nào ở G0. Mọi kết luận phụ thuộc nguồn thiếu bị **HOLD** (mục 3).

## 1. Kiểm kê tài liệu thực sự đã đọc (cập nhật lần 2, sau khi NCS đính kèm thêm)

Các tệp nguồn nay nằm trong `sources/`. "Mức đọc" nói rõ phần đã mở thật.

| # | Tài liệu | Mức đọc | Ghi chú | sha256 (12 ký tự đầu) |
|---|---|---|---|---|
| 1 | `RQ3_CLOUD_PAPER_AUDIT_TASK_v1.md` (80 dòng) | ĐỌC TOÀN BỘ | Chỉ thị, không phải nguồn khoa học | be119c8f30fc |
| 2 | `outline_v14_3_RQ3_RQ4_verbatim.txt` (82 dòng) | ĐỌC TOÀN BỘ | **Nguồn thẩm quyền.** Bản đính kèm lần 2 (`1d6a2614-…`) giống hệt lần 1 (cùng sha256) | abb527808d5a |
| 3 | `RQ2_DECISION_LOG.md` (v2, 144 dòng) | ĐỌC TOÀN BỘ | Cập nhật tới mục 10 (04/11/2026); có HB2, CIDDS-001, novelty audit | a40950669455 |
| 4 | `REVIEW_SKELETON.md` (82 dòng) | ĐỌC TOÀN BỘ | Mục 4 (RQ3) tự ghi "cần được mở rộng bởi nhóm RQ3"; bảng KT3 là ánh xạ khóa↔số tham khảo | 9900c45044ac |
| 5 | `REVIEW_REFS_STATUS.csv` (145 dòng) | ĐỌC TOÀN BỘ | Trạng thái xác minh từng khóa | 32872959aa26 |
| 6 | `REVIEW_REFS.bib` (1803 dòng, 167 mục) | ĐỌC MỘT PHẦN | Đã mở các mục RQ3: zliobaite2014active, cacciarelli2024, settles2010, roy2001eer, treerath2026tabaicl, gupta2025netguard, ndichu2026stral, andresini2021, ghi chú Outline-ref. Chưa duyệt hết 167 mục | 337d5fe6c13b |
| 7 | `bai1_manuscript_v4_2_clean.md` (707 dòng, đính kèm lần 3, chưa được yêu cầu trong hồ sơ) | ĐỌC MỘT PHẦN | Mới tìm có chủ đích: số đo thời gian TabFM (dòng ~205–212), Bảng 11 (dòng 481), vị trí tham số b/η/k/τ. Chưa đọc toàn văn; sẽ đọc phần giao thức khi vào G1 | e25f39ee8cd3 |
| 8 | `outline_v14_3_references.txt` | **KHÔNG CÓ** | SOURCE MISSING | — |
| 9 | Báo cáo nhóm RQ3 khác (ActiveLab × FS-FI) | KHÔNG CÓ | Tùy chọn; không đối chiếu, không trộn | — |
| 10 | `README.md` repo | ĐỌC | Chỉ tiêu đề | — |

Các tài liệu nhắc tên trong `REVIEW_SKELETON.md` mà **không đính kèm** (không coi là đã đọc): `NOVELTY_AUDIT_2.md`, `PRIOR_ART_1.md`, `RQ4_GAP.md`, `RQ4_PRIOR_ART.md`, `COVERAGE.md`, `REF_CHECK.csv`, `outline_v14_3_overview_KT.txt`, `rq2_REFS_v2_1.bib`.

## 2. Phần đề cương thực sự có trong tệp #2 (và phần bị cắt)

Có (nguyên văn): RQ2/H2 (dòng 2–4); RQ3, H3 (8–10); RQ4, H4a, H4b (14–18); đoạn "Ba câu hỏi RQ2–RQ4 không độc lập… lọc → chọn → nạp" (20); công thức (2-2) và câu giải thích (21–23, **bắt đầu giữa Định nghĩa 2, không có đầu**); Định nghĩa 3 (25); Định nghĩa 4 (27); Định nghĩa 5 (29); Định nghĩa 6 + công thức (2-3) + đoạn "Ngân sách nhãn cho V_t và D_cal" (31–37); Nội dung 1 (43–52); Nội dung 3 gồm (2-6) (54–64); Nội dung 4 gồm (2-7), (2-8) (66–80).

**Không có / bị cắt trong tệp:**
- Định nghĩa 1 và phần đầu Định nghĩa 2 (chỉ còn đuôi (2-2)). Không biết định nghĩa "ngữ cảnh C", "chính sách π", k(B) đầy đủ.
- **Nội dung 2** (không có trong tệp; cũng không rõ "mục 2.1" được Nội dung 3 viện dẫn là mục nào).
- **Nội dung 5** (chỉ có tiêu đề "Nội dung 5 – Đánh giá kết hợp", dòng 82, thân rỗng) — mà dòng 20 và hồ sơ giao việc dựa vào để quy định chạy chung RQ3+RQ4.
- Mục 3.1 (Bộ đo tài nguyên, thủ tục DoP) được viện dẫn nhưng không có trong tệp.
- Mục tiêu 1/RQ1/H1a/H1b (H1a được Nội dung 3 viện dẫn: "để kiểm chứng H1a").
- Danh mục tài liệu tham khảo: mọi trích dẫn `[1] [2] [3] [4] [30] [31] [32] [33] [47] [49]` chỉ là số, **không phân giải được** tên công trình/URL.

## 3. Danh sách thiếu và hệ quả (HOLD) — sau cập nhật lần 2

| Thiếu | Hệ quả |
|---|---|
| `outline_v14_3_references.txt` | Số tham khảo [2] (nguồn chỉ số phơi nhiễm) **không phân giải được**: không có khóa nào trong `.bib` ghi "Outline ref [2]". Chỉ số phơi nhiễm ở G1: HOLD đối chiếu nguồn. Ánh xạ [1] [3] [4] [30] [31] chỉ có gián tiếp từ bảng KT3 của `REVIEW_SKELETON.md` (xem `01_REQUIREMENT_TRACE.md` mục E); chưa kiểm với danh mục gốc của đề cương → CHƯA XÁC MINH. |
| Định nghĩa HB2 ở mức mã (cách H nhận dòng, BASE) | `RQ2_DECISION_LOG.md` §8 cho đủ mô tả mức quyết định (CBRS_FAMILY + H = 200 dòng benign, xếp theo điểm tấn công của mô hình, top-k; k = 2.000 tổng) nhưng không cho cơ chế nạp từng ngày. A4 viết được ở mức giấy với giả định ghi rõ; chi tiết thời điểm nạp: HOLD. |
| Nội dung 2, Nội dung 5 (thân), mục 3.1, Định nghĩa 1–2, H1a | Vẫn thiếu. Phần "chạy chung" RQ3+RQ4 bị HOLD. |
| NOVELTY_AUDIT_2 / PRIOR_ART_1 | `treerath2026tabaicl` chỉ có bib + ghi chú "methods read per NOVELTY_AUDIT_2"; nội dung bài chưa được mở trong phiên này. G3 phải mở lại (cần web). |
| Mạng/web | Chưa thử; NCS chưa trả lời có cho phép dùng web ở G3 không. |

**Đã giải quyết so với lần 1:** `RQ2_DECISION_LOG.md`, `REVIEW_*` (3 tệp), bản thảo Bài 1 (một phần). Hệ số TabFM trong hồ sơ nay có nguồn: bản thảo Bài 1 ghi 9,6 s/1.000 hàng và 56,8 s/10.000 hàng (3 ngày pilot), hồi quy tuyến tính cho 4,36 s + 5,25 s/1.000 hàng/ngày — khớp với hồ sơ giao việc (kiểm số học: 4,36+5,25 = 9,61; 4,36+52,5 = 56,86). Bài 1 cũng đo thời gian chấm lại sau khi bỏ một dòng ngữ cảnh (k = 2.000, 1.000 hàng truy vấn): 9,61 s. Bảng 11 báo giá trị khác: 5,84 s GPU/1.000 hàng đánh giá (median, L4, fit+predict, k = 2.000, lần chạy chính). Hai con số chênh nhau; G2-A2 phải nêu cả hai. Vẫn là số đo của NCS, chưa được kiểm độc lập.

## 4. Câu hỏi cho NCS (để duyệt G0)

1. Đính kèm `outline_v14_3_references.txt` (đặc biệt mục [2], và xác nhận [1] [3] [4] [30] [31]) được không? Nếu không, G1 để chỉ số phơi nhiễm ở trạng thái "nguồn [2] chưa mở".
2. Ở G3 tôi có được dùng web để mở bài báo (EER/Roy-McCallum đã có bib; Tab-AICL, INSOMNIA, NetGuard, STRAL, Zliobaite 2014) không?
3. Bản thảo Bài 1 đính kèm lần 3 có phải để dùng làm nguồn giao thức/chi phí cho G1–G2 không? (Hồ sơ gốc không liệt kê tệp này; tôi sẽ dùng nếu bạn xác nhận.)
4. Duyệt G0 để sang G1?
