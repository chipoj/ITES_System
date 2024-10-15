# Intelligent Tutoring Expert System (ITES) for CTA Program - README

## Overview
The Intelligent Tutoring Expert System (ITES) is designed to assist students in the Certificate in the Theory of Accounting (CTA) program by providing personalized learning paths and adaptive feedback. The system uses Bayesian Knowledge Tracing (BKT) and the OpenAI API to track students' knowledge levels and provide customized feedback on complex accounting concepts. For a quick over of how the system looks check the Systems_Pics folder.
Model evaluations are found in the MOdel_Evaluations folder

## System Features
- Adaptive learning paths using Bayesian Knowledge Tracing (BKT)
- Personalized feedback generated via the OpenAI API
- No need for external database setup; the system uses Django's inbuilt database management system (DBMS)
- Knowledge Base (KB) for accounting and taxation rules
- Student performance tracking and skill mastery monitoring
- User interface for delivering quizzes and scenario-based questions
- Integration of various learning models (student model, tutoring model, explanation module)

## Requirements
- Linux environment (preferred) or Windows Subsystem for Linux (WSL) for Windows users
- Python 3.8+
- OpenAI API key for personalized feedback integration

### Dependencies
All required packages are listed in the `requirements.txt` file and can be installed with the following command:

```bash
pip install -r requirements.txt
```

## Installation Instructions

### For Linux Users
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/ITES_System.git
   cd ITES_System
   ```

2. **Install Dependencies**:
   Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure `.env` file**:
   Add your OpenAI API key to the `.env` file in the root directory.
   NB: Key already added but it set to expire once it reaches its limit of a few more request less than 10 

5. **Run the System**:
   Navigate to the `ITE_S` folder and run the system using `manage.py`:
   ```bash
   cd ITE_S
   python manage.py runserver
   ```

   The system uses Django's inbuilt SQLite database, so no external database configuration is required.

### For Windows Users (Using WSL)
1. **Install WSL**:
   Follow the instructions to install Windows Subsystem for Linux (WSL) from the official Microsoft documentation: [Install WSL](https://docs.microsoft.com/en-us/windows/wsl/install).

2. **Follow Linux Installation Instructions**:
   Once WSL is installed, follow the steps outlined above for Linux users. Ensure you're in the Linux environment when executing the commands.
3.  System runs on http://127.0.0.1:8000   

## How to Use
Once the system is up and running:
1. **Login**: admin (password 123),  student1(hW9vfrDD9563Xj$)


## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements you'd like to make.

## Known Issues
- Incomplete data can affect the accuracy of student progress tracking.
- The system requires more extensive datasets to further refine adaptive learning effectiveness.

## Future Developments
- Integration of a customized Large Language Model (LLM) specifically trained on taxation content for enhanced feedback.
- Expansion of feedback methods to include visual aids and video explanations.

## Support
For support, please contact chipojj@gmail.com.

---

Make sure to install all dependencies and follow the setup instructions to experience the full capabilities of the ITES system!
