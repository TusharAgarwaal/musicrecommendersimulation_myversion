# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

--- MODEL_NAME = "BeatHive 1.0"

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

--- It generates a ranked song recommendations from the catalog, where each song scores using the "Algorithm Recipe".
It assumes the user's tastes using the 5 categories: Genre, mood, Target Energy Level, Target BPM and if they like acoustic.
This is for classroom exploration since the catalog is very small (10 songs) and this model is to understand the algorithm behind song recommender.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

--- The score uses the five features of the song: Genre, Mood, Intensity, Acousticness, and Valence. User preferences like target energy level and target bpm is taken into consideration for the logic. 
The user preference is calculated as intensity level and acousticness is taken as a preference signal, which contributes to the majority of scoring while other attributes contribute the remaining.
There was no scoring logic, and user preference was also considered, hence I added the score logic as explained above.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

--- There are 10 songs in the catalog to understand the recommender logic a music streaming application uses.
There are 6 genres and 5 moods in the model.
I did add some data, which is user profile, to understand what a user preference can be.
While there is nothing missing related to music taste, there are some mid-range inetnsity level songs missing which could have increased the accuracy of the model.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

--- The user profiles that have clear details on the preference gets better recommendations.
Intensity level (Energy level + BPM) is proving to be working better, scoring better and recommender make better decisions.
The lofi profiles: Library Rain and Midnight Coding are both low-intensity, acoustic, chill, where the scores reflect that with very little ambiguity.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

--- There are 10 songs in the .csv file, and checking by their intensity values, no one accurately covers the user's preferred intensity.
The medium-intensity user is systematically penalized 0.4 points on intensity before the scoring even looks at genre or mood.
For ultra-high intensity users, user can't have 1.0 intensity song as per the current song catalogue, setting the one preference.
The formula set for calculating score treats overshooting and undershooting equally because of the gap size between intensity of different songs in the current catalogue.


---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

--- I added these profiles for testing:
The Gym Goer, The Late Night Studier, The Mood Listener, The Genre Purist, and The Neutral User.
Tried to make recommendations based on Genre and Mood, which showed that not all profiles are taking both the parameteres in consideration.
When the mid-range intensity valued songs were removed from the model, it resulted in the tighter rankings with lower accuracy of decisiveness. This ensured that my model works correctly logically.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

--- The only major improvement I could see in the model is to add more songs in the 0.5-0.65 intensity range, in order to reduce the limitations that the model brings.
The scoring logic itself isn't an issue, but it's the data coverage that assists the biasing.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

--- The biggest insight was how much work the categorical features do. Genre and mood makes up to the majority of the scoring, which shows the users preference and their tastes.
The most interesting part is the inclusion of acousticness not for scoring but for consideration & how it influences the recommendation.
I was able to catch a glimpse of how the music streaming apps work. Though they feed it with more data like streaming history, repetition etc., and much larger catalog.