# supernovashaman
This is largely a clone of Miguel Grinberg's 'Microblog' (https://github.com/miguelgrinberg/microblog).
I am deeply indebted to Mr. Grinberg for this sandbox of sorts!

~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.

MISSION STATEMENT

Spirictraft is a strategy card game I designed for my family and friends once upon a Christmas and while, unfortunately, they all thought it was "too complicated to play,"  they did like the cards themselves and some of them even expressed interest in a simpler remake of the game. So, I figured I'd rework Spiritcraft into something that doesn't last for more than a half hour per session and can be played well and enjoyably without much experience. That way, I could issue new cards to keep the game fresh or just for the fun of drawing and, for others, the fun of collecting art pieces. If you're reading this, get your unique access code from me, sign up, and start collecting some Spiritcraft cards! Making this card game has been incredibly, indescribably meaningful and motivating for me. So, thank you immensely for participating.

~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.

Key differences between Grinberg's Microblog and this project include:

- The SQLAlchemy ORM has been replaced in favor of PyMySQL and raw SQL statments.
- '.format()' methods have been replaced with 'f'-strings

Key differences between Grinberg's Microbog and this project will include:

- No Bootstrap. Instead, I will have built the HTML and CSS entirely from scrap.
- No localization/internationalization.
- Password validation, e.g. "must include a number, letter, special character..."
- Search capabilities other than Elasticsearch. I have found Elasticsearch difficult to work with.
- Disqus comment section for each card

~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.

UPCOMING FEATURES (in no particular order)

- CSS grid all the way!
- "Build-a-Card" feature
- "Greatest Gazette" feature
- "Trader's Tent" feature
- "What I do with your data" page (A: "Absolutely nothing.")
- Add favicons
- Admin access via Flask-Admin
- API: Buy me a coffee
- API: Facebook
- API: Instagram
- API: PayPal
- API: Twitter
- Avatar: Gravatar or upload
- Notification in user profile to sign up with Gravatar
- Card mgmt: Add an "upload image" link in "add card" form
- Database changes: Shopping cart, Orders
- Highlight most popular cards
- Form for making recommendations
- Form for reporting an issue (minor bugs, typos, etc.)
- Front page as news page
- Include address form on profile (plus one-time reminder for user to add address)
- Gray out shopping cart capabilities if no address, full name in profile.
- Move Buddha Bell
- No more cards: Sign-up feature to be notified when a card is restocked
- No more cards: Gray out cards that have a quantity of 0 (Or overlay "All gone!" symbol)
- Polls ("What feature should I work on next?" etc.)
- QR code to link to site (code found on promotional cards)
- Responsive design
- Restrictions on usernames, e.g. can't have 'shaman', 'SHAMAN', etc. in name
- Shopping/purchase capabilities
- Small CSS slide-up box that says, "Got it! Added to your favorites..."
- Switches to show/not show retired cards, in-stock cards
- Upon registration, log user in automatically
- Work on graying out profile info: no birthday checkbox if no address or if no name
- Prepare empty database "catch-alls"
- Supernova Shaman image on left of reg. form, Pythons below login form
- Admin forms: gray out Entity/Genera vs. Item/Order choices
- Badges over images/in right-hand corner of single-card pages: "New!," "Editor's Choice," "Running out!"
- "Powered by Python"
- Add available cards (original-art-only cards) soon...
- In card profiles: "This card is best compatible with (...)
- Brainstorm card fields