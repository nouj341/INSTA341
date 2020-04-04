## **Acceptance Tests for Additional Features**

**SEARCH BAR + BUTTON**

Scenario #1
***
* Given I'm in a role of a signed-in user
* When I want to follow a specific user
* Then I write the username or email I wish to follow in the search bar and click "Search"

Scenario #2
***
* Given I'm in a role of a signed-in user
* When I want to follow a specific user and I do not know the correct username of who I wish to follow
* Then I can write part of the username or email, the pattern will be matched to the most similar option.

**LIKE BUTTON**

Scenario #1
***
* Given I'm in a role of a signed-in user
* When I view my follower's posts and like them 
* Then I can click "Like" button and it will display the amount of likes next to the picture

Scenario #2
***
* Given I'm in a role of a signed-in user
* If I want to like the post of someone I am not following
* Then I will visit their profile page which includes the display of all the posts  
* Then I can click "Like" button and it will display the amount of likes next to the picture
