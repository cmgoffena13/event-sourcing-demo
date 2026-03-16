from decimal import Decimal
from uuid import UUID

from eventsourcing.domain import Aggregate, event


class Transfer(Aggregate):
    @event("Executed")
    def __init__(
        self, from_account_id: UUID, to_account_id: UUID, amount: Decimal
    ) -> None:
        self.from_account_id: UUID = from_account_id
        self.to_account_id: UUID = to_account_id
        self.amount: Decimal = amount
