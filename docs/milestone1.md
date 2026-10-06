**CP317B – Software Engineering**

**Milestone 01: Food Delivery System**

**Group ID:** CP-317-B - Software Engineering - 6

**Team Members:**

Amir Syed — \[Backend- distance validation, authentication, APIs\]

Ervin Aggari — \[Frontend- menu/restaurant browsing, customer/restaurant
dashboards\]

Rahman Popalzai — \[Product Owner- order placement, order processing\]

Hammad Khan — \[Database- restaurant accounts, menu management,
messages\]

Omar Najwa — \[Live tracking- order tracking, delivery status, customer
messages\]

**Abstract:**

The Food Delivery System is designed to provide customers with a simple
way to browse nearby restaurants, view menus, place food orders, and
have those orders delivered to a selected location. The system will
limit available restaurants to those within a 35 km radius of the
delivery location and will provide customers with order status updates
and an estimated delivery time.

The system will also support restaurant managers and delivery drivers by
allowing restaurants to manage menus and orders while drivers receive
delivery information and routing assistance. A monitored messaging
system will allow customers and restaurants to communicate about active
orders. The overall goal of the project is to create a convenient,
reliable, and privacy-conscious food delivery platform for customers,
restaurants and drivers.

Existing food delivery services can sometimes create problems when
payment methods fail unexpectedly or when orders are accepted even
though the delivery distance is impractical for the assigned driver.
These situations can lead to cancelled deliveries, confusion between
customers, restaurants and drivers. Resulting in wasted time for
everyone involved. Our Food Delivery System aims to reduce these issues
by verifying delivery distance before an order is accepted and providing
clearer order communication and creating a more reliable ordering
process for customers, restaurants, and drivers.

**1. Project Description**

The Food Delivery System will allow customers to browse nearby
restaurants, view menus, place food orders and have those orders
delivered to a location of their choice. Restaurants within a maximum
distance of 35 km from the delivery location will be available to the
customer. The system will also allow customers to track the status of
their orders and communicate with the restaurant through a monitored
messaging system. This communication feature will allow customers and
restaurants to contact each other about orders while helping maintain
appropriate standards within the platform. Restaurants will also be able
to manage their menus, incoming orders, delivery statuses and basic
sales information.

**2. Project Objectives**

1.  Allow customers to browse restaurants within a 35 km radius of their
    selected delivery location.

2.  Allow customers to view restaurant menus and place food orders
    through a simple and easy-to-use interface.

3.  Provide accurate distance checking so that orders can only be placed
    with restaurants that fall within the supported delivery range.

4.  Allow customers to track the current status of their order from
    placement to delivery.

5.  Provide a monitored messaging system that allows customers and
    restaurants to communicate about an active order.

6.  Allow restaurants to manage their menus, incoming orders, and
    delivery status.

**3.** **Initial Product Backlog**

| **Story ID** | **Story Title** | **User Story** |
|:--:|----|----|
| CUS-1 | Browse Restaurants | As a customer, I want to browse restaurants within 35 km of my selected delivery location so that I can see which restaurants can deliver to me. |
| MENU-1 | View Menu | As a customer, I want to view a restaurant's menu so that I can decide what food I want to order. |
| ORD-1 | Place Order | As a customer, I want to place a food order through the system so that I can have food delivered to my selected location. |
| ORD-2 | Delivery Estimate | As a customer, I want to see an estimated delivery time so that I know approximately when my food will arrive. |
| ORD-3 | Track Order | As a customer, I want to track the status of my order so that I know what stage my order is currently at. |
| REST-1 | Update Order Status | As a restaurant manager, I want to update an order's status so that customers know whether their order is accepted, being prepared or ready or on the way. |
| DRV-1 | Delivery Routing | As a delivery driver, I want the system to provide an efficient route between the restaurant and customer so that I can complete deliveries in a timely manner. |
| DRV-2 | Delivery Assignment | As a delivery driver, I want the system to assign deliveries based on my location and availability so that deliveries can be completed efficiently. |
| CHAT-1 | Order Messaging | As a customer, I want to communicate with the restaurant about an active order so that I can resolve problems or ask questions. |
| MENU-2 | Manage Menu | As a restaurant manager, I want to add, update, or remove menu items so that customers always see the restaurant's current offerings. |

**4. Ethical Considerations**

1\. Customer Location and Privacy

> The Food Delivery System will require a delivery location in order to
> complete an order. To protect customer privacy the system will not
> require constant live location tracking. Instead, customers will
> manually choose or enter the location where they want their food
> delivered. The delivery address will only be shared with the
> restaurant and delivery driver when it is necessary to complete the
> order. Precise location information should only be kept for as long as
> it is required and should not be used for unrelated purposes.

2\. Payment and Financial Security

> Customers may need to provide credit or debit card information when
> placing an order. This information must be protected. The system
> should use a secure third-party payment service rather than storing
> complete card information directly. Only the information required to
> confirm that a payment was successful should be kept by the Food
> Delivery System.

3\. Communication Privacy and User Safety

> The system will allow customers and restaurants to communicate about
> active orders through a monitored messaging system. Messages should
> only be used for communication related to the order and users should
> be informed that inappropriate or abusive messages may be reviewed.
> Access to conversations should be limited to the people involved in
> the order and authorized administrators when necessary. This helps
> protect users while still allowing the platform to respond to
> harassment, threats or other inappropriate behaviour.
