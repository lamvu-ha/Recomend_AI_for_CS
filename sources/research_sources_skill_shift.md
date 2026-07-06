# Research Sources: Skill Shift and AI Agent Recommendations

This source log supports the analysis plan for the topic: "Phan tich va dua ra khuyen nghi AI Agent trong nganh khoa hoc may tinh" with the research theme "su dich chuyen ky nang".

## Core Research Sources

1. Autor, Levy, and Murnane (2003), "The Skill Content of Recent Technological Change"
   - URL: https://academic.oup.com/qje/article-abstract/118/4/1279/1925105
   - Search mirror/PDF: https://economics.mit.edu/sites/default/files/publications/the%20skill%20content%202003.pdf
   - Use: Foundation for task-based technological change. Computers substitute routine tasks and complement nonroutine problem-solving and communication.

2. Brynjolfsson, Mitchell, and Rock (2018), "What Can Machines Learn, and What Does It Mean for Occupations and the Economy?"
   - URL: https://www.aeaweb.org/articles?id=10.1257%2Fpandp.20181019
   - SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3224100
   - Use: Supports task-level measurement of suitability for machine learning and the idea that few occupations are fully automatable.

3. Felten, Raj, and Seamans (2021), "Occupational, Industry, and Geographic Exposure to Artificial Intelligence"
   - URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3822412
   - Use: Supports AI exposure measurement at occupation/industry level and the point that exposure is not identical to replacement.

4. Eloundou, Manning, Mishkin, and Rock (2023), "GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models"
   - URL: https://arxiv.org/abs/2303.10130
   - Science DOI page: https://www.science.org/doi/10.1126/science.adj0998
   - Use: Supports LLM task exposure framing; estimates broad task exposure and distinguishes LLM alone from LLM-powered software.

5. OECD Employment Outlook 2023: Artificial Intelligence and the Labour Market
   - URL: https://www.oecd.org/en/publications/oecd-employment-outlook-2023_08785bba-en.html
   - Chapter: https://www.oecd.org/en/publications/oecd-employment-outlook-2023_08785bba-en/full-report/artificial-intelligence-and-the-labour-market-introduction_ea35d1c5.html
   - Use: Supports workforce transition framing, automation risk, job quality, and changing skill needs.

6. OECD (2024), "Artificial Intelligence and the Changing Demand for Skills in the Labour Market"
   - URL: https://www.oecd.org/en/publications/artificial-intelligence-and-the-changing-demand-for-skills-in-the-labour-market_88684e36-en.html
   - Use: Supports analysis of skill demand in AI-exposed occupations, especially management, business process, cognitive, digital, and social skills.

7. Brynjolfsson, Li, and Raymond (2023/2025), "Generative AI at Work"
   - URL: https://academic.oup.com/qje/article/140/2/889/7990658
   - NBER: https://www.nber.org/system/files/working_papers/w31161/w31161.pdf
   - Use: Supports AI augmentation, productivity effects, heterogeneity across workers, and possible learning effects.

8. Dell'Acqua et al. (2023/2025), "Navigating the Jagged Technological Frontier"
   - HBS page: https://www.hbs.edu/faculty/Pages/item.aspx?num=64700
   - SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321
   - Use: Supports the idea that AI performance is uneven across tasks, so agent recommendations must be task-specific.

9. Peng et al. (2023), "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot"
   - URL: https://arxiv.org/abs/2302.06590
   - Microsoft Research page: https://www.microsoft.com/en-us/research/publication/the-impact-of-ai-on-developer-productivity-evidence-from-github-copilot/
   - Use: Directly relevant to computer science/software development tasks; supports AI pair programming productivity but not full autonomy.

## Data Context From Local Dataset

- Task base: `task_statement_with_metadata.csv`, 2,131 O*NET task rows.
- Worker signal: `domain_worker_desires.csv`, 5,731 responses.
- Expert signal: `expert_rated_technological_capability.csv`, 2,057 ratings.
- Integrated table: `outputs/task_ai_skill_shift.csv`, 2,131 rows and 85 columns.
- Computer and Mathematical sector: 261 tasks, 29 occupations.
- Key sector values from `outputs/sector_shift_summary.csv`:
  - `automation_exposure_index`: 0.699
  - `worker_pull_index`: 0.514
  - `human_complementarity_index`: 0.509
  - `innovation_momentum_index`: 0.790
  - `skill_shift_pressure`: 1.191
