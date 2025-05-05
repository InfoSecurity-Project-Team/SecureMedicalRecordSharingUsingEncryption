# Secure Medical Record Sharing Using Encryption :

##  Table of contents :
- [Secure Medical Record Sharing Using Encryption :](#secure-medical-record-sharing-using-encryption-)
  - [Table of contents :](#table-of-contents-)
  - [1. Project Description :](#1-project-description-)
  - [2. Key features :](#2-key-features-)
    - [1) User Authentication and registeration :](#1-user-authentication-and-registeration-)
    - [2) Creation and Management of medical records :](#2-creation-and-management-of-medical-records-)
    - [3) Block chain for data integrity :](#3-block-chain-for-data-integrity-)
  - [3. Technologies Used :](#3-technologies-used-)
    - [1) Back end :](#1-back-end-)
    - [2) Front end :](#2-front-end-)
## 1. Project Description :
* In this project we made a ___medical record sharing___ system whose data is meant to bes stored in a ___block chain___
*  It aims to ensure the confidentiality, integrity, and accessibility of sensitive patient data while maintaining a robust and transparent record-keeping mechanism.
*  This system allows healthcare professionals, such as doctors, to manage and view medical records securely, while ensuring that patient privacy is protected.
  
## 2. Key features :
### 1) User Authentication and registeration :
>* When users (Doctors and Patients) register or log in to the system their ___Passwords are stored using SHA-256 hashing___ for additional security.
* The system ensures strong password policies for better user authentication.

### 2) Creation and Management of medical records :
* The doctors can create, view and manage medical records for their patients.
>* Each record contains sensitive information of the patient due to which the medical information of the patients are encrypted using ___Fernet encryption___.
>* Encryption keys are securely generated and stored in a separate file ___(secret.key)___

### 3) Block chain for data integrity :
* In this project we have used block chain to ensure data integrity.
* In block chain ___each block consists of timestamp, data and the hash of previous block___
* The first block in block chain known as ___Genisis block___ is automatically created upon system initializtion.
>* Medical records can be retrieved by querying the blockchain. 
>* Each record is encrypted before being added in block chain.

## 3. Technologies Used :
### 1) Back end :
> Python
* For implementing core logic and integrating block chain functionality.
> Json file
* used to store data (as a simple prototype).
> Cryptography (Fernet)
* For encrypting and decrypting sensitive information.
### 2) Front end :
> Tkinter 
* used for developing GUI so that the users can easily interact with the system  
