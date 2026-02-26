# Question 3 – Data Ethics: AI Ethics in Healthcare

## A. Healthcare Data Privacy

### HIPAA vs. GDPR

Two main frameworks govern health data protection: **HIPAA** (USA) and **GDPR** (EU). HIPAA targets the healthcare industry — hospitals, insurers, and their partners — and permits data sharing for treatment or billing without explicit consent each time. Its primary focus is operational security.

The GDPR takes a broader approach, covering all personal data of EU residents regardless of sector. Health data is treated as a special category requiring clear, informed consent. A key distinction is the **"Right to be Forgotten"** — EU residents can request permanent deletion of their data. HIPAA has no equivalent, as US law often mandates retaining medical records for years to support legal accountability.

### The Limits of Anonymization

Removing names and ID numbers is commonly assumed to be sufficient protection. In practice, it rarely is. "De-identified" datasets can be re-identified by cross-referencing with publicly available information. In one well-known case, a researcher identified a Governor's medical records by matching anonymous hospital data with his birth date and zip code from public voter files. If a public figure's records can be traced this way, ordinary patients face the same risk.

### Why Health Data Is Different

Health data is largely **permanent**. A stolen credit card can be cancelled; a leaked genetic profile or mental health history cannot be changed. The consequences of such a breach can affect a person's employment and insurance eligibility for a lifetime. Beyond data misuse, there is also a direct physical risk — compromised connected medical devices such as pacemakers could be used to harm patients, not merely expose their information.

---

## B. Algorithmic Bias in Medical AI

### Where Bias Originates

AI systems learn from data — and if that data reflects historical inequalities, the AI will inherit them. A model trained predominantly on images of lighter skin tones will perform poorly when diagnosing conditions on darker skin. If past clinical records reflect patterns where women's cardiac symptoms were taken less seriously, the AI absorbs that same bias. A more subtle issue arises when **cost is used as a proxy for health need**, since healthcare spending is shaped by income, geography, and access to care — not just illness severity.

### The Obermeyer Case (2019)

Obermeyer et al. (2019) examined a widely used hospital algorithm designed to identify patients who would benefit from enhanced care. The algorithm used healthcare costs as its primary signal for medical need — a seemingly reasonable assumption. However, because systemic inequalities meant Black patients historically received less healthcare spending than White patients with equivalent conditions, the algorithm consistently ranked them as healthier than they actually were. The outcome was stark: Black patients had to be considerably sicker than White patients to receive the same level of support. Correcting this single flaw was estimated to more than double the number of Black patients receiving appropriate care.

### Mitigation

Addressing bias demands action on both technical and organisational levels. Techniques such as **resampling** can help ensure training data represents all demographic groups fairly, and health-specific outcome metrics should replace indirect proxies like cost. At the organisational level, building **diverse teams** to design and audit these systems is equally important — people with different backgrounds are far more likely to identify the assumptions that a homogeneous team would never think to question.

---

## C. Ethical Framework for Data Scientists

Before deploying any AI tool in healthcare, six questions need honest answers:

1. **Is the data representative?** Does it meaningfully include people of different ages, races, genders, and socioeconomic backgrounds?
2. **Are we measuring the right thing?** Are we relying on genuine clinical indicators, or convenient but misleading shortcuts?
3. **Can we explain it?** Could a clinician articulate, in plain terms, why the AI reached a specific recommendation?
4. **What happens when it fails?** Is there a clear process for human oversight to intervene?
5. **Does it benefit patients?** Is this tool genuinely improving health outcomes, or primarily reducing institutional costs?
6. **Have patients consented?** Are individuals aware that an AI system is influencing decisions about their care?

The ability to explain AI reasoning is critical for safety. If a model flags a lung cancer diagnosis, a clinician must understand why — otherwise there is no way to distinguish a genuine finding from the model reacting to an imaging artefact. An unexplainable AI is not a clinical tool; it is a liability.

---

## D. Stakeholder Impact and Policy Recommendation

**Patients** stand to benefit from faster diagnoses and more personalised treatment, but face significant risks from privacy breaches and biased systems. Strong protections are needed to ensure that data shared for research purposes cannot be used against patients by insurers or employers.

**Healthcare providers** benefit from AI efficiency but risk **automation bias** — over-reliance on algorithmic output that erodes independent clinical judgement. Training must emphasise critical evaluation of AI recommendations, not just their use, and legal accountability around AI-driven errors remains largely unresolved.

**Researchers and developers** carry the deepest responsibility. A model that performs well on aggregate metrics is not automatically safe or fair. If bias is identified before deployment, the ethical response is to delay release and address it — not to proceed and patch it later under pressure.

**Policy recommendation:** A qualified human clinician must retain final decision-making authority for all significant medical interventions. This protects patients through meaningful oversight and preserves the professional accountability of healthcare providers. AI should function as a tool that enhances clinical expertise — not one that substitutes for it.