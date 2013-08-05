![Screen Shot](http://cattopus23.com/img/panel-CAT540.jpg)

CAT540 Guardian Picture Grid
============================

A few people asked me what it could look like having a grid of iamges from the latest Guardian stories. So I created a quick _resizable_ sketch which pulls in the latest stuff from the Guardian API. You can run it full screen right down to a narrow single column :)

I've put the code here incase it's useful for anyone *but* because it uses the fullsized 460 images you'll need a _partner tier_ API key to make it run (unless you hack the code to use just the thumbnails). When you 1st run the app in the browser it'll ask you for your API key.

+ Running: http://guardianpicturegrid.appspot.com/

Secondary goal
--------------

The other reason for writing this code was experimenting with the framework of making the _owner_ of the application enter their own Guardian API key, which then gets placed into the database (or in a cookie/local storage if the project is client side only). Just so I don't have to make sure I don't accidently commit my own API key into github, or make a user have to edit a config file to get things running.
