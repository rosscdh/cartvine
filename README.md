### SHOP HAPPY ###

Shop Happy is a shopify app designed to allow shopify shops to post sale market and interact with their customers.

The app flow is:

1. Owner installs app
2. App sets up order/create webhook
3. Email invitation to review and comment is sent to the customer; who's info we have from the order/create webhook
4. Customer logs in using twitter/facebook
5. Customer can upload pics of their product, write reviews as well as share on twitter/facebook
6. Additionally; the Owner can view a list of invitations (pending/sent)


###### Owner sign up ######

1. Owner installs shopify app in the normal way; via form on base page or by passing in ?shop=domain/full url to shop
2. On login/install a local shop is set up
3. On login/install a local user is set up (manytomany relationship between owner and shop; allows for many owners of 1 shop)
4. On login/install a webhook is installed on the shopify app; is re-installed if the user deletes it from shopify
5. **@TODO On login/install an invitation email is scheduled to go out to the customer
6. Sync Products
7. Sync Customers
8. **@TODO List of Products
9. **@TODO List of Product Reviews
10. **@TODO List of Reviewers
11. **@TODO List of Emails


###### Customer Invitation Email ######

1. *@TODO Email is sent to the email provided by the Customer and supplied in the order/create Webhook and stored locally
2. On the date scheduled in the @mail app model the email is sent to the Customer
3. The email invites the user to come and review their product


###### Customer sign up ######

1. User is taken to Customer sign in page (from email link)
2. *@TODO User elects to sign in using twitter or facebook (required)
3. *@TODO Once signed in; the user can upload photos of their product and comment on them as well as on the base product
3. *@TODO The Customer is also able to share the page on facebook and/or twitter (both options are present regardless)


###### Technical Notes ######

* All shopify items are replicated locally and have a shopify_id field which is used for syncing_
* On Owner login a task to sync each object is initialzed asynchronously and updates the local list using the .find(since_id=shopify_id)
* *@TODO Email sending should be done via Mailchimp? or similar


