# Challenge 01 — Problem framing

## Top 3 lessons (fill in after comparing with the reference answers)

1. 
2. 
3. 

---

## 1. An online store wants to predict how many units of each product will sell next week.

- **Input → output:** product × week → units
- **Problem type:** Time series forecasting
- **Labels:** past sales
- **Baseline:** same week last year, or last 4-week average.
- **Metric (and which mistake is worse):** MAE or WAPE
- **Is ML needed, and why?:** Yes, Overstock vs stockout cost decides which direction of error is worse.

**Correction after checking the reference:** 

---

## 2. A bank wants to flag credit-card transactions that might be fraud, for a team that can review 200 a day.
- **Input → output:** amount, time -> fraud
- **Problem type:** Imbalanced Classification
- **Labels:** confirmed fraud cases
- **Baseline:** rules (amount > X, new country).
- **Metric (and which mistake is worse):** precision in the top 200 per day (capacity!)
- **Is ML needed, and why?:** Yes, Missing fraud costs money; false alarms waste reviewer time.

**Correction after checking the reference:** 

---

## 3. A real-estate site wants to suggest a listing price for a house from its details.

- **Input → output:** price, time
- **Problem type:** Regression
- **Labels:** 
- **Baseline:** median price 
- **Metric (and which mistake is worse):** MAE in currency, or percentage error.
- **Is ML needed, and why?:** Yes

**Correction after checking the reference:** 

---

## 4. A telecom company wants to know which customers are likely to cancel next month, to offer them a discount.

- **Input → output:** customer data -> pron to cancel
- **Problem type:** Classification
- **Labels:** 
- **Baseline:** customer complaint in last month
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 5. A marketing team wants to "understand our different types of customers." They have purchase history but no customer categories.

- **Input → output:** different types of customer -> cluster
- **Problem type:** Clustering or unsupervised learning
- **Labels:** no labels
- **Baseline:** simple segment by spend and freq
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 6. A support team receives 5,000 emails a day and wants each one routed to one of 30 departments.

- **Input → output:** emails -> department
- **Problem type:** Text classification
- **Labels:** department
- **Baseline:**  keyword rules or TF-IDF + logistic regression.
- **Metric (and which mistake is worse):** macro-F1 plus accuracy
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 7. A factory wants to spot cracked parts from photos on a production line. Cracks are rare.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 8. A hospital wants to outline tumors in MRI scans, pixel by pixel, to help radiologists.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 9. A warehouse wants to count and locate boxes on shelves from camera images.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 10. A legal team wants to ask questions about 3,000 internal contracts and get answers with the clause cited.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 11. An HR team wants to pull name, email, years of experience, and skills out of PDF résumés into a spreadsheet.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 12. A news site wants to show "related articles" under each article.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 13. A server team wants to be alerted when a machine "behaves strangely." They have metrics but no history of labeled incidents.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 14. A company wants a chatbot that answers questions about its HR policies.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 15. A travel company wants an assistant that can search flights, check the user's calendar, and book a trip after the user confirms.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 16. An app wants to block toxic comments. Some comments are toxic in several ways at once (insult *and* threat).

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 17. A bank wants product descriptions rewritten in its brand voice. It has 2,000 examples of approved rewrites.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 18. A retailer wants to know whether a product review is positive or negative.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 19. A city wants to predict hourly bike-rental demand to plan bike redistribution.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 20. A company wants to know which of its 50 support macros to suggest to an agent while they type a reply.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 21. A school wants to detect whether essays were copied from each other.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 22. A game company wants to generate new background art in the style of its existing game.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 23. A company wants to translate its help center into Spanish.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 24. A manager wants a weekly report of "how many tickets were opened per category." Tickets already have a category field.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 

---

## 25. A clinic wants to predict a patient's risk of readmission within 30 days, for use in care planning.

- **Input → output:** 
- **Problem type:** 
- **Labels:** 
- **Baseline:** 
- **Metric (and which mistake is worse):** 
- **Is ML needed, and why?:** 

**Correction after checking the reference:** 
