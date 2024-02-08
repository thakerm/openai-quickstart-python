import spacy
from spacy.matcher import Matcher
import re

nlp = spacy.load("en_core_web_sm")

def extract_information(report):
    doc = nlp(report)
    matcher = Matcher(nlp.vocab)

    # Adjust patterns to ensure they capture the full details
    gleason_pattern = [{"LOWER": "gleason"}, {"LOWER": "score"}, {"IS_DIGIT": True}, {"TEXT": "+"}, {"IS_DIGIT": True}]
    cores_pattern = [{"IS_DIGIT": True}, {"LOWER": "of"}, {"IS_DIGIT": True}, {"LOWER": "cores"}]
    # For tumor measurements, consider adjusting the pattern or directly processing the text
     #this pattern should find the following text: tumor measures ddMM
    tumor_measure_pattern = [{"LOWER": "tumor"}, {"LOWER": "measures"}, {"SHAPE": "dMM"}]
   


    matcher.add("GLEASON_SCORE", [gleason_pattern])
    matcher.add("CORES_POSITIVE", [cores_pattern])
    matcher.add("TUMOR_MEASURE", [tumor_measure_pattern])

    gleason_scores = []
    cores_positive_info = []
    tumor_measurements = []

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end].text
        rule_id = nlp.vocab.strings[match_id]

        if rule_id == "GLEASON_SCORE":
            # Extract the entire Gleason Score, not just the pattern name
            gleason_scores.append(span)
        elif rule_id == "CORES_POSITIVE":
            print(span)
            cores_positive_info.append(span)
        elif rule_id == "TUMOR_MEASURE":
            # Extract the entire measurement detail
            print(span)
            tumor_measurements.append(span)

    summary = {
        'Gleason Scores': gleason_scores,
        'Cores Positive Info': cores_positive_info,
        'Tumor Measurements': tumor_measurements
    }

    return summary

# Process the report
report_text = """Provider:  MGT
Collected: 12/6/2023                    Case #:  SRTS23-225537
  
                     Surgical Pathology Report 
  
  
  
FINAL PATHOLOGIC DIAGNOSIS 
A.  PROSTATE NEEDLE BX - A RT APEX: 
     --     FOCAL ATYPICAL SMALL ACINAR PROLIFERATION   
     --     CHRONIC AND ACUTE PROSTATITIS 
  
B.  PROSTATE NEEDLE BX - B RT MID:   
     --     BENIGN PROSTATIC TISSUE WITH CHRONIC AND ACUTE 
PROSTATITIS 
  
C.  PROSTATE NEEDLE BX - C RT BASE:   
     --     BENIGN PROSTATIC TISSUE 
     tumor measures 2MM
  
D.  PROSTATE NEEDLE BX - D LT APEX:   
          --     PROSTATIC ADENOCARCINOMA, GLEASON SCORE 3 + 4 = 7 
(PATTERN 4 = 10%, GRADE GROUP 2), INVOLVING 4 OF 6 CORES tumor measures 5 IN 5 MM CORE; tumor measures 3 IN 2 MM CORE; TUMOR 
MEASURES 1MM IN 8 MM CORE; TUMOR MEASURES 3MM IN 5 MM CORE 
Perineural invasion present
  
E.  PROSTATE NEEDLE BX - E LT MID: 
     --     BENIGN PROSTATIC TISSUE WITH CHRONIC PROSTATITIS 
  
F.  PROSTATE NEEDLE BX - F LT BASE: 
          --     PROSTATIC ADENOCARCINOMA, GLEASON SCORE 3 + 4 = 7 
(PATTERN 4 = 10%, GRADE GROUP 2), INVOLVING 2 OF 3 CORES (TUMOR 
MEASURES 2MM IN 7 MM CORE; TUMOR MEASURES 2MM IN 14 MM CORE) 
  
  
                         Karls Forege M.D. 
                         ** Report Electronically Signed by JB ** 
Comment 
Dr. C doss has reviewed this case and concurs. 
The microscopic examination and immunohistochemical findings 
(prostate triple stain with appropriate positive and negative 
controls) support the above diagnosis. 
  
[DISCLAIMER:  This immunoperoxidase stain/panel was developed and 
its performance characteristics determined by the Kaiser Regional 
Immunohistochemistry Laboratory/The Permanente Medical Group, Inc., 
Northern California. It has not been cleared or approved by the 
U.S. Food and Drug Administration (FDA). The FDA has determined 
that such clearance or approval is not necessary. This test is used 
for clinical purposes. It should not be regarded as investigational 
or for research. This laboratory is certified under the Clinical 
Laboratory Improvement Amendments of 1988 (CLIA-88) as qualified to 
perform high complexity clinical laboratory testing. Positive and 
negative control studies were evaluated and stained appropriately.] 
  
  
  
Clinical History 
DIAGNOSIS/CLINICAL IMPRESSION: 
  
Gross Description 
A.  Received in formalin labeled with the patient's name and 
medical record number ending in 3095, and labeled as "A," and 
consist of 3 tan core biopsy fragments measuring 1.3-1.7 cm in 
length and <0.1 cm in diameter. All in cassette "A1." 
  
B.  Received in formalin labeled with the patient's name and 
medical record number ending in 3095, and labeled as "B," and 
consist of 2 tan core biopsy fragments measuring 1.2 and 1.5 cm in 
length and <0.1 cm in diameter. All in cassette "B1." 
  
C.  Received in formalin labeled with the patient's name and 
medical record number ending in 3095, and labeled as "C," and 
consist of 2 tan core biopsy fragments measuring 1.0 and 1.2 cm in 
length and <0.1 cm in diameter. All in cassette "C1." 
  
D.  Received in formalin labeled with the patient's name and 
medical record number ending in 3095, and labeled as "D," and 
consists of 2 tan core biopsy fragments measuring 1.6 and 1.8 cm in 
length and <0.1 cm in diameter. All in cassette "D1." 
  
E.  Received in formalin labeled with the patient's name and 
medical record number ending in 3095, and labeled as "E," and 
consist of 2 tan core biopsy fragments measuring 1.4 and 1.8 cm in 
length and <0.1 cm in diameter. All in cassette "E1." 
  
F.  Received in formalin labeled with the patient's name and 
medical record number ending in 3095, and labeled as "F," and 
consist of 3 tan core biopsy fragments measuring 0.6-1.5 cm in 
length and <0.1 cm in diameter. All in cassette "F1."  KPS 
  
  
kps/12/7/2023 
Specimen(s) Received 
A:PROSTATE NEEDLE BX  - A RT APEX 
B:PROSTATE NEEDLE BX  - B RT MID 
C:PROSTATE NEEDLE BX  - C RT BASE 
D:PROSTATE NEEDLE BX  - D LT APEX 
E:PROSTATE NEEDLE BX  - E LT MID 
F:PROSTATE NEEDLE BX  - F LT BASE 
  
  
Patient Name:  Heart, love A 
Med. Rec #:  005530951    DOB/Age:  1/1/1954 (Age: 69)   Sex:  M 
Facility:  Santa Carlo Med Ctr 
Location:  UROLOGY 
  
FHIR Pathology
1 Washington Way
Santa Carlo, CA 95403 
Hi Me, M.D., Laboratory Director 
  

can you help me create a very simple flask app. the main page has an input text box and a submit button. when the user hits the button it should call chatChatGPT python api and process the data. i want the api to summarize the prostate pathology report by simply reporting the Gleason Score, number of cores positive, maximum length of the core, calculate the percent positive for each core with cancer. The app should then display this information nicely in a html page. 
"""
report_summary = extract_information(report_text)

# Print the summaries
for key, value in report_summary.items():
    print(f"{key}: {value}")
