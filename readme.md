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

<hr>

## Implementation

### Structure
The project is structured to monitor the status of various services via a Python application. It comprises several components, each residing in its specific file within the `src` directory. Here is an overview of the main components and their responsibilities:

#### `main.py`
- **Overview**: Serves as the entry point of the application. It initializes and starts the monitoring and dummy services, handling the main execution flow.
- **Key Functions**:
  - Initializes the monitoring service with specified configurations.
  - Starts the dummy services to simulate real services turning on and off.
  - Sets up signal handling for graceful shutdown.

#### `MonitorService.py`
- **Location**: `src/MonitorService.py`
- **Purpose**: Continuously checks the status of registered services by attempting TCP connections. It extends `ConfigService` to utilize the registered services and their configurations.
- **Key Features**:
  - Implements efficient polling of services, ensuring checks are not more frequent than once per second.
  - Notifies subscribers about status changes, adhering to their polling frequencies and grace periods.

#### `ConfigService.py`
- **Location**: `src/ConfigService.py`
- **Purpose**: Manages the registration and deregistration of services and callers. It acts as a central configuration manager for adding, removing, and updating service and caller details.
- **Key Features**:
  - Allows adding and removing services dynamically.
  - Supports caller registration and management, enabling notifications for service status changes.


#### `DummyServicesCreationAndDeletion.py`
- **Location**: `src/DummyServices/DummyServicesCreationAndDeletion.py`
- **Purpose**: Simulates service status changes by programmatically starting and stopping services. This component is crucial for testing the monitor's responsiveness and correctness.
- **Key Features**:
  - Automatically creates and deletes dummy services to simulate a dynamic environment.
  - Helps in testing the monitor's ability to detect service status changes accurately.

#### Models
Models define the data structures used by the application:

- **`Caller.py`**:
  - **Location**: `src/models/Caller.py`
  - **Purpose**: Represents a caller or subscriber who receives notifications about service status changes.
  - **Key Features**:
    - Stores caller details and subscription information.

- **`Service.py`**:
  - **Location**: `src/models/Service.py`
  - **Purpose**: Represents a service being monitored, identified by host and port.
  - **Key Features**:
    - Holds service details, including status, outage schedules, and subscriber lists.

<hr>

#### Running Unit Tests
To run unit tests effectively, it's necessary to ensure that the `src` directory is appropriately referenced in the import statements. This can be done by prefixing `src.` to the module paths in the following files:

- **main.py**:
  - Change import statements to:
    ```python
    from src.MonitorService import MonitorService
    from src.DummyServices.DummyServicesCreationAndDeletion import PORTS, DummyServiceMain
    ```
- **ConfigService.py**:
  - Modify import statements to:
    ```python
    from src.models.Service import Service
    from src.models.Caller import Caller
    ```
- **MonitorService.py**:
  - Update the import statement to:
    ```python
    from src.ConfigService import ConfigService
    ```
These adjustments are necessary to ensure that Python can locate and import the modules correctly when the unit tests are executed, especially when the tests are run from a different directory that might not recognize the project's structure without the `src.` prefix.

<hr>

### Running the Application

#### Running Default Setup
To run the application, navigate to the `src` directory and execute `main.py`:

```bash
python main.py
```
This will start the service monitoring system along with dummy services and fake callers for testing.

#### Running Custom Setup
To add your own services and callers, under `src` directory, in python terminal execute these lines 
```python
import threading
import signal
from MonitorService import MonitorService
from DummyServices.DummyServicesCreationAndDeletion import PORTS, DummyServiceMain
from main import start_dummy_services, setup_monitor_service, setup_config_service, shutdown_handler

shutdown_event = threading.Event()

signal.signal(signal.SIGINT, shutdown_handler)

# To Initiate dummy services (Optional)
dummy_service_thread = threading.Thread(target=start_dummy_services)
dummy_service_thread.start()

# To Initiate Monitoring service
monitor_service = setup_monitor_service()

# ________________________________________________________________
# Commands for MonitorService
monitor_service.logs['<callerId>']  # holds logs related to callerId
monitor_service.services  # holds all services currently registered
monitor_service.callers  # holds all callers currently registered

# ________________________________________________________________
# Commands for ConfigService (Management)

# register a service
monitor_service.register_service(host='127.0.0.1', port=8080)

# unregister a service
monitor_service.unregister_service(host='127.0.0.1', port=8080)

# Set Planned Outage for a Service
from datetime import datetime
start_time = datetime(year=2023, month=1, day=1, hour=12, minute=0)
end_time = datetime(year=2023, month=1, day=1, hour=14, minute=0)
monitor_service.set_outage_time(host='127.0.0.1', port=8080, start=start_time, end=end_time)

# register a caller
monitor_service.register_caller(name="Example Caller", callerId="exampleCaller01")

# unregister a caller
monitor_service.unregister_caller(callerId="exampleCaller01")

# Subscription Management
monitor_service.subscribe_service(host="127.0.0.1", port=8080, callerId="exampleCaller01", polling_frequency=60)

# Unsubscribe a Caller from a Service
monitor_service.unsubscribe_service(host="127.0.0.1", port=8080, callerId="exampleCaller01")

```

### Future Improvements

- **ConfigService Database Integration**: ConfigService will transition to using a database for data storage, enhancing data persistence and scalability.
- **Disk-based Logging**: Logs will be stored on disk to ensure better log management and historical data analysis capabilities.
- **MonitorService Hosting and UX Enhancements**: MonitorService will be hosted as a standalone service, featuring a user-friendly interface that retains all current functionalities. This improvement aims to provide a better user experience and ease of access to monitoring features.
- **Customizable Alert Notifications**: Alerts will be sent through the preferred communication medium of each caller, allowing for more personalized and effective notifications.
