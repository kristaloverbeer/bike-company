# Bike Company

## Improve this project


### Message Queue Broker
This project currently does not provide a Message Queue broker infrastructure to allow the gateway to update database records 
from `trip` and/or `bike` service as of the location of a bike or if it is currently in use or not.

Ideas to do so:

Create a directory `infrastructure` at the root of the project that will contains a `docker-compose` file with a image 
of `RabbitMQ` for instance.

To consume message, we need a listener that listen continuously for new messages on a queue on a common Exchange(RabbitMQ specific).
RabbitMQ allows to develop a Publish/Suscribe architecture, which means that a service can publish one message on an
Exchange with a routing key, and consumers can then create their queue to consume this message,
on the condition that the consumer register its queue with the same Exchange and binding key.
Then, if all registered consumers consumed the message, the latter is deleted (if this policy is chosen).

- Publish a message with Kombu (library implementing messaging for a lot of differents message broker services,
allowing us to change the technology if need be later without touching the code base).

```python
import typing

from kombu import Producer, Connection, Exchange


class MessageProducer:
    def __init__(self, connection: Connection, exchange: Exchange, routing_key: str) -> None:
        self.connection = connection
        self.exchange = exchange
        self.routing_key = routing_key

    def send(self, body: typing.Any) -> None:
        producer = self._get_producer()
        producer.publish(
            body=body,
            routing_key=self.routing_key,
        )

    def _get_producer(self) -> Producer:
        return Producer(self.connection, self.exchange, self.routing_key)

```

- Listen and consume messages:
```python
from kombu import Connection
from kombu.mixins import ConsumerMixin


class Runner(ConsumerMixin):
    def __init__(self, connection, config, executor):
        self.config = config
        self.executor = executor
        self.connection = connection

    def get_consumers(self, consumer_cls, channel):
        return [
            consumer_cls(
                queues=[self.config.queue_1],
                no_ack=True,
                callbacks=[self.callback_function_1],
            ),
            consumer_cls(
                queues=[self.config.queue_2],
                no_ack=True,
                callbacks=[self.callback_function_2],
            )
        ]

    def stop(self):
        self.should_stop = True
        self.connection.release()

    def callback_function_1(self, body, message):
        executee = self.executor.submit(self._process_callback_function_1, body, message)

        potential_exception = executee.exception()
        if potential_exception:
            self.logger.critical(executee.exception())

    def callback_function_2(self, body, message):
        executee = self.executor.submit(self._process_enriched_transaction_annotated_message, body, message)

        potential_exception = executee.exception()
        if potential_exception:
            self.logger.critical(executee.exception())

    def _process_callback_function_1(self, body, message):
        # apply business logic here to actually process the message
        pass
        
    def _process_callback_function_2(self, body, message):
        # apply business logic here to actually process the message
        pass

def run(executor):
    config = Configuration()

    with Connection(config.AMQP_URI) as amqp_connection:
        runner = Runner(
            connection=amqp_connection,
            config=config,
            executor=executor,
        )
        try:
            runner.run()
        except KeyboardInterrupt:
            runner.stop()


if __name__ == '__main__':
    with ThreadpoolExecutor(max_workers=2) as executor:
        run(executor)

```
Why the ThreadPoolExecutor ?
In its basic state, the Runner will stop at any message that throws an error.
To avoid this behaviour, we just wrap the processing function in a thread that will allows us to get the error logs,
yet keep alive the Consumer process.

```python
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor


class ThreadpoolExecutor(ThreadPoolExecutor):
    def submit(self, function, *args, **kwargs):
        return super(ThreadpoolExecutor, self).submit(
            self._function_wrapper, function, *args, **kwargs
        )

    def _function_wrapper(self, function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            raise sys.exc_info()[0](traceback.format_exc())

```

To finish with, we just have to add this consumer runner:
- Either in a separate docker along the API docker (to respect the Docker philosophy to keep one process per docker)
- Or by using for instance `Supervisord` to launch both services in the same Docker container.

### Project structure
This project might be improve by a better project structure.

- Service packages

Because a lot of interactions between the different services might occur, a `service` package containing all the logic 
needed (one module per service to interact with) might improve the readability and testing of the project.
Each service should be represented by a class which will be injected in the API repositories for instance.

### Tests
This project currently does not contain any tests of any nature.
Unit tests and integration tests should be implemented for each service.

### Common code base
Because a lot of services with reuse the same code base (publish/consume messages from the broker, expose API endpoints),
a new package at the root of this project and regrouping all repetitive pieces of code might improve a lot the 
 readability and have a much cleaner code base.
In order to easily make use of this package, a good solution might by to create a base Docker image for all projects,
and install all common dependencies (external packages) and install the common package (logging, API factory,...).
Then, you just have to make every services created inherit from this image instead of the base image (here python:3.6-alpine).

### Main Makefile
In order to easily launch a local infrastructure and all services at the same time, a `Makefile` at the root of the project
launching all services with the gateway might make the life of developers much easier.
We can even extend the idea with a mako template to allow the developer to launch specific services in order not to overflow
his computer.

### wait-for-database.sh
This kind of script help to answer a major problem in docker and the interactions between containers.
Docker consider a container ready when this one return a status `ready`, yet this does not mean that
the process launched inside the container has finished.
To answer this problem (which can come up when for instance you want to apply your latest database migrations at the start of the service)
it is highly recommanded to develop a script or find one online (https://github.com/vishnubob/wait-for-it) and execute it
in the docker container entrypoint/command.

### Corner cases
A direct impact from the lack of tests is that a few corner cases only were tested,
specifically regarding the API response on bad input for instance.
There is probably some places where some conditional checks should be added. 


## Explanations/Decisions on this project
The choices regarding the technology (Python, Flask framework for the APIs, Postgresql for a database...) were made exclusively because I feel the
most comfortable with them.

- `flask_*` for utilities around the APIs like migrations, database handler,...

Flask is a micro-framework that can have differents issues with circling dependencies imports, having a unique engine for the 
database per API etc..., which lead to either having to develop our own modules for handling the database or tricking the paths
to use tools like `alembic`. It can take time and give headaches. Which is why I choose to use these packages,
mainly to gain time on developing the important features.

- `v1` prefix for each route expect the basic ones (index, ping,...)

Versioning APIs is an important part that allows developers to more easily update the routes and develop
breaking changes in a new version.
This can then be handled by the gateway to maintain some old APIs to be exposed to the front for users that does not have
the latest version of the mobile application but still make it work or
the latest updates for browers or other technology limits for instance.

To complete this, Flask give a `blueprint` utility that help reflect this versioning and/or routes that answer different purposes.

- `schema` module for each database model.

`marshmallow` is a convenient library that allows developers to execute operations such as serialization and deserialization
more easily and return errors when the format is not respected or business rules are broken before interrogating the database
or inserting bad records. Per field rules or rules for the whole object can be implemented in that purpose.

- `repository package`

In a "Domain Driven Design" approach, the seperation of concerns is a important point.
To try and answer this, I like to keep my API routes clear of business rules (repositories) or
technological implementations (schemas, models, flask_sqlalchemy) out of the routes, and just keep
input processing and output formatting logic in it.
This make, in my opinion, code better structured, more easily readable and more extensible.

- `Makefiles`

The written `makefile` per service are a sweet syntaxic sugar that dispose the burden to remember all
docker and docker-compose commands and just apply `make run` to build and launch a stack,
`make clean` if we want a clean slate to test manually some cases.

- Docker networks

In order for all services to communicate between themselves, we need a common network for each service in
the same group.
Creating public and/or private named networks help to this purpose.

Be careful, you often have to manually create the networks before using them : 
```bash
docker network create >named_network<
```

