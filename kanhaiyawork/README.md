# 🚗 AI-Powered Car Lease & Loan Contract Review Assistant

Welcome to the repository for the **Car Lease & Loan Contract Review and Negotiation Assistant**, developed as part of the Infosys Winter Internship program.  
This project focuses on simplifying one of the most confusing consumer journeys — understanding and negotiating vehicle finance contracts.

---

## 📌 Introduction

Car lease and loan forms are long, dense, and often difficult for buyers to interpret.  
This application aims to act as a **personal automotive finance advisor**, powered by AI models that read, extract, and explain key contract terms in plain language.  
It complements this intelligence with real-world vehicle data to help buyers evaluate fairness and negotiate confidently.

---

## 🎯 Core Objectives

- Help users understand contract clauses without legal expertise
- Highlight financial risks and hidden conditions
- Verify market pricing and car condition using public datasets
- Assist buyers in negotiating better deals with dealers or lenders

---

## 🔍 Main Features

### 📄 Automated Contract Review

Users upload their lease/loan agreement (PDF or scanned images).  
The system scans and extracts essential parameters such as:

- APR / Interest rate
- Contract duration
- Mileage rules and penalties
- Monthly payment
- Buyout option
- Fee structure
- Early termination rules

The output is a **clean summary** plus potential warnings for unfair or unusual terms.

---

### 💰 Market Price Benchmarking

By referencing publicly accessible automotive datasets, the app estimates **fair pricing** based on:

- Model
- Make
- Year
- Region

This gives the user a realistic comparison point for negotiation.

---

### 🔎 VIN Intelligence

Entering a VIN allows the app to fetch:

- Vehicle specifications
- Recall records
- History alerts

Paid reports like Carfax can be linked externally when needed.

---

### 🤖 Negotiation Assistant

An interactive AI chatbot helps users:

- Identify discussion points
- Ask important dealership questions
- Generate response messages

---

### 📱 End-User Application

The UI is developed with **Flutter** to provide a smooth, mobile-first experience, including:

- Document upload viewer
- Data dashboard
- Contract comparison
- Real-time chat assistant

---

## ⚙️ Technology Overview

| Component            | Implementation                       |
| -------------------- | ------------------------------------ |
| Contract Parsing     | LLMs and prompt-tuned extraction     |
| Pricing Data         | Public automotive APIs + web data    |
| VIN Lookup           | NHTSA and open vehicle datasets      |
| Frontend             | Flutter                              |
| Recommendation Logic | Rule-based + model-assisted insights |

---

## 🏗 High-Level Flow

User → Mobile App → Upload Contract
↓
AI Clause Extraction
↓
Price Benchmark / VIN Check
↓
Negotiation Recommendations

---

## 📌 Repository Layout

/docs → architecture & research notes
/mobile → Flutter front-end
/backend → API and AI logic
/datasets → sample contracts & VIN data
/prompts → clause extraction prompt tuning
README.md

---

## ✉ Contact

Feel free to reach out or suggest improvements.  
Contact information can be added here based on your project submission guidelines.
