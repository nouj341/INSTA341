## **Acceptance Tests for Core Features**

**POST**

Scenario #1
***
* Given I'm not a signed-in user
* When I try to post
* Then I am redirected to the "Login Page" 

Scenario #2
***
* Given I'm in a role of signed-in user 
and I am directed to the "Post page"
* When I leave the form with either title or image field blank
* Then the post is not made and an error message pops up according to the field that is left.

Scenario #3
***
* Given I'm in a role of signed-in user
* When I am done choosing my post and do not add a comment to my post
* Then error message "Comment can't be blank!" pops up on the screen

Scenario #4
***
* Given I'm in a role of signed-in user 
and I am directed to the "Post page"
* When I have filled both the title and image field,
* Then the post has been made and any user of Instagram can see your posts


**COMMENT**

Scenario #1
***
* Given I'm in a role of signed-in user
* When I have filled the comment with content and click "comment"
* Then the comment is successfully posted with my username and respective date/time is indicated.

Scenario #2
***
* Given I'm in a role of signed-in user
* When I do not fill the comment with content and click "comment"
* Then I am redirected to the a Page labeled "Invalid Form"


**FOLLOW**

Scenario #1
***
* Given I'm in a role of a signed-in user
* If I do not already follow a specific user
* Then I see a "Follow" button on the right side of the username 
* Then I am successfully able to follow by clicking the follow button 
* And the relationship is saved

Scenario #2
***
* Given I'm in a role of a signed-in user
* If I do already follow a specific user
* Then I see an "Unfollow" button instead of the "Follow" button
* Once you are "unfollowing a user", their posts are not longer visible on your homepage
