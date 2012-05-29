### CartVine ###

CartVine is a shopify app designed to allow shopify shops to post sale market and interact with their customers.

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
6. Sync Webhook
7. Sync Products - @TODO need to check for updated products that we have already imported; use the shopify updatedated_at_date
8. Sync Customers - @TODO need to check for updated customers that we have already imported; use the shopify updatedated_at_date
9. List of Products **@TODO pagination,design
10. List of Product Reviews **@TODO pagination,design
11. List of Reviewers **@TODO pagination,design
12. List of Emails **@TODO pagination,design


###### Customer Invitation Email ######

####### On Shopify order create #######
1. Store a record Webhook for local reference (and comparison checks to see if the user has deleted the webhook from their store)
2. On login/install an invitation email is scheduled to go out to the customer

####### On Shopify order create #######
1. Store Local Webhook record - for reference
2. settings.EMAIL_POST_DATE_TIMEDELTA stores the amount of time to wait before sending the email
2. Email to be sent to the Customer is created and post dated. This email will be sent to the email provided by the Customer and supplied in the order/create Webhook and stored locally
3. On the date scheduled in the @mail app model; the email is sent out to the Customer
4. The email invites the user to come and review their product


###### Customer sign up @TBD ######

1. Am considering making this process unnecessary and simply using JS to hook into a particular shops product list;
2. This JS is loaded from teh shop side; and will automatically create/update teh currently views products details
3. this js hook will also allow the user to login via facebook/twitter


1. User is taken to Customer sign in page (from email link)
2. *@TODO User elects to sign in using twitter or facebook (required)
3. *@TODO Once signed in; the user can upload photos of their product and comment on them as well as on the base product
3. *@TODO The Customer is also able to share the page on facebook and/or twitter (both options are present regardless)


###### Technical Notes ######

* All shopify items are replicated locally and have a shopify_id field which is used for syncing_
* On Owner login a task to sync each object is initialzed asynchronously and updates the local list using the .find(since_id=shopify_id)
* Email sending should be done via Mailchimp? or similar.. am using https://github.com/bradwhittington/django-templated-email which hooks intomailchimp or whats better postageapp
* @TODO will be abstracting the shopify interface at some point to allow for multiple endpoint providers other than just shopify



##### FACEBOOK LOGIN #####

### Perefer to use Assets api to store a javascript asset
http://api.shopify.com/asset.html
Allows us to load ssl version of our site if the shopify site is behind ssl without throwing ssl warnings

### Can be used in worst case but loses ssl validity
http://api.shopify.com/scripttag.html

Have access to Shopify object on teh shopify site
<script type="text/javascript">      var Shopify = Shopify || {};
      Shopify.shop = "price-turcotte-and-gleichner1525.myshopify.com";
      Shopify.theme = {"name":"radiance","id":3020382};
</script>
