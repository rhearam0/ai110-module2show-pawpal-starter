# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The initial UML design was created show how the four main classes interacted with each other. Each one outlined the attributes and methods. For example, Owner class is connected to one or more Pet objects, each Pet contains multiple Task objects, and CarePlan ordganizes tasks into a daily schedule based on available time/priority.

- What classes did you include, and what responsibilities did you assign to each?

The classes I chose were Owner, Pet, Task, and CarePlan. 
    1. I chose the Owner class because the app needs to store information about the pet owner including their name and the pets they own. 
    2. The Pet class stores information about each pet, such as its name, species, breed, age, and the tasks associated with it. 
    3. I created the Task class because the app revolves around managing pet care tasks like feeding, walking, and medications. 
    4. Finally, I added the CarePlan class to organize the pet's daily schedule by storing the scheduled tasks and the available time, allowing the app to generate a daily care plan.


**b. Design changes**

- Did your design change during implementation?
Yes, the design did change based on AI feedback. The reason was because there were flaws in the original that would have made the system not as realistic nor accurate. 

- If yes, describe at least one change and why you made it.
One change was ensuring the Owner and the CarePlan were related. The reason for this is because care plan is is created for the owner's pet so adding the owner to careplan or vice versa would make the model more realistic. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The constraints included the scheduler skipping completed tasks when building a schedule so the plan reflects only what still needs to be done. 

- How did you decide which constraints mattered most?
I decided these constrained mattered most becaue they are the most direct and practical for pet care app. Time helps the owner know when tasks should happen and priority helps distinguish urgent tasks from less urgent ones, and completion status prevents finished tasks from appearing in the next plan.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff my scheduler makes is that it prioritizes tasks by time and priority, but it does not yet try to optimize for the most efficient route or for the total amount of time spent moving between tasks.

- Why is that tradeoff reasonable for this scenario?
This is reasonable because the main goal of the app is to help a busy pet owner stay organized and avoid missing important care tasks not to create a perfect logistics plan. A simple time based scheduler is easier to understand, faster to run, and still very useful for everyday pet care.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used VS Code chat feature to help me throughout the project with things like debugging, helping with setting up algorithmic methods, and also making the UI of the code more readible. 

- What kinds of prompts or questions were most helpful?
Questions that were most helpful included "How can I improve this scheduler method?". I think having the chat using my code and improving it not only made it more accurate but also easier when it came to undertsanding it. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment where I did not accept AI suggestion was when it proposed a more complex way to structure the scheduler logic. I felt this was uncessary and would just make the code hard to follow and less aligned with the simple design of the project. 

- How did you evaluate or verify what the AI suggested?
By completing test cases. ran the test suite and checked if the behavior matched the intended scheduling rules including things lke the sorting tasks by time and handling recurring tasks correctly. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Behaviors I tested included scheduler being able to detect when two tasks share the same time. I also tested the basic model behavior such as adding pets and tasks, generating a care plan, and filtering completed tasks. 

- Why were these tests important?
These behaviors are importance because if sorting, reccurence, or conflict detion failed, the app would not reliably help a user plan daily pet care tasks.


**b. Confidence**

- How confident are you that your scheduler works correctly?
I am pretty confident because the implmented test suite passed successfuly including new tests for sorting, recurrence, and conflict detection. 

- What edge cases would you test next if you had more time?
I would test tasks with missing or invalid preferred times. Then I would also test behavior when multiple pets have overlapping tasks and when a task is completed more than once. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satsified with just being able to learn more about how AI can simplify the whole coding process. Also learning about UML was pretty cool! It was cool to see how the info I provided was able to be turned into something simple and visual.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would improve the user interface to make it more interactive and visually appealing. I would also enhance the Streamlit app by displaying the generated schedule more clearly and making it easier for users to add, edit, and manage their pets and tasks. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing I learned about designing systems is that having a clear design before writing code makes the implementation much easier. I also learned that AI is most helpful when you give it specific instructions and carefully review its suggestions instead of accepting them automatically. Throughout this project, I used AI to help design the UML, build the class structure, and improve my code, but I still needed to test the program, run test cases, and make changes myself to ensure everything worked correctly.