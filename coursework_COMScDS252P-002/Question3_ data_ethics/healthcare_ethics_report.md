# AI Ethics in Healthcare

## A. Healthcare Data Privacy

### HIPAA vs. GDPR

HIPAA and GDPR are standard frameworks for data privacy. HIPAA is a US-based framework for healthcare data, while GDPR is an EU-based framework for all data.

HIPAA often implies use for treatment, billing, or operations. It has no `right to be forgotten`, and medical records generally require to be kept for at least 6 years. So, that is a main difference between HIPAA and GDPR. Also, the Breach Reporting period is significantly longer in HIPAA (which is 60 days) than in GDPR.

GDPR is for All Personal Data (e.g., IP addresses, names, emails, health info, etc.). It has a `right to be forgotten`, so individuals can request their data be deleted. It also has a Breach Reporting period of 72 hours. So, it likely gives more power to individuals.

**Why "Anonymization" Usually Isn't Enough**

People think using fake names and ID numbers or deleting names and ID numbers makes data safe to share. But it doesn't.

A famous study by Latanya Sweeney has shown that most (87%) Americans can be identified using just three simple facts: their birth date, gender, and zip code. She was even capable of identifying US Governor William Weld in a hospital database that did not have names on it by matching it with public voter records. People's data has patterns, and those patterns represent individuals. It doesn't need a name to be identified.

Another example is genetic data. The 1000 Genomes Project shared anonymous DNA data. But later, researchers were able to identify the people and their relatives by using public family tree websites.

---

## B. Algorithmic Bias in Medical AI

### What is the origin of the bias?

When an AI becomes biased, it usually happens for three reasons:

1. **Underrepresentation in training data:** If an AI that checks skin for cancer is only trained on lighter skin, it will not be able to spot cancer on darker skin.
2. **Geographic and socioeconomic collection bias:** Most AI data comes from hospitals in wealthy cities. Because of this, the AI may not work well for patients from rural areas or poorer patients.
3. **Historical treatment biases:** If old medical records show that doctors did not take women's heart attack symptoms seriously, the AI will learn to do the same thing.

**A Real-World Warning: The Obermeyer Study (2019)**

A study was held in 2019 covering health systems in the US. An AI was used to identify patients who needed care. Assuming that sicker patients cost more to treat, the AI used "healthcare costs" to decide who was the sickest. But the AI was not able to identify Black patients as being as sick as White patients with the same condition. Because of biases in the system, Black patients were not getting the same level of care as White patients.

As a result, the AI made a conclusion that Black patients were healthier than they were. In order to get the same level of care as White patients, Black patients had to be sicker than White patients. After correcting this issue, the number of Black persons who were correctly identified for medical support more than doubled.

**How Do We Fix It?**

Considering reasons for bias on both technical and organizational levels, using techniques such as `resampling` can help to balance the data. Also, developers need to make sure their data is balanced and their assumptions are relevant.

For example, they should not measure health outcomes just using easy shortcuts like "cost." Hospitals need to have teams to test these tools before using them on real patients.

---

## C. Ethical Decision Framework

Before deploying any AI system, data scientists should ask themselves the following questions:

1. **Is the data representative?** Does it include all ages, genders, ethnicities, and socioeconomic backgrounds?
2. **Are targets clinically valid?** Is the predicted outcome a direct health measure, not a proxy that leads to inequalities?
3. **Can the output be explained?** Can the doctor tell the patient the reasoning behind the AI's choice?
4. **Is human oversight preserved?** Does the doctor have permission to overrule the AI?
5. **Does it benefit patients?** Is there any practical benefit for the patients, rather than saving money for the hospital?
6. **Have patients been informed?** Are patients aware that AI is being used to enhance their treatments?

Patients have a `"right to explanation."` If an AI makes a medical choice but nobody understands how, it leads to insecurity for patients' treatments.

---

## D. Stakeholder Impact Analysis

### How This Impacts Everyone

**Patients** can benefit from faster and personalized diagnoses but face risks from breaches, biased outputs, and inaccurate decisions. To prevent that, we should include data minimization, informed consent, independent advocacy in AI governance, and prohibitions on using clinical data for insurance pricing or employment screening.

**Healthcare providers** can benefit from AI decision-support but face the risk of `automation bias`, blindly trusting the machine and losing their own skills. Liability for AI-influenced harm remains unresolved, and training must cover critical evaluation of recommendations, not only their use.

**Researchers and developers** have the deepest responsibility. An AI might be 95% accurate overall but completely fail minority groups. If developers find bias during testing, the ethical duty is to stop the launch and fix it. It is not a bug you can patch later.

**Policy recommendation:** Regulators must treat clinical AI like new medicine. Before an AI is allowed in hospitals, it needs mandatory testing by independent auditors. This keeps patients safe while ensuring humans always have the final say.

---

## References

Gymrek, M. et al. (2013) 'Identifying personal genomes by surname inference', *Science*, 339(6117), pp. 321–324.

Obermeyer, Z. et al. (2019) 'Dissecting racial bias in an algorithm used to manage the health of populations', *Science*, 366(6464), pp. 447–453.

Sweeney, L. (2000) 'Simple demographics often identify people uniquely', *Carnegie Mellon University, Data Privacy Working Paper*, 3, pp. 1–34.

