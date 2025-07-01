# Credit Risk Model Project

## Credit Scoring Business Understanding

### How does the Basel II Accord’s emphasis on risk measurement influence our need for an interpretable and well-documented model?

The Basel II Accord significantly influences the necessity for interpretable and well-documented credit scoring models, primarily through its three pillars: Minimum Capital Requirements (Pillar 1), Supervisory Review Process (Pillar 2), and Market Discipline (Pillar 3).

Under Pillar 1, banks adopting the Internal Ratings-Based (IRB) approach rely on their own models to calculate critical risk parameters like Probability of Default (PD) and Loss Given Default (LGD). For these calculations to be accepted by regulators, the underlying models must be **interpretable**, allowing supervisors to understand the drivers of risk assessment, validate the model's logic, and ensure its integrity.

Pillar 2, the Supervisory Review Process, mandates a robust dialogue between banks and supervisors regarding risk management and capital adequacy. This necessitates **well-documented** models, detailing their development, validation, and usage. Such documentation facilitates rigorous auditing and enables supervisors to verify compliance, assess model fairness, and ensure that the bank's internal processes for capital assessment (ICAAP) are sound. Without clear interpretability and thorough documentation, banks would struggle to justify their risk calculations and decision-making processes to regulatory bodies.

Finally, Pillar 3, Market Discipline, requires transparent disclosure of a bank's risk profile. While not directly about model internals, the ability to articulate how risk is measured and managed—a capability underpinned by interpretable and well-documented models—enhances market confidence and accountability.

In essence, Basel II transforms credit scoring models from mere predictive tools into critical components of regulatory compliance, demanding transparency, explainability, and auditable processes to ensure financial stability and protect stakeholders.

### Since we lack a direct "default" label, why is creating a proxy variable necessary, and what are the potential business risks of making predictions based on this proxy?

The necessity of creating a proxy variable stems from the absence of a direct "default" or "credit risk" label in the provided transactional dataset. Predictive machine learning models require a defined target variable to learn patterns and make predictions. In lieu of explicit loan performance data, a proxy variable serves as an observable substitute that is hypothesized to correlate strongly with actual creditworthiness. For this project, Recency, Frequency, and Monetary (RFM) patterns will be engineered to infer customer engagement, with low engagement serving as a proxy for high credit risk.

However, relying on a proxy carries significant business risks:

1.  **Inaccuracy of Proxy Correlation:** The primary risk is that the proxy may not perfectly reflect true credit default behavior. A customer deemed "high-risk" based on low RFM might, in reality, be creditworthy but simply have different purchasing habits or be new to the platform.
2.  **Financial Losses (False Negatives):** If the model, based on the proxy, incorrectly identifies a high-risk customer as low-risk (false negative), Bati Bank could approve loans to individuals who subsequently default. This directly leads to financial losses from unpaid principal and interest, increased debt collection costs, and erosion of profitability.
3.  **Lost Revenue and Customer Dissatisfaction (False Positives):** Conversely, if the model incorrectly classifies a creditworthy customer as high-risk (false positive), the bank may deny them the buy-now-pay-later service. This results in lost revenue opportunities, potential damage to customer relationships, and customers opting for competitors' services.
4.  **Bias and Ethical Concerns:** The chosen proxy might inadvertently correlate with demographic or socio-economic factors, leading to discriminatory lending practices. This poses significant ethical concerns and potential legal and reputational damage for Bati Bank.
5.  **Regulatory Scrutiny:** Financial regulators would meticulously scrutinize the methodology behind the proxy variable, demanding clear justification, validation, and a thorough understanding of its limitations, especially given its impact on risk assessments and capital allocation.

Therefore, while necessary, predictions based on a proxy variable demand careful validation, transparent communication of assumptions, and continuous monitoring to mitigate these inherent business risks.

### What are the key trade-offs between using a simple, interpretable model (like Logistic Regression with WoE) versus a complex, high-performance model (like Gradient Boosting) in a regulated financial context?

In a regulated financial environment, the choice between simple, interpretable models (e.g., Logistic Regression with Weight of Evidence (WoE)) and complex, high-performance models (e.g., Gradient Boosting) involves critical trade-offs between predictive accuracy and model interpretability, impacting regulatory compliance, risk management, and business operations.

**Simple, Interpretable Models (e.g., Logistic Regression with WoE):**
* **Advantages:** These models offer high interpretability, meaning their decision-making process is transparent and easily understood. The impact of each feature on the prediction is clear (e.g., through coefficients or WoE values), which is crucial for:
    * **Regulatory Compliance:** Facilitates adherence to Basel II's emphasis on supervisory review and auditability, allowing banks to clearly explain risk calculations and capital adequacy.
    * **Explainability:** Enables loan officers to articulate the reasons behind credit decisions to customers and stakeholders.
    * **Bias Detection:** Simplifies the identification and mitigation of potential biases, ensuring fairness in lending.
    * **Validation:** Easier to validate model logic and ensure it aligns with business expectations.
* **Disadvantages:** Their simplicity often comes at the cost of **lower predictive performance**. They may not capture complex non-linear relationships or intricate feature interactions as effectively, potentially leading to less precise risk assessments.

**Complex, High-Performance Models (e.g., Gradient Boosting):**
* **Advantages:** These models typically achieve **superior predictive performance** by identifying nuanced patterns and interactions within the data, leading to higher accuracy in risk probability estimation and potentially reducing financial losses.
* **Disadvantages:** Their primary drawback is their **"black box" nature**, meaning the internal workings and the specific reasons for individual predictions are difficult to ascertain. This lack of interpretability poses significant challenges in a regulated financial context:
    * **Regulatory Approval:** Obtaining approval from regulatory bodies is arduous due to demands for transparency, auditability, and the ability to explain decision rationales.
    * **Accountability and Trust:** Difficult to assign accountability for individual predictions or to build trust with customers if decisions cannot be adequately explained.
    * **Bias Management:** More challenging to detect, understand, and mitigate embedded biases, raising concerns about fairness and potential discrimination.
    * **Validation Complexity:** More difficult to thoroughly validate and ensure the model's behavior under various scenarios.

**Key Trade-off:** The fundamental trade-off is between maximizing **predictive accuracy** (which complex models excel at) and ensuring **interpretability and explainability** (a hallmark of simpler models). In a financial regulatory context, **interpretability often takes precedence**, even if it means a slight reduction in raw predictive power. This is because the ability to explain, audit, and demonstrate fairness is paramount for compliance, risk management, and maintaining public trust, making models like Logistic Regression with WoE often a preferred choice for their transparency, while advanced models might be used in conjunction or with strong Explainable AI (XAI) techniques if performance gains are substantial and regulatory hurdles can be cleared.