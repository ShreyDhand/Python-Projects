import random
class Question:
    def __init__(self, question, correct_answer, incorrect_answers, category, difficulty):
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.category = category
        self.difficulty = difficulty
        #store all answers
        self.answers = [correct_answer] + incorrect_answers
        #randomize:
        random.shuffle(self.answers)
        # store correct answer:
        self.answer_id = self.answers.index(correct_answer)+1

    def __str__(self):
        qna = self.question + '\n'
        for i in range(len(self.answers)):
            qna += f"{i+1} {self.answers[i]} \n"
        return qna


import json
class QuestionLibrary:
    def __init__(self, filename = "trivia.json"):
        with open(filename, "r") as file:
            data = json.load(file)
        self.question = []
        for record in data:
            q = Question(
                question = record["question"],
                correct_answer = record["correct_answer"],
                incorrect_answers = record["incorrect_answers"],
                category = record["category"],
                difficulty = record["difficulty"] 
            )
            self.question.append(q)

    def get_categories(self):
        c = set()
        for question in self.question:
            c.add(question.category)
        return list(c)

    def get_questions(self, category=None, difficulty=None, number=None):
        filter_questions = [] 
        for question in self.question:  # Loop through all questions
            if category is None or question.category == category:  # Filter by category 
                if difficulty is None or question.difficulty == difficulty:  # Filter by difficulty 
                    filter_questions.append(question)  # Add filtered questions to the list

        if number is not None:
            return filter_questions[:number] 

        return filter_questions  # Return all questions if no number



class Game:
    def __init__(self, category=None, difficulty=None, number=None):
        self.score = 0  
        self.library = QuestionLibrary()  
        self.questions = self.library.get_questions(category, difficulty, number)  # Get questions based on filters

    def play(self):
        # Loop through all selected questions
        for question in self.questions:
            print(f"\nQuestion: {question.question}")  # Display the question

            # Display answer options
            for i in range(len(question.answers)):
                print(f"{i + 1}. {question.answers[i]}")

            while True: 
                try:
                    player_input = int(input("Select your answer (1, 2, 3, or 4): "))
                    if 1 <= player_input <= 4:
                        break  # Exit loop if input is valid
                    else:
                        print("Please select a number between 1 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 4.")  

            # Check if the answer is correct
            if player_input == question.answer_id:
                # Give points based on difficulty
                if question.difficulty == "easy":
                    self.score += 1
                elif question.difficulty == "medium":
                    self.score += 2
                elif question.difficulty == "hard":
                    self.score += 3

                print("Correct answer!\n")
            else:
                print(f"Wrong answer. The correct answer was: {question.answers[question.answer_id - 1]}\n")

        print(f"Game over! Your final score is: {self.score}")


