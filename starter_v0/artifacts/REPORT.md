# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: 05 Zone 1
- Members: 
    Luu Cong Thai - 2A202600949
    Nguyen Duc Manh - 2A202600724
    Lê Hữu Đạt - 2A202600630
- Provider/model: OpenAI-4o-mini

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).



**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL: 

## A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline | Lấy các tweet/bài đăng gần đây nhất từ một tài khoản Twitter/X cụ thể. Dùng khi … | không |
| social_search | Tìm kiếm tweet/bài đăng trên Twitter/X theo từ khóa. Dùng khi cần tìm thảo luận … | không |
| lookup | Tìm kiếm thông tin trên web qua Tavily. Dùng cho tra cứu tin tức (topic=news) ho… | không |
| fetch | Đọc và trích xuất nội dung từ một URL cụ thể. Dùng khi user cung cấp URL/link tr… | không |
| format | Định dạng danh sách items đã thu thập thành bản tin markdown. KHÔNG tự tìm dữ li… | không |
| send  | Gửi tin nhắn qua Telegram Bot. ĐÂY LÀ ACTION TOOL — chỉ thực sự gửi khi confirme… | có |
| policy | Tìm trong chính sách nội bộ công ty. PHẢI dùng khi user hỏi: policy, quy định, c… | có |
| papers |  Tìm kiếm bài báo khoa học trên arXiv theo từ khóa. Trả về danh sách papers với t… | có |
| paper_text  | Tải và trích xuất nội dung text từ một bài báo arXiv (PDF → text). Dùng KHI CÓ S… | có |
| summarize | Tóm tắt văn bản dài bằng phương pháp extractive (chọn câu quan trọng nhất). Chạy… | có |
| translate | Dịch văn bản sang ngôn ngữ khác. Dùng khi user yêu cầu dịch nội dung hoặc kết qu… |  có |
| dedupe | Loại bỏ các item trùng lặp hoặc gần giống nhau trong danh sách kết quả.  | có |
| rank_item | Sắp xếp và xếp hạng danh sách items theo một trường số (score, favorites, views,… | có |
| extract_entities | Trích xuất thực thể có cấu trúc từ văn bản: emails, URLs, arXiv IDs, hashtags, @… | có |


## A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.Gửi thông tin paper cho telegram
2. Năm một lớn hơn ba năm không
3. Dịch bài báo sang tiếng Ả Rập

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

## B2. Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Bonus Evidence

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) |  |  |  |
| arXiv/company policy |  |  |  |
| UI |  |  |  |

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?
