# Exotel Integration

Exotel Integration for ERPNext.


## Installation
1. Install [bench & ERPNext](https://github.com/frappe/erpnext#installation).

2. Once setup is complete, add the "Exotel Integration" app to your bench by running
    ```
    $ bench get-app exotel_integration
    ```
3. Install the "Exotel Integration" app on the required site by running
    ```
    $ bench --site <sitename> install-app exotel_integration
    ```


## Setup

### Credentials setup
Once the installation is complete, go to you exotel account (my.exotel.com) and generate API key to setup the integration.

1. In your exotel account go to "API" page.
<img width="1440" alt="Screenshot 2022-07-31 at 9 02 19 AM" src="https://user-images.githubusercontent.com/13928957/182023434-b939ddef-28e9-4a8f-84b1-5baa9a8625b5.png">

2. Next click on "Create API Key" and create an API key with following permissions
<img width="540" alt="Screenshot 2022-07-31 at 9 13 43 AM" src="https://user-images.githubusercontent.com/13928957/182023498-df33970c-27f7-43db-80c5-f3fef5b7e5e8.png">

3. Once the key is generated got to you ERPNext account and open "Exotel Settings" page. Click on enable and fill the values of "Account SID", "API Key" & "API Token"
![explainer](https://user-images.githubusercontent.com/13928957/182023954-3dd3acc5-d691-4398-ae74-ee8276520d96.png)

### Setup to track calls

1. Login to your Exotel account and go to App Bazar.
2. Create a new App for a new flow.
3. Setup the flow as you wish it to be.
4. In your connect API under "Create popup..." and paste URL that you'll see in your "Exotel Settings" page once you are done with the [credentials setup](#credentials-setup).
<img width="1354" alt="Screenshot 2022-07-31 at 3 25 56 PM" src="https://user-images.githubusercontent.com/13928957/182024295-399e28ce-c3d6-4e0a-b670-c308b1696578.png">
5. After that add a "Passthru applet" under "After Call Conversation ends" and paste the same URL.

<img width="607" src="https://user-images.githubusercontent.com/13928957/182024373-f0fca261-3ee5-45eb-a39e-b92a94ff96bf.png">
<img width="607" alt="Screenshot 2022-07-31 at 5 06 52 PM" src="https://user-images.githubusercontent.com/13928957/182024422-3853eaef-60a4-4583-8577-260ad6b03fca.png">

> **Note:** Make sure to check "Make Passthru Async".

6. Similary, add another "Passthru applet" under "If nobody answers..." section and paste the same URL.

<img width="607" src="https://user-images.githubusercontent.com/13928957/182024475-02807c67-8917-46e1-87fa-6f37244dae92.png">
<img width="607" alt="Screenshot 2022-07-31 at 5 06 52 PM" src="https://user-images.githubusercontent.com/13928957/182024422-3853eaef-60a4-4583-8577-260ad6b03fca.png">

> **Note:** Make sure to check "Make Passthru Async".

7. Save the flow.
8. Now assign this newly created app to your **ExoPhone** from which you receive your business calls.

Once this is done, you should see all new incoming calls on your exotel phone number in the "Call Log" list in your ERPNext instance. 

## Setup for call popup

1. Create "Employee Group" based on call handling schedule. Make sure each employee in the group has a user linked to them and that it is correctly fetched into the table. Also make sure all the employees have their "mobile number" specified in the Employee master. Employees will recieve pop up only when calls are made to their number.
![image](https://user-images.githubusercontent.com/13928957/182024718-bca67c68-1b2e-4563-8579-ee1f9b295f21.png)

2. Go to Communication Medium.
3. Add your **ExoPhone** and schedule that number. Based on this schedule employees will receive the popup. Make sure that the name of the communication medium is your ExoPhone number. 
![image](https://user-images.githubusercontent.com/13928957/182024708-9cbfa255-0959-427e-8246-e6bb88687a49.png)



#### License

GNU General Public License (v3)
