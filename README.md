# Fall Online MCS Course Recommender

CS 410 Final Project: A course recommendation system for UIUC MCS Online students using NLP techniques.

## How to Run

Run these commands in the terminal:
```
py -m pip install -r requirements.txt
py -m nltk.downloader stopwords punkt wordnet punkt_tab
py -m streamlit run app.py
```

The application will open in your browser using Streamlit. Enter a description of the course you want and the amount of courses recommended to you. The system will recommend matching courses based on your requirements. 

To exit the program, enter Ctrl + C in the terminal.

## NLP Techniques Used

- Text preprocessing (tokenization, stopword removal, lemmatization)
- TF-IDF vectorization
- Naive Bayes classification for difficulty prediction
- Keyword extraction for query parsing
- Aspect-based analysis (detecting exam-heavy, project-based courses, etc.)

## Data

- 19 courses from the Fall 2024 MCS Online catalog
- 50+ student reviews from uiucmcs.org

## Limitations

Originally, the application was supposed to encompass all of the courses available to students in the MCS Online program. However, our team ran into an issue of confirming whether a class was meant for the Online MCS track. We decided to stick to the confirmed courses for MCS Online students via an email we were sent for available classes from the beginning of the semester for accuracy. To confirm this, we checked with the course catalog for the courses offered terms. 

In addition, we were not able to find reputable or significant reviews for some courses (namely CS 446 and CS 461) which will affect the recommendation's accuracy since we were not able to have any of the course reviews for training. 

Another issue we came across from our data collection was that there was a lot of differing academic experiences from reviewers that skewed some of the review scores. For example, some students that had already had a background in a certain topic found the course easier than someone who was new to the topic. In addition, the difficulty scoring was slightly inaccurate because some reviewers had given a course a difficult or medium review based on instructor or TA availability or quality.

## Aspects to Improve 
- Finding more reviews from other platforms for queries regarding TA or instructor quality (RateMyProfessor, Reddit)
- Adding most recent syllabus for the courses to give user a more accurate depiction of course structure (exam-heavy vs project-heavy)
- Manually adding more scores to make recommendation more accurate (course quality, teaching staff satisfaction, etc.)
- Inquiring about all the available courses for MCS Online students from official sources for a larger course data set