# Exploring NATS in 5 Minutes

Hello, I am Sazzad, Staff Software Engineer in Machine learning at Infolytx Inc. Today I am going to discuss NATS, its different architectures, and why & how we have used it in our solution.
First of all, Let’s have a clear understanding of why we need a Message queue. For an application, we have several services that are needed to interact with each other. If we develop it using the synchronous model, services will be highly coupled and will have to wait for other services. In our case, neither immediate response is necessary nor immediate consistency is necessary. Some ms delay or eventual consistency is fine. So message queue is a great service for that. But Why we choose NATS as a message queue? I am going to discuss it below.

## NATS
So what is NATS? what official document says is
“ NATS messaging enables the exchange of data that is segmented into messages among computer applications and services. These messages are addressed by subjects and do not depend on the network location. This provides an abstraction layer between the application or service and the underlying physical network. Data is encoded and framed as a message and sent by a publisher. The message is received, decoded, and processed by one or more subscribers.”
That means it is serving the purpose of a message queue. I am not going to discuss any comparison between NATS and other Message queues like Kafka, RabbitMQ. I am more focused to describe the features of NATS.
## Why we choose NATS for our solution?
- Scalable Services and Streams.
- At-most-Once and At-least-Once Qos
- Routing on Subjects/ Topics, not IP and Hostnames.
- Proven High-performance Publish/Subscribe Router.
- Simple, Secure, Performant, and resilient.
- Built from the ground up to be Cloud-native.
- Support for over 30 different client languages.
- Production-Proven for over 9 years.

## Use Cases
- Cloud Messaging
- IoT and Edge
- Augmenting or Replacing Legacy Messaging
## NATS Integrations
- can be easily installed and deployed to Kubernetes
- Prometheus Exporters
- Dapr.io Component Integration
- Spring Boot starter
- NATS/ Kafka Bridge
- Go-Cloud and Go-Micro pub/sub integration

## Service Latency

service latency

## Using a NATS System
- Free Community Serves(demo.nats.io)
- Kubernetes scripts
- docker ( docker run -p 4222:4222 -ti nats:latest
- Additional Information ( Installation)

## Some NATS user

## Contribution and Project Velocity
- Over 1k contributors
- 33 client languages
- 15k GitHub stars across repositories
- 75 public repositories
- 100M download
- ~1600 Slack members
- 20+ releases of the NATS server since June 2014, ~= 5/yr

## NATS different Architectures
NATS implements a publish-subscribe message distribution model for one-to-many communication. All messages in NATS are subject-based and by-default architecture is Publish-Subscribe.
Let’s say a publisher publishes a message with the subject “a”. all the subscribers who are listening on the subject will get that message. So if you have any part architecture where service posts an event and some other services ( one or more ) need to know that event, you can use this model.

### Publish-Subscribe

Publish-Subscribe
### Subject-Based Messaging
Fundamentally, NATS is about publishing and listening for messages. Both of these depend heavily on Subjects that scope messages into streams or topics. At its simplest, a subject is just a string of characters that form a name the publisher and subscriber can use to find each other.

### Subject-Based Messaging
#### Subject Hierarchies
The . character is used to create a subject hierarchy. For example, a world clock application might define the following to logically group related subjects:
time.us
time.us.east
time.us.east.atlanta
time.eu.east
time.eu.warsaw
#### Wildcards
NATS provides two wildcards that can take the place of one or more elements in a dot-separated subject. Subscribers can use these wildcards to listen to multiple subjects with a single subscription but Publishers will always use a fully specified subject, without the wildcard.
you can read here in more detail.
#### Queue Groups
NATS provides a built-in load balancing feature called distributed queues. Using queue subscribers will balance message delivery across a group of subscribers which can be used to provide application fault tolerance and scale workload processing.

### Queue Groups Load Balancing
For example, a service upload 1000 images to be processed. You have 10 ImageProcessorServer. when the publisher publishes the event, all 1k images will be distributed to your 10 ImageProcessorServer by NATs when you use the Queue group model. NATS will do load-balancing for you. isn’t it cool? :)
### Request-Reply
Request-Reply is a common pattern in modern distributed systems. A request is sent and the application either waits on the response with a certain timeout or receives a response asynchronously. The increased complexity of modern systems requires features such as location transparency, scale up and scale down observability, and more. Many technologies need additional components, sidecars, and proxies to accomplish the complete feature set.

When you need an acknowledgment from Subscriber you can use this model. So? Nats can work both synchronous ways as well as asynchronous way. Great!!

## Our need and NATS
So which nats architecture we have used finally? In our Solution architecture, we needed the synchronous model( request-reply), publish-Subscribe, load balancing all of that.
We have the mobile app (both android and ios)which will upload images through the backend. We could use NATS request-reply. But we have kept trust in the traditional request-reply(REST-based) model.
With the Image, Our ML-engine does some have a prediction. We will be using Queue-group load-balancing model here.
Some services in our architecture are waiting (obviously non-blocking ) for the prediction results. After the prediction results have been prepared, notification is sent to them using the publish-subscribe model.
This is all we can share for you now. :)
## Resources


## need to use 
https://medium.com/@abdulhasibsazzad/exploring-nats-in-5-minutes-e53291821eb3

for images