# Ke hoach phan tich: Su dich chuyen ky nang va khuyen nghi AI Agent trong nganh khoa hoc may tinh

## 1. Dinh nghia lam viec

Trong de tai nay, "su dich chuyen ky nang" khong duoc hieu don gian la AI thay the nguoi lao dong. Dinh nghia phu hop hon la:

> Su dich chuyen ky nang la su thay doi vai tro cua ky nang con nguoi khi AI tham gia vao task: tu truc tiep thuc hien sang dat muc tieu, giam sat, kiem dinh, xu ly ngoai le, giai thich ket qua va chiu trach nhiem cuoi cung.

Voi nganh khoa hoc may tinh, dieu nay co nghia la mot so task lap lai nhu ghi nhan thong tin, test co cau truc, sinh code mau, xu ly log hoac tao bao cao co the chuyen sang AI agent/copilot. Nguoc lai, cac ky nang thiet ke he thong, bao mat, review logic, ra quyet dinh kien truc, phan tich yeu cau va chiu trach nhiem van can con nguoi manh.

## 2. Co so nghien cuu can dua vao

- Ly thuyet task-based technological change: cong nghe thuong thay the task co quy tac ro, nhung bo tro task phi lap lai, giai quyet van de va giao tiep.
- AI exposure khac voi job replacement: task/nghe co exposure cao chua chac bi thay the; co the la noi can copilot va tai cau truc workflow.
- LLM va AI-powered software lam tang pham vi task co the duoc ho tro, nhung tac dong khong deu giua cac task.
- "Jagged frontier": AI lam tot mot so task tri thuc, nhung co the lam kem o task tuong tu neu vuot ngoai frontier. Vi vay khuyen nghi phai o cap task, khong chi cap nghe.
- Nghien cuu coding assistant cho thay AI co the tang toc mot so task lap trinh, nhung van can review, test, traceability va human-in-the-loop.

Nguon chi tiet: `sources/research_sources_skill_shift.md`.

## 3. Du lieu hien co

### Bang chinh

- `outputs/task_ai_skill_shift.csv`: bang task trung tam, 2,131 task, 85 cot.
- `outputs/skill_shift_summary.csv`: tong hop theo ky nang.
- `outputs/occupation_shift_summary.csv`: tong hop theo nghe.
- `outputs/sector_shift_summary.csv`: tong hop theo nganh.
- `outputs/worker_group_summary.csv`: tong hop theo nhom worker.

### Tin hieu quan trong

- Worker signal: 844/2,131 task co tin hieu worker.
- Expert signal: 846/2,131 task co tin hieu expert.
- Paired worker-expert signal: 844/2,131 task.
- Paper signal: 2,116/2,131 task.
- Company signal: 2,015/2,131 task.

### Trong tam CS/IT/Data

Sector `Computer and Mathematical`:

- 261 task.
- 29 occupation.
- `automation_exposure_index`: 0.699.
- `worker_pull_index`: 0.514.
- `human_complementarity_index`: 0.509.
- `innovation_momentum_index`: 0.790.
- `skill_shift_pressure`: 1.191.

## 4. Cau hoi phan tich

1. Trong nganh Computer and Mathematical, task nao co ap luc dich chuyen ky nang cao nhat?
2. Task nao phu hop de giao cho AI agent tu dong, task nao chi nen dung copilot/human-in-the-loop?
3. Ky nang nao dang dich chuyen tu "tu lam" sang "giam sat, review, dieu phoi va chiu trach nhiem"?
4. Co lech pha nao giua nang luc AI va mong muon cua worker khong?
5. Nhom nghe nao trong CS/IT/Data nen uu tien trien khai agent truoc?
6. Nhom ky nang nao can reskilling de nguoi lao dong lam viec tot voi AI agent?

## 5. Bien va chi so su dung

### Bien dau vao chinh

- `automation_exposure_index`: muc AI co the tham gia task.
- `worker_pull_index`: muc worker muon AI ho tro/tu dong hoa.
- `human_complementarity_index`: muc task van can con nguoi.
- `innovation_momentum_index`: tin hieu nghien cuu, paper, company quanh task/workflow.
- `task_importance_weight`: trong so task theo importance/relevance/frequency neu can.
- `sector`, `occupation`, `skill_list`: cap tong hop.

### Bien ket qua

- `skill_shift_pressure`: diem ap luc dich chuyen ky nang.
- `transition_type`: nhan loai dich chuyen.
- `mismatch_type`: nhan lech pha capability/desire.
- `polarization_score`: nghe co task vua de automation vua can con nguoi hay khong.

## 6. Phuong phap phan tich de xuat

### Buoc 1: Loc pham vi nganh khoa hoc may tinh

Loc cac dong co:

- `sector == "Computer and Mathematical"`, va/hoac
- occupation/task co lien quan software, data, web, systems, QA, security, database, network, analytics.

Muc tieu: tao subset CS/IT/Data de tranh ket luan lan sang cac nganh khac.

### Buoc 2: Mo ta tong quan

Tinh:

- So task, so nghe, so ky nang.
- Trung binh/phan vi cua 4 chi so: exposure, worker pull, human complementarity, innovation.
- Ti le `transition_type`.
- Top occupation/skill theo `skill_shift_pressure`.

Output:

- Bang ranking task/nghe/ky nang.
- Bieu do bar top skill shift pressure.
- Bieu do distribution cua cac chi so.

### Buoc 3: Ban do quadrant task

Ve scatter:

- Truc X: `automation_exposure_index`.
- Truc Y: `human_complementarity_index`.
- Mau: `transition_type`.
- Kich thuoc diem: `task_importance_weight` hoac `employment`.

Dien giai:

- Cao exposure, thap human complementarity: automation/agent candidate.
- Cao exposure, cao human complementarity: AI-augmented human premium.
- Thap exposure, cao human complementarity: durable human skill.
- Cao worker pull nhung exposure thap: worker wants help before tech is ready.

### Buoc 4: Phan tich lech pha capability-desire

Dung:

- `capability_desire_gap`
- `desire_capability_gap`
- `mismatch_type`

Muc tieu:

- Tim task AI co kha nang cao nhung worker chua muon giao.
- Tim task worker muon AI giup nhung nang luc cong nghe chua ro.
- Lam co so cho khuyen nghi UX, governance, training va human approval.

### Buoc 5: PCA cho su dich chuyen ky nang

Dung PCA tren cac bien:

- `automation_exposure_index`
- `worker_pull_index`
- `human_complementarity_index`
- `innovation_momentum_index`
- co the them `job_security_score`, `core_skill_score`, `enjoyment_score` neu khong bi thieu qua nhieu.

Muc tieu PCA:

- Rut gon nhieu chi so thanh 2-3 truc chinh.
- Dat ten cac truc, vi du:
  - PC1: Ap luc AI/automation.
  - PC2: Gia tri bo tro cua con nguoi.
  - PC3: Lech pha adoption/worker desire.
- Ve ban do PC1-PC2 cho task/nghe/ky nang.

Luu y:

- PCA chi de kham pha pattern, khong chung minh nhan qua.
- Chi nen chay PCA tren subset co du tin hieu worker-expert, hoac dung imputing ro rang.

### Buoc 6: Hoi quy kham pha

Dung hoi quy de giai thich/kiem tra pattern, khong nen noi la nhan qua.

Mo hinh 1: Linear regression

```text
skill_shift_pressure ~ automation_exposure_index
                    + worker_pull_index
                    + human_complementarity_index
                    + innovation_momentum_index
                    + task_importance_weight
```

Mo hinh 2: Logistic regression

```text
Automation candidate = 1/0
~ automation_exposure_index
+ worker_pull_index
+ human_complementarity_index
+ innovation_momentum_index
```

Muc tieu:

- Xem bien nao dong gop manh vao ap luc dich chuyen.
- Kiem tra task nao co xac suat cao thuoc nhom agent/candidate.

### Buoc 7: Chuyen ket qua thanh khuyen nghi AI Agent

Tao bang khuyen nghi theo task:

| Dieu kien | Khuyen nghi |
|---|---|
| Exposure cao, complementarity thap, worker pull cao | Autonomous/semiautonomous AI agent |
| Exposure cao, complementarity cao | Copilot co human approval |
| Worker pull cao, exposure trung binh/thap | Pilot tool ho tro, chua tu dong hoa |
| Complementarity cao, uncertainty/domain/interpersonal cao | Human-led AI assistance |
| Signal thieu | Khong khuyen nghi, can thu thap them du lieu |

## 7. Dau ra can tao

1. `outputs/cs_task_agent_recommendations.csv`
   - Task, occupation, skill, index scores, transition type, recommendation type, rationale.

2. `outputs/cs_skill_shift_summary.csv`
   - Ranking ky nang CS/IT/Data theo ap luc dich chuyen.

3. `outputs/cs_occupation_agent_summary.csv`
   - Ranking nghe theo muc do phu hop voi AI Agent.

4. `outputs/figures/cs_task_quadrant.png`
   - Ban do exposure vs human complementarity.

5. `outputs/figures/cs_pca_skill_shift_map.png`
   - Ban do PCA cua task/occupation/skill.

6. `outputs/ai_agent_recommendation_report.md`
   - Bao cao dien giai va khuyen nghi.

## 8. Nguyen tac dien giai

- Khong noi "AI se thay the nghe X"; chi noi "task/ky nang trong nghe X co ap luc dich chuyen cao".
- Phan biet exposure voi automation readiness.
- Neu human complementarity cao, khuyen nghi copilot/human-in-the-loop thay vi autonomous agent.
- Neu signal thieu, gan nhan `Insufficient signal` va khong ket luan manh.
- Voi AI agent trong CS, luon them dieu kien review, test, logging, rollback va human approval cho task co rui ro.

## 9. Thu tu thuc hien tiep theo

1. Tao subset CS/IT/Data.
2. Tao bang mo ta va ranking ban dau.
3. Ve quadrant task.
4. Chay PCA tren cac chi so chinh.
5. Chay hoi quy kham pha.
6. Sinh bang khuyen nghi AI Agent.
7. Viet bao cao ngan: insight, rui ro, khuyen nghi trien khai.
