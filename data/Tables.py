from dataclasses import dataclass, replace as copy, field
from decimal import Decimal
from typing import List


@dataclass
class Table9_2AEntry:
    n_line: int
    country_code: int
    code: str

    realized_year: int
    realized_month: int
    realized_day: int
    realized_value: Decimal

    acquisition_year: int
    acquisition_month: int
    acquisition_day: int
    acquisition_value: Decimal

    expenses: Decimal
    tax_paid_abroad: Decimal

    counterpart_country_code: int

@dataclass
class Table9_2A:
    entries: List[Table9_2AEntry] = field(default_factory=lambda: [])

    def get_sum_acquisition(self) -> Decimal:
        return sum(
            map(
                lambda e: e.acquisition_value,
                self.entries
            )
        )

    def add_entry(self, entry: Table9_2AEntry):
        # replace line number with the right one
        cpy = copy(entry)
        cpy.n_line = 951 + len(self.entries)

        self.entries.append(cpy)

