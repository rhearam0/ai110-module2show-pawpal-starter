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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff my scheduler makes is that it prioritizes tasks by time and priority, but it does not yet try to optimize for the most efficient route or for the total amount of time spent moving between tasks.
- Why is that tradeoff reasonable for this scenario?
This is reasonable because the main goal of the app is to help a busy pet owner stay organized and avoid missing important care tasks, not to create a perfect logistics plan. A simple time-based scheduler is easier to understand, faster to run, and still very useful for everyday pet care.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
