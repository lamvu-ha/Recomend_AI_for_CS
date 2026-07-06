# Kế hoạch phân tích sự chuyển dịch kỹ năng của con người khi AI tác động

## 1. Mục tiêu phân tích

Mục tiêu là đo và giải thích sự dịch chuyển kỹ năng lao động dưới tác động của AI theo ba lớp:

1. **Kỹ năng/task dễ được AI hỗ trợ hoặc tự động hóa**: AI có năng lực làm task ở mức nào, đang được dùng thực tế ra sao, và hệ sinh thái công ty/paper có tập trung vào đó không.
2. **Kỹ năng/task con người muốn chuyển giao cho AI**: người lao động có muốn tự động hóa task đó không, vì lý do tiết kiệm thời gian, giảm lặp lại, giảm lỗi, giảm stress, mở rộng quy mô hay giảm độ khó.
3. **Kỹ năng/task vẫn cần con người giữ vai trò trung tâm**: task yêu cầu agency, kiểm soát, chuyên môn miền, giao tiếp, đồng cảm, đạo đức, xử lý tình huống động hoặc hành động vật lý.

Kết quả mong muốn là một bản đồ chuyển dịch kỹ năng: kỹ năng nào bị thay thế một phần, kỹ năng nào được khuếch đại bởi AI, kỹ năng nào tăng giá trị vì AI chưa thay được, và nhóm lao động/ngành nghề nào chịu tác động mạnh nhất.

Quan trọng: các câu hỏi như "task nào người lao động muốn AI làm thay" hay "task nào vẫn cần con người" không phải là insight cuối cùng. Chúng là biến trung gian để phát hiện các cơ chế sâu hơn: nơi nào AI tạo ra dịch chuyển thật, nơi nào chỉ tạo áp lực tâm lý, nơi nào kỹ năng không biến mất mà đổi vai trò từ thực thi sang kiểm định, điều phối và chịu trách nhiệm.

## 1.1. Trọng tâm insight mới

Thay vì chỉ xếp hạng task/kỹ năng theo mức tự động hóa, nghiên cứu nên hướng tới các insight mới sau:

1. **Skill Reconfiguration, không chỉ Skill Replacement**
   - Câu hỏi mới: AI làm kỹ năng biến mất, hay làm kỹ năng đổi hình thái?
   - Ví dụ: "Analyzing Data" có thể chuyển từ tự phân tích sang đặt câu hỏi, kiểm định output, phát hiện sai lệch và diễn giải cho người khác.

2. **Automation Desire-Capability Mismatch**
   - Câu hỏi mới: đâu là nơi người lao động muốn AI hỗ trợ nhưng công nghệ chưa đủ mạnh, và đâu là nơi AI mạnh nhưng con người không muốn giao?
   - Insight tiềm năng: rào cản adoption không nằm ở công nghệ mà ở niềm tin, agency, trách nhiệm hoặc ý nghĩa công việc.

3. **Human Agency Premium**
   - Câu hỏi mới: khi AI càng giỏi, kỹ năng con người nào lại tăng giá trị?
   - Insight tiềm năng: một số kỹ năng không bị giảm giá trị bởi AI, mà trở thành "premium layer" bao quanh AI: kiểm soát, đạo đức, giao tiếp, domain judgment, quality oversight.

4. **Hidden Complementarity**
   - Câu hỏi mới: task có vẻ dễ tự động hóa nhưng thật ra cần con người ở bước cuối nào?
   - Insight tiềm năng: AI không thay cả task, mà thay các subtask có cấu trúc; phần còn lại của con người trở nên tinh hơn, ít lặp lại hơn nhưng chịu trách nhiệm cao hơn.

5. **Skill Polarization Within Occupations**
   - Câu hỏi mới: trong cùng một nghề, kỹ năng nào bị kéo xuống và kỹ năng nào được đẩy lên?
   - Insight tiềm năng: tác động của AI không đồng nhất theo nghề. Một occupation có thể vừa mất nhu cầu ở kỹ năng xử lý thông tin lặp lại, vừa tăng nhu cầu ở kỹ năng giao tiếp, ra quyết định và giám sát.

6. **AI Adoption Inequality**
   - Câu hỏi mới: ai có khả năng chuyển dịch sang kỹ năng bổ trợ AI, và ai bị kẹt ở nhóm task dễ tự động hóa?
   - Insight tiềm năng: LLM familiarity, education, experience, income hoặc ngành nghề có thể tạo ra khoảng cách mới giữa nhóm "AI-augmented workers" và nhóm "AI-exposed workers".

7. **Innovation-Use Gap**
   - Câu hỏi mới: nơi nào có nhiều paper/company nhưng usage thực tế thấp, hoặc usage cao nhưng hệ sinh thái startup/paper chưa theo kịp?
   - Insight tiềm năng: có thể phát hiện các vùng "overhyped", "under-commercialized", hoặc "quietly adopted".

8. **Reskilling Priority by Transition Path**
   - Câu hỏi mới: mỗi nhóm kỹ năng nên được đào tạo lại theo hướng nào?
   - Không chỉ nói "học AI", mà phân loại transition path:
     - từ thực thi sang giám sát,
     - từ tìm kiếm thông tin sang tổng hợp/đánh giá,
     - từ sản xuất nội dung sang kiểm định chất lượng,
     - từ thao tác quy trình sang xử lý ngoại lệ,
     - từ chuyên môn đơn lẻ sang phối hợp người-AI.

## 2. Dữ liệu hiện có

### 2.1. Bảng chính

| File | Quy mô | Vai trò trong phân tích |
|---|---:|---|
| `task_statement_with_metadata.csv` | 2,131 task, 14 cột | Bảng xương sống: task, nghề O*NET, loại task, tần suất, tầm quan trọng, mức liên quan, wage/employment, O*NET work activity/skill. |
| `domain_worker_desires.csv` | 5,731 đánh giá, 31 cột | Góc nhìn người lao động: mong muốn tự động hóa, core skill, job security, enjoyment, human agency và lý do. |
| `domain_worker_metadata.csv` | 1,500 người, 26 cột | Hồ sơ người trả lời: nghề, tuổi, giới, race, income, education, experience, thái độ với AI, mức quen thuộc và kiểu dùng LLM. |
| `expert_rated_technological_capability.csv` | 2,057 đánh giá, 11 cột | Góc nhìn chuyên gia: năng lực tự động hóa, yêu cầu vật lý, bất định, chuyên môn miền, giao tiếp, human agency. |

### 2.2. Bảng bổ trợ

| File | Vai trò |
|---|---|
| `external_data/usage_from_anthropic.csv` | Tín hiệu sử dụng AI thực tế theo task. |
| `external_data/paper_to_workflow_mapping_aggregated.csv` | Cường độ nghiên cứu AI liên quan đến từng workflow/task. |
| `external_data/company_to_workflow_aggregation.csv` | Cường độ thương mại hóa/startup liên quan đến từng workflow/task. |
| `external_data/M2024_bls_wage_data.csv` | Wage và employment theo occupation ở cấp BLS 2024. |
| `external_data/bls_age.csv`, `external_data/bls_race_gender.csv` | Cấu trúc nhân khẩu học nghề nghiệp. |
| `external_data/onet_data/tasks_to_dwas.csv` | Nối task sang Detailed Work Activities, độ phủ 98.6% trên task chính. |
| `external_data/onet_data/dwa_reference.csv` | Từ điển DWA/IWA/GWA để gom nhóm kỹ năng. |
| `external_data/onet_data/onet_sector/*.csv` | Ánh xạ occupation sang sector/ngành lớn. |

## 3. Chất lượng và khả năng nối dữ liệu

Các điểm đã kiểm tra nhanh:

- `domain_worker_desires.csv` phủ 844/2,131 task chính, khoảng 39.6%.
- `expert_rated_technological_capability.csv` phủ 846/2,131 task chính, khoảng 39.7%.
- `tasks_to_dwas.csv` phủ 2,101/2,131 task chính, khoảng 98.6%.
- `paper_to_workflow_mapping_aggregated.csv` phủ khoảng 99.3% task chính theo cặp task + occupation.
- `company_to_workflow_aggregation.csv` phủ khoảng 94.6% task chính theo cặp task + occupation.
- `usage_from_anthropic.csv` phủ khoảng 37.4% task chính theo tên task.
- 100% bản ghi trong `domain_worker_desires.csv` có `User ID` nối được sang `domain_worker_metadata.csv`.

Hàm ý: phân tích kỹ năng nên dùng `task_statement_with_metadata.csv` làm bảng nền, sau đó nối thêm expert rating, worker rating, DWA, paper/company/usage signal và BLS. Với các chỉ số chuyên gia/người lao động, cần ghi rõ đây là subset khoảng 40% task chính, không phải toàn bộ task.

## 4. Câu hỏi nghiên cứu chính

Các câu hỏi dưới đây nên được dùng để tạo insight mới, không chỉ để mô tả bảng xếp hạng.

1. **AI đang tái cấu trúc kỹ năng như thế nào?**
   - Kỹ năng nào chuyển từ "doing" sang "checking", "directing", "explaining", "coordinating" hoặc "owning accountability"?

2. **Ở đâu có nghịch lý giữa năng lực AI và mong muốn của người lao động?**
   - AI làm được nhưng người lao động không muốn giao.
   - Người lao động muốn giao nhưng AI chưa đủ năng lực.
   - Cả hai đều cao nhưng vẫn cần human agency.

3. **Kỹ năng nào trở thành "human premium skills" trong môi trường có AI?**
   - Các kỹ năng liên quan đến domain judgment, empathy, ethics, communication, dynamic context, quality oversight.

4. **Trong cùng một nghề, kỹ năng bị thay thế và kỹ năng được nâng cấp có đi cùng nhau không?**
   - Tìm cấu trúc phân cực nội bộ của occupation thay vì gắn nhãn cả nghề là "dễ bị thay thế".

5. **Nhóm lao động nào có lợi thế chuyển sang kỹ năng bổ trợ AI?**
   - So sánh theo LLM familiarity, LLM use in work, education, experience, age, income, occupation.

6. **Tín hiệu nghiên cứu, startup và usage thực tế có đang chỉ cùng một hướng không?**
   - Nếu không, các vùng lệch này chính là insight: hype, lag, adoption friction hoặc market gap.

7. **Reskilling nên đi theo đường chuyển dịch nào cho từng nhóm kỹ năng/nghề?**
   - Tạo transition path cụ thể thay vì khuyến nghị chung chung.

## 5. Thiết kế chỉ số phân tích

### 5.1. Chỉ số ở cấp task

Tạo bảng `task_ai_skill_shift` ở cấp `Task ID` hoặc `Task + Occupation`, gồm:

- `ai_capability_score`: trung bình `Automation Capacity Rating`.
- `worker_desire_score`: trung bình `Automation Desire Rating`.
- `human_agency_score`: trung bình hoặc kết hợp worker + expert `Human Agency Scale Rating`.
- `core_skill_score`: trung bình `Core Skill Rating`.
- `job_security_concern`: trung bình `Job Security Rating`.
- `enjoyment_score`: trung bình `Enjoyment Rating`.
- `physical_requirement`, `uncertainty_requirement`, `domain_expertise_requirement`, `interpersonal_requirement`.
- `ai_usage_score`: `pct` từ Anthropic usage, chuẩn hóa log hoặc percentile.
- `innovation_signal`: kết hợp `paper_count` và `company_count`, nên dùng `log1p()` rồi chuẩn hóa.
- `labor_market_weight`: employment hoặc wage/employment từ BLS/O*NET metadata.

### 5.2. Chỉ số chuyển dịch kỹ năng

Đề xuất bốn chỉ số chính:

1. **Automation Exposure Index**
   - Đo mức task/kỹ năng có thể bị AI đảm nhiệm.
   - Thành phần: expert capability, AI usage, paper/company signal.

2. **Worker Pull Index**
   - Đo lực kéo từ phía người lao động muốn AI hỗ trợ.
   - Thành phần: automation desire, lý do repetitive/free time/stress/difficulty/scale.

3. **Human Complementarity Index**
   - Đo phần con người còn bổ trợ hoặc giữ quyền quyết định.
   - Thành phần: human agency, domain expertise, interpersonal communication, uncertainty, ethical/quality oversight reasons.

4. **Skill Shift Pressure**
   - Đo áp lực chuyển dịch tổng hợp.
   - Công thức gợi ý:

```text
Skill Shift Pressure =
  z(Automation Exposure Index)
+ z(Worker Pull Index)
- z(Human Complementarity Index)
```

Chỉ số này nên được dùng để xếp hạng task/kỹ năng theo áp lực chuyển giao sang AI. Ngược lại, các kỹ năng có `Human Complementarity Index` cao và `Automation Exposure Index` cũng cao nên được xem là nhóm **AI-augmented human skills**: không mất đi, nhưng cách làm sẽ đổi mạnh.

### 5.3. Ma trận phân loại 2x2 hoặc 3x3

Dùng trục X = `Automation Exposure Index`, trục Y = `Human Complementarity Index`, thêm màu hoặc kích thước = `Worker Pull Index`.

Các nhóm diễn giải:

- **Replace/Automate Candidate**: exposure cao, complementarity thấp.
- **Augment/Co-pilot Candidate**: exposure cao, complementarity cao.
- **Human-Centric Durable Skill**: exposure thấp, complementarity cao.
- **Low-AI-Impact Routine/Peripheral**: exposure thấp, complementarity thấp.

Có thể thêm một trục phụ:

- Worker desire cao: người lao động sẵn sàng chuyển giao.
- Worker desire thấp: có rào cản chấp nhận, rủi ro adoption.

## 6. Quy trình phân tích đề xuất

### Bước 1. Chuẩn hóa và nối dữ liệu

1. Chuẩn hóa tên cột, tên nghề, task text:
   - lowercase, trim whitespace, normalize punctuation.
   - ưu tiên join bằng `Task ID` khi có.
   - với `usage`, `paper`, `company`, dùng normalized `task + occupation` hoặc normalized `task`.

2. Deduplicate:
   - `expert_rated_technological_capability.csv` có 19 dòng duplicate, cần kiểm tra và loại bản ghi trùng hoàn toàn.

3. Parse các cột list:
   - `Skill (O*NET Work Activity)`.
   - `Skill ID (O*NET Generalized Work Activity ID)`.

4. Chuẩn hóa numeric:
   - Các trường BLS có dấu phẩy hoặc ký tự `#` cần convert sang numeric.
   - Với `paper_count`, `company_count`, dùng `log1p()` để giảm lệch do đuôi dài.

### Bước 2. EDA mô tả

1. Phân phối rating:
   - Automation desire trung bình hiện khoảng 3.00/5.
   - Expert automation capacity trung bình hiện khoảng 3.40/5.
   - Worker job security concern trung bình hiện khoảng 2.38/5.
   - Worker human agency trung bình hiện khoảng 2.88/5.
   - Expert human agency trung bình hiện khoảng 2.66/5.

2. Kiểm tra độ khác biệt giữa worker và expert:
   - So sánh rating cùng task.
   - Tính chênh lệch `expert automation capacity - worker automation desire`.
   - Tính tương quan giữa desire, capability, agency, core skill, job security.

3. Phân tích missingness:
   - Wage/employment trong task metadata thiếu khoảng 30%.
   - Zip code thiếu khoảng 53%.
   - LLM usage-by-type thiếu khoảng 18%, nhiều khả năng do câu hỏi rẽ nhánh.

### Bước 3. Phân tích theo task và occupation

1. Xếp hạng top task:
   - AI capability cao nhất.
   - Worker desire cao nhất.
   - Human agency cao nhất.
   - Chênh lệch worker-expert lớn nhất.

2. Tạo scatter/bubble chart:
   - X: automation capability.
   - Y: human agency.
   - Size: employment hoặc company_count.
   - Color: sector hoặc worker desire.

3. Phân tích nghề:
   - Tổng hợp theo occupation: trung bình có trọng số theo task importance/frequency.
   - Tạo rank nghề chịu chuyển dịch mạnh nhất.
   - Tính tỷ trọng task trong từng nghề thuộc 4 nhóm: automate, augment, durable, low-impact.

### Bước 4. Phân tích theo kỹ năng O*NET

1. Explode `Skill (O*NET Work Activity)` để mỗi task-skill là một dòng.
2. Tổng hợp theo skill:
   - Số task.
   - Automation Exposure Index trung bình.
   - Human Complementarity Index trung bình.
   - Worker Pull Index trung bình.
   - Employment-weighted exposure.
3. Dùng DWA/IWA/GWA để gom chi tiết:
   - `tasks_to_dwas.csv` nối task sang Detailed Work Activities.
   - `dwa_reference.csv` giúp ánh xạ lên nhóm hoạt động rộng hơn.

Kết quả nên là bảng:

| Skill / Work Activity | Exposure | Complementarity | Worker Pull | Nhóm chuyển dịch | Diễn giải |
|---|---:|---:|---:|---|---|
| Processing Information | cao | thấp/trung bình | cao | Automate/Augment | AI xử lý thông tin tốt, cần con người kiểm định đầu ra. |
| Communicating with others | trung bình | cao | tùy ngành | Augment/Durable | AI hỗ trợ soạn thảo, nhưng con người giữ quan hệ và trách nhiệm. |
| Inspecting physical materials | thấp/trung bình | cao nếu có vật lý | Durable/Augment | Phụ thuộc robot/sensor, không chỉ LLM. |

### Bước 5. Phân tích theo nhóm người lao động

Nối `domain_worker_desires.csv` với `domain_worker_metadata.csv` theo `User ID`.

Phân tích:

1. Người dùng LLM thường xuyên có desire khác không?
2. Experience/education/age có liên quan đến automation desire hay job security concern không?
3. Nhóm occupation nào có khoảng cách lớn giữa job security concern và AI capability?
4. Các kiểu dùng LLM hiện tại như coding, analysis, communication, information access có dự báo desire với một số task không?

Mô hình gợi ý:

- Linear/mixed-effects model:

```text
Automation Desire Rating ~
  Automation Capacity Rating
+ Human Agency Scale Rating
+ Core Skill Rating
+ Enjoyment Rating
+ Job Security Rating
+ LLM Familiarity
+ LLM Use in Work
+ Education + Experience + Age
+ (1 | Occupation)
+ (1 | User ID)
```

- Nếu muốn dễ diễn giải hơn, dùng ordinal logistic regression vì rating là thang 1-5.

### Bước 6. Phân tích tín hiệu thời gian và hệ sinh thái AI

Dùng:

- `paper_id_to_year_mapping.csv`.
- `company_to_year_mapping.csv`.
- `paper_to_workflow_mapping_aggregated.csv`.
- `company_to_workflow_aggregation.csv`.

Mục tiêu:

1. Với mỗi task/workflow, đếm paper và company theo năm.
2. Tạo trend `AI innovation momentum`.
3. So sánh momentum với automation capacity và worker desire.
4. Xác định nhóm kỹ năng "đang tăng tốc": chưa được AI dùng nhiều nhưng paper/company tăng nhanh.

Chỉ số gợi ý:

```text
Innovation Momentum =
  normalized recent paper count
+ normalized recent company count
+ growth rate 2023-2025
```

### Bước 7. Trọng số thị trường lao động

Nối occupation sang wage/employment từ `task_statement_with_metadata.csv` và BLS.

Phân tích:

1. Exposure-weighted employment: bao nhiêu lao động nằm trong nhóm skill/task có pressure cao.
2. Wage-weighted exposure: kỹ năng lương cao có bị AI tác động nhiều hơn không.
3. Sector-level impact map:
   - Computer & Mathematical.
   - Business & Financial.
   - Office & Administrative Support.
   - Healthcare.
   - Education.
   - Production.

Kết quả nên ưu tiên biểu đồ:

- heatmap sector x skill group.
- bubble chart occupation exposure x employment.
- stacked bar tỷ trọng task theo nhóm chuyển dịch trong từng sector.

## 7. Sản phẩm đầu ra nên có

1. **Bảng master phân tích**
   - `outputs/task_ai_skill_shift.csv`
   - mỗi dòng là một task hoặc task-skill.

2. **Bảng xếp hạng**
   - top skills có pressure cao.
   - top skills có complementarity cao.
   - top occupations chịu tác động mạnh.
   - top occupations có khoảng lệch worker-expert lớn.

3. **Dashboard hoặc notebook**
   - overview dữ liệu.
   - task/skill quadrant.
   - occupation/sector heatmap.
   - worker demographic analysis.
   - innovation momentum over time.

4. **Báo cáo diễn giải**
   - Executive summary 1-2 trang.
   - Methodology.
   - Findings theo skill, occupation, sector.
   - Hạn chế dữ liệu.
   - Hàm ý đào tạo/reskilling.

## 8. Visualizations ưu tiên

1. **Skill Shift Quadrant**
   - X: automation exposure.
   - Y: human complementarity.
   - Color: worker pull.
   - Size: employment/company_count.

2. **Occupation Exposure Heatmap**
   - Rows: occupation hoặc sector.
   - Columns: O*NET work activities.
   - Values: skill shift pressure.

3. **Worker vs Expert Gap Plot**
   - X: expert capability.
   - Y: worker desire.
   - Diagonal line: alignment.
   - Highlight outliers.

4. **Human Agency Reasons Bar Chart**
   - Tỷ lệ chọn physical, control, domain knowledge, empathy, quality oversight, dynamic, ethical.

5. **Innovation Momentum Timeline**
   - Paper/company counts theo năm cho từng skill group.

6. **Reskilling Priority Matrix**
   - X: exposure.
   - Y: employment.
   - Color: complementarity.
   - Label: skill/occupation.

## 9. Diễn giải kỳ vọng

Một khung diễn giải nên tránh nói "AI thay thế nghề" quá sớm. Dữ liệu phù hợp hơn để nói:

- AI tác động trước hết ở cấp **task**, sau đó mới tổng hợp lên occupation.
- Một nghề có thể có task bị tự động hóa, task được AI hỗ trợ, và task con người càng quan trọng hơn cùng lúc.
- Kỹ năng tương lai không chỉ là "biết dùng AI", mà là kết hợp:
  - đặt vấn đề và kiểm định đầu ra,
  - judgment chuyên môn,
  - giao tiếp và phối hợp,
  - oversight chất lượng,
  - xử lý tình huống bất định,
  - trách nhiệm đạo đức và quyền quyết định.

## 10. Hạn chế cần ghi rõ

1. Worker/expert ratings chỉ phủ khoảng 40% task chính.
2. Rating 1-5 là chủ quan, cần phân tích độ nhạy và độ tin cậy.
3. Paper/company count phản ánh sự chú ý của hệ sinh thái AI, không trực tiếp chứng minh năng suất hoặc thay thế lao động.
4. Anthropic usage chỉ phản ánh một nguồn quan sát sử dụng AI, có thể thiên lệch theo người dùng/nền tảng.
5. Một task có thể gắn nhiều skill, nên khi explode skill cần tránh double-count không kiểm soát.
6. Dữ liệu wage/employment thiếu khoảng 30% trong bảng task metadata, cần bổ sung/đối chiếu với BLS.

## 11. Thứ tự triển khai khuyến nghị

1. Tạo notebook/script `01_build_master_dataset`.
2. Tạo bảng master task-level với các join chính.
3. Tính 3 chỉ số: exposure, worker pull, complementarity.
4. Làm EDA và visualizations cấp task.
5. Explode sang skill/DWA và tổng hợp skill-level.
6. Tổng hợp occupation/sector với trọng số frequency, importance, relevance và employment.
7. Phân tích worker heterogeneity theo metadata.
8. Thêm paper/company/year để phân tích momentum.
9. Viết báo cáo kết quả và khuyến nghị reskilling.

## 12. Các câu trả lời phân tích cuối cùng nên hướng tới

1. **Những kỹ năng nào đang dịch chuyển từ thực thi thủ công sang giám sát AI?**
2. **Những kỹ năng nào giảm nhu cầu lao động trực tiếp nhưng tăng nhu cầu kiểm định/chịu trách nhiệm?**
3. **Những ngành/nghề nào có tỷ trọng task dễ tự động hóa cao nhất?**
4. **Những nhóm lao động nào muốn AI hỗ trợ nhiều nhất và vì sao?**
5. **Khoảng cách lớn nhất giữa khả năng công nghệ và mong muốn của người lao động nằm ở đâu?**
6. **Ưu tiên đào tạo lại nên tập trung vào kỹ năng nào để con người bổ trợ AI thay vì bị thay thế bởi AI?**
