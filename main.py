"""
CAFE ORDER MANAGEMENT SYSTEM
  1. SINGLETON PATTERN       -> OrderTracker (Central order counter & tracking)
  2. FACTORY METHOD PATTERN  -> PaymentHandler (Creates Card vs Cash payment)
  3. ABSTRACT FACTORY PATTERN -> PackagingFactory (Creates matching Cup & Container)

from abc import ABC, abstractmethod


# SINGLETON PATTERN

class OrderTracker:
    """
    Singleton Class:
    Guarantees only a single instance exists to manage global order counting.
    """
    _instance = None  # Holds the single instance

    def __new__(cls):
        """If no instance exists yet, create one else return the existing instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.order_count = 0  # Global order counter
        return cls._instance

    def get_next_order_id(self) -> int:
        """Increments and returns the next sequential order number."""
        self.order_count += 1
        return self.order_count


# FACTORY METHOD PATTERN: Payment Processing
# Defines a method for creating a Payment object, letting subclasses
# decide whether to instantiate CardPayment or CashPayment.

# Product
class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


# Concrete Products 
class CardPayment(Payment):
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} using Credit/Debit Card.")


class CashPayment(Payment):
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} using Cash.")


# Creator (Contains the Factory Method)
class PaymentHandler(ABC):
    @abstractmethod
    def create_payment(self) -> Payment:
        """The Factory Method: Overridden by subclasses to return a Payment object."""
        pass

    def process_bill(self, amount: float) -> None:
        """Core business workflow relying on the product from the factory method."""
        payment = self.create_payment()  # Call the factory method
        payment.pay(amount)


# Concrete Creators
class CardPaymentHandler(PaymentHandler):
    def create_payment(self) -> Payment:
        return CardPayment()
    

class CashPaymentHandler(PaymentHandler):
    def create_payment(self) -> Payment:
        return CashPayment()


# ABSTRACT FACTORY PATTERN: Packaging Suite
# Creates FAMILIES of matching packaging items (Cup + Container).
# - Reusable Family  -> Ceramic Cup + Glass Plate
# - Disposable Family -> Paper Cup + Paper Bag
# Prevents mixing a Ceramic Cup with a Paper Bag!

# Abstract Products
class Cup(ABC):
    @abstractmethod
    def serve(self) -> str:
        pass


class Container(ABC):
    @abstractmethod
    def serve(self) -> str:
        pass


# Concrete Products: Reusable Family
class CeramicCup(Cup):
    def serve(self) -> str:
        return "Reusable Ceramic Cup"


class GlassPlate(Container):
    def serve(self) -> str:
        return "Reusable Glass Plate"


# Concrete Products: Disposable Family
class PaperCup(Cup):
    def serve(self) -> str:
        return "Disposable Paper Cup"


class PaperBag(Container):
    def serve(self) -> str:
        return "Disposable Paper Bag"


# Abstract Factory
class PackagingFactory(ABC):
    """Abstract Factory: Declares methods to create all items in the packaging family."""
    @abstractmethod
    def create_cup(self) -> Cup:
        pass

    @abstractmethod
    def create_container(self) -> Container:
        pass


# Concrete Factories
class ReusablePackagingFactory(PackagingFactory):
    """Produces the Reusable family of packaging."""
    def create_cup(self) -> Cup:
        return CeramicCup()

    def create_container(self) -> Container:
        return GlassPlate()


class DisposablePackagingFactory(PackagingFactory):
    """Produces the Disposable family of packaging."""
    def create_cup(self) -> Cup:
        return PaperCup()

    def create_container(self) -> Container:
        return PaperBag()


# CLIENT CODE
def process_cafe_order (
    item_name: str,
    amount: float,
    payment_handler: PaymentHandler,
    packaging_factory: PackagingFactory
) -> None:
    """
      1. Uses Singleton (OrderTracker) to assign unique order IDs.
      2. Uses Factory Method (payment_handler) to process the bill.
      3. Uses Abstract Factory (packaging_factory) to assemble matching packaging.
    """
    # Singleton: Get next unique order ID from the shared tracker
    tracker = OrderTracker()
    order_id = tracker.get_next_order_id()
    print(f">>> [Order #{order_id}] New Order: '{item_name}' (Total: ${amount:.2f})")

    # Factory Method: Process payment dynamically
    payment_handler.process_bill(amount)

    # Abstract Factory: Prepare matched packaging family
    cup = packaging_factory.create_cup()
    container = packaging_factory.create_container()
    print(f"Packaging : Served in a {cup.serve()} & {container.serve()}")
    print(f"Order #{order_id} Completed Successfully!\n")


if __name__ == "__main__":
    print("CAFE ORDER MANAGEMENT SYSTEM")

    # Order 1: Cappuccino paid with Card (Reusable Packaging)
    process_cafe_order(
        item_name="Cappuccino",
        amount=8.50,
        payment_handler=CardPaymentHandler(),          # Factory Method
        packaging_factory=ReusablePackagingFactory()     # Abstract Factory
    )

    # Order 2: Muffin paid with Cash (Disposable Packaging)
    process_cafe_order(
        item_name="Muffin",
        amount=6.75,
        payment_handler=CashPaymentHandler(),          # Factory Method
        packaging_factory=DisposablePackagingFactory()   # Abstract Factory
    )

    # Order 3: Espresso paid with Card (Reusable Packaging)
    process_cafe_order(
        item_name="Double Espresso",
        amount=4.00,
        payment_handler=CardPaymentHandler(),          # Factory Method
        packaging_factory=ReusablePackagingFactory()     # Abstract Factory
    )

    # Show that all orders updated the same tracker
    tracker = OrderTracker()
    print(f"Total Orders Processed Today: {tracker.order_count}")
