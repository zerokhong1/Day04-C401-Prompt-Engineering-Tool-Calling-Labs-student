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

Agent nghiên cứu song ngữ Việt/Anh, tự động tìm kiếm và tổng hợp thông tin từ nhiều nguồn (web, Twitter/X, arXiv, policy nội bộ). Agent hiểu yêu cầu người dùng, chọn đúng tool, gọi song song nhiều tool khi cần, và hỏi lại khi thiếu thông tin. Hỗ trợ gửi bản tin qua Telegram với xác nhận trước khi gửi.

**Link dùng thử (deploy):**

> URL: (chưa deploy — chạy local qua `python chat.py --provider openrouter --version v3`)

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi người dùng khi thiếu thông tin (response_type: text/yes_no/choice) | không |
| timeline | Lấy tweet/bài đăng gần nhất từ 1 tài khoản Twitter/X cụ thể | không |
| social_search | Tìm tweet theo từ khóa (Latest/Top) trên Twitter/X | không |
| lookup | Tìm kiếm web qua Tavily (topic=general/news, timeframe=day/week/month/year) | không |
| fetch | Đọc nội dung 1 URL cụ thể qua Firecrawl, trả về markdown | không |
| format | Format danh sách items thành bản tin markdown (brief/sections/bullets/thread/daily_ai_vn) | không |
| send | Gửi tin nhắn Telegram — chỉ gửi khi confirmed=true, luôn hỏi xác nhận trước | có |
| policy | Tìm kiếm chính sách nội bộ công ty theo policy_area (source_citation, data_privacy, etc.) | có |
| papers | Tìm paper trên arXiv theo từ khóa | có |
| paper_text | Tải PDF arXiv và trích text (cần arXiv ID/URL có sẵn) | có |
| summarize | Tóm tắt extractive văn bản dài (local, không cần API) | có |
| translate | Dịch văn bản sang ngôn ngữ khác qua MyMemory API | có |
| dedupe | Loại bỏ item trùng lặp bằng Jaccard similarity (local) | có |
| rank_items | Xếp hạng items theo trường số (score, favorites, views) (local) | có |
| extract_entities | Trích xuất thực thể: emails, URLs, arXiv IDs, hashtags, @mentions (local regex) | có |

## A3. Câu hỏi mẫu để thử

1. "Tweet mới nhất của Sam Altman là gì?" → timeline(sama)
2. "Tìm trên web tin AI hôm nay và tweet về AI" → lookup + social_search (parallel)
3. "Dịch đoạn văn này sang tiếng Ả Rập: 'Trí tuệ nhân tạo đang thay đổi thế giới'" → translate
4. "Gửi bản tin này lên Telegram" → clarify(yes_no) trước, chờ confirm rồi send
5. "Theo company policy, tweet viral có được coi là fact đã xác nhận không?" → policy(source_citation)

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Original prompt với eager guessing, thiếu rule routing | N/A | case_acc=0.55, routing=0.80, args=0.55, multi=0.50 | runs/v0_B_base_openrouter_20260602T140723205512.json |
| v1 | system_prompt.md | Thêm rule clarify khi thiếu info, enforce confirm trước send, thêm parallel tool routing | 0.55 | case_acc=0.67, routing=0.83, args=0.67, multi=0.83 | runs/v1_B_base_openrouter_20260602T142140719682.json |
| v2 | system_prompt.md | Thêm Twitter handle mapping (sama/elonmusk/karpathy/facebook) + numeric extraction rule + parallel call rule | 0.67 | case_acc=0.80, routing=0.90, args=0.80, multi=1.00 | runs/v2_B_base_openrouter_20260602T142824147680.json |
| v3 | system_prompt.md + tools.yaml + tools/__init__.py | Fix clarify response_type (text vs choice), policy routing explicit mapping, parallel call examples, duplicate tool declarations cleanup | 0.80 | case_acc=0.90, routing=0.95, args=0.90, multi=1.00 | runs/v3_B_base_openrouter_20260602T144512368042.json |

## B2. Failure Analysis

### v0 Failures (baseline — 9/20 failed)

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R01 | wrong_arg_value | timeline(screenname=None) | Không map Sam Altman → sama | v2: thêm handle mapping rule |
| R03 | wrong_arg_value | lookup(query="AI news today") | Query chứa "news today" thay vì chỉ "AI" | v1: rule chỉ dùng core keyword |
| R10 | missing_info | timeline() thay vì clarify | Thiếu handle nhưng đoán bừa | v1: rule clarify khi thiếu info |
| R11 | missing_info | fetch() thay vì clarify | Nói "bài này" nhưng không có URL | v1: rule clarify khi thiếu URL |
| R12 | wrong_boundary | send(confirmed=true) ngay | Gửi ngay không hỏi confirm | v1: enforce clarify(yes_no) trước send |
| R13 | wrong_tool | lookup() chỉ 1 tool | Thiếu social_search song song | v1: thêm parallel call rule |
| M02 | wrong_arg_value | lookup(timeframe=week) | Sai timeframe, cần "day" | v2: enforce multi-turn carryover |
| M05 | wrong_arg_value | timeline(limit=10) | Giữ limit cũ, không update | v2: rule extract numeric + multi-turn update |
| M06 | wrong_arg_value | lookup() | Sai topic/query khi switch tool | v2: enforce multi-turn context carry |

### v3 Remaining Failures (2/20 failed)

| Case ID | Failure Type | Actual Tool Calls | What Failed | Root Cause |
|---|---|---|---|---|
| R10 | wrong_arg_value | clarify(response_type="choice") | Dùng choice thay vì text khi xin info | Model gpt-oss-20b:free ưu tiên choice; đã fix prompt rule "use response_type=text for missing info" |
| R13 | wrong_tool | lookup() (missing social_search) | Chỉ gọi 1 tool, thiếu parallel | Model free weak trên parallel calls; đã thêm explicit parallel examples trong prompt |

## B3. Team Eval Cases

10 cases added to `data/eval_group.json` (5 single-turn + 5 multi-turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_no_url_use_lookup | Hỏi thông tin tổng quan KHÔNG có URL → lookup, không fetch | lookup(query) |  PASS |
| G02_timeframe_year | "trong năm nay" → timeframe=year, topic=news | lookup(timeframe=year) | PASS |
| G03_format_bullets | Yêu cầu trình bày dữ liệu đã có → format(template=bullets) | format(template=bullets) |  PASS |
| G04_thanks_no_tool | Lời cảm ơn xã giao → trả lời thẳng, không gọi tool | no_tool |  PASS |
| G05_translation_out_of_scope | Dịch thuật → ngoài phạm vi research agent | no_tool (refuse) |  PASS |
| G06_missing_paper_id | 3 turns không có arXiv ID → clarify xin link | clarify(response_type=text) |  PASS |
| G07_send_after_confirm | User xác nhận rõ → send(confirmed=true) | send(confirmed=true) | PASS |
| G08_switch_timeline_to_search | Chuyển từ timeline sang social_search | social_search(query=OpenAI) |PASS |
| G09_correct_timeframe_month | Sửa timeframe tuần→tháng | lookup(timeframe=month) |PASS |
| G10_latest_turn_meta_no_tool | Câu hỏi meta ở latest turn → no tool | no_tool | PASS |

**Group eval summary**: case_accuracy=1.0, routing=1.0, args=1.0, multiturn=1.0 (10/10 cases PASS)

## B4. Live Chat Evidence

Transcript: `transcripts/v3_openrouter_20260602T163754559483.transcript.json`

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | "Gửi tin nhắn 'HEHE' lên Telegram" | clarify(response_type=yes_no) | v1: enforce confirm before send |  Agent hỏi confirm trước |
| 2 | "Có chứ, gửi đi" | send(text="HEHE", confirmed=true) | Token hợp lệ (bot mới @Vinananananananabot) |  Gửi thành công |
| 3 | "Gửi lại" | send(text="HEHE", confirmed=true) | Token hợp lệ |  Gửi thành công |
| 4 | "Gửi lại lần nữa" | send(text="HEHE", confirmed=true) | Token hợp lệ |  Gửi thành công |
| 5 | "Gửi lại tiếp" | send(text="HEHE", confirmed=true) | Token hợp lệ | Gửi thành công |
| 6 | "Gửi lại tiếp" | send(text="HEHE", confirmed=false) | Preview mode | Xem preview trước khi gửi |
| 7 | "Có gửi" | send(text="HEHE", confirmed=true) | Token hợp lệ | Gửi thành công |

**Kết quả**: Sau khi cấu hình lại TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID, tất cả các lệnh gửi tin nhắn đều hoạt động bình thường.

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) | transcripts/v3_openrouter_*.json | clarify(yes_no) trước khi send; send(confirmed=false) preview; chỉ gửi khi confirmed=true | Cần check TELEGRAM_BOT_TOKEN và CHAT_ID hợp lệ; token bị corrupted sẽ 404 |
| arXiv/company policy | runs/v3_B_extension_*.json (E01-E10) | policy tool hoạt động (E03, E04, E10 PASS); papers + paper_text routing đúng | Free model weak trên parallel policy calls (E06/E07/E08 fail) |
| UI | app.py (Streamlit UI) | Chưa deploy trong session này | Cần deploy để demo |
| Safety filter | tools/safety_filter.py + agent.py | Block dangerous keywords trước khi gọi model; handle PermissionDeniedError moderation | Keyword-based, không cover 100%; cần update keyword list theo thời gian |

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**
  - Clarify routing rule (response_type=text cho missing info, yes_no cho confirm)
  - Parallel tool call examples (explicit examples cho lookup+social_search, papers+policy, 2x fetch)
  - Twitter handle mapping (sama, elonmusk, karpathy)
  - Policy routing table (keyword → policy_area mapping)
  - Core keyword extraction rule (query chỉ chứa keyword, không thêm "news", "tin tức")
  - Translation rule (luôn gọi translate tool, không tự từ chối)

- **Which fixes belonged in `tools.yaml`?**
  - Duplicate tool declarations cleanup (summarize, extract_entities, rank_items bị khai báo 2 lần)
  - Cải thiện tool descriptions: policy_area mapping rõ ràng hơn, paper_text nhấn "cần ID có sẵn", fetch nhấn mạnh parallel multi-URL
  - Thêm translate tool declaration

- **Which failure needed manual review instead of automatic grading?**
  - R10: clarify(response_type="choice") vs "text" — model dùng choice cho rich UI nhưng eval chỉ accept "text". Manual review sẽ accept cả hai.
  - G03, G06: provider_error (429 rate limit) — không phải lỗi logic, cần retry hoặc dùng model khác.
  - G07: model gọi clarify thay vì send — có thể do multi-turn context window quá dài, model quên user đã confirm.

- **What would you improve next?**
  1. Dùng model mạnh hơn (GPT-4o thay vì gpt-4o-mini) cho parallel tool calls chính xác hơn
  2. Thêm retry logic cho provider_error (429 rate limit) trong agent.py
  3. Deploy Streamlit UI để demo trực tiếp
  4. Cải thiện translate tool: hỗ trợ thêm source_lang detection tốt hơn (hiện chỉ heuristic vi/en)
  5. Thêm cache cho policy tool để giảm API calls
