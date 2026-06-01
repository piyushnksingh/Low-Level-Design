"""
1. Functional Requirements
    The system should:
        -> Accept a call request
        -> Route the call to an appropriate provider
        -> Retry on failure
        -> Track call state transitions
        -> Expose current status of a call

2. Core Concepts
A call can go through states like:
CREATED -> ROUTING -> IN_PROGRESS -> SUCCESS
                           |
                        FAILED
                           |
                        RETRYING

3. High Level Components:
Client
   |
CallOrchestrator
   |
   +---- RouterStrategy
   |
   +---- ProviderFactory
   |
   +---- RetryManager
   |
   +---- CallRepository

"""

import uuid
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod

# =========================
# CALL STATES
# =========================
class CallState(Enum):
    CREATED = "CREATED"
    ROUTING = "ROUTING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


# =========================
# CALL ENTITY
# =========================
@dataclass
class Call:
    call_id: str
    customer_id: str
    phone_number: str
    call_state: CallState
    retry_count: int = 0
    provider: str = None
    created_at: datetime = datetime.now()


# =========================
# PROVIDER INTERFACE
# =========================
class CallProvider(ABC):
    @abstractmethod
    def place_call(self, call: Call) -> bool:
        pass

# =========================
# CONCRETE PROVIDER IMPLEMENTATIONS
# =========================
class TwilioProvider(CallProvider):
    def place_call(self, call: Call) -> bool:
        print(f"Calling via Twilio for {call.phone_number}")
        return False # Simulating failure

class ExotelProvider(CallProvider):
    def place_call(self, call: Call) -> bool:
        print(f"Calling via Exotel for {call.phone_number}")
        return True # Simulating success


# =========================
# FACTORY PATTERN
# =========================
class ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str) -> CallProvider:
        providers = {
            "twilio": TwilioProvider(),
            "exotel": ExotelProvider()
        }
        return providers[provider_name]


# =========================
# STRATEGY PATTERN
# =========================
class RoutingStrategy(ABC):
    @abstractmethod
    def route(self, call: Call) -> str:
        pass

# =========================
# ROUND ROBIN STRATEGY
# =========================
class RoundRobinStrategy(RoutingStrategy):
    def __init__(self):
        self.providers = ["twilio", "exotel"]
        self.current_index = 0

    def route(self, call: Call) -> str:
        provider = self.providers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.providers)
        return provider

class LeastFailureRoutingStrategy(RoutingStrategy):
    def __init__(self):
        self.failure_count = {
            "twilio": 5,
            "exotel": 2
        }

    def route(self, call: Call) -> str:
        provider = min(self.failure_count,key=self.failure_count.get)
        return provider

    def record_failure(self, provider_name: str):
        self.failure_count[provider_name] += 1


# =========================
# REPOSITORY PATTERN
# =========================
class CallRepository:
    def __init__(self):
        self.calls = {}

    def save(self, call: Call):
        self.calls[call.call_id] = call

    def get(self, call_id: str) -> Call:
        return self.calls.get(call_id)


# =========================
# RETRY MANAGER
# =========================
class RetryManager:
    MAX_RETRIES = 3

    def should_retry(self, call: Call) -> bool:
        return call.retry_count < self.MAX_RETRIES


# =========================
# MAIN ORCHESTRATOR
# =========================
class CallOrchestrator:
    def __init__(self, router: RoutingStrategy, repository: CallRepository, retry_manager: RetryManager):
        self.router = router
        self.repository = repository
        self.retry_manager = retry_manager

    def create_call(self, customer_id: str, phone_number: str) -> str:
        call = Call(
            call_id=str(uuid.uuid4()),
            customer_id=customer_id,
            phone_number=phone_number,
            call_state=CallState.CREATED
        )

        self.repository.save(call)
        self.process_call(call)
        return call.call_id

    def process_call(self, call: Call) -> None:
        while True:
            call.call_state = CallState.ROUTING
            provider_name = self.router.route(call)
            provider = ProviderFactory.get_provider(provider_name)

            call.call_state = CallState.IN_PROGRESS
            success = provider.place_call(call)

            if success:
                call.call_state = CallState.SUCCESS
                print(f"Call Success via {provider_name}")
                break

            print(f"Call Failed via {provider_name}")
            call.call_state = CallState.FAILED

            if not self.retry_manager.should_retry(call):
                print("Max retries reached")
                break

            call.call_state = CallState.RETRYING
            call.retry_count += 1
            print(f"Retrying call... Attempt {call.retry_count}")

        self.repository.save(call)

    def get_call_status(self, call_id: str) -> CallState | str:
        call = self.repository.get(call_id)
        if not call:
            return "Call Not Found"
        return call.call_state


# =========================
# CLIENT CODE
# =========================

def main():

    repository = CallRepository()
    router = RoundRobinStrategy()
    retry_manager = RetryManager()

    orchestrator = CallOrchestrator(router, repository, retry_manager)

    call_id = orchestrator.create_call("cust_01", "9139143356")

    print("\nFinal Call Status:", orchestrator.get_call_status(call_id))


if __name__ == "__main__":
    main()