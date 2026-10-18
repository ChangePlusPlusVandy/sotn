# Creating Branches & Submitting PRs

Workflow:
- Create new branch
- Push your branch
- Submit a PR so your code can merge into main
- I'll review and/or approve the code so it gets merged into main

### Create a new branch: 
`git switch -c branch_name`
 - Ex. `git switch -c jesse/test`

Name the branch with a prefix. For example, `feature/login-page`, where "feature" is the prefix and "login-page" is the feature being developed.

Avoid using only these as the branch name without having a "/..." after the prefix:
- `feature`
- `bugfix`
- `hotfix`
- `refactor`
- `chore`
- `docs`

If you create a branch with only the name "feature", then subsequent branches that use "feature" as the prefix can't be created unless the "feature" branch is renamed. In other words, "feature" is not a good name but "feature/anything-here" is fine. 

### Submit a PR:
On GitHub, after you push to your branch, you'll see a message asking to compare changes between your branch. Alternatively, you can click on "This branch is x commits behind/ahead `main`". 

Click on "Create pull request" and fill in the header/description with appropriate details.