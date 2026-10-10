# Demos

This details some demos of workflows that might take place for both user groups (individuals interested in T4L, and admins). This was presented at a conference and received good feedback. The stakeholders were in agreement with how the demo looked, but it is vague as to if they agree 100% with every single workflow or if there is anything that may need to be changed. Nonetheless, the purpose of this document is to detail some example processes a user would work through, in hopes of helping guide architecture decisions (languages, framework, technologies). 

## 1. User-Facing

- Reach / landing page --> Hit "Start Intake" button 
- Reach /intake --> Fill out a series of questions. Sequence of pages depends on answers. 
    - Which best describes you (athlete/volunteer/coach/donor/etc.)
    - Where in TN are you based
    - Preferred method of contact, how soon are you looking to get involved, are you currently involved with SOTN, what are you most interested in (United Champion Schools, Youth leadership, Hosting events, Inclusive PE & clubs, Staff Training), have you participated in SOTN before, any accessibility or communication or support needs we shoudl know?
    - Personalized question depending on user group. 
        - for example: for oragnization: org name, type, your role, is your school currently a Unified Champion School?
    - How can we reach you: full name, email, phone
    - Confirm details before submitting form: show important responses from previous pages
    - Submit intake
- Reach /results: show several items for users to do next
    - banner saying "Under human review - a SOTN coordinator will review your submission and get back within 2 business days, etc."
    - "Contact SOTN" questions button
    - There will be several programs matched depending on form answers (ex. show program X because it's a great fit for schools in Middle TN). Users will be able to click "Interested" to show interest
    - Users will be able to click on PDF resources like "Unified Champion Schools Playbook" 

- Log in for use after initial form submission? not in the demo but something to consider.


## 2. Admin-Facing

- Login to reach /admin page --> shows admin dashboard
- Dashboard: 
    - shows # new intakes, # awaiting state review, # routed this week, # qualified, # follow-up queue, # active volunteers
    - shows graph of intakes over time
    - shows bar graph of intakes by region
    - shows bar graph of referral sources
    - shows pie chart for user groups (ex. 10% potential athlete, 5% donors)
    - shows priority list, with a list of users + their user group + status (new vs. under review vs. routed)
- Click to "Intake triage" page
    - Shows list of all form submissions/users
        - Clicking on a user shows all relevant information
        - Option to click "Approve," "Follow up later," "Flag as spam"
        - Dropdown to select where they are routed to. Selected any value triggers an action
        - Add internal notes for this user
        - Toggle on/off a "follow-up reminder: we'll ping you in 7 days"
    - Search by name/email
    - Filter by status (new/under review/routed/contacted/onboarded/etc.)
    - Filter by user group
- Click to "Contacts" page
    - See a list of routed athletes, guardians, volunteers, sponsors, and orgs.
        - name, tags (user group, location), last touch ("just now," "5d ago"), button to "Log touch" for communication
    - Search bar for searching contacts
- Click to "Communications" page
    - Compose messages (school partnership follow-up, welcome to T4L athletics, volunteer orientation invite, donor thank you and next steps, etc.) from templates and send them
- Click to "Follow-ups" page
    - Shows list of tasks sorted into "Not started," "In progress," "Complete"
- Click to "Resources" page
    - Shows a list of resources (videos, PDFs, etc.) available to users
    - Preview resources
    - Edit resources
    - Add resources
