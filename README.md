# FutQuiz / Quiz Python Game - Ett Interaktivt Quizspel

![FutQuiz Banner](https://github.com/Peppino9/quiz-python-game/blob/main/static/assets/stadium.jpg)


## Om Projektet
FutQuiz är ett webbaserat quizspel utvecklat i Python med Flask-ramverket. Projektet är avsett att erbjuda användare en interaktiv plattform för att testa sina kunskaper inom olika områden relaterade till fotboll.


## Directory Structure /Mappstruktur

- **quiz-python-game/** (Main Directory) 
  - **app.py** (Main Python file for the Flask application)
  - **db_connection_utils.py** (Utility file for database connections)
  - **.venv/** (Directory for HTML templates)
  - **templates/** (Directory for HTML templates)
    - **index.html** (Homepage template)
    - **admin.html** (Admin dashboard template)
    - **admin_question_template.html** (Template for admin page)
    - **admin_question_bank_template.html** (Template for quesstion bank)
    - **main.html** (Main template for the quiz)
    - **login.html** (Login page template)
    - **signup.html** (Signup page template)
    - **users.html** (Template for managing users)
    - **quiz.html** (Template for the quiz)
    - **answer.html** (Template for displaying answers)
    - **result.html** (Template for displaying quiz results)
    - **question.html** (Template for displaying questions)
    - **question_template.html** (Template for individual questions)
    - **suggest.html** (Template for suggesting questions)
  - **static/** (Directory for CSS, and other static files)
    - **assets/** *(Directory for image assets)
      - **Stadium.jpg** (Image asset)
      - **futquiz.jpeng** (Image asset)
    - **form_style.css** (CSS for form styles)
    - **quiz.css** (CSS for quiz layout)
    - **quizflow.css** (CSS for quiz flow)
    - **style.css** (Main CSS styles)
  - **tests/** (Directory for HTML templates)
    - **Empty.py** (emty for now)
  - **README.md** (Project README file)
  - **.gitignore** (Git ignore file)
  - **requirement.txt** (requirement file)



## Hur Man Kommer Igång 1
1. Klona detta repository till din lokala maskin med kommandot `git clone https://github.com/Peppino9/quiz-python-game.git`.
2. Navigera till katalogen `quiz-python-game` med kommandot `cd quiz-python-game`.
3. Installera de nödvändiga beroendena med kommandot `pip install -r requirements.txt`.
4. Starta applikationen genom att köra `python app.py`.
5. Besök `http://localhost:5000/` i din webbläsare för att använda FutQuiz.

## Hur Man Kommer Igång 2 /Usage
1. Installera quiz-python-game som zip
2. Installera de nödvändiga beroendena med kommandot `pip install -r requirements.txt`
3. köra `app.py` för att starta applicationen.
4. Besök `http://localhost:5000/` i din webbläsare för att använda FutQuiz.

## Hur Man Använder FutQuiz
- Gå till huvudsidan för att spela quizet.
- Använd inloggnings-/registreringsfunktionerna för att skapa ett konto och spara dina framsteg.
- Administratörsgränssnittet ger möjlighet att hantera frågor och användare.

## Teknologier
- **Python:** Huvudspråket för applikationslogiken.
- **Flask:** Ett Python-ramverk för att bygga webbapplikationer.
- **HTML/CSS:** Används för att bygga användargränssnittet.
- **SQLite:** Ett lättviktigt inbäddat databassystem som används för att lagra frågor och användardata.

## Licens
Detta projekt är licensierat under [MIT License](https://github.com/Peppino9/quiz-python-game/blob/main/LICENSE).

## Kontakt
Har du frågor eller förslag till förbättringar? Kontakta oss på [GitHub - Simon](https://github.com/Peppino9/), [GitHub - Sayed](https://github.com/Biseda/), [GitHub - Abbe](https://github.com/Abbehamid/), [GitHub - Jerry](https://github.com/jaydiggz/), [GitHub - Thomas](https://github.com/thomasiordanescu/).




GitHub Repository: [quiz-python-game](https://github.com/Peppino9/quiz-python-game)