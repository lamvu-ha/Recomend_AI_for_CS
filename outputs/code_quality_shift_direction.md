# Huong phan tich: AI lam tang code nhung day rui ro sang chat luong

## 1. Cau chuyen nen dat lai cho chat

Cau chuyen ban dau:

> Khi chua co AI, lap trinh van lam binh thuong. Khi AI vao, toc do/code output tang, nhung chat luong co nguy co giam.

Trong du lieu hien co, khong co bien do truc tiep:

- so dong code sinh ra,
- so pull request,
- defect rate,
- bug production,
- failed CI,
- code review rejection,
- maintainability score.

Vi vay khong nen ket luan truc tiep "chat luong da giam". Huong phan tich nen viet chat hon:

> AI lam tang kha nang tu dong hoa/sinh dau ra trong cac task lap trinh, nhung dong thoi lam noi bat rui ro chat luong va nhu cau review, test, giam sat, domain expertise va human approval.

Noi cach khac, day la cau chuyen "dich chuyen diem nghen":

```text
Truoc AI: viet code la diem nghen
Sau AI: review, test, security, maintainability va governance la diem nghen
```

## 2. Chung cu ban dau tu du lieu

Subset `Computer and Mathematical`:

- 261 task.
- 29 occupation.
- `automation_exposure_index`: 0.699.
- `worker_pull_index`: 0.514.
- `human_complementarity_index`: 0.509.
- `innovation_momentum_index`: 0.790.
- `skill_shift_pressure`: 1.191.

Nhom task coding/development:

- 138 task.
- `automation_exposure_index`: 0.748.
- `innovation_momentum_index`: 0.854.
- `skill_shift_pressure`: 1.453.
- 45 task la `Automation candidate`.
- 25 task la `AI-augmented human premium`.

Nhom task quality/QA/review/test:

- 95 task.
- `automation_exposure_index`: 0.723.
- `human_complementarity_index`: 0.507.
- `skill_shift_pressure`: 1.329.
- `human_agency_quality_oversight_share`: 0.300.
- 22 task la `Automation candidate`.
- 16 task la `AI-augmented human premium`.

Dien giai:

- AI co tin hieu manh o task sinh code va task ky thuat.
- Nhung task lien quan chat luong/test/review cung co human complementarity kha cao.
- Dieu nay ung ho cau chuyen: AI co the tang toc tao dau ra, nhung khong loai bo nhu cau kiem soat chat luong.

## 3. Cac vi du task quan trong

### Task co kha nang AI ho tro/sinh dau ra cao

- `Write supporting code for Web applications or Web sites`
  - exposure: 0.963
  - transition: Automation candidate

- `Write, update, and maintain computer programs or software packages...`
  - exposure: 0.959
  - transition: Automation candidate

- `Compile and write documentation of program development...`
  - exposure: 0.970
  - transition: Worker-pulled automation

### Task nam trong vung rui ro chat luong

- `Write, analyze, review, and rewrite programs...`
  - exposure: 0.875
  - human complementarity: 0.675
  - transition: AI-augmented human premium

- `Provide technical guidance or support for the development or troubleshooting of systems`
  - exposure: 0.847
  - human complementarity: 0.755
  - transition: AI-augmented human premium

- `Design and conduct hardware or software tests`
  - exposure: 0.713
  - human complementarity: 0.671
  - quality oversight share: 0.600
  - transition: AI-augmented human premium

Dien giai:

- Task "viet code" co the giao AI nhieu hon.
- Task "review, rewrite, troubleshoot, test, technical guidance" khong nen giao tu dong hoan toan.
- Day la noi ky nang con nguoi dich tu "tu viet code" sang "kiem dinh va chiu trach nhiem chat luong".

## 4. Gia thuyet phan tich

H1. Task coding/development trong CS co `automation_exposure_index` va `innovation_momentum_index` cao hon trung binh, cho thay AI co kha nang tang toc tao dau ra.

H2. Task quality/QA/review/test van co `human_complementarity_index`, `domain_expertise_requirement` va `quality_oversight_share` cao, cho thay chat luong van can con nguoi kiem soat.

H3. Nghe co exposure cao nhu Web Developers, Computer Programmers, Software QA Analysts and Testers se co `skill_shift_pressure` cao, nhung khuyen nghi agent nen phan tang theo rui ro.

H4. Neu task co exposure cao va human complementarity cao, khuyen nghi phu hop la copilot/human-in-the-loop, khong phai autonomous agent.

## 5. Cach tao bien phan tich

### Nhom task

Tao cot `task_group`:

- `code_generation`: write code, update program, develop application, script, web code.
- `quality_control`: test, QA, validate, debug, review, defect, compatibility, documentation accuracy.
- `architecture_governance`: design system, technical guidance, security, architecture, evaluate technology.
- `documentation_reporting`: documentation, report, record, standard procedure.

### Chi so de xuat

`code_acceleration_potential`:

```text
mean(automation_exposure_index,
     innovation_momentum_index,
     worker_pull_index)
```

`quality_risk_need`:

```text
mean(human_complementarity_index,
     expert_uncertainty_requirement_normalized,
     expert_domain_expertise_requirement_normalized,
     human_agency_quality_oversight_share)
```

`agent_autonomy_recommendation`:

```text
if high acceleration and low quality risk:
    autonomous_or_semiautonomous_agent
elif high acceleration and high quality risk:
    copilot_with_mandatory_review
elif low acceleration and high quality risk:
    human_led_ai_assistance
else:
    observe_or_low_priority
```

## 6. Bieu do nen lam

1. Bar chart: coding/development vs QA/review/test
   - So sanh `automation_exposure_index`, `human_complementarity_index`, `skill_shift_pressure`.

2. Quadrant:
   - X: `code_acceleration_potential`
   - Y: `quality_risk_need`
   - Mau: `agent_autonomy_recommendation`

3. Top occupation chart:
   - Web Developers
   - Computer Programmers
   - Software QA Analysts and Testers
   - Computer Systems Analysts
   - Computer Systems Engineers/Architects

4. Task examples table:
   - Task
   - Occupation
   - Exposure
   - Quality risk
   - Transition type
   - Agent recommendation

## 7. Huong khuyen nghi sau phan tich

Khong nen khuyen nghi "dung AI de viet code cang nhieu cang tot".

Nen khuyen nghi:

- AI Agent cho task lap lai, ro quy trinh, de test.
- Coding Copilot cho sinh code, refactor nho, tao test, tao documentation.
- QA/Review Agent cho phat hien loi, tao checklist, chay test, doc log.
- Human approval bat buoc voi task co domain expertise, architecture, security, production impact.
- Them governance: test suite, CI, code review, audit log, rollback, security scan.

## 8. Cau ket luan nen dung

> Ket qua phan tich khong chung minh truc tiep rang AI lam chat luong code giam, vi du lieu khong co defect rate hay code quality metric. Tuy nhien, du lieu cho thay cac task sinh code trong nganh khoa hoc may tinh co exposure va innovation momentum cao, trong khi cac task review, test, troubleshooting va technical guidance van co human complementarity va quality oversight cao. Vi vay, tac dong chinh cua AI khong chi la tang toc viet code, ma la dich chuyen ky nang lap trinh sang nang luc kiem soat chat luong, review, test, bao tri va giam sat AI Agent.
