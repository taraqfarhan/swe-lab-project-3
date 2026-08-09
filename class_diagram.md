# Class Diagram Specification

## System: Cafe Order Management System

**Patterns Demonstrated:** Singleton, Factory Method, Abstract Factory

---

## 1. Unified Class Diagram (Complete System)

```mermaid
classDiagram
    direction TB

    %% =========================================================================
    %% 1. SINGLETON PATTERN
    %% =========================================================================
    class OrderTracker {
        -OrderTracker _instance$
        +int order_count
        +__new__(cls) OrderTracker$
        +get_next_order_id() int
    }

    %% =========================================================================
    %% 2. FACTORY METHOD PATTERN
    %% =========================================================================
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

    Payment <|.. CardPayment : implements
    Payment <|.. CashPayment : implements
    PaymentHandler <|-- CardPaymentHandler : inherits
    PaymentHandler <|-- CashPaymentHandler : inherits

    CardPaymentHandler ..> CardPayment : creates
    CashPaymentHandler ..> CashPayment : creates
    PaymentHandler ..> Payment : uses

    %% =========================================================================
    %% 3. ABSTRACT FACTORY PATTERN
    %% =========================================================================
    class Cup {
        <<interface>>
        +serve()* str
    }

    class Container {
        <<interface>>
        +serve()* str
    }

    class CeramicCup {
        +serve() str
    }

    class GlassPlate {
        +serve() str
    }

    class PaperCup {
        +serve() str
    }

    class PaperBag {
        +serve() str
    }

    class PackagingFactory {
        <<interface>>
        +create_cup()* Cup
        +create_container()* Container
    }

    class ReusablePackagingFactory {
        +create_cup() Cup
        +create_container() Container
    }

    class DisposablePackagingFactory {
        +create_cup() Cup
        +create_container() Container
    }

    Cup <|.. CeramicCup : implements
    Cup <|.. PaperCup : implements
    Container <|.. GlassPlate : implements
    Container <|.. PaperBag : implements

    PackagingFactory <|.. ReusablePackagingFactory : implements
    PackagingFactory <|.. DisposablePackagingFactory : implements

    ReusablePackagingFactory ..> CeramicCup : creates
    ReusablePackagingFactory ..> GlassPlate : creates
    DisposablePackagingFactory ..> PaperCup : creates
    DisposablePackagingFactory ..> PaperBag : creates

    %% =========================================================================
    %% 4. CLIENT WORKFLOW RELATIONSHIPS
    %% =========================================================================
    class CafeClient {
        <<client>>
        +process_cafe_order(item_name, amount, payment_handler, packaging_factory)
    }

    CafeClient ..> OrderTracker : calls
    CafeClient ..> PaymentHandler : invokes
    CafeClient ..> PackagingFactory : invokes
```

---

## 2. Pattern-Specific Class Diagrams

### 2.1 Singleton Pattern (`OrderTracker`)

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

### 2.2 Factory Method Pattern (`PaymentHandler`)

```mermaid
classDiagram
    direction TB

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
    PaymentHandler --> Payment : uses
```

---

### 2.3 Abstract Factory Pattern (`PackagingFactory`)

```mermaid
classDiagram
    direction TB

    class PackagingFactory {
        <<interface>>
        +create_cup()* Cup
        +create_container()* Container
    }

    class ReusablePackagingFactory {
        +create_cup() Cup
        +create_container() Container
    }

    class DisposablePackagingFactory {
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

    class CeramicCup {
        +serve() str
    }

    class GlassPlate {
        +serve() str
    }

    class PaperCup {
        +serve() str
    }

    class PaperBag {
        +serve() str
    }

    PackagingFactory <|.. ReusablePackagingFactory
    PackagingFactory <|.. DisposablePackagingFactory

    Cup <|.. CeramicCup
    Cup <|.. PaperCup
    Container <|.. GlassPlate
    Container <|.. PaperBag

    ReusablePackagingFactory ..> CeramicCup : creates
    ReusablePackagingFactory ..> GlassPlate : creates
    DisposablePackagingFactory ..> PaperCup : creates
    DisposablePackagingFactory ..> PaperBag : creates
```

---

## 3. Relationship & Multiplicity Summary

| Source Class                 | Target Class       | Relationship Type                      | Notation | Description                       |
| :--------------------------- | :----------------- | :------------------------------------- | :------- | :-------------------------------- |
| `CardPaymentHandler`         | `PaymentHandler`   | Inheritance (Generalization)           | `--\|>`  | Extends base creator class        |
| `CashPaymentHandler`         | `PaymentHandler`   | Inheritance (Generalization)           | `--\|>`  | Extends base creator class        |
| `CardPayment`                | `Payment`          | Realization (Interface Implementation) | `..\|>`  | Implements payment contract       |
| `CashPayment`                | `Payment`          | Realization (Interface Implementation) | `..\|>`  | Implements payment contract       |
| `ReusablePackagingFactory`   | `PackagingFactory` | Realization (Interface Implementation) | `..\|>`  | Implements factory contract       |
| `DisposablePackagingFactory` | `PackagingFactory` | Realization (Interface Implementation) | `..\|>`  | Implements factory contract       |
| `CeramicCup` / `PaperCup`    | `Cup`              | Realization (Interface Implementation) | `..\|>`  | Implements cup interface          |
| `GlassPlate` / `PaperBag`    | `Container`        | Realization (Interface Implementation) | `..\|>`  | Implements container interface    |
| `CafeClient`                 | `OrderTracker`     | Dependency (Usage)                     | `..>`    | Retrieves next unique order ID    |
| `CafeClient`                 | `PaymentHandler`   | Dependency (Usage)                     | `..>`    | Delegates payment execution       |
| `CafeClient`                 | `PackagingFactory` | Dependency (Usage)                     | `..>`    | Requests matched packaging family |
