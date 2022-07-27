## API Reference

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 404,
    "message": "Resource Not Found"
}
```

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Unprocessable
=============================
500: Internal Server Error
405: Method Not Allowed

### Endpoints


**GET /categories**

General:
- Returns a list of categories, success value
- Results are paginated in groups of 10. Include a request argument to choose page number that starts from 1.

Sample: ```curl http://localhost:5000/categories```

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

**DELETE /questions/{question_id}**

General:
- Deletes the question of the given ID if it exists. Returns success value.

Sample ```curl -X DELETE http://localhost:5000/questions/5 ```


```
{
  "success": true
  "deleted": question_id
}
```

**POST /questions**


General:
- Creates a new question using the submitted title, answer, category and difficulty. Returns the id of the created question id, success value, total questions number, and questions list based on current page number to update the frontend

Sample: ```curl -X POST -H "Content-Type:application/json" -d '{"question": "What is the name of the lead actor in black panther.", "answer": "Chadwick Boseman", "difficulty": "4", "category": "5"}' http://localhost:5000/questions```


```
{
  "question created": 7,
  "questions": [
    {
      "answer": "Joe Bidden",
      "category": 4,
      "difficulty": 3,
      "id": 1,
      "question": "what is the name of the current USA president"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Atiku Abubakar",
      "category": 4,
      "difficulty": 3,
      "id": 3,
      "question": "what is the name of presidential aspirant for pdp."
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Chadwick Boseman",
      "category": 5,
      "difficulty": 4,
      "id": 7,
      "question": "What is the name of the lead actor in black panther."
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```


**POST /search**

General:
- search for a question using the submitted search term. Returns the results, success value, total questions.


Sample ```curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}' http://localhost:5000/search```

```
{
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Joe Bidden",
      "category": 4,
      "difficulty": 3,
      "id": 1,
      "question": "what is the name of the current USA president"
    },
    {
      "answer": "Atiku Abubakar",
      "category": 4,
      "difficulty": 3,
      "id": 3,
      "question": "what is the name of presidential aspirant for pdp."
    }
  ],
  "success": true,
  "total_questions": 11
}

```

**GET /categories/{category_id}/questions**


General:

- Returns a list of questions, in the given category, category total_questions and success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.


Sample: ```curl http://localhost:5000/categories/5/questions```

```
{
  "current_category": "Entertainment",
  "current_category_id": 5,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Chadwick Boseman",
      "category": 5,
      "difficulty": 4,
      "id": 7,
      "question": "What is the name of the lead actor in black panther."
    }
  ],
  "success": true,
  "total_questions": 4
}

```

**POST /quizzes**

General:
- recive the actual question and the category
- return the next question in the same category and success value.


Sample``` curl -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"History","id":"4"}, "previous_questions":[9]}' http://localhost:5000/quizzes``` 


```

{
  "previousQuestion": [
    9
  ],
  "question": {
    "answer": "Chadwick Boseman",
    "category": 5,
    "difficulty": 4,
    "id": 7,
    "question": "What is the name of the lead actor in black panther."
  },
  "success": true
}

```
