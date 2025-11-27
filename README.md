# currency-hackathon
This repo contains the code that is used for a POC of automating the process of documentations 



# Jenkins Job workflow

**Flow Explanation:**

> Developer pushes new code to GitHub repo.

> Jenkins job is automatically triggered.

> Jenkins Pipeline:

    > Checkout code

    > Build Docker image

    > Run tests & code

    > Generate documentation (api_docs.html & api_docs.txt)

    > Publish docs files in confluence 



<img width="2400" height="1600" alt="image" src="https://github.com/user-attachments/assets/6af0f9be-ad82-4308-868c-6ee431740688" />




# api_docs.html
“As part of our CI workflow, after every build, Jenkins auto-generates a clear HTML documentation file for our APIs.”

“This web-based doc lists every endpoint, the main functionality, modules (like Flask and requests) and highlights areas such as error handling and edge cases.”

“It helps all stakeholders—developers, managers, testers—instantly understand what our API does, and (if needed) onboard faster.”

“No more manual documentation—our process ensures docs are as fresh as our latest release.”

<img width="1096" height="611" alt="image" src="https://github.com/user-attachments/assets/f567fc59-f316-4404-97b0-3bb1478a714b" />







# **api_docs.text**
Plain English overview of your backend code, auto-generated after each build.

Covers:

  API endpoints: Names, paths, and their main functionality.

  Functions and modules used: What each does and why.

  Error handling: Highlights on how invalid inputs or API failures are managed.

  Use cases: Lists main scenarios for using each piece of the code.

  Compact and readable: Text file format makes it easy to share, review, and search.
  
  Always up-to-date: Jenkins automation keeps it synced with your latest changes.

Ideal for quick onboarding and code understanding: Anyone can read it and instantly get the big picture of your API and workflow, without digging into details or code.

<img width="1317" height="494" alt="image" src="https://github.com/user-attachments/assets/e2b87c91-2cc3-4f32-adb4-8d153389572e" />


