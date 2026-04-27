"""
LegalSarthi - Legal Rules Database
Curated rules for common legal situations in India.
Each rule has keywords, a category, and step-by-step legal advice.

NOTE: These are general legal information only, NOT legal advice.
Always consult a qualified lawyer for specific situations.
"""

LEGAL_RULES = [
    # ═══════════════════════════════════════════
    # POLICE & BRIBERY
    # ═══════════════════════════════════════════
    {
        "id": "police_bribe_traffic",
        "category": "police",
        "keywords": [
            "police", "bribe", "bribery", "traffic", "challan", "money",
            "pay", "cop", "fine", "stopped", "asking money", "hafta",
            "rischvat", "ghoos", "paisa maang",
        ],
        "title": "Police Demanding Bribe (Traffic / General)",
        "summary": "Demanding or accepting a bribe is a criminal offence under the Prevention of Corruption Act, 1988.",
        "steps": [
            "Stay calm and be polite. Do NOT pay the bribe.",
            "Ask the officer for their name, badge/belt number, and posting details.",
            "If a traffic violation occurred, ask for an official e-challan or written receipt — you are legally entitled to one.",
            "Record the interaction on your phone if safe to do so (audio/video is legal in public spaces for self-protection).",
            "Note the exact time, date, location, and vehicle number of the patrol vehicle.",
            "File a complaint on the Anti-Corruption Bureau (ACB) helpline of your state.",
            "You can also lodge a complaint on the Central Vigilance Commission (CVC) portal: cvc.gov.in.",
            "File an online complaint on the CPGRAMS portal (pgportal.gov.in) for central government officers.",
            "If the officer threatens or intimidates you, call 112 (national emergency) or 1064 (anti-corruption helpline in many states).",
            "As a last resort, file an FIR at the nearest police station under the Prevention of Corruption Act, 1988.",
        ],
        "relevant_laws": [
            "Prevention of Corruption Act, 1988 — Section 7 (public servant taking gratification)",
            "Indian Penal Code (BNS) — Section 171B (bribery)",
            "Right to Information Act, 2005 — to get officer details",
            "Motor Vehicles Act, 1988 — Section 200 (compounding of offences, e-challan)",
        ],
    },
    {
        "id": "police_fir_refusal",
        "category": "police",
        "keywords": [
            "fir", "refuse", "not filing", "complaint", "register",
            "police station", "won't register", "not taking complaint",
            "zero fir", "refused to file",
        ],
        "title": "Police Refusing to File FIR",
        "summary": "Under Section 154 CrPC (now Section 173 BNSS), police MUST register an FIR for cognizable offences. Refusal is a punishable offence.",
        "steps": [
            "Clearly state to the SHO (Station House Officer) that you want an FIR registered for a cognizable offence.",
            "If the SHO refuses, send your complaint in writing via registered post or email to the Superintendent of Police (SP).",
            "Under Section 154(3) CrPC / Section 173 BNSS, the SP must investigate if the SHO refuses.",
            "You can file a 'Zero FIR' at ANY police station — it does not have to be in the jurisdiction where the crime occurred.",
            "File an online FIR via your state's police website (most states now support e-FIR).",
            "Approach the Judicial Magistrate under Section 156(3) CrPC / Section 175(3) BNSS and request them to direct the police to register the FIR.",
            "File a complaint with the State Human Rights Commission if police are being negligent.",
            "Keep copies of all written complaints and acknowledgements.",
        ],
        "relevant_laws": [
            "CrPC — Section 154 (information in cognizable cases) / BNSS Section 173",
            "CrPC — Section 156(3) (Magistrate can order investigation) / BNSS Section 175(3)",
            "CrPC — Section 166 (Zero FIR provision)",
            "Indian Penal Code — Section 166A (public servant disobeying law) / BNS Section 220",
        ],
    },
    {
        "id": "police_illegal_detention",
        "category": "police",
        "keywords": [
            "arrest", "detained", "custody", "lockup", "jail",
            "without warrant", "illegal arrest", "rights",
            "taken to station", "picked up",
        ],
        "title": "Illegal Detention or Arrest Without Grounds",
        "summary": "Every arrested person has fundamental rights under Article 22 of the Constitution and the CrPC.",
        "steps": [
            "Ask the officer for the reason of arrest — they are legally bound to inform you (Article 22(1)).",
            "You must be produced before a Magistrate within 24 hours of arrest (Article 22(2)).",
            "You have the right to consult and be defended by a lawyer of your choice.",
            "Inform a family member or friend about your arrest — police must facilitate this.",
            "Women cannot be arrested after sunset and before sunrise except in exceptional circumstances, and only by a female officer.",
            "Do NOT sign any blank papers or documents under pressure.",
            "If you believe the arrest is illegal, your family/lawyer can file a Habeas Corpus petition in High Court.",
            "File a complaint with the National/State Human Rights Commission (NHRC/SHRC).",
        ],
        "relevant_laws": [
            "Constitution of India — Article 22 (protection against arrest and detention)",
            "CrPC — Section 50 (person arrested to be informed of grounds) / BNSS Section 47",
            "CrPC — Section 57 (person not to be detained more than 24 hours) / BNSS Section 58",
            "CrPC — Section 41 (when police may arrest without warrant) / BNSS Section 35",
            "DK Basu v. State of West Bengal (1997) — Supreme Court guidelines on arrest",
        ],
    },
    {
        "id": "police_license_vehicle_seized",
        "category": "police",
        "keywords": [
            "license", "licence", "driving license", "dl", "seized",
            "took my license", "confiscated", "impound", "vehicle seized",
            "bike seized", "car seized", "took my bike", "took my car",
            "towed", "towing", "vehicle confiscated", "rc", "registration",
            "took documents", "took my documents", "not returning license",
            "not returning vehicle", "kept my bike", "kept my car",
        ],
        "title": "License or Vehicle Seized by Police",
        "summary": "Police can only seize your license or vehicle under specific legal provisions. Illegal seizure without a receipt is an offence.",
        "steps": [
            "Ask the officer to issue a written seizure memo/receipt — this is MANDATORY under law.",
            "The seizure memo must mention: reason for seizure, officer's name & badge number, date, time, and condition of the vehicle.",
            "If they refuse to give a receipt, note the officer's name, badge number, station, and take photos/videos.",
            "Under the Motor Vehicles Act, only specific officers (not every constable) can seize a license.",
            "Your license can only be seized if you have committed a specific offence — ask which section you are being charged under.",
            "If the vehicle is towed, you are entitled to get it back upon paying the applicable fine/challan — they cannot hold it indefinitely.",
            "Go to the police station and file a written application for return of your license/vehicle.",
            "If not returned within a reasonable time, file a complaint with the SP/DCP office.",
            "You can file a complaint on the traffic police helpline of your city.",
            "As a last resort, approach the local court for an order directing return of your property.",
            "IMPORTANT: Pay the legitimate fine/challan if you violated traffic rules, but demand a proper receipt.",
        ],
        "relevant_laws": [
            "Motor Vehicles Act, 1988 — Section 206 (power to seize documents)",
            "Motor Vehicles Act, 1988 — Section 207 (power to detain vehicles)",
            "Motor Vehicles Act, 1988 — Section 200 (compounding of offences)",
            "CrPC — Section 102 (power of police officer to seize property) / BNSS Section 106",
            "IPC — Section 384 (extortion) / BNS Section 308 — if seizure is used to extort money",
        ],
    },

    # ═══════════════════════════════════════════
    # CONSUMER RIGHTS
    # ═══════════════════════════════════════════
    {
        "id": "consumer_defective_product",
        "category": "consumer",
        "keywords": [
            "defective", "product", "refund", "replacement", "warranty",
            "broken", "faulty", "consumer", "bought", "purchase",
            "not working", "fraud", "cheated", "seller",
        ],
        "title": "Defective Product / Consumer Fraud",
        "summary": "The Consumer Protection Act, 2019 provides strong remedies for defective products and unfair trade practices.",
        "steps": [
            "Keep all purchase receipts, warranty cards, and product packaging as evidence.",
            "Send a written complaint (email + registered post) to the seller/manufacturer demanding refund or replacement.",
            "Give them 15-30 days to respond.",
            "If unresolved, file a complaint on the National Consumer Helpline: 1800-11-4000 or consumerhelpline.gov.in.",
            "For amounts up to ₹1 crore: file in District Consumer Disputes Redressal Forum.",
            "For ₹1 crore to ₹10 crore: file in State Consumer Disputes Redressal Commission.",
            "You can file the complaint online at edaakhil.nic.in (e-Daakhil portal).",
            "No lawyer is mandatory — you can argue your own case in consumer forums.",
            "You can claim compensation for mental agony, loss, and litigation costs.",
        ],
        "relevant_laws": [
            "Consumer Protection Act, 2019 — Section 2(6) (definition of complaint)",
            "Consumer Protection Act, 2019 — Section 34-37 (District Commission jurisdiction)",
            "Consumer Protection Act, 2019 — Section 18 (Central Consumer Protection Authority)",
            "Consumer Protection Act, 2019 — Section 2(42) (unfair trade practice)",
        ],
    },

    # ═══════════════════════════════════════════
    # PROPERTY & TENANT
    # ═══════════════════════════════════════════
    {
        "id": "tenant_illegal_eviction",
        "category": "property",
        "keywords": [
            "landlord", "eviction", "tenant", "rent", "kicked out",
            "lock changed", "thrown out", "deposit", "security deposit",
            "not returning deposit", "rental", "lease",
        ],
        "title": "Illegal Eviction or Security Deposit Issues",
        "summary": "Tenants have strong protections under state-specific Rent Control Acts and the Model Tenancy Act, 2021.",
        "steps": [
            "A landlord CANNOT evict you without a court order — self-help eviction (changing locks, cutting utilities) is illegal.",
            "If illegally locked out, file a police complaint for criminal trespass and house trespass (IPC 441/442, BNS 329/330).",
            "Send a legal notice via registered post to the landlord demanding restoration of possession.",
            "File a complaint in the Rent Controller / Rent Court in your city.",
            "If security deposit is not returned, send a legal notice and then file in civil court or consumer forum.",
            "Always keep copies of rent agreement, payment receipts, and communication records.",
            "The landlord must give adequate notice (usually 1-3 months as per agreement or state law) before asking you to vacate.",
            "Document any damage to your belongings during illegal eviction.",
        ],
        "relevant_laws": [
            "Model Tenancy Act, 2021 (central guidelines)",
            "State-specific Rent Control Act (varies by state)",
            "IPC — Section 441 (criminal trespass) / BNS Section 329",
            "IPC — Section 443 (lurking house-trespass) / BNS Section 331",
            "Transfer of Property Act, 1882 — Section 106 (notice to quit)",
        ],
    },

    # ═══════════════════════════════════════════
    # WORKPLACE / LABOUR
    # ═══════════════════════════════════════════
    {
        "id": "workplace_harassment",
        "category": "workplace",
        "keywords": [
            "harassment", "workplace", "office", "boss", "sexual harassment",
            "posh", "inappropriate", "touching", "comments", "hostile",
            "threatened at work", "fired unfairly", "wrongful termination",
        ],
        "title": "Workplace Harassment / Sexual Harassment (POSH)",
        "summary": "The POSH Act, 2013 mandates every employer with 10+ employees to have an Internal Complaints Committee (ICC).",
        "steps": [
            "Document every incident — dates, times, witnesses, screenshots of messages.",
            "File a written complaint with your company's Internal Complaints Committee (ICC) within 3 months of the incident.",
            "If your company has no ICC or fewer than 10 employees, complain to the Local Complaints Committee (LCC) at the district level.",
            "The ICC must complete inquiry within 90 days.",
            "You can also file a police complaint (FIR) if the harassment involves criminal acts.",
            "For non-sexual workplace harassment or wrongful termination, approach the Labour Commissioner.",
            "You can file a case in the Labour Court / Industrial Tribunal for wrongful termination.",
            "Consult a lawyer specializing in employment law for complex cases.",
        ],
        "relevant_laws": [
            "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
            "IPC — Section 354A (sexual harassment) / BNS Section 75",
            "IPC — Section 509 (word, gesture or act intended to insult modesty) / BNS Section 79",
            "Industrial Disputes Act, 1947 — Section 25F (conditions for retrenchment)",
        ],
    },

    # ═══════════════════════════════════════════
    # RTI (RIGHT TO INFORMATION)
    # ═══════════════════════════════════════════
    {
        "id": "rti_filing",
        "category": "rti",
        "keywords": [
            "rti", "right to information", "government", "information",
            "public authority", "transparency", "documents", "records",
            "government scheme", "ration card", "passport delay",
        ],
        "title": "Filing an RTI Application",
        "summary": "The RTI Act, 2005 empowers any citizen to request information from public authorities within 30 days.",
        "steps": [
            "Identify the correct public authority (department/ministry) that holds the information.",
            "Write an RTI application addressed to the Public Information Officer (PIO) of that authority.",
            "Pay ₹10 as application fee (BPL applicants are exempt).",
            "You can file RTI online at rtionline.gov.in for central government departments.",
            "For state departments, check if your state has an online RTI portal.",
            "The PIO must respond within 30 days (48 hours for matters involving life and liberty).",
            "If no response or unsatisfactory response, file a First Appeal with the First Appellate Authority within 30 days.",
            "If still unresolved, file a Second Appeal with the State/Central Information Commission.",
            "Keep copies of all applications, receipts, and responses.",
        ],
        "relevant_laws": [
            "Right to Information Act, 2005 — Section 6 (request for information)",
            "RTI Act — Section 7 (disposal of request, 30-day limit)",
            "RTI Act — Section 19 (appeal process)",
            "RTI Act — Section 20 (penalties for non-compliance by PIO)",
        ],
    },

    # ═══════════════════════════════════════════
    # CYBER CRIME
    # ═══════════════════════════════════════════
    {
        "id": "cyber_fraud",
        "category": "cyber",
        "keywords": [
            "online fraud", "cyber", "scam", "scammed", "scammer",
            "hacked", "hacking", "phishing",
            "upi fraud", "upi", "bank fraud", "otp", "identity theft",
            "online scam", "online money", "online cheated",
            "social media", "fake account", "online threat", "cyber bullying",
            "morphed photos", "blackmail online", "internet fraud",
            "digital fraud", "payment fraud", "gpay", "phonepe", "paytm",
        ],
        "title": "Cyber Crime / Online Fraud",
        "summary": "The IT Act, 2000 and BNS provide legal remedies for cyber crimes including fraud, hacking, and online harassment.",
        "steps": [
            "Immediately call the Cyber Crime Helpline: 1930 (available 24/7).",
            "File an online complaint at cybercrime.gov.in — the national cyber crime reporting portal.",
            "For financial fraud: call your bank IMMEDIATELY to block the account/card and request a transaction reversal.",
            "Under RBI guidelines, if you report unauthorized transactions within 3 days, your liability is limited.",
            "Take screenshots of all evidence — messages, transaction IDs, emails, fake profiles.",
            "File an FIR at the nearest police station or Cyber Crime Cell.",
            "Do NOT delete any messages or evidence from your phone/computer.",
            "For social media crimes, also report the content to the platform (Instagram, Facebook, etc.).",
            "If blackmailed with photos/videos, do NOT pay — report to police immediately.",
        ],
        "relevant_laws": [
            "Information Technology Act, 2000 — Section 66 (computer-related offences)",
            "IT Act — Section 66C (identity theft)",
            "IT Act — Section 66D (cheating by impersonation using computer resource)",
            "IT Act — Section 67 (publishing obscene material)",
            "IPC — Section 420 (cheating) / BNS Section 318",
            "RBI Circular on Unauthorized Electronic Banking Transactions (2017)",
        ],
    },

    # ═══════════════════════════════════════════
    # DOMESTIC VIOLENCE
    # ═══════════════════════════════════════════
    {
        "id": "domestic_violence",
        "category": "domestic",
        "keywords": [
            "domestic violence", "husband", "wife", "beating", "abuse",
            "dowry", "in-laws", "marital", "cruelty", "domestic abuse",
            "protection order", "women helpline",
        ],
        "title": "Domestic Violence / Dowry Harassment",
        "summary": "The Protection of Women from Domestic Violence Act, 2005 provides civil remedies including protection orders, residence orders, and monetary relief.",
        "steps": [
            "Call Women Helpline: 181 (available 24/7 in most states) or National Emergency: 112.",
            "If in immediate danger, go to the nearest police station and file an FIR.",
            "Contact a Protection Officer in your district (mandated under the DV Act).",
            "You can file a Domestic Incident Report (DIR) with the Protection Officer or a registered NGO.",
            "Apply to the Magistrate for a Protection Order (stops the abuser from committing further violence).",
            "You can also seek a Residence Order (right to live in the shared household, even if it is in the abuser's name).",
            "Seek monetary relief and compensation through the Magistrate.",
            "For dowry harassment, file an FIR under Section 498A IPC / Section 85-86 BNS.",
            "Reach out to NCW (National Commission for Women): ncw.nic.in or helpline 7827-170-170.",
        ],
        "relevant_laws": [
            "Protection of Women from Domestic Violence Act, 2005",
            "IPC — Section 498A (cruelty by husband or relatives) / BNS Section 85",
            "Dowry Prohibition Act, 1961",
            "IPC — Section 304B (dowry death) / BNS Section 80",
            "CrPC — Section 125 (maintenance) / BNSS Section 144",
        ],
    },

    # ═══════════════════════════════════════════
    # NOISE / NEIGHBOURHOOD
    # ═══════════════════════════════════════════
    {
        "id": "noise_pollution",
        "category": "environment",
        "keywords": [
            "noise", "loud music", "construction", "neighbour", "neighbor",
            "loudspeaker", "dj", "party", "night", "disturbance",
            "pollution", "festival noise",
        ],
        "title": "Noise Pollution / Neighbourhood Disturbance",
        "summary": "The Noise Pollution Rules, 2000 and the Environment Protection Act regulate noise levels and give citizens the right to a peaceful environment.",
        "steps": [
            "Call the police (100/112) if noise continues after 10 PM — it is a punishable offence.",
            "File a written complaint to the local police station about ongoing noise issues.",
            "Complain to the local Municipal Corporation / Pollution Control Board.",
            "Loudspeakers cannot be used between 10 PM and 6 AM (Supreme Court ruling).",
            "File a complaint on the state Pollution Control Board's website.",
            "For construction noise, check if the builder has necessary environmental clearances.",
            "You can file a civil suit for nuisance in the local court.",
            "Document the disturbance with timestamps, audio/video recordings.",
        ],
        "relevant_laws": [
            "Noise Pollution (Regulation and Control) Rules, 2000",
            "Environment Protection Act, 1986",
            "IPC — Section 268 (public nuisance) / BNS Section 292",
            "IPC — Section 290 (punishment for public nuisance) / BNS Section 294",
            "In Re: Noise Pollution (2005) — Supreme Court guidelines",
        ],
    },
]
