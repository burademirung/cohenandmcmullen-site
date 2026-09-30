#!/usr/bin/env python3
"""Static site builder for Cohen & McMullen, P.A.

Generates every page as /<slug>/index.html with shared chrome, per-page film,
JSON-LD (LegalService, Person, Service, FAQPage, VideoObject, BreadcrumbList),
plus sitemap.xml, robots.txt, llms.txt and _redirects.

Run:  python3 build.py
"""
import html
import json
import os
from datetime import date

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
BASE = "https://www.cohenandmcmullen.com"
TODAY = date.today().isoformat()
FILM_DATE = "2026-09-30"

FIRM = "Cohen & McMullen, P.A."
PHONE = "(954) 523-7774"
PHONE_TEL = "+19545237774"
TOLLFREE = "(888) COHEN-LAW"
TOLLFREE_TEL = "+18882643652"
EMAIL = "info@floridajusticefirm.com"
FAX = "954-523-2656"
MOTTO_LA = "Si vis pacem, para bellum"
MOTTO_EN = "If you want peace, prepare for war"
SOCIAL = [
    "https://www.instagram.com/cohen_mcmullen/",
    "https://www.facebook.com/cohenandmcmullen/",
]

OFFICES = {
    "fort-lauderdale": {
        "name": "Fort Lauderdale",
        "street": "1132 SE 3rd Avenue",
        "city": "Fort Lauderdale", "state": "FL", "zip": "33316",
        "map": "https://www.google.com/maps/search/?api=1&query=1132+SE+3rd+Avenue+Fort+Lauderdale+FL+33316",
        "embed": "https://www.google.com/maps?q=1132+SE+3rd+Avenue,+Fort+Lauderdale,+FL+33316&output=embed",
        "film": "fort-lauderdale",
        "areas": ["Fort Lauderdale, FL", "Broward County, FL", "Miami-Dade County, FL", "Palm Beach County, FL"],
    },
    "new-york": {
        "name": "New York",
        "street": "745 Fifth Avenue, Suite 500",
        "city": "New York", "state": "NY", "zip": "10151",
        "map": "https://www.google.com/maps/search/?api=1&query=745+Fifth+Avenue+Suite+500+New+York+NY+10151",
        "embed": "https://www.google.com/maps?q=745+Fifth+Avenue,+New+York,+NY+10151&output=embed",
        "film": "new-york",
        "areas": ["New York, NY", "Manhattan"],
    },
}

# Films (Runway Gen-4.5). key -> description used for VideoObject
FILMS = {
    "courtroom": "An empty American courtroom at night, lit by shafts of golden light.",
    "courthouse": "The stone steps and columns of a federal courthouse at blue hour, in the rain.",
    "boardroom": "A walnut boardroom table high above a financial district at night.",
    "pen": "A gold-nib fountain pen signing a contract beside an embossed seal.",
    "lily": "Rain on a window at dusk, a white lily and a lit candle on the sill.",
    "lights": "Emergency lights reflecting on wet asphalt on a city street at night.",
    "forensic": "A fractured mechanical part examined under a lighted lens in an engineering lab.",
    "sword": "A steel sword with a gold hilt resting on leather-bound law books.",
    "library": "A two-story law library at night with brass ladders and banker's lamps.",
    "fort-lauderdale": "Aerial view of Fort Lauderdale's waterways and skyline at golden hour.",
    "new-york": "Aerial view of Fifth Avenue in Manhattan at blue hour.",
    "los-angeles": "Aerial view of Los Angeles at dusk as the city lights come on.",
    "office": "A private law office at night, a desk lamp glowing against a rain-streaked city window.",
    "card": "An unbranded metal credit card and a billing statement on black marble under a sweep of light.",
    "chess": "A marble and brass chess king under a single spotlight.",
    "evidence": "Case files, photographs and a gavel spread across a table under a spotlight.",
    "crest": "The gold Cohen & McMullen crest: shield, sword and interlocking M and C monogram, catching a sweep of light.",
}


def poster(key, small=False):
    return f"/assets/img/film/{key}{'-sm' if small else ''}.webp"


def vsrc(key, small=False):
    return f"/assets/video/{key}{'-sm' if small else ''}.mp4"


def e(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# People (source: cohenandmcmullen.com bios; nothing added)
# ---------------------------------------------------------------------------
PEOPLE = {
    "bradford-cohen": {
        "name": "Bradford M. Cohen", "role": "Partner", "img": "/assets/img/bradford-cohen.webp",
        "short": "A trial lawyer of more than twenty-five years, in criminal and civil courtrooms.",
        "practices": ["commercial-litigation", "criminal-defense", "wrongful-death", "catastrophic-injury", "contracts-corporate-formation"],
        "bio": [
            "Bradford Cohen is a trial lawyer with more than twenty-five years of litigation and trial experience representing individuals, corporations and politicians in a vast array of legal matters. He served as President of the Broward Association of Criminal Defense Lawyers and received the triple “Hat Trick” for nine acquittals in a row.",
            "He has tried federal, state and administrative cases throughout the United States and moves between criminal and civil jury trials without losing a step. He takes a holistic approach to the law: sound legal advice and strategy, attention to the psychological weight of litigation, and complete transparency with the client about every decision.",
            "Mr. Cohen began his career in the public sector before heading the trial division of a major commercial litigation firm, where he focused on complex commercial litigation, banking regulation, UCC law and transactional matters such as contract formation and negotiation. He then opened his own practice in criminal defense, contracts and business formation, representing Fortune 500 organizations, musicians, athletes, politicians and other public figures.",
            "He has built and exited more than thirty-five businesses, and early-stage companies call on him for what he calls the “three P’s”: policy, procedure and process. He is a rated chess player, a car collector and a philanthropist supporting justice reform and children’s causes.",
            "He is regularly asked for legal commentary on high-profile cases and has appeared on Law&Crime Network, CNBC, NBC, The Dan Abrams Show, Nancy Grace, Fox News, CNN and Celebrity Justice. His clients have included President Donald Trump.",
        ],
        "pull": "From the public sector, to heading a commercial trial division, to his own practice.",
        "meta": "Bradford M. Cohen, partner at Cohen & McMullen, P.A. Trial lawyer of more than twenty-five years in criminal defense and commercial litigation.",
        "education": ["J.D., Nova Southeastern University, Shepard Broad College of Law", "B.S.B.A., Western New England College"],
        "bars": ["The Florida Bar", "New York Bar", "District of Columbia Bar"],
        "courts": ["U.S. District Court, District of Puerto Rico", "U.S. District Court, Southern District of Florida", "U.S. District Court, Middle District of Florida", "Supreme Court of Florida", "United States Tax Court", "U.S. Court of Appeals for the Eleventh Circuit"],
        "memberships": ["Florida Association of Criminal Defense Lawyers", "National Association of Criminal Defense Lawyers", "Broward County Bar Association", "Broward Association of Criminal Defense Lawyers, former President"],
        "awards": ["American Jurisprudence Award for Criminal Justice", "Super Lawyers Rising Star, 2009", "Nominated for The Best Lawyers in America, 2008 and 2009", "Hat Trick Award for three consecutive not-guilty verdicts", "National Association of Distinguished Counsel, Nation’s Top One Percent, 2015", "The National Trial Lawyers, Top 100 Criminal Defense Attorneys, 2016"],
        "media": ["Law&Crime Network", "CNBC", "NBC", "The Dan Abrams Show", "Nancy Grace", "Fox News", "CNN", "Celebrity Justice"],
        "alumni": ["Nova Southeastern University Shepard Broad College of Law", "Western New England College"],
    },
    "michael-mcmullen": {
        "name": "Michael J. McMullen", "role": "Partner", "img": "/assets/img/michael-mcmullen.webp",
        "short": "Raised in Fort Lauderdale. Commercial litigation, catastrophic injury, contracts and technology companies.",
        "practices": ["commercial-litigation", "wrongful-death", "catastrophic-injury", "contracts-corporate-formation", "criminal-defense"],
        "bio": [
            "Michael J. McMullen focuses his practice on commercial litigation, catastrophic injury and wrongful death, contractual matters and criminal defense.",
            "He grew up in Fort Lauderdale, attended Saint Thomas Aquinas High School and graduated from the University of Central Florida with a B.S.B.A. in Finance. He earned his law degree at the University of Miami School of Law while clerking for highly regarded trial attorneys on criminal matters, including complex financial crimes. That early view of the justice system set the course of his career: fighting for people and businesses harmed by the wrongdoing of others.",
            "Mr. McMullen represents his clients with vigor and uses his advocacy and negotiation skills on his clients’ behalf. He also has extensive experience with e-commerce, software (SaaS) and subscription companies, covering contract review, due diligence, M&A planning and data privacy.",
            "He is licensed in the State of Florida, the U.S. District Courts for the Southern and Middle Districts of Florida, U.S. Immigration Court and U.S. Bankruptcy Court, and represents individuals and businesses throughout South Florida, including Broward, Miami-Dade and Palm Beach counties.",
        ],
        "pull": "Fighting for people and businesses harmed by the wrongdoing of others.",
        "meta": "Michael J. McMullen, partner at Cohen & McMullen, P.A. Commercial litigation, catastrophic injury, wrongful death and contracts in South Florida.",
        "education": ["J.D., University of Miami School of Law", "B.S.B.A. in Finance, University of Central Florida"],
        "bars": ["The Florida Bar"],
        "courts": ["U.S. District Court, Southern District of Florida", "U.S. District Court, Middle District of Florida", "United States Immigration Court", "United States Bankruptcy Court", "U.S. Court of Appeals for the Eleventh Circuit"],
        "memberships": ["American Association for Justice", "Broward County Justice Association", "Broward County Bar Association"],
        "awards": [],
        "media": [],
        "alumni": ["University of Miami School of Law", "University of Central Florida"],
    },
    "andrew-courtney": {
        "name": "Andrew B. Courtney", "role": "Partner", "img": "/assets/img/andrew-courtney.webp",
        "short": "Former lead felony prosecutor in Broward County. Now he defends.",
        "practices": ["criminal-defense", "commercial-litigation", "contracts-corporate-formation"],
        "bio": [
            "Andrew B. Courtney’s practice focuses on criminal defense, commercial litigation and contractual matters. Born and raised in the Bronx, New York, he earned his Bachelor of Science in Criminal Justice and Writing at the University of Scranton in Pennsylvania, then made South Florida his home while attending the Shepard Broad College of Law at Nova Southeastern University.",
            "In law school he was Vice President of the Nova Trial Association, where he excelled in mock trial competition, and worked in Nova’s Family Law Clinic helping clients of limited means with matters from marital dissolution to child custody hearings.",
            "Mr. Courtney sharpened his litigation skills as an Assistant State Attorney in the Seventeenth Judicial Circuit in and for Broward County. He started in misdemeanor court and rose to lead prosecutor in the felony trial unit, trying cases ranging from DUI to murder.",
            "Before joining Cohen & McMullen, P.A., he gained extensive civil litigation experience at boutique firms focused on personal injury, contractual disputes and estate planning, and he is known for strategies tailored to the needs of each client.",
        ],
        "pull": "He rose from misdemeanor court to lead prosecutor in the felony trial unit.",
        "meta": "Andrew B. Courtney, partner at Cohen & McMullen, P.A. Former lead felony prosecutor in Broward County. Criminal defense and commercial litigation.",
        "education": ["J.D., Nova Southeastern University, Shepard Broad College of Law", "B.S., Criminal Justice and Writing, University of Scranton"],
        "bars": ["The Florida Bar", "District of Columbia Bar"],
        "courts": ["U.S. District Court, Southern District of Florida"],
        "memberships": ["Broward County Justice Association", "Broward County Bar Association"],
        "awards": [],
        "media": [],
        "alumni": ["Nova Southeastern University Shepard Broad College of Law", "University of Scranton"],
    },
    "ethan-strauss": {
        "name": "Ethan J. Strauss", "role": "Associate", "img": "/assets/img/ethan-strauss.webp",
        "short": "Summa cum laude, Nova Law Review, and former judicial intern. Personal injury, commercial litigation and defense.",
        "practices": ["catastrophic-injury", "commercial-litigation", "criminal-defense"],
        "bio": [
            "Ethan J. Strauss focuses his practice on personal injury, commercial litigation and criminal defense.",
            "Born in New York City and raised in North Miami Beach, Florida, he attended Dr. Michael M. Krop Senior High School and graduated from the University of South Florida with a Bachelor of Science in Finance. He earned his law degree summa cum laude from the Shepard Broad College of Law at Nova Southeastern University, graduating in the top seven percent of his class.",
            "In law school he was a member of the Nova Law Review, the Nova Trial Association and Nova’s Moot Court Team. He served as a judicial intern for the Honorable Thomas J. Coleman and as a law clerk at Cohen & McMullen, P.A.",
            "Mr. Strauss understands the complexities of the litigation process and does not stop working until the job is done. His experience and drive put him in a strong position to advocate for his clients. He is licensed in the State of Florida and the U.S. District Court for the Southern District of Florida.",
        ],
        "pull": "He does not stop working until the job is done.",
        "meta": "Ethan J. Strauss, associate at Cohen & McMullen, P.A. Summa cum laude Nova Law graduate handling personal injury, commercial litigation and defense.",
        "education": ["J.D., summa cum laude, Nova Southeastern University, Shepard Broad College of Law", "B.S. in Finance, University of South Florida"],
        "bars": ["The Florida Bar"],
        "courts": ["U.S. District Court, Southern District of Florida"],
        "memberships": ["American Association for Justice", "Broward County Justice Association", "Broward County Bar Association"],
        "awards": [],
        "media": [],
        "alumni": ["Nova Southeastern University Shepard Broad College of Law", "University of South Florida"],
    },
}
PEOPLE_ORDER = ["bradford-cohen", "michael-mcmullen", "andrew-courtney", "ethan-strauss"]

# ---------------------------------------------------------------------------
# Practice areas
# ---------------------------------------------------------------------------
PRACTICES = {
    "criminal-defense": {
        "name": "Criminal Defense", "film": "courthouse",
        "h1": "Criminal defense in state and federal court",
        "title": "Criminal Defense Attorneys in Fort Lauderdale & New York",
        "desc": "Cohen & McMullen, P.A. defends people charged or investigated in Florida state court and federal court. Former prosecutor on staff. Free case evaluation: (954) 523-7774.",
        "tile": "Charged, or under investigation. Defense in state and federal courts.",
        "lede": "When you are charged with a crime, or suspect you are being investigated, the most important thing you can do is speak with an experienced criminal defense attorney before you speak with anyone else.",
        "answer": "If you are under investigation or have been charged, stop talking to investigators and call a defense attorney. Cohen & McMullen, P.A. tries criminal cases in Florida state court and federal court, from misdemeanors to serious felonies.",
        "body": [
            ("How does the firm defend criminal cases?", [
                "Our attorneys have significant criminal trial experience in both state and federal courts. Bradford M. Cohen, a former President of the Broward Association of Criminal Defense Lawyers, received the triple “Hat Trick” for nine acquittals in a row. Prior results do not guarantee a similar outcome. Andrew B. Courtney was a lead felony prosecutor in Broward County and tried cases from DUI to murder.",
                "We prepare every case with a jury in mind. That preparation is designed to strengthen your position in every negotiation, and it is what protects you if the case does go to trial.",
            ]),
        ],
        "matters": [
            ("Federal investigations and charges", "Grand jury matters, indictments and federal trials"),
            ("White-collar and financial crimes", "Fraud, complex financial allegations and regulatory exposure"),
            ("Violent felonies", "From aggravated assault to homicide"),
            ("Drug offenses", "Possession, distribution and trafficking allegations"),
            ("DUI and traffic crimes", "Arrest, license consequences and trial"),
            ("Administrative proceedings", "Hearings that affect licenses and livelihoods"),
        ],
        "faq": [
            ("Should I talk to the police if I am being investigated?", "You have the constitutional right to remain silent and the right to an attorney. Clearly say that you are invoking your right to remain silent and that you want a lawyer, then stop answering questions. Statements made to investigators, even ones you believe are harmless, are often the strongest evidence in a case."),
            ("What is the difference between state and federal charges?", "State charges are brought by a State Attorney under Florida law in state court. Federal charges are brought by the U.S. Attorney’s Office under federal law in federal district court, often after a longer investigation. The procedures and sentencing rules differ, and our attorneys are admitted to practice in both systems."),
            ("Can charges be dropped before trial?", "Yes. Prosecutors can decline to file or dismiss charges, and the defense can move to suppress unlawfully obtained evidence or dismiss a legally deficient case. Early involvement by a defense attorney gives the most room to shape the outcome."),
            ("Do you offer a free case evaluation?", f"Yes. Call {PHONE} or send a short description of your situation through our contact page and an attorney will follow up."),
        ],
        "team": ["bradford-cohen", "andrew-courtney", "michael-mcmullen", "ethan-strauss"],
    },
    "commercial-litigation": {
        "name": "Commercial Litigation", "film": "boardroom",
        "h1": "Commercial litigation for businesses and their owners",
        "title": "Commercial Litigation Attorneys in Fort Lauderdale & New York",
        "desc": "Business disputes, partner and shareholder conflicts, and contract litigation. Cohen & McMullen, P.A. takes on the largest corporations. Free case evaluation: (954) 523-7774.",
        "tile": "Partner disputes, broken deals and corporate adversaries. We litigate to the finish.",
        "lede": "Because of the intimate nature of closely held companies, disputes often arise. For many owners the business is their passion, their dream and their livelihood, and we treat it that way.",
        "answer": "Commercial litigation covers lawsuits between businesses, owners and partners: breach of contract, shareholder and partnership disputes, and business torts. Cohen & McMullen, P.A. litigates these cases in Florida and New York, including against large corporations.",
        "body": [
            ("How does the firm handle business disputes?", [
                "Our team of trial lawyers gives clients the ability to challenge the largest of corporations. Bradford M. Cohen previously headed the trial division of a major commercial litigation firm, focusing on complex commercial litigation, banking regulation and UCC law.",
                "When a dispute is really about the future of a company, we work to make the transition as smooth as possible, whether that means a negotiated exit or a verdict.",
            ]),
        ],
        "matters": [
            ("Partnership and shareholder disputes", "Closely held companies, buyouts and deadlock"),
            ("Breach of contract", "Enforcing agreements and defending against claims"),
            ("Banking and UCC matters", "Commercial paper, secured transactions and lending disputes"),
            ("Technology and SaaS disputes", "E-commerce, subscription and software agreements"),
            ("Business torts", "Fraud, interference and unfair competition"),
        ],
        "faq": [
            ("What should I do first in a dispute with my business partner?", "Gather your operating or shareholder agreement, financial records and key communications, and speak with a litigator before taking unilateral action. Many agreements set out buyout, notice or dispute-resolution procedures that shape what happens next."),
            ("Can a small company realistically sue a large corporation?", "Yes. Outcomes turn on evidence and preparation, not company size. Our firm was built so clients can take on the largest corporations with a team of experienced trial lawyers behind them."),
            ("Do commercial cases always go to trial?", "No. Many resolve through negotiation, mediation or dispositive motions. Preparing each case for trial is what gives a client leverage in every one of those settings."),
        ],
        "team": ["bradford-cohen", "michael-mcmullen", "andrew-courtney", "ethan-strauss"],
    },
    "contracts-corporate-formation": {
        "name": "Contracts & Corporate Formation", "film": "pen",
        "h1": "Contracts and corporate formation that prevent the fight",
        "title": "Business Contracts & Corporate Formation Lawyers in Florida",
        "desc": "Contracts drafted to prevent disputes, plus business formation, due diligence and M&A planning for Florida companies and individuals.",
        "tile": "Agreements designed by trial lawyers, to hold up if they are ever tested.",
        "lede": "Our goal is to create and design contractual agreements that prevent disputes and avoid costly litigation, for businesses and individuals throughout Florida.",
        "answer": "The best contract is one that is never litigated. Cohen & McMullen, P.A. drafts, negotiates and reviews agreements and forms companies for businesses and individuals throughout Florida, with trial lawyers who know how contracts fail in court.",
        "body": [
            ("How does trial experience shape our contracts?", [
                "We see every day how agreements break down in litigation. That experience goes into the documents we draft: clear obligations, workable remedies and dispute-resolution terms that protect you if things go wrong.",
                "Bradford M. Cohen has built and exited more than thirty-five businesses and advises early-stage companies on policy, procedure and process. Michael J. McMullen advises e-commerce, software (SaaS) and subscription companies on contract review, due diligence, M&A planning and data privacy.",
            ]),
        ],
        "matters": [
            ("Business formation", "Choosing and structuring the right entity"),
            ("Operating and shareholder agreements", "Ownership, control, buyouts and exits"),
            ("Commercial contracts", "Drafting, negotiation and review"),
            ("Due diligence and M&A planning", "Preparing to buy, sell or raise"),
            ("Technology and data privacy", "SaaS, subscription and e-commerce terms"),
        ],
        "faq": [
            ("When should I involve a lawyer in a business contract?", "Before you sign. Changing terms during negotiation is far cheaper than litigating them later, and a lawyer can spot missing protections such as limitation of liability, termination rights and dispute-resolution clauses."),
            ("Do I need an operating or shareholder agreement for a small company?", "Florida does not require one, but if there is more than one owner it is strongly advisable. It sets out who controls decisions, how profits are shared and what happens if an owner leaves, dies or wants out, which are the questions behind most business-partner disputes."),
            ("Can you review a contract someone else drafted?", "Yes. We review, redline and negotiate agreements prepared by the other side and explain in plain language what you are agreeing to."),
        ],
        "team": ["bradford-cohen", "michael-mcmullen", "andrew-courtney"],
    },
    "wrongful-death": {
        "name": "Wrongful Death", "film": "lily",
        "h1": "Wrongful death claims for families who deserve answers",
        "title": "Wrongful Death Attorneys in Fort Lauderdale, Florida",
        "desc": "When a loved one is taken through negligence or misconduct, Cohen & McMullen, P.A. holds individuals and corporations accountable. Free case evaluation: (954) 523-7774.",
        "tile": "When negligence takes someone you love, we pursue accountability.",
        "lede": "The death of a loved one is one of the hardest things a person can face. When that loss is caused by the negligence or misconduct of another person or corporation, it demands justice.",
        "answer": "A wrongful death claim holds a person or company accountable when their negligence or misconduct causes a death. In Florida the claim is brought by the personal representative of the estate on behalf of the family, and strict filing deadlines apply, so families should speak with an attorney early.",
        "body": [
            ("How does the firm help families after a wrongful death?", [
                "At Cohen & McMullen, P.A. we hold our family and ethical values higher than anything else. We handle the investigation, the insurers and the litigation so families can grieve, and we pursue those responsible with the full weight of a trial team.",
                "We focus on holding individuals and corporations responsible for their negligence or misconduct while pursuing the best possible outcome for the family.",
            ]),
        ],
        "matters": [
            ("Vehicle and trucking collisions", "Drivers, fleets and the companies behind them"),
            ("Dangerous products", "Manufacturers, distributors and sellers"),
            ("Unsafe property", "Negligent security and hazardous conditions"),
            ("Corporate and professional negligence", "When institutions fail the people who rely on them"),
        ],
        "faq": [
            ("Who can bring a wrongful death claim in Florida?", "Under Florida’s Wrongful Death Act, the claim is filed by the personal representative of the deceased person’s estate on behalf of the estate and the survivors defined by statute, such as a spouse, children, parents and certain dependent relatives. Which survivors may recover, and for what, depends on the relationship and the facts."),
            ("How long does a family have to file?", "Florida law sets a strict deadline that is generally measured from the date of death, and some claims involving government entities have additional notice requirements. Speak with an attorney as soon as possible so evidence is preserved and no deadline is missed."),
            ("What does it cost to talk to your firm?", f"Your first case evaluation is free. Call {PHONE} or reach us through the contact page."),
        ],
        "team": ["michael-mcmullen", "bradford-cohen", "ethan-strauss"],
    },
    "catastrophic-injury": {
        "name": "Catastrophic Injury", "film": "lights",
        "h1": "Catastrophic injury representation when everything changes",
        "title": "Catastrophic Injury Lawyers in Fort Lauderdale, Florida",
        "desc": "Brain, spinal cord and life-altering injuries caused by negligence. Cohen & McMullen, P.A. fights for injured people and their families. Free case evaluation: (954) 523-7774.",
        "tile": "Life-altering injuries caused by someone else’s negligence. We fight for what you need.",
        "lede": "A catastrophic injury can happen without warning and leave a person and their family in a dire position, facing significant medical expenses and an uncertain future.",
        "answer": "A catastrophic injury is one that permanently changes a person’s life, such as a brain or spinal cord injury, amputation or severe burns. If another person’s negligence or misconduct caused it, you may be entitled to compensation for medical care, lost income and future needs.",
        "body": [
            ("What does a catastrophic injury claim pay for?", [
                "Our attorneys are committed to fighting for the rights of people injured by another’s negligence or misconduct. That means documenting the full, lifelong cost of an injury, not just the bills already received, and making the responsible party answer for it.",
                "If you or a loved one has suffered a catastrophic injury, do not wait to contact us. Early action preserves evidence and protects your rights.",
            ]),
        ],
        "matters": [
            ("Traumatic brain injury", "Cognitive, emotional and long-term care needs"),
            ("Spinal cord injury and paralysis", "Lifetime medical and accessibility costs"),
            ("Amputation and severe burns", "Surgeries, prosthetics and recovery"),
            ("Serious vehicle and trucking crashes", "Commercial carriers and insurers"),
        ],
        "faq": [
            ("What compensation is available after a catastrophic injury?", "Depending on the facts, compensation can include past and future medical care, lost wages and lost earning capacity, rehabilitation and home modifications, and pain and suffering. Any award may be reduced by the injured person’s share of fault."),
            ("Is there a deadline to file an injury claim in Florida?", "Yes. Florida’s 2023 tort reform shortened the deadline for most negligence claims arising after March 24, 2023, and Florida now bars recovery if the injured person is found more than half at fault. Separate deadlines and notice rules apply to claims against government entities. Contact an attorney promptly."),
            ("Should I speak with the other side’s insurance company?", "Be cautious. Insurers may ask for recorded statements or offer an early settlement before the full extent of an injury is known. Speak with an attorney before giving a statement or signing anything."),
        ],
        "team": ["michael-mcmullen", "bradford-cohen", "ethan-strauss"],
    },
    "products-liability": {
        "name": "Products Liability", "film": "forensic",
        "h1": "Products liability claims against the companies behind defective products",
        "title": "Defective Product & Products Liability Lawyers in Florida",
        "desc": "Injured by a defective product? Cohen & McMullen, P.A. determines whether the manufacturer, distributor or seller is responsible. Free case evaluation.",
        "tile": "Defective products, dangerous designs and missing warnings. We find who is responsible.",
        "lede": "If you or a loved one has been injured by a dangerous or defective product, contact an experienced products liability attorney right away. As a member of the unsuspecting public, you may be entitled to compensation.",
        "answer": "A products liability claim seeks compensation from the companies that design, make, distribute or sell a product that injures someone because it was defective. Keep the product, its packaging and your receipts, and speak with an attorney before returning or discarding anything.",
        "body": [
            ("How is a products liability case built?", [
                "We have the knowledge and skills to determine whether the manufacturer, distributor or seller is responsible for a defective product. That starts with preserving the product itself and bringing in the right experts to examine how and why it failed.",
                "Product cases are often brought against large, well-funded corporations. Our team is prepared to meet them.",
            ]),
        ],
        "matters": [
            ("Design defects", "Products that are dangerous even when made as intended"),
            ("Manufacturing defects", "Flaws introduced when a specific product was made"),
            ("Failure to warn", "Missing or inadequate instructions and warnings"),
            ("Vehicle, equipment and consumer products", "From auto parts to household goods"),
        ],
        "faq": [
            ("Who can be held responsible for a defective product?", "Responsibility can extend to the manufacturer, the maker of a component part, the distributor and the retailer that sold it, depending on where the defect arose."),
            ("What should I do with the product that injured me?", "Keep it, along with its packaging, manuals and proof of purchase. Do not repair, return or throw it away. The product is often the most important piece of evidence."),
            ("What if the product was recalled?", "A recall can support a claim, but it is not required. Many defective products are never recalled, and a recall does not by itself settle who is responsible."),
        ],
        "team": ["michael-mcmullen", "bradford-cohen"],
    },
}
FLORIDA = {
 "criminal-defense": [
  "After an arrest, Florida rules require a first appearance before a judge within twenty-four hours, where release conditions are set.",
  "State cases in Broward County are heard in the Seventeenth Judicial Circuit. Federal cases in Fort Lauderdale are heard in the U.S. District Court for the Southern District of Florida.",
  "Anything said to investigators, including in a voluntary interview, can be used as evidence. Speak with a defense attorney first."
 ],
 "commercial-litigation": [
  "Florida generally allows five years to sue on a written contract and four years on an oral one, and some claims have shorter deadlines.",
  "Operating and shareholder agreements often require notice, mediation or arbitration before a lawsuit can be filed.",
  "Preserve emails, texts and financial records as soon as a dispute begins. Destroying evidence can lead to sanctions."
 ],
 "contracts-corporate-formation": [
  "Florida companies are formed by filing with the Florida Division of Corporations, known as Sunbiz.",
  "Florida LLCs and corporations must file an annual report between January first and May first to stay active.",
  "A written agreement should say how disputes are resolved, where, and under which state’s law."
 ],
 "wrongful-death": [
  "Florida’s Wrongful Death Act allows a claim when a death is caused by another’s negligence or misconduct.",
  "The claim is brought by the personal representative of the estate, on behalf of the estate and the survivors the statute recognizes.",
  "Florida generally sets a two-year deadline from the date of death, with added notice rules for claims against government entities."
 ],
 "catastrophic-injury": [
  "Florida’s 2023 tort reform shortened the deadline for most negligence claims arising after March 24, 2023.",
  "Florida now uses modified comparative fault: an injured person found more than half at fault cannot recover.",
  "Documenting future medical care and lost earning capacity is central to the value of a catastrophic injury claim."
 ],
 "products-liability": [
  "Florida recognizes products claims based on strict liability, negligence and breach of warranty.",
  "Florida has a statute of repose that generally bars many product claims brought more than twelve years after delivery to the first buyer, with exceptions.",
  "Keep the product, its packaging and your receipts. Do not repair, return or discard it."
 ]
}
PRACTICE_ORDER = ["criminal-defense", "commercial-litigation", "contracts-corporate-formation", "wrongful-death", "catastrophic-injury", "products-liability"]
RELATED = {
    "criminal-defense": ["commercial-litigation", "contracts-corporate-formation", "wrongful-death"],
    "commercial-litigation": ["contracts-corporate-formation", "criminal-defense", "products-liability"],
    "contracts-corporate-formation": ["commercial-litigation", "criminal-defense", "catastrophic-injury"],
    "wrongful-death": ["catastrophic-injury", "products-liability", "commercial-litigation"],
    "catastrophic-injury": ["wrongful-death", "products-liability", "criminal-defense"],
    "products-liability": ["catastrophic-injury", "wrongful-death", "commercial-litigation"],
}
TILE_LAYOUT = ["tile--7", "tile--5", "tile--5", "tile--7", "tile--6", "tile--6"]

BADGES = ["badge-1.png", "badge-2.png", "badge-3.png", "badge-4.png", "badge-5.png"]
BADGE_ALT = ["Super Lawyers", "The Best Lawyers in America", "National Association of Criminal Defense Lawyers", "Florida Association of Criminal Defense Lawyers", "National Association of Distinguished Counsel, Top One Percent"]

NAV = [
    ("Home", "/", "courtroom"),
    ("Practice Areas", "/practice-areas/", "evidence"),
    ("About the Firm", "/about/", "crest"),
    ("People", "/people/", "library"),
    ("Locations", "/locations/", "fort-lauderdale"),
    ("Contact", "/contact/", "office"),
]

# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------

def film_video(key, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{poster(key)}" srcset="{poster(key, True)} 960w, {poster(key)} 1920w" sizes="100vw" alt="" width="1920" height="1080" {load} decoding="async">'
            f'<video muted loop playsinline preload="none" aria-hidden="true" data-src="{vsrc(key)}" data-src-sm="{vsrc(key, True)}"></video>')


def tile_video(key):
    return (f'<img src="{poster(key, True)}" alt="" width="960" height="540" loading="lazy" decoding="async">'
            f'<video muted loop playsinline preload="none" aria-hidden="true" data-src="{vsrc(key, True)}"></video>')


def practice_tile(slug, cls="tile--6", short=False):
    p = PRACTICES[slug]
    return f'''<a class="tile {cls}{' tile--short' if short else ''}" href="/{slug}/">
  <div class="tile__media">{tile_video(p["film"])}</div>
  <div class="tile__body">
    <h3 class="tile__title">{e(p["name"])}</h3>
    <p class="tile__text"><span>{e(p["tile"])}</span></p>
  </div>
</a>'''


def link_people(text):
    for slug in PEOPLE_ORDER:
        n = e(PEOPLE[slug]["name"])
        text = text.replace(n, f'<a class="link-line" href="/{slug}/">{n}</a>', 1)
    return text


def person_card(slug, heading="h3"):
    p = PEOPLE[slug]
    return f'''<a class="person" href="/{slug}/">
  <img src="{p["img"]}" alt="" loading="lazy" decoding="async">
  <div class="person__body"><span class="person__role">{e(p["role"])}</span><{heading} class="person__name">{e(p["name"])}</{heading}><p class="person__short">{e(p["short"])}</p><span class="person__more">Read biography</span></div>
</a>'''


def qa_block(faq):
    items = "".join(f'<details><summary><h3 class="qa__q">{e(q)}</h3></summary><div class="qa__a"><p>{e(a)}</p></div></details>' for q, a in faq)
    return f'<div class="qa" data-reveal>{items}</div>'


def cta_band(heading="Tell us what happened. We will tell you where you stand.", film="office"):
    return f'''<section class="cta" aria-labelledby="cta-h">
  <div class="film__media">{film_video(film)}</div>
  <div class="wrap cta__inner">
    <h2 id="cta-h" data-reveal>{e(heading)}</h2>
    <a class="cta__phone" href="tel:{PHONE_TEL}" data-reveal>{PHONE}</a>
    <p data-reveal>Free case evaluation. Offices in Fort Lauderdale and New York. Attorneys referring a case can call or email us directly.</p>
    <div class="film__actions" data-reveal><a class="btn btn--solid" href="/contact/">Request a free case evaluation</a><a class="btn" href="mailto:{EMAIL}">Email the firm</a></div>
  </div>
</section>'''


def blade():
    return '<div class="blade" aria-hidden="true"><span class="blade__tip"></span><span class="blade__line"></span></div>'


def hero(key, h1, lede, crumbs=None, actions=True, rail=True):
    crumb_html = ""
    if crumbs:
        parts = []
        for i, (name, url) in enumerate(crumbs):
            if i:
                parts.append('<span aria-hidden="true">/</span>')
            parts.append(f'<a href="{url}">{e(name)}</a>' if url else f'<span aria-current="page">{e(name)}</span>')
        crumb_html = f'<nav class="crumbs" aria-label="Breadcrumb" data-hero-fade>{"".join(parts)}</nav>'
    acts = ""
    if actions:
        acts = f'<div class="film__actions" data-hero-fade><a class="btn btn--solid" href="/contact/">Request a free case evaluation</a><a class="btn" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>'
    rail_html = f'<p class="film__rail" aria-hidden="true" lang="la">{MOTTO_LA}</p>' if rail else ""
    return f'''<section class="film" aria-label="Introduction">
  <div class="film__media">{film_video(key, eager=True)}</div>
  {rail_html}
  <div class="wrap film__content">
    {crumb_html}
    <h1 data-split>{e(h1)}</h1>
    <div class="film__lede"><p class="lede" data-hero-fade>{e(lede)}</p>{acts}</div>
  </div>
  <span class="scroll-cue" aria-hidden="true"></span>
</section>'''


def header(current):
    films = "".join(f'<video muted loop playsinline preload="none" data-key="{k}" data-src="{vsrc(k, True)}" aria-hidden="true"></video>' for k in dict.fromkeys(n[2] for n in NAV))
    links = []
    for i, (name, url, film) in enumerate(NAV):
        cur = ' aria-current="page"' if url == current else ""
        links.append(f'<a href="{url}" data-film="{film}" style="--i:{i}"{cur}>{e(name)}</a>')
    subs = "".join(f'<a href="/{s}/">{e(PRACTICES[s]["name"])}</a>' for s in PRACTICE_ORDER)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="header">
  <a class="brand" href="/" aria-label="{e(FIRM)} home"><img src="/assets/img/brand/lockup-320.webp" srcset="/assets/img/brand/lockup-320.webp 320w, /assets/img/brand/lockup-640.webp 640w" sizes="160px" alt="{e(FIRM)}" width="320" height="141"></a>
  <div class="header__right">
    <a class="header__phone" href="tel:{PHONE_TEL}">{PHONE}</a>
    <a class="btn btn--solid header__cta" href="/contact/">Request a free case evaluation</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-menu"><span class="menu-btn__label">Menu</span><span class="menu-btn__bars" aria-hidden="true"></span></button>
  </div>
</header>
<div class="menu" id="site-menu" role="dialog" aria-modal="true" aria-label="Site menu" data-lenis-prevent>
  <div class="menu__bg"></div><img class="menu__crest" src="/assets/img/brand/crest.webp" alt="" aria-hidden="true" loading="lazy" width="487" height="900">
  <div class="menu__films" aria-hidden="true">{films}</div>
  <div class="menu__inner">
    <nav class="menu__nav" aria-label="Main">{"".join(links)}</nav>
    <div class="menu__side">
      <p class="menu__label">Practice areas</p>
      <div class="menu__sub">{subs}</div>
      <p class="menu__label">Fort Lauderdale</p>
      <address>1132 SE 3rd Avenue<br>Fort Lauderdale, FL 33316</address>
      <p class="menu__label">New York</p>
      <address>745 Fifth Avenue, Suite 500<br>New York, NY 10151</address>
      <a class="btn btn--solid" href="tel:{PHONE_TEL}">Call {PHONE}</a>
      <p><button class="motion-toggle link-line" type="button" aria-pressed="false">Pause motion</button></p>
    </div>
  </div>
</div>'''


def footer():
    prac = "".join(f'<li><a href="/{s}/">{e(PRACTICES[s]["name"])}</a></li>' for s in PRACTICE_ORDER)
    ppl = "".join(f'<li><a href="/{s}/">{e(PEOPLE[s]["name"])}</a></li>' for s in PEOPLE_ORDER)
    return f'''<footer class="footer">
  <div class="footer__big" aria-hidden="true" lang="la">{MOTTO_LA} &nbsp; {MOTTO_LA}</div>
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <img class="footer__logo" src="/assets/img/brand/lockup-640.webp" alt="{e(FIRM)}" loading="lazy" width="640" height="281">
        <p class="muted">A boutique trial firm for complex litigation and criminal defense, with offices in Fort Lauderdale and New York.</p>
        <p><a class="link-line" href="tel:{PHONE_TEL}">{PHONE}</a><br><a class="link-line" href="tel:{TOLLFREE_TEL}">{TOLLFREE}</a><br><a class="link-line" href="mailto:{EMAIL}">{EMAIL}</a><br><span class="muted">Fax {FAX}</span></p>
      </div>
      <div><p class="footer__h">Practice areas</p><ul>{prac}</ul></div>
      <div><p class="footer__h">People</p><ul>{ppl}</ul><p class="footer__h" style="margin-top:28px">Firm</p><ul><li><a href="/about/">About</a></li><li><a href="/locations/">Locations</a></li><li><a href="/contact/">Contact</a></li><li><a href="/discover-card-legal-claim/">Discover merchant settlement</a></li></ul></div>
      <div>
        <p class="footer__h">Offices</p>
        <address><a href="/fort-lauderdale/">Fort Lauderdale</a><br>1132 SE 3rd Avenue<br>Fort Lauderdale, FL 33316</address>
        <address><a href="/new-york/">New York</a><br>745 Fifth Avenue, Suite 500<br>New York, NY 10151</address>
        <p><a class="link-line" href="{SOCIAL[0]}" rel="noopener" target="_blank">Instagram</a> &nbsp; <a class="link-line" href="{SOCIAL[1]}" rel="noopener" target="_blank">Facebook</a></p>
      </div>
    </div>
    <div class="footer__base">
      <p>Attorney Advertising. Prior results do not guarantee a similar outcome. The information on this website is general information, not legal advice, and does not create an attorney–client relationship. {e(FIRM)}, 1132 SE 3rd Avenue, Fort Lauderdale, FL 33316, {PHONE}. The hiring of a lawyer is an important decision that should not be based solely upon advertisements.</p>
      <p>&copy; {date.today().year} {e(FIRM)} &nbsp; <button class="motion-toggle link-line" type="button" aria-pressed="false">Pause motion</button></p>
    </div>
  </div>
</footer>
<nav class="callbar" aria-label="Quick contact"><a href="/contact/">Request a free case evaluation</a><a href="tel:{PHONE_TEL}">Call now</a></nav>
<div class="curtain" aria-hidden="true"><div class="curtain__panel"></div><div class="curtain__edge"></div><img class="curtain__crest" src="/assets/img/brand/crest-sm.webp" alt="" width="141" height="260"></div>
<div class="grain" aria-hidden="true"></div>'''


# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------

def postal(o):
    return {"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"], "addressRegion": o["state"], "postalCode": o["zip"], "addressCountry": "US"}


def office_ld(slug):
    o = OFFICES[slug]
    return {
        "@type": "LegalService", "@id": f"{BASE}/{slug}/#office",
        "name": f"{FIRM} {o['name']}", "url": f"{BASE}/{slug}/", "telephone": PHONE_TEL, "email": EMAIL,
        "image": f"{BASE}{poster(o['film'])}", "address": postal(o), "hasMap": o["map"],
        "parentOrganization": {"@id": f"{BASE}/#firm"}, "areaServed": o.get("areas", []),
    }


FIRM_LD = {
    "@type": "Organization", "@id": f"{BASE}/#firm", "name": FIRM, "legalName": FIRM, "alternateName": "Cohen and McMullen",
    "url": f"{BASE}/", "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/img/brand/logo-square-512.png", "width": 512, "height": 512},
    "image": f"{BASE}/assets/img/brand/og.jpg",
    "slogan": f"{MOTTO_LA}. {MOTTO_EN}.", "foundingDate": "2014",
    "description": "Boutique law firm for complex litigation and criminal defense with offices in Fort Lauderdale, Florida and New York, New York.",
    "telephone": PHONE_TEL, "email": EMAIL, "faxNumber": "+1-954-523-2656", "address": postal(OFFICES["fort-lauderdale"]),
    "department": [{"@id": f"{BASE}/fort-lauderdale/#office"}, {"@id": f"{BASE}/new-york/#office"}],
    "areaServed": ["Broward County, FL", "Miami-Dade County, FL", "Palm Beach County, FL", "Florida", "New York, NY"],
    "knowsAbout": [PRACTICES[s]["name"] for s in PRACTICE_ORDER],
    "employee": [{"@id": f"{BASE}/{s}/#person"} for s in PEOPLE_ORDER],
    "sameAs": SOCIAL,
    "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_TEL, "email": EMAIL, "contactType": "Free case evaluation", "areaServed": "US", "availableLanguage": "English"},
}


def person_ld(slug):
    p = PEOPLE[slug]
    d = {
        "@type": "Person", "@id": f"{BASE}/{slug}/#person", "name": p["name"], "jobTitle": p["role"],
        "url": f"{BASE}/{slug}/", "image": f"{BASE}{p['img']}", "worksFor": {"@id": f"{BASE}/#firm"},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": n} for n in p["alumni"]],
        "memberOf": [{"@type": "Organization", "name": m.split(",")[0]} for m in p["memberships"]],
        "knowsAbout": [PRACTICES[s]["name"] for s in p["practices"]],
        "hasOccupation": {"@type": "Occupation", "name": "Attorney"},
        "description": p["short"],
        "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": f"Admitted to {b}", "recognizedBy": {"@type": "Organization", "name": b}} for b in p["bars"]]
                         + [{"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": d} for d in p["education"]],
    }
    if p["awards"]:
        d["award"] = p["awards"]
    return d


def video_ld(key, name, page_url):
    # Page films are decorative ambient loops, not primary video content; not marked up.
    return None
    return {
        "@type": "VideoObject", "@id": f"{page_url}#film", "name": name, "description": FILMS[key],
        "thumbnailUrl": f"{BASE}{poster(key)}", "contentUrl": f"{BASE}{vsrc(key)}", "uploadDate": FILM_DATE,
        "duration": "PT10S", "isFamilyFriendly": True, "publisher": {"@id": f"{BASE}/#firm"},
    }


def crumbs_ld(crumbs):
    return {"@type": "BreadcrumbList", "@id": f"{BASE}{crumbs[-1][1] or ''}#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{BASE}{u or ''}"} for i, (n, u) in enumerate(crumbs)]}


def faq_ld(faq, url):
    return {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


# ---------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------

def page(path, title, desc, body, current, film, graph, speakable=True, page_type="WebPage", main_entity=None, og=None, og_type="website", og_alt=None):
    url = f"{BASE}{path}"
    desc = desc.replace(" Free case evaluation: (954) 523-7774.", " Free case evaluation.")
    assert len(desc) <= 160, (path, len(desc), desc)
    og_image = og or ("/assets/img/brand/og.jpg" if path == "/" else f"/assets/img/og/{film}.jpg")
    og_alt = og_alt or f"{FIRM}: {title.split(' | ')[0]}"
    graph = [g for g in graph if g]
    crumb = next((g for g in graph if g.get("@type") == "BreadcrumbList"), None)
    webpage = {
        "@type": page_type, "@id": f"{url}#webpage", "url": url, "name": title, "description": desc,
        "isPartOf": {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": FIRM, "publisher": {"@id": f"{BASE}/#firm"}},
        "about": {"@id": f"{BASE}/#firm"}, "primaryImageOfPage": f"{BASE}{og_image}", "dateModified": modified(path, body), "inLanguage": "en-US",
    }
    if crumb:
        webpage["breadcrumb"] = {"@id": crumb["@id"]}
    if main_entity:
        webpage["mainEntity"] = {"@id": main_entity}
    speakable = speakable and 'class="answer"' in body
    if speakable:
        webpage["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".answer", ".lede"]}
    ld = json.dumps({"@context": "https://schema.org", "@graph": [FIRM_LD] + graph + [webpage]}, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'''<!doctype html>
<html lang="en-US" class="is-loading">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-video-preview:-1, max-snippet:-1">
<meta name="theme-color" content="#060f1c">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{e(FIRM)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}{og_image}">
<meta name="twitter:image:alt" content="{e(og_alt)}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" as="image" href="{poster(film)}" imagesrcset="{poster(film, True)} 960w, {poster(film)} 1920w" imagesizes="100vw" fetchpriority="high">
<link rel="stylesheet" href="/assets/css/fonts.css?v={ver('/assets/css/fonts.css')}">
<link rel="stylesheet" href="/assets/css/site.css?v={ver('/assets/css/site.css')}">
<script>(function(d){{var h=d.documentElement;try{{if(matchMedia('(prefers-reduced-motion: reduce)').matches)h.classList.remove('is-loading')}}catch(e){{}}setTimeout(function(){{if(h.classList.contains('is-loading')&&!window.__cmReady){{h.classList.remove('is-loading');h.classList.add('no-motion')}}}},3000)}})(document)</script>
<script type="speculationrules">{{"prefetch":[{{"where":{{"href_matches":"/*"}},"eagerness":"moderate"}}]}}</script>
<noscript><style>.curtain{{display:none}}[data-reveal]{{opacity:1;transform:none}}.film__media video,.tile__media video,.crest-film video,.rail__film video,.menu__films{{display:none}}</style></noscript>
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/vendor/gsap.min.js?v=3.12.5" defer></script>
<script src="/assets/js/vendor/ScrollTrigger.min.js?v=3.12.5" defer></script>
<script src="/assets/js/vendor/lenis.min.js?v=1.1.13" defer></script>
<script src="/assets/js/site.js?v={ver('/assets/js/site.js')}" defer></script>
</body>
</html>
'''


SITEMAP = []
HASHFILE = os.path.join(os.path.dirname(ROOT), "scripts", "pagehash.json")
try:
    with open(HASHFILE) as _f:
        PAGEHASH = json.load(_f)
except (OSError, ValueError):
    PAGEHASH = {}


def modified(path, body):
    """Date of the last real content change for a page (stable across rebuilds)."""
    import hashlib
    h = hashlib.sha1(body.encode("utf-8")).hexdigest()
    rec = PAGEHASH.get(path)
    if not rec or rec["hash"] != h:
        rec = PAGEHASH[path] = {"hash": h, "date": TODAY}
    return rec["date"]


def ver(rel):
    import hashlib
    with open(os.path.join(ROOT, rel.lstrip("/")), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def write(path, content):
    out = os.path.join(ROOT, "index.html") if path == "/" else os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    SITEMAP.append(path)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

HOME_FAQ = [
    ("What kind of law firm is Cohen & McMullen, P.A.?", "Cohen & McMullen, P.A. is a boutique law firm focused on complex litigation and criminal defense. It handles commercial litigation, criminal defense, contracts and corporate formation, wrongful death, catastrophic injury and products liability."),
    ("Where are the firm’s offices?", "The firm has offices at 1132 SE 3rd Avenue, Fort Lauderdale, Florida 33316, and 745 Fifth Avenue, Suite 500, New York, New York 10151, with a Los Angeles location being opened."),
    ("Does the firm handle both state and federal cases?", "Yes. The firm’s attorneys have significant trial experience in both state and federal courts, and are admitted in Florida, New York and the District of Columbia, as well as several federal district courts and the Eleventh Circuit Court of Appeals."),
    ("How do I get a free case evaluation?", f"Call {PHONE} or {TOLLFREE}, email {EMAIL}, or send a short description of your case through the contact page. Attorneys who want to refer a case can call or email the firm directly."),
    ("Who are the attorneys at Cohen & McMullen, P.A.?", "Partners Bradford M. Cohen, Michael J. McMullen and Andrew B. Courtney, and associate Ethan J. Strauss."),
]


def badges_marquee():
    """Real network logos where Bradford M. Cohen has given legal commentary (source: his bio)."""
    logos = [("cnn", "CNN"), ("fox-news", "Fox News"), ("nbc", "NBC"), ("cnbc", "CNBC")]
    row = "".join(f'<li><img src="/assets/img/press/{k}.svg" alt="{e(n)}" loading="lazy" width="160" height="64"></li>' for k, n in logos)
    others = "Law&Crime Network, The Dan Abrams Show, Nancy Grace and Celebrity Justice"
    return (f'<section class="press" aria-labelledby="press-h"><div class="wrap">'
            f'<p class="press__label" id="press-h">Legal commentary by <a class="link-line" href="/bradford-cohen/">Bradford M. Cohen</a> has been featured on</p>'
            f'<ul class="press__logos">{row}</ul><p class="press__more">Also {e(others)}.</p></div></section>')

def city_tiles(la_cls='style="grid-column: span 3"'):
    return f'''
<a class="tile tile--5 tile--short" href="/fort-lauderdale/">
  <div class="tile__media">{tile_video("fort-lauderdale")}</div>
  <div class="tile__body"><h3 class="tile__title">Fort Lauderdale</h3><span class="city__addr">1132 SE 3rd Avenue, Fort Lauderdale, FL 33316</span></div>
</a>
<a class="tile tile--4 tile--short" href="/new-york/">
  <div class="tile__media">{tile_video("new-york")}</div>
  <div class="tile__body"><h3 class="tile__title">New York</h3><span class="city__addr">745 Fifth Avenue, Suite 500, New York, NY 10151</span></div>
</a>
<a class="tile tile--short tile--la" href="/locations/">
  <div class="tile__media">{tile_video("los-angeles")}</div>
  <div class="tile__body"><h3 class="tile__title">Los Angeles</h3><span class="city__addr">A third office is being opened.</span></div>
</a>'''


def build_home():
    tiles = "".join(practice_tile(s, TILE_LAYOUT[i]) for i, s in enumerate(PRACTICE_ORDER))
    people = "".join(person_card(s) for s in PEOPLE_ORDER)
    body = f'''
{hero("courtroom", "Litigation and criminal defense, prepared for trial", "A boutique trial firm in Fort Lauderdale and New York for complex litigation and the most serious charges.")}

<section class="section" aria-labelledby="intro-h">
  <div class="wrap split">
    <h2 id="intro-h" data-reveal>Built for the courtroom, and everything before it.</h2>
    <div data-reveal>
      <p class="lede">We are a boutique law firm with offices in South Florida and New York, and a third location being opened in Los Angeles. Our reach gives us the strategic flexibility to serve clients across many sectors in an ever-changing environment.</p>
      <p class="muted">A team of experienced litigators lets our clients take on the largest corporations. We prepare matters with trial in mind.</p>
      <a class="link-line" href="/about/">About the firm</a>
    </div>
  </div>
</section>

<section class="section section--flush-top" aria-labelledby="practice-h">
  <div class="wrap">
    <div class="head-row"><h2 id="practice-h" data-reveal>Where we fight</h2><p data-reveal>Every practice, one standard: prepared for trial.</p></div>
    <div class="tiles">{tiles}</div>
  </div>
</section>

{blade()}

<section class="manifesto" aria-label="Firm motto">
  <div class="manifesto__stage">
    <div class="film__media">{film_video("sword")}</div>
    <div class="wrap">
      <p class="motto" lang="la" style="position:relative;z-index:2;margin-bottom:24px">{MOTTO_LA}.</p>
      <p class="manifesto__text">If you want peace, prepare for war. We prepare every case as if a jury is waiting.</p>
      <p class="manifesto__body">That preparation shapes every negotiation, and it protects you when a case does go to trial.</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="people-h">
  <div class="wrap">
    <div class="head-row"><h2 id="people-h" data-reveal>The trial team</h2><p data-reveal>Partners and an associate with experience prosecuting, defending and trying cases in state and federal court. <a class="link-line" href="/people/">Meet everyone</a></p></div>
    <div class="people-grid people-grid--four">{people}</div>
  </div>
</section>

{badges_marquee()}

<section class="section" aria-labelledby="cities-h">
  <div class="wrap">
    <div class="head-row"><h2 id="cities-h" data-reveal>Two cities, one trial team</h2><p data-reveal>Downtown Fort Lauderdale, and Fifth Avenue in Manhattan.</p></div>
    <div class="tiles">{city_tiles()}</div>
  </div>
</section>

<section class="crest-film" aria-label="The firm crest">
  {film_video("crest")}
  <div class="crest-film__cap"><p class="motto" lang="la">{MOTTO_LA}</p><p class="muted">{MOTTO_EN}</p></div>
</section>

<section class="section" aria-labelledby="faq-h">
  <div class="wrap split">
    <div><h2 id="faq-h" data-reveal>Straight answers</h2><p class="muted" data-reveal>The questions people ask us most, answered plainly.</p></div>
    {qa_block(HOME_FAQ)}
  </div>
</section>

{cta_band()}
'''
    url = f"{BASE}/"
    graph = [office_ld("fort-lauderdale"), office_ld("new-york"), video_ld("courtroom", "Cohen & McMullen, P.A. courtroom film", url), faq_ld(HOME_FAQ, url)] + [person_ld(s) for s in PEOPLE_ORDER]
    write("/", page("/", "Cohen & McMullen, P.A. | Complex Litigation & Criminal Defense Lawyers",
                    "Trial firm in Fort Lauderdale and New York for criminal defense, commercial litigation, contracts, wrongful death, catastrophic injury and product claims.",
                    body, "/", "courtroom", graph))


def build_practice_index():
    tiles = "".join(practice_tile(s, TILE_LAYOUT[i]) for i, s in enumerate(PRACTICE_ORDER))
    crumbs = [("Home", "/"), ("Practice Areas", None)]
    faq = [(f"What does the firm’s {PRACTICES[s]['name'].lower()} practice handle?", PRACTICES[s]["answer"]) for s in PRACTICE_ORDER]
    body = f'''
{hero("evidence", "Practice areas", "Complex litigation and criminal defense for individuals, families and businesses, in Florida and New York.", crumbs)}
<section class="section" aria-labelledby="pa-h">
  <div class="wrap">
    <div class="head-row"><h2 id="pa-h" data-reveal>Choose your fight</h2><p data-reveal>Each practice is led by attorneys who try cases, and it shows in how every file is prepared.</p></div>
    <div class="tiles">{tiles}</div>
  </div>
</section>
<section class="section section--flush-top" aria-labelledby="pa-faq">
  <div class="wrap split">
    <div><h2 id="pa-faq" data-reveal>In short</h2><p class="muted" data-reveal>What each practice covers, in a sentence or two.</p></div>
    {qa_block(faq)}
  </div>
</section>
{cta_band()}'''
    url = f"{BASE}/practice-areas/"
    graph = [crumbs_ld([("Home", "/"), ("Practice Areas", "/practice-areas/")]), video_ld("evidence", "Practice areas film", url), faq_ld(faq, url),
             {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/{s}/", "name": PRACTICES[s]["name"]} for i, s in enumerate(PRACTICE_ORDER)]}]
    write("/practice-areas/", page("/practice-areas/", "Practice Areas | Cohen & McMullen, P.A.",
                                   "Criminal defense, commercial litigation, contracts and corporate formation, wrongful death, catastrophic injury and products liability in Florida and New York.",
                                   body, "/practice-areas/", "evidence", graph))


def build_practice(slug):
    p = PRACTICES[slug]
    crumbs = [("Home", "/"), ("Practice Areas", "/practice-areas/"), (p["name"], None)]
    prose = "".join(f'<h2>{e(h)}</h2>' + "".join(f"<p>{link_people(e(x))}</p>" for x in paras) for h, paras in p["body"])
    florida = "".join(f"<li>{e(x)}</li>" for x in FLORIDA[slug])
    matters = "".join(f'<li>{e(a)}<span>{e(b)}</span></li>' for a, b in p["matters"])
    team = "".join(person_card(s) for s in p["team"])
    others = RELATED[slug]
    related = "".join(practice_tile(s, "tile--4", short=True) for s in others)
    body = f'''
{hero(p["film"], p["h1"], p["lede"], crumbs)}
<section class="section" aria-label="{e(p["name"])} overview">
  <div class="wrap split">
    <aside class="rail" aria-label="Talk to an attorney">
      <p class="answer" data-reveal>{e(p["answer"])}</p>
      <div class="rail__card" data-reveal>
        <div class="rail__film">{tile_video(p["film"])}</div>
        <div class="rail__body">
          <p class="rail__title">Talk to an attorney about {e(p["name"].lower())}</p>
          <p class="rail__team">{", ".join(f'<a class="link-line" href="/{t}/">{e(PEOPLE[t]["name"])}</a>' for t in p["team"])}</p>
          <a class="btn btn--solid rail__btn" href="/contact/">Request a free case evaluation</a>
          <a class="rail__phone" href="tel:{PHONE_TEL}">{PHONE}</a>
        </div>
      </div>
    </aside>
    <div class="prose" data-reveal>
      {prose}
      <h2>What to know in Florida</h2>
      <ul class="fl-list">{florida}</ul>
      <p class="disclaimer">General information, not legal advice. Deadlines depend on the facts of each case.</p>
      <h2>What we handle</h2>
      <ul class="matters">{matters}</ul>
      <p>Handled from our <a class="link-line" href="/fort-lauderdale/">Fort Lauderdale</a> and <a class="link-line" href="/new-york/">New York</a> offices.</p>
      <a class="btn btn--solid" href="/contact/">Request a free case evaluation</a>
    </div>
  </div>
</section>
{blade()}
<section class="section" aria-labelledby="team-h">
  <div class="wrap">
    <div class="head-row"><h2 id="team-h" data-reveal>Who will be in your corner</h2><p data-reveal>Attorneys who handle {e(p["name"].lower())} matters at the firm.</p></div>
    <div class="people-grid">{team}</div>
  </div>
</section>
<section class="section section--flush-top" aria-labelledby="faq-h">
  <div class="wrap split">
    <div><h2 id="faq-h" data-reveal>Questions about {e(p["name"].lower())}</h2><p class="disclaimer" data-reveal>General information, not legal advice. Every case turns on its own facts.</p></div>
    {qa_block(p["faq"])}
  </div>
</section>
<section class="section section--flush-top" aria-labelledby="rel-h">
  <div class="wrap">
    <div class="head-row"><h2 id="rel-h" data-reveal>Related practice areas</h2></div>
    <div class="tiles">{related}</div>
  </div>
</section>
{cta_band()}'''
    path = f"/{slug}/"
    url = f"{BASE}{path}"
    graph = [
        crumbs_ld([("Home", "/"), ("Practice Areas", "/practice-areas/"), (p["name"], path)]),
        {"@type": "Service", "@id": f"{url}#service", "name": p["name"], "serviceType": p["name"], "description": p["answer"],
         "provider": {"@id": f"{BASE}/#firm"}, "areaServed": ["Florida", "New York"], "url": url,
         "availableChannel": {"@type": "ServiceChannel", "servicePhone": PHONE_TEL, "serviceUrl": f"{BASE}/contact/"}},
        video_ld(p["film"], f"{p['name']} film", url), faq_ld(p["faq"], url),
    ]
    write(path, page(path, f"{p['title']} | Cohen & McMullen, P.A.", p["desc"], body, "/practice-areas/", p["film"], graph, main_entity=f"{url}#service"))


def build_about():
    crumbs = [("Home", "/"), ("About the Firm", None)]
    faq = [
        ("What does “Si vis pacem, para bellum” mean?", "It is Latin for “If you want peace, prepare for war.” It is the firm’s motto and appears on its crest."),
        ("Where is the firm based?", "The firm has offices in Fort Lauderdale, Florida, and on Fifth Avenue in New York, with a Los Angeles location being opened."),
        ("Is the firm large or small?", "It is a boutique firm by design: a small team of attorneys and professionals, so clients work directly with experienced trial lawyers."),
    ]
    body = f'''
{hero("crest", "If you want peace, prepare for war", "Cohen & McMullen, P.A. is a boutique trial firm for complex litigation and criminal defense, with offices in South Florida and New York.", crumbs)}
<section class="section" aria-labelledby="ab-h">
  <div class="wrap split">
    <h2 id="ab-h" data-reveal>A boutique firm with a trial team’s reach.</h2>
    <div class="prose" data-reveal>
      <p class="lede">We are a boutique law firm with offices in South Florida and New York, and a third location being opened in Los Angeles. Our geographic reach gives us the strategic flexibility to serve clients in many sectors in an ever-changing environment.</p>
      <p>Having a team of skilled litigators allows our clients to challenge the largest of corporations. When we represent victims of wrongful conduct, we focus on holding individuals and corporations responsible while pursuing the best possible outcome for our clients.</p>
      <blockquote class="pull"><span lang="la">{MOTTO_LA}</span>. {MOTTO_EN}.</blockquote>
      <p>The motto on our crest is also how we work. A file built for trial is the strongest position from which to negotiate. So we build every one that way.</p>
      <dl class="facts">
        <div><dt>Firm</dt><dd>{e(FIRM)}, a boutique law firm for complex litigation and criminal defense</dd></div>
        <div><dt>Offices</dt><dd>Fort Lauderdale, Florida and New York, New York, with Los Angeles being opened</dd></div>
        <div><dt>Attorneys</dt><dd>{link_people("Partners Bradford M. Cohen, Michael J. McMullen and Andrew B. Courtney, and associate Ethan J. Strauss")}</dd></div>
        <div><dt>Practice areas</dt><dd>{", ".join(f'<a class="link-line" href="/{s}/">{e(PRACTICES[s]["name"])}</a>' for s in PRACTICE_ORDER)}</dd></div>
        <div><dt>Bar admissions</dt><dd>Florida, New York and the District of Columbia, plus federal courts including the Eleventh Circuit</dd></div>
        <div><dt>Contact</dt><dd><a class="link-line" href="tel:{PHONE_TEL}">{PHONE}</a><br><a class="link-line" href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      </dl>
    </div>
  </div>
</section>
{blade()}
<section class="section section--flush-top" aria-labelledby="val-h">
  <div class="wrap">
    <div class="head-row"><h2 id="val-h" data-reveal>How we work</h2></div>
    <div class="tiles">
      <a class="tile tile--7" href="/people/"><div class="tile__media">{tile_video("library")}</div><div class="tile__body"><h3 class="tile__title">Trial lawyers at the table</h3><p class="tile__text"><span>A former felony prosecutor, a former commercial trial-division head and a law review alumnus, trying cases in state and federal court.</span></p></div></a>
      <a class="tile tile--5" href="/criminal-defense/"><div class="tile__media">{tile_video("chess")}</div><div class="tile__body"><h3 class="tile__title">Strategy first</h3><p class="tile__text"><span>A holistic approach: sound legal strategy, attention to the human toll of litigation and complete transparency.</span></p></div></a>
      <a class="tile tile--5" href="/commercial-litigation/"><div class="tile__media">{tile_video("boardroom")}</div><div class="tile__body"><h3 class="tile__title">Unafraid of size</h3><p class="tile__text"><span>Prepared to face the largest corporations and their counsel.</span></p></div></a>
      <a class="tile tile--7" href="/locations/"><div class="tile__media">{tile_video("new-york")}</div><div class="tile__body"><h3 class="tile__title">South Florida, New York and growing</h3><p class="tile__text"><span>Fort Lauderdale and New York today, with Los Angeles being opened.</span></p></div></a>
    </div>
  </div>
</section>
{badges_marquee()}
<section class="section" aria-labelledby="ab-faq">
  <div class="wrap split"><div><h2 id="ab-faq" data-reveal>About the firm</h2></div>{qa_block(faq)}</div>
</section>
{cta_band()}'''
    url = f"{BASE}/about/"
    graph = [crumbs_ld([("Home", "/"), ("About the Firm", "/about/")]), faq_ld(faq, url)]
    write("/about/", page("/about/", "About the Firm | Cohen & McMullen, P.A.",
                          "Si vis pacem, para bellum. Cohen & McMullen, P.A. is a boutique trial firm for complex litigation and criminal defense in Fort Lauderdale and New York.",
                          body, "/about/", "crest", graph, page_type="AboutPage", main_entity=f"{BASE}/#firm"))


def build_people_index():
    crumbs = [("Home", "/"), ("People", None)]
    cards = "".join(person_card(s, "h2") for s in PEOPLE_ORDER)
    body = f'''
{hero("library", "The people who stand beside you", "Partners and an associate whose experience includes felony prosecution, leading a commercial trial division, law clerkships and law review.", crumbs)}
<section class="section" aria-label="Attorneys">
  <div class="wrap">
    <div class="people-grid">{cards}</div>
  </div>
</section>
{blade()}
<section class="section section--flush-top" aria-labelledby="pp-h">
  <div class="wrap split">
    <h2 id="pp-h" data-reveal>Admitted where your case will be heard.</h2>
    <div class="prose" data-reveal>
      <p class="lede">Between them, our attorneys are admitted in Florida, New York and the District of Columbia, in federal district courts in Florida and Puerto Rico, in the United States Tax Court, Immigration Court and Bankruptcy Court, and in the Eleventh Circuit Court of Appeals.</p>
      <p>They belong to the Florida and National Associations of Criminal Defense Lawyers, the American Association for Justice, the Broward County Justice Association and the Broward County Bar Association.</p>
    </div>
  </div>
</section>
{cta_band()}'''
    url = f"{BASE}/people/"
    graph = [crumbs_ld([("Home", "/"), ("People", "/people/")]), video_ld("library", "People film", url)] + [person_ld(s) for s in PEOPLE_ORDER]
    write("/people/", page("/people/", "Attorneys | Cohen & McMullen, P.A.",
                           "Meet Bradford M. Cohen, Michael J. McMullen, Andrew B. Courtney and Ethan J. Strauss, the trial attorneys of Cohen & McMullen, P.A.",
                           body, "/people/", "library", graph))


def build_person(slug):
    p = PEOPLE[slug]
    crumbs = [("Home", "/"), ("People", "/people/"), (p["name"], None)]
    bio = "".join(f"<p>{e(x)}</p>" for x in p["bio"])

    def fact(label, items):
        if not items:
            return ""
        lis = "".join(f"<li>{e(i)}</li>" for i in items)
        return f'<div><dt>{e(label)}</dt><dd><ul>{lis}</ul></dd></div>'
    facts = (fact("Education", p["education"]) + fact("Bar admissions", p["bars"]) + fact("Court admissions", p["courts"]) +
             fact("Memberships", p["memberships"]) + fact("Recognition", p["awards"]) + fact("Featured on", p["media"]))
    prac = "".join(practice_tile(s, "tile--4", short=True) for s in p["practices"])
    others = "".join(person_card(s) for s in PEOPLE_ORDER if s != slug)
    first = p["name"].split()[0]
    body = f'''
{hero("chess", p["name"], f'{p["role"]}. {p["short"]}', crumbs)}
<section class="section" aria-labelledby="bio-h">
  <div class="wrap split">
    <figure class="bio-portrait" data-reveal><img src="{p["img"]}" alt="Portrait of {e(p["name"])}" loading="lazy"><figcaption>{e(p["name"])}, {e(p["role"])}</figcaption></figure>
    <div class="prose" data-reveal>
      <h2 id="bio-h">About {e(first)}</h2>
      {bio}
      {'<p class="disclaimer">Prior results do not guarantee a similar outcome.</p>' if slug == "bradford-cohen" else ''}
      <blockquote class="pull">{e(p["pull"])}</blockquote>
      <dl class="facts">{facts}</dl>
      <a class="btn btn--solid" href="/contact/">Request a free case evaluation</a>
    </div>
  </div>
</section>
<section class="section section--flush-top" aria-labelledby="pr-h">
  <div class="wrap">
    <div class="head-row"><h2 id="pr-h" data-reveal>Practice focus</h2></div>
    <div class="tiles">{prac}</div>
  </div>
</section>
<section class="section section--flush-top" aria-labelledby="ot-h">
  <div class="wrap">
    <div class="head-row"><h2 id="ot-h" data-reveal>The rest of the team</h2></div>
    <div class="people-grid">{others}</div>
  </div>
</section>
{cta_band()}'''
    path = f"/{slug}/"
    url = f"{BASE}{path}"
    graph = [crumbs_ld([("Home", "/"), ("People", "/people/"), (p["name"], path)]), person_ld(slug),
             ]
    write(path, page(path, f"{p['name']}, {p['role']} | Cohen & McMullen, P.A.", p["meta"], body, "/people/", "chess", graph,
                     page_type="ProfilePage", main_entity=f"{url}#person", og=f"/assets/img/og/{slug}.jpg", og_type="profile", og_alt=f"{p['name']}, {p['role']}, {FIRM}"))


def build_locations():
    crumbs = [("Home", "/"), ("Locations", None)]
    body = f'''
{hero("los-angeles", "Fort Lauderdale. New York. Los Angeles next.", "Our geographic reach gives clients strategic flexibility across sectors, jurisdictions and courtrooms.", crumbs)}
<section class="section" aria-labelledby="loc-h">
  <div class="wrap">
    <div class="head-row"><h2 id="loc-h" data-reveal>Our offices</h2><p data-reveal>Meetings by appointment. Call {PHONE} to schedule.</p></div>
    <div class="tiles">
      <a class="tile tile--7" href="/fort-lauderdale/"><div class="tile__media">{tile_video("fort-lauderdale")}</div><div class="tile__body"><h3 class="tile__title">Fort Lauderdale</h3><span class="city__addr">1132 SE 3rd Avenue, Fort Lauderdale, FL 33316</span></div></a>
      <a class="tile tile--5" href="/new-york/"><div class="tile__media">{tile_video("new-york")}</div><div class="tile__body"><h3 class="tile__title">New York</h3><span class="city__addr">745 Fifth Avenue, Suite 500, New York, NY 10151</span></div></a>
      <div class="tile tile--12 tile--short"><div class="tile__media">{tile_video("los-angeles")}</div><div class="tile__body"><h3 class="tile__title">Los Angeles</h3><span class="city__addr">A third location is being opened.</span></div></div>
    </div>
  </div>
</section>
{cta_band()}'''
    url = f"{BASE}/locations/"
    graph = [crumbs_ld([("Home", "/"), ("Locations", "/locations/")]), office_ld("fort-lauderdale"), office_ld("new-york"), video_ld("los-angeles", "Locations film", url)]
    write("/locations/", page("/locations/", "Office Locations | Cohen & McMullen, P.A.",
                              "Cohen & McMullen, P.A. offices: 1132 SE 3rd Avenue, Fort Lauderdale, FL and 745 Fifth Avenue, Suite 500, New York, NY. Los Angeles office being opened.",
                              body, "/locations/", "los-angeles", graph))


def build_office(slug):
    o = OFFICES[slug]
    if slug == "fort-lauderdale":
        h1 = "Fort Lauderdale trial lawyers"
        lede = "Our South Florida office on SE 3rd Avenue is minutes from the Broward County courthouse and the federal courthouse in downtown Fort Lauderdale."
        text = [
            "Fort Lauderdale is home. Partner Michael J. McMullen grew up here, and the firm represents individuals and businesses throughout South Florida, including Broward, Miami-Dade and Palm Beach counties.",
            "From this office we handle criminal cases in the Seventeenth Judicial Circuit and in the U.S. District Court for the Southern District of Florida, along with commercial litigation, injury and wrongful death claims across the state.",
        ]
        areas = ["Broward County", "Miami-Dade County", "Palm Beach County", "Statewide Florida matters"]
        title = "Fort Lauderdale Criminal Defense & Litigation Lawyers"
    else:
        h1 = "New York office on Fifth Avenue"
        lede = "Our Manhattan office at 745 Fifth Avenue serves clients with matters in New York and gives Florida clients a base in the city."
        text = [
            "Partner Bradford M. Cohen is admitted to the New York Bar, and partner Andrew B. Courtney was born and raised in the Bronx. The New York office extends the firm’s reach for clients whose businesses and disputes cross state lines.",
            "Meetings are by appointment. Call the firm to arrange a consultation in Manhattan.",
        ]
        areas = ["Manhattan", "New York City", "Clients with matters in both New York and Florida"]
        title = "New York Office on Fifth Avenue"
    faq = [
        (f"Where is the {o['name']} office?", f"{o['street']}, {o['city']}, {o['state']} {o['zip']}."),
        (f"How do I schedule a meeting at the {o['name']} office?", f"Call {PHONE} or email {EMAIL}. Consultations are by appointment, and the first case evaluation is free."),
    ]
    tiles = "".join(practice_tile(s, "tile--4", short=True) for s in PRACTICE_ORDER)
    crumbs = [("Home", "/"), ("Locations", "/locations/"), (o["name"], None)]
    paras = "".join(f"<p>{e(t)}</p>" for t in text)
    area_li = "".join(f"<li>{e(a)}</li>" for a in areas)
    body = f'''
{hero(o["film"], h1, lede, crumbs)}
<section class="section" aria-labelledby="of-h">
  <div class="wrap split">
    <div data-reveal>
      <h2 id="of-h">Visit us</h2>
      <address class="lede" style="font-style:normal;margin:24px 0">{e(FIRM)}<br>{e(o["street"])}<br>{e(o["city"])}, {o["state"]} {o["zip"]}</address>
      <p><a class="link-line" href="tel:{PHONE_TEL}">{PHONE}</a><br><a class="link-line" href="mailto:{EMAIL}">{EMAIL}</a></p>
      <a class="btn" href="{o["map"]}" target="_blank" rel="noopener">Get directions</a>
    </div>
    <div class="prose" data-reveal>
      {paras}
      <dl class="facts"><div><dt>Areas served</dt><dd><ul>{area_li}</ul></dd></div></dl>
      <p><a class="link-line" href="/people/">Meet the attorneys</a></p>
      <iframe class="map" src="{o["embed"]}" title="Map of the {e(o["name"])} office" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>
<section class="section section--flush-top" aria-labelledby="ofp-h">
  <div class="wrap">
    <div class="head-row"><h2 id="ofp-h" data-reveal>What we handle from {e(o["name"])}</h2></div>
    <div class="tiles">{tiles}</div>
  </div>
</section>
<section class="section section--flush-top" aria-labelledby="off-h">
  <div class="wrap split"><div><h2 id="off-h" data-reveal>Visiting the office</h2></div>{qa_block(faq)}</div>
</section>
{cta_band()}'''
    path = f"/{slug}/"
    url = f"{BASE}{path}"
    graph = [crumbs_ld([("Home", "/"), ("Locations", "/locations/"), (o["name"], path)]), office_ld(slug), video_ld(o["film"], f"{o['name']} film", url), faq_ld(faq, url)]
    write(path, page(path, f"{title} | Cohen & McMullen, P.A.",
                     f"{FIRM} {o['name']} office: {o['street']}, {o['city']}, {o['state']} {o['zip']}. Call {PHONE} for a free case evaluation.",
                     body, "/locations/", o["film"], graph))


def build_contact():
    crumbs = [("Home", "/"), ("Contact", None)]
    opts = "".join(f'<option>{e(PRACTICES[s]["name"])}</option>' for s in PRACTICE_ORDER)
    body = f'''
{hero("office", "Share your experience and we will call you", "Our team brings decades of combined experience to every case. If you believe you need an attorney, contact us as soon as possible.", crumbs, actions=False)}
<section class="section" aria-labelledby="ct-h">
  <div class="wrap split">
    <div data-reveal>
      <h2 id="ct-h">Free case evaluation</h2>
      <a class="cta__phone" href="tel:{PHONE_TEL}">{PHONE}</a>
      <p><a class="link-line" href="tel:{TOLLFREE_TEL}">{TOLLFREE}</a><br><a class="link-line" href="mailto:{EMAIL}">{EMAIL}</a><br><span class="muted">Fax {FAX}</span></p>
      <p class="muted" style="margin-top:30px">Attorneys looking to refer a case can email us or call directly.</p>
      <address style="font-style:normal;margin-top:30px"><strong>Fort Lauderdale</strong><br>1132 SE 3rd Avenue, Fort Lauderdale, FL 33316</address>
      <address style="font-style:normal;margin-top:18px"><strong>New York</strong><br>745 Fifth Avenue, Suite 500, New York, NY 10151</address>
    </div>
    <form class="form" data-evaluation data-endpoint="" action="mailto:info@floridajusticefirm.com" method="post" enctype="text/plain" data-reveal>
      <div class="form__row">
        <div class="field"><input id="f-name" name="name" type="text" autocomplete="name" placeholder=" " required><label for="f-name">Your name</label></div>
        <div class="field"><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder=" " required><label for="f-phone">Phone number</label></div>
      </div>
      <div class="field"><input id="f-email" name="email" type="email" autocomplete="email" placeholder=" " required><label for="f-email">Email</label></div>
      <div class="field"><select id="f-area" name="area"><option value="">Not sure yet</option>{opts}</select><label for="f-area">Practice area</label></div>
      <div class="field"><textarea id="f-msg" name="message" placeholder=" " required></textarea><label for="f-msg">Briefly, what happened?</label></div>
      <button class="btn btn--solid" type="submit">Request a free case evaluation</button>
      <p class="form__status" role="status" aria-live="polite"></p>
      <p class="form__note">Please do not send confidential details until an attorney has agreed to represent you. Submitting this form does not create an attorney–client relationship.</p>
    </form>
  </div>
</section>
<section class="section section--flush-top" aria-label="Offices">
  <div class="wrap">
    <div class="tiles">
      <a class="tile tile--6 tile--short" href="/fort-lauderdale/"><div class="tile__media">{tile_video("fort-lauderdale")}</div><div class="tile__body"><h3 class="tile__title">Fort Lauderdale</h3><span class="city__addr">1132 SE 3rd Avenue</span></div></a>
      <a class="tile tile--6 tile--short" href="/new-york/"><div class="tile__media">{tile_video("new-york")}</div><div class="tile__body"><h3 class="tile__title">New York</h3><span class="city__addr">745 Fifth Avenue, Suite 500</span></div></a>
    </div>
  </div>
</section>'''
    url = f"{BASE}/contact/"
    graph = [crumbs_ld([("Home", "/"), ("Contact", "/contact/")]), office_ld("fort-lauderdale"), office_ld("new-york"), video_ld("office", "Contact film", url),
             ]
    write("/contact/", page("/contact/", "Free Case Evaluation | Contact Cohen & McMullen, P.A.",
                            f"Call {PHONE} or {TOLLFREE}, email {EMAIL}, or request a free case evaluation online. Offices in Fort Lauderdale and New York.",
                            body, "/contact/", "office", graph, page_type="ContactPage", main_entity=f"{BASE}/#firm"))


def build_discover():
    crumbs = [("Home", "/"), ("Discover Merchant Settlement", None)]
    faq = [
        ("What is the Discover merchant settlement about?", "The settlement resolves class claims that Discover overcharged merchants on card transaction fees between January 1, 2007 and December 31, 2023. Discover denies wrongdoing. A $1.225 billion class settlement was reached. The official settlement documents describe the claims in full."),
        ("What is an interchange fee?", "When a customer pays with a credit or debit card, an interchange fee applies to the transaction, usually a small percentage of the purchase price. Interchange fees are typically the largest part of what merchants pay to accept Discover cards."),
        ("Is it still possible to file a claim?", "The claim filing period ended on May 18, 2026. See the official settlement website for current status."),
        ("I signed up with the firm before the deadline. What happens now?", f"If you signed up before the deadline and have questions about your claim status, contact us at {PHONE} or {EMAIL} and we will direct your inquiry. Payouts on accepted claims were anticipated in 2026."),
        ("What if my business has closed?", "A business did not need to be active to qualify. It needed to have existed and accepted Discover at some point between January 1, 2007 and December 31, 2023."),
        ("Where can I find the official settlement information?", "The official Discover Card Merchant Class Action Settlement website is discovermerchantsettlement.com."),
    ]
    body = f'''
{hero("card", "Discover merchant settlement", "Businesses that accepted Discover cards between 2007 and 2023 may have been eligible to claim part of a Discover class action settlement.", crumbs, actions=False)}
<section class="section" aria-labelledby="ds-h">
  <div class="wrap split">
    <div data-reveal>
      <div class="notice"><h2 id="ds-h">The claim filing period has closed</h2><p>Claims could be submitted until May 18, 2026. If you signed up before the deadline and have a question about your claim, contact us and we will direct your inquiry.</p><a class="btn btn--solid" href="/contact/">Ask about my claim</a></div>
      <p class="muted">Official information: <a class="link-line" href="https://www.discovermerchantsettlement.com/" target="_blank" rel="noopener">discovermerchantsettlement.com</a></p>
    </div>
    <div class="prose" data-reveal>
      <p class="lede">If you owned a business that accepted Discover at any time between 2007 and 2023, you may have been overcharged fees on credit card transactions.</p>
      <p>Discover was sued for overcharging credit card transaction fees during that time. A class action settlement allowed qualifying businesses to submit claims to recover a portion of those fees. The amount each approved claimant receives depends on its interchange fees on Discover transactions, the total value of all valid claims, and the costs and fees approved by the court.</p>
      <p>The cases resolved by the settlement include CAPP, Inc. v. Discover Financial Services, Lemmo’s Pizzeria, LLC v. Discover Financial Services and Support Animal Holdings, LLC v. Discover Financial Services, brought in the U.S. District Court for the Northern District of Illinois.</p>
    </div>
  </div>
</section>
<section class="section section--flush-top" aria-labelledby="dsf-h">
  <div class="wrap split"><div><h2 id="dsf-h" data-reveal>Settlement questions</h2><p class="disclaimer" data-reveal>Summary for general information. The official settlement documents control.</p></div>{qa_block(faq)}</div>
</section>
{cta_band("Questions about a business claim? Talk to us.")}'''
    url = f"{BASE}/discover-card-legal-claim/"
    graph = [crumbs_ld([("Home", "/"), ("Discover Merchant Settlement", "/discover-card-legal-claim/")]), video_ld("card", "Merchant settlement film", url), faq_ld(faq, url)]
    write("/discover-card-legal-claim/", page("/discover-card-legal-claim/", "Discover Merchant Settlement Claim | Cohen & McMullen, P.A.",
                                              "Status of the Discover merchant fee settlement for businesses that accepted Discover cards from 2007 to 2023. The claim period closed May 18, 2026.",
                                              body, "", "card", graph))


def build_404():
    tiles = "".join(practice_tile(s, "tile--4", short=True) for s in PRACTICE_ORDER[:3])
    body = f'''{hero("courtroom", "This page has left the courtroom", "The page you were looking for has moved or no longer exists. Try the practice areas, our people, or call the firm.")}
<section class="section"><div class="wrap"><div class="head-row"><h2>Try one of these</h2></div><div class="tiles">{tiles}</div></div></section>'''
    out = page("/404.html", "Page not found | Cohen & McMullen, P.A.", "Page not found.", body, "", "courtroom", [], speakable=False)
    out = out.replace('content="index, follow, max-image-preview:large, max-video-preview:-1, max-snippet:-1"', 'content="noindex"')
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(out)


def build_meta():
    home_video = (f"<video:video><video:thumbnail_loc>{BASE}{poster('courtroom')}</video:thumbnail_loc><video:title>{e(FIRM)}</video:title>"
                  f"<video:description>{e(FILMS['courtroom'])}</video:description><video:content_loc>{BASE}{vsrc('courtroom')}</video:content_loc></video:video>")
    urls = "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{PAGEHASH[p]['date']}</lastmod></url>" for p in SITEMAP)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("# Search and AI answer engines are welcome.\nUser-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(ROOT, "_redirects"), "w") as f:
        f.write("/blank /ethan-strauss/ 301\n/credit-card-legal-claim /discover-card-legal-claim/ 301\n/robinhood-class-action /practice-areas/ 301\n")
    os.makedirs(os.path.dirname(HASHFILE), exist_ok=True)
    with open(HASHFILE, "w") as f:
        json.dump(PAGEHASH, f, indent=1, sort_keys=True)
    build_llms_full()
    lines = [f"# {FIRM}", "",
             f"> Boutique law firm for complex litigation and criminal defense. Offices: 1132 SE 3rd Avenue, Fort Lauderdale, FL 33316 and 745 Fifth Avenue, Suite 500, New York, NY 10151; Los Angeles location being opened. Phone {PHONE}, toll-free {TOLLFREE}, email {EMAIL}. Free case evaluation. Motto: “{MOTTO_LA}” ({MOTTO_EN}).", "",
             "## Practice areas"]
    lines += [f"- [{PRACTICES[s]['name']}]({BASE}/{s}/): {PRACTICES[s]['answer']}" for s in PRACTICE_ORDER]
    lines += ["", "## Attorneys"]
    lines += [f"- [{PEOPLE[s]['name']}]({BASE}/{s}/), {PEOPLE[s]['role']}: {PEOPLE[s]['short']} Education: {'; '.join(PEOPLE[s]['education'])}. Admissions: {'; '.join(PEOPLE[s]['bars'])}." for s in PEOPLE_ORDER]
    lines += ["", "## Firm", f"- [About]({BASE}/about/)", f"- [Locations]({BASE}/locations/)", f"- [Fort Lauderdale office]({BASE}/fort-lauderdale/)",
              f"- [New York office]({BASE}/new-york/)", f"- [Contact]({BASE}/contact/)", f"- [Discover merchant settlement]({BASE}/discover-card-legal-claim/)", "",
              "## Optional", f"- [Full site text]({BASE}/llms-full.txt): every page in plain text", f"- [Sitemap]({BASE}/sitemap.xml)", "",
              "## Notes", "- Attorney advertising. General information only, not legal advice."]
    with open(os.path.join(ROOT, "llms.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


def build_llms_full():
    """Plain-text export of every page's main content for AI answer engines."""
    from html.parser import HTMLParser

    class Text(HTMLParser):
        def __init__(self):
            super().__init__()
            self.out, self.on, self.skip = [], 0, 0

        def handle_starttag(self, tag, attrs):
            if tag == "main":
                self.on += 1
            if tag in ("script", "style", "video", "nav"):
                self.skip += 1
            if self.on and tag in ("h1", "h2", "h3", "p", "li", "summary", "dt", "address"):
                self.out.append("\n" + {"h1": "# ", "h2": "## ", "h3": "### "}.get(tag, "- " if tag == "li" else ""))

        def handle_endtag(self, tag):
            if tag == "main":
                self.on -= 1
            if tag in ("script", "style", "video", "nav"):
                self.skip -= 1

        def handle_data(self, data):
            if self.on and not self.skip:
                self.out.append(" ".join(data.split()) + " " if data.strip() else "")

    parts = [f"# {FIRM} — full site text", "", f"Source: {BASE}/ · Attorney advertising. General information, not legal advice.", ""]
    for path in SITEMAP:
        f = os.path.join(ROOT, "index.html") if path == "/" else os.path.join(ROOT, path.strip("/"), "index.html")
        t = Text()
        t.feed(open(f, encoding="utf-8").read())
        body = "".join(t.out)
        body = "\n".join(line.rstrip() for line in body.splitlines() if line.strip())
        parts += [f"---\nURL: {BASE}{path}\n", body.replace("\n# ", "\n## ").replace("\n## ## ", "\n### "), ""]
    with open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))


if __name__ == "__main__":
    build_home()
    build_practice_index()
    for s in PRACTICE_ORDER:
        build_practice(s)
    build_about()
    build_people_index()
    for s in PEOPLE_ORDER:
        build_person(s)
    build_locations()
    for s in OFFICES:
        build_office(s)
    build_contact()
    build_discover()
    build_404()
    build_meta()
    print(f"Built {len(SITEMAP)} pages")
