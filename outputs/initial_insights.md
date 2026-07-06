# Initial AI Skill Shift Insights

This report is generated from `skill_shift_analysis.py`.

## Dataset coverage

- Task rows: 2,131
- Tasks with worker desire signal: 844
- Tasks with expert capability signal: 846
- Tasks with Anthropic usage signal: 819
- Tasks with paper signal: 2,116
- Tasks with company signal: 2,015

## Transition type distribution

| transition_type            |   task_count |
|:---------------------------|-------------:|
| Insufficient signal        |         1285 |
| Low near-term shift        |          296 |
| Durable human skill        |          203 |
| Automation candidate       |          169 |
| Worker-pulled automation   |           95 |
| AI-augmented human premium |           83 |

## Capability-desire mismatch distribution

| mismatch_type                          |   task_count |
|:---------------------------------------|-------------:|
| Missing worker/expert pair             |         1287 |
| Moderate or mixed                      |          748 |
| Capable but low worker pull            |           52 |
| Aligned automation opportunity         |           36 |
| Worker wants help before tech is ready |            8 |

## Top skills by shift pressure

Filtered to skills with enough task count and paired worker-expert signal.

| skill_list                                                    |   task_count |   paired_worker_expert_task_count |   automation_exposure_index |   worker_pull_index |   human_complementarity_index |   skill_shift_pressure | dominant_transition_observed   |
|:--------------------------------------------------------------|-------------:|----------------------------------:|----------------------------:|--------------------:|------------------------------:|-----------------------:|:-------------------------------|
| Inspecting Equipment, Structures, or Materials                |           36 |                                19 |                       0.622 |               0.518 |                         0.487 |                  1.564 | Automation candidate           |
| Working with Computers                                        |          133 |                                57 |                       0.541 |               0.521 |                         0.388 |                  1.467 | Low near-term shift            |
| Documenting/Recording Information                             |          420 |                               163 |                       0.467 |               0.547 |                         0.451 |                  0.937 | Low near-term shift            |
| Processing Information                                        |          104 |                                41 |                       0.491 |               0.518 |                         0.375 |                  0.895 | Low near-term shift            |
| Monitoring and Controlling Resources                          |           55 |                                23 |                       0.406 |               0.528 |                         0.412 |                  0.634 | Low near-term shift            |
| Analyzing Data or Information                                 |          214 |                                89 |                       0.563 |               0.508 |                         0.532 |                  0.566 | Low near-term shift            |
| Monitoring Processes, Materials, or Surroundings              |           78 |                                40 |                       0.445 |               0.543 |                         0.527 |                  0.5   | Low near-term shift            |
| Communicating with People Outside the Organization            |           22 |                                 8 |                       0.37  |               0.482 |                         0.434 |                  0.369 | Low near-term shift            |
| Evaluating Information to Determine Compliance with Standards |           55 |                                26 |                       0.474 |               0.496 |                         0.45  |                  0.304 | Low near-term shift            |
| Performing for or Working Directly with the Public            |           16 |                                 8 |                       0.511 |               0.412 |                         0.464 |                  0.254 | Automation candidate           |

## Top occupations by shift pressure

| Occupation (O*NET-SOC Title)                    | sector                            |   task_count |   automation_exposure_index |   worker_pull_index |   human_complementarity_index |   skill_shift_pressure |   polarization_score |
|:------------------------------------------------|:----------------------------------|-------------:|----------------------------:|--------------------:|------------------------------:|-----------------------:|---------------------:|
| Web Administrators                              | Computer and Mathematical         |           16 |                       0.822 |               0.647 |                         0.357 |                  3.184 |                0.166 |
| Bookkeeping, Accounting, and Auditing Clerks    | Office and Administrative Support |           19 |                       0.584 |               0.602 |                         0.263 |                  2.364 |                0.131 |
| Web Developers                                  | Computer and Mathematical         |           13 |                       0.821 |               0.507 |                         0.376 |                  2.306 |                0.335 |
| Lawyers                                         | Legal                             |            4 |                       0.596 |               0.624 |                         0.383 |                  2.219 |                0.204 |
| Computer Programmers                            | Computer and Mathematical         |           11 |                       0.851 |               0.481 |                         0.401 |                  2.167 |                0.218 |
| Search Marketing Strategists                    | Business and Financial Operations |           18 |                       0.699 |               0.589 |                         0.39  |                  2.113 |                0.149 |
| Online Merchants                                | Business and Financial Operations |           20 |                       0.665 |               0.531 |                         0.279 |                  2.079 |                0.133 |
| Payroll and Timekeeping Clerks                  | Office and Administrative Support |           18 |                       0.475 |               0.631 |                         0.305 |                  1.854 |                0.214 |
| Software Quality Assurance Analysts and Testers | Computer and Mathematical         |           19 |                       0.842 |               0.503 |                         0.495 |                  1.838 |                0.214 |
| Supply Chain Managers                           | Management                        |            9 |                       0.68  |               0.61  |                         0.472 |                  1.808 |                0.208 |

## Top sectors by shift pressure

| sector                              |   task_count |   occupation_count |   automation_exposure_index |   worker_pull_index |   human_complementarity_index |   skill_shift_pressure |
|:------------------------------------|-------------:|-------------------:|----------------------------:|--------------------:|------------------------------:|-----------------------:|
| Legal                               |           34 |                  5 |                       0.546 |               0.576 |                         0.419 |                  1.375 |
| Healthcare Support                  |            8 |                  1 |                       0.603 |               0.56  |                         0.428 |                  1.308 |
| Computer and Mathematical           |          261 |                 29 |                       0.699 |               0.514 |                         0.509 |                  1.191 |
| Sales and Related                   |           44 |                  4 |                       0.579 |               0.497 |                         0.366 |                  1.154 |
| Office and Administrative Support   |          399 |                 34 |                       0.452 |               0.517 |                         0.363 |                  0.795 |
| Management                          |          151 |                 27 |                       0.536 |               0.511 |                         0.51  |                  0.657 |
| Business and Financial Operations   |          289 |                 34 |                       0.505 |               0.497 |                         0.482 |                  0.212 |
| Educational Instruction and Library |          118 |                 19 |                       0.429 |               0.529 |                         0.534 |                 -0.021 |
| Life Physical and Social Science    |          155 |                 37 |                       0.525 |               0.566 |                         0.681 |                 -0.097 |
| Architecture and Engineering        |          346 |                 52 |                       0.438 |               0.482 |                         0.615 |                 -1.074 |

## Worker group signals

| group_variable   | group_value                           |   response_count |   user_count |   automation_desire |   job_security |   human_agency |
|:-----------------|:--------------------------------------|-----------------:|-------------:|--------------------:|---------------:|---------------:|
| Income           | 529K+                                 |               52 |           14 |               4.077 |          3.135 |          3.173 |
| Education        | Doctorate (e.g., PhD)                 |              235 |           67 |               3.536 |          2.847 |          3.315 |
| LLM Use in Work  | Yes, I use them every day in my work. |             1999 |          470 |               3.343 |          2.378 |          2.915 |
| Income           | 209K-529K                             |              232 |           53 |               3.306 |          2.147 |          2.94  |
| Education        | Prefer not to say                     |               36 |           13 |               3.306 |          3.194 |          2.611 |
| Income           | 165K-209K                             |              464 |          106 |               3.226 |          2.289 |          2.806 |
| LLM Familiarity  | I use them regularly.                 |             3227 |          763 |               3.2   |          2.373 |          2.866 |
| Education        | Master’s Degree                       |             1441 |          346 |               3.162 |          2.377 |          2.932 |
| Income           | Prefer not to say                     |              212 |           56 |               3.108 |          2.396 |          3.165 |
| LLM Familiarity  | No, I've never heard of them.         |               26 |            8 |               3.038 |          2.308 |          2.269 |

## Output files

- `outputs/task_ai_skill_shift.csv`
- `outputs/skill_shift_summary.csv`
- `outputs/reliable_skill_shift_summary.csv`
- `outputs/occupation_shift_summary.csv`
- `outputs/sector_shift_summary.csv`
- `outputs/worker_group_summary.csv`
- `outputs/figures/task_skill_shift_quadrant.png`
- `outputs/figures/capability_desire_mismatch.png`
- `outputs/figures/top_skill_shift_pressure.png`