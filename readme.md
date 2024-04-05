# Monitoring Service

## Instructions
This project aims to design and implement a service monitoring class in Python, enabling the monitoring of the status of multiple services. A service is defined by a host/port combination, and its status is determined by attempting a TCP connection on the specified port.


### Problem Statement
Design and implement a **service monitoring class**. This monitor will be tasked with monitoring the status of multiple services.

#### Service Definition
A service is defined as a host/port combination. The monitor checks the service status by establishing a TCP connection to the host on the specified port:
- If a connection is established, the service is considered up.
- If the connection is refused, the service is considered not up.

#### Features Overview
- **Service Status Monitoring:** Checks service availability via TCP connections, determining if services are up or down.
- **Dynamic Registration & Updates:**
    - **Service & Caller Management:** Supports adding or removing services and callers, enabling tailored monitoring.
    - **Subscription Management:** Allows callers to manage their subscriptions to service status updates, ensuring relevant notifications.
- **Efficient Polling:** Limits service polling to no more than once per second, optimizing resource use and ensuring efficient monitoring, regardless of subscriber count.
- **Planned Outage Management:** Offers a system for registering planned outages, suspending notifications during these periods to avoid unnecessary alerts.
- **Grace Periods:** Provides a grace time for unresponsive services before issuing notifications, minimizing false alarms. Adjusts polling frequency as needed for more accurate and timely monitoring.

<hr>

#### Criteria

* Object-Oriented Programming (OOP)
* SOLID Principles
  - *Single Responsibility Principle:* Each class has a single responsibility.
  - *Open/Closed Principle:* The system is open for extension but closed for modification.
  - *Liskov Substitution Principle:* Objects of a superclass shall be replaceable with objects of subclasses without breaking the application.
  - *Interface Segregation Principle:* Many client-specific interfaces are better than one general-purpose interface.
  - *Dependency Inversion Principle:* Depend on abstractions, not on concretions.
* Multi-threading and Concurrency
  * Given the need to monitor multiple services concurrently, implement efficient multi-threading or asynchronous programming to manage polling and notifications.

