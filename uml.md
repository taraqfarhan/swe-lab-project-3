# UML Design Specification: Cafe Order Management System

## 1. Unified Conceptual Architecture

A single software application integrating **Singleton**, **Factory Method**, and **Abstract Factory** into one order processing workflow:

```
                          [ OrderTracker (Singleton) ]
                                       ^
                                       | (assigns order ID)
                                       |
Customer Order ------> [ process_cafe_order() ]
                             /                 \
                            /                   \
                           v                     v
            [ PaymentHandler ]            [ PackagingFactory ]
            (Factory Method)              (Abstract Factory)
             /            \                 /             \
            v              v               v               v
       CardPayment     CashPayment   DineInFactory   TakeawayFactory
                                           |                 |
                                     (creates Ceramic   (creates Paper
                                      Cup + Plate)       Cup + Bag)
```

---

## 2. Pattern-by-Pattern Sub-Diagrams

### 2.1 Singleton (`OrderTracker`)

```
Client A --------\
                  +------> [ OrderTracker ] (Single Global Counter)
Client B --------/
```

```mermaid
classDiagram
    class OrderTracker {
        -OrderTracker _instance$
        +int order_count
        +__new__(cls) OrderTracker$
        +get_next_order_id() int
    }
```

---

### 2.2 Factory Method (`PaymentHandler`)

```
PaymentHandler (Creator) ---------> Payment (Interface)
       ^                                    ^
       |                                    |
  +----+------------------+            +----+------------------+
  |                       |            |                       |
CardPaymentHandler  CashPaymentHandler  CardPayment        CashPayment
  |                       |
  v (creates)             v (creates)
CardPayment          CashPayment
```

```mermaid
classDiagram
    class PaymentHandler {
        <<abstract>>
        +create_payment()* Payment
        +process_bill(amount: float) void
    }
    class CardPaymentHandler {
        +create_payment() Payment
    }
    class CashPaymentHandler {
        +create_payment() Payment
    }
    class Payment {
        <<interface>>
        +pay(amount: float)* void
    }
    class CardPayment {
        +pay(amount: float) void
    }
    class CashPayment {
        +pay(amount: float) void
    }

    PaymentHandler <|-- CardPaymentHandler
    PaymentHandler <|-- CashPaymentHandler
    Payment <|.. CardPayment
    Payment <|.. CashPayment
    CardPaymentHandler ..> CardPayment : creates
    CashPaymentHandler ..> CashPayment : creates
```

---

### 2.3 Abstract Factory (`PackagingFactory`)

```
PackagingFactory (Interface) ------> Cup (Interface) + Container (Interface)
       ^                                    ^                    ^
       |                                    |                    |
  +----+--------------------+               |                    |
  |                         |               |                    |
DineInPackagingFactory  TakeawayPackagingFactory |               |
  |                         |               |                    |
  +---> CeramicCup          +---> PaperCup -+                    |
  +---> GlassPlate          +---> PaperBag ----------------------+
```

```mermaid
classDiagram
    class PackagingFactory {
        <<interface>>
        +create_cup()* Cup
        +create_container()* Container
    }
    class DineInPackagingFactory {
        +create_cup() Cup
        +create_container() Container
    }
    class TakeawayPackagingFactory {
        +create_cup() Cup
        +create_container() Container
    }
    class Cup {
        <<interface>>
        +serve()* str
    }
    class Container {
        <<interface>>
        +serve()* str
    }

    PackagingFactory <|.. DineInPackagingFactory
    PackagingFactory <|.. TakeawayPackagingFactory
    DineInPackagingFactory ..> Cup : creates
    DineInPackagingFactory ..> Container : creates
    TakeawayPackagingFactory ..> Cup : creates
    TakeawayPackagingFactory ..> Container : creates
```
