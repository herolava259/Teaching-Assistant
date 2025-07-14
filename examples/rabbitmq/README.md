# How to use RabbitMQ

## I. What is exchanges
- In AMQP o-9-1 exchanges là các thực thể mà các publishers publish thông điệp sau đó được route đến một tập các queue hay là stream

## II. Exchanges Types 
- Exchange có thể là các kiểu khác nhau. An exchange type controls how to it routes the messages published to it. For example, one exchange type may use a topic (pattern)-based routing, while another can route all mesages to every bound queue unconditionally 

- RabbitMQ ships with multiple exchange types:

    * Fanout ~ multi-cast
    * Topic 
    * Direct 
    * Default direct exchange: a built-in with special characteristics
    * Load Randoms 
    * JMS Topic 
    * Consistent Hashing exchange 
    * Random exchange 
    * Recent history exchange 
### 1. Fanout

- Fanout exchanges route a copy of every message published to them to every queue, stream or exchange bound to it. The message's routing key is completely ignored 

### 2. Topic 
- Topic exchange use pattern matching of the message routing's key to the routing (binding) key pattern used at binding time 
- For the purpose of routing, the keys are separated into segments by. Some segments are populated by specific values, while others are populated by wildcards: * for exactly one segment and # for zero or more (including multiple) segments 

### 3. Direct 
- Direct exchanges route to one or more bound queues, streams or exchanges using an exact equivalance of a binding's routing key. 
- For example, a binding (routing) key of "abc" will match "abc" 


## VII. Examples:


## END. References

- [exchange-docs](https://www.rabbitmq.com/docs/exchanges)
- [basic-exchange-python](https://www.rabbitmq.com/tutorials/tutorial-one-python)
- [work-queues-python](https://www.rabbitmq.com/tutorials/tutorial-three-python)
- [publish-subcribe-python](https://www.rabbitmq.com/tutorials/tutorial-three-python)
- [routing-python](https://www.rabbitmq.com/tutorials/tutorial-four-python)
- [topis-python](https://www.rabbitmq.com/tutorials/tutorial-five-python)
- [rpc-python](https://www.rabbitmq.com/tutorials/tutorial-six-python)
- [github-docs](https://github.com/rabbitmq/rabbitmq-server/tree/main/deps)