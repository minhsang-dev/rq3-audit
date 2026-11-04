# 00 — SOURCE MANIFEST (G0)

- **STATUS:** G0 DRAFT — chờ NCS duyệt. Chưa làm G1–G5.
- **SOURCE ANCHORS:** `outline_v14_3_RQ3_RQ4_verbatim.txt` (dòng 1–82); `RQ3_CLOUD_PAPER_AUDIT_TASK_v1.md` (dòng 1–80).
- **ASSUMPTIONS:** (1) Hai tệp trong repo là bản sao nguyên trạng của hai tệp NCS tải lên (sha256 khớp, xem dưới). (2) "Đã đọc" chỉ nghĩa là nội dung tệp đã được mở trong phiên này; tài liệu chỉ được nhắc tên thì không tính.
- **OPEN QUESTIONS:** xem mục 3 (danh sách thiếu) và mục 4.
- **DECISION:** Không có quyết định khoa học nào ở G0. Mọi kết luận phụ thuộc nguồn thiếu bị **HOLD** (mục 3).

## 1. Kiểm kê tài liệu thực sự đã đọc

| # | Tài liệu | Có trong repo/phiên? | Đã đọc? | Ghi chú | sha256 |
|---|---|---|---|---|---|
| 1 | `RQ3_CLOUD_PAPER_AUDIT_TASK_v1.md` (hồ sơ giao việc, 80 dòng) | CÓ | ĐÃ ĐỌC toàn bộ | Là chỉ thị, không phải nguồn khoa học | `be119c8f…dcab4` |
| 2 | `outline_v14_3_RQ3_RQ4_verbatim.txt` (trích đề cương, 82 dòng) | CÓ | ĐÃ ĐỌC toàn bộ | **Nguồn thẩm quyền duy nhất** hiện có. Là bản trích, không phải toàn đề cương | `abb52780…56d6bc0` |
| 3 | `outline_v14_3_references.txt` | KHÔNG | — | SOURCE MISSING | — |
| 4 | `REVIEW_SKELETON.md` | KHÔNG | — | SOURCE MISSING | — |
| 5 | `REVIEW_REFS.bib` | KHÔNG | — | SOURCE MISSING | — |
| 6 | `REVIEW_REFS_STATUS.csv` | KHÔNG | — | SOURCE MISSING | — |
| 7 | `RQ2_DECISION_LOG.md` | KHÔNG | — | SOURCE MISSING | — |
| 8 | Báo cáo nhóm RQ3 khác (ActiveLab × FS-FI v0.1/v0.2) | KHÔNG | — | Tùy chọn ("nếu có"); không đính kèm → không đối chiếu, không trộn | — |
| 9 | `README.md` của repo | CÓ | ĐÃ ĐỌC | Chỉ chứa tiêu đề `# rq3-audit`; không có nội dung khoa học | — |

Kiểm tra thêm: repo chỉ có 1 commit (`375d903 Initial commit`), không có tệp nào khác.

## 2. Phần đề cương thực sự có trong tệp #2 (và phần bị cắt)

Có (nguyên văn): RQ2/H2 (dòng 2–4); RQ3, H3 (8–10); RQ4, H4a, H4b (14–18); đoạn "Ba câu hỏi RQ2–RQ4 không độc lập… lọc → chọn → nạp" (20); công thức (2-2) và câu giải thích (21–23, **bắt đầu giữa Định nghĩa 2, không có đầu**); Định nghĩa 3 (25); Định nghĩa 4 (27); Định nghĩa 5 (29); Định nghĩa 6 + công thức (2-3) + đoạn "Ngân sách nhãn cho V_t và D_cal" (31–37); Nội dung 1 (43–52); Nội dung 3 gồm (2-6) (54–64); Nội dung 4 gồm (2-7), (2-8) (66–80).

**Không có / bị cắt trong tệp:**
- Định nghĩa 1 và phần đầu Định nghĩa 2 (chỉ còn đuôi (2-2)). Không biết định nghĩa "ngữ cảnh C", "chính sách π", k(B) đầy đủ.
- **Nội dung 2** (không có trong tệp; cũng không rõ "mục 2.1" được Nội dung 3 viện dẫn là mục nào).
- **Nội dung 5** (chỉ có tiêu đề "Nội dung 5 – Đánh giá kết hợp", dòng 82, thân rỗng) — mà dòng 20 và hồ sơ giao việc dựa vào để quy định chạy chung RQ3+RQ4.
- Mục 3.1 (Bộ đo tài nguyên, thủ tục DoP) được viện dẫn nhưng không có trong tệp.
- Mục tiêu 1/RQ1/H1a/H1b (H1a được Nội dung 3 viện dẫn: "để kiểm chứng H1a").
- Danh mục tài liệu tham khảo: mọi trích dẫn `[1] [2] [3] [4] [30] [31] [32] [33] [47] [49]` chỉ là số, **không phân giải được** tên công trình/URL.

## 3. Danh sách thiếu và hệ quả (HOLD)

| Thiếu | Hệ quả — kết luận bị HOLD |
|---|---|
| `outline_v14_3_references.txt` + `REVIEW_REFS.*` | Không xác minh được [1] NetGuard, [2] (nguồn của chỉ số phơi nhiễm), [3] INSOMNIA, [4] STRAL, [30], [31] (EER). G3: trạng thái các đối chứng chưa thể là VERIFIED. G1 (chỉ số phơi nhiễm): HOLD đối chiếu với [2]. |
| `RQ2_DECISION_LOG.md` | Định nghĩa HB2 (CBRS-family + ngăn benign khó, "H chỉ nhận benign", "BASE"), cơ chế nạp, k. G2-A4 (tương tác với HB2) và G1 timeline nạp: HOLD. Hồ sơ giao việc chỉ mô tả HB2 bằng một câu, không đủ để phân tích. Lưu ý: H2 trong đề cương vẫn viết "chính sách ba ngăn" trong khi RQ2 hiện dùng HB2 (ThreeBin đã CLOSED_AT_DEV) — lệch giữa đề cương và trạng thái RQ2 (chỉ ghi nhận, không xử lý ở RQ3). |
| Số đo "Bài 1" (4,36 s + 5,25 s/1.000 hàng, k = 2.000) | Chỉ có con số trong hồ sơ giao việc, không có báo cáo gốc (phần cứng, phiên bản TabFM, độ lệch). G2-A2: ngoại suy TabFM phải ghi "hệ số do NCS cung cấp, chưa kiểm". |
| Nội dung 2, 5, Định nghĩa 1–2 đầy đủ, mục 3.1 | G1 (timeline lọc→chọn→nạp, Nội dung 5), G2-A4: HOLD các phần phụ thuộc. |
| Quyền truy cập nguồn bên ngoài (bài báo EER, INSOMNIA, NetGuard, STRAL, Tab-AICL…) | Chưa thử; sẽ làm ở G3 bằng WebSearch/WebFetch nếu NCS duyệt và mạng cho phép. Hiện **không** có công trình nào "đã mở". `RQ3_REFS.bib` sẽ chỉ chứa nguồn đã mở thật. |

## 4. Câu hỏi cho NCS (để duyệt G0)

1. Có đính kèm bổ sung được các tệp #3–#7 (và #8 nếu muốn đối chiếu) trước khi sang G1 không? Nếu không, G1–G2 chạy với các HOLD ở mục 3 và ghi rõ trong từng tệp.
2. Nội dung 2 và Nội dung 5 có thể đưa thêm bản trích nguyên văn không (đặc biệt phần chạy chung và quy định "lọc → chọn → nạp")?
3. Có cho phép dùng web (tìm/đọc bài báo) ở G3 không?
