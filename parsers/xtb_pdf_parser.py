from decimal import Decimal
from data.Tables import Table9_2AEntry
from typing import List

import pypdf
import re

__TABLE_I_B_PREAMBLE = '9.2 INCREMENTOS PATRIMONIAIS DE OPÇÃO DE ENGLOBAMENTO*'

__TABLE_I_B_ENTRY_REGEX = re.compile(
    '\\d{3,} \\d{1,3} G\\d{2} \\d{4} \\d{1,2} \\d{1,2} \\d+\\.\\d{2} \\d{4} \\d{1,2} \\d{1,' \
    '2} \\d+\\.\\d{2} \\d+\\.\\d{2} \\d+\\.\\d{2} \\d+')

__TABLE_III_B_PREAMBLE = 'OUTROS INCREMENTOS PATRIMONIAIS DE OPÇÃO DE ENGLOBAMENTO [art.º 10.º, n.º 1, als. c), ' \
                       'e e) a h), do CIRS]'


def extract_table_9_2a_entries(pdf_file_path: str) -> List[Table9_2AEntry]:
    reader = pypdf.PdfReader(pdf_file_path)

    table_pages = filter(lambda page: __TABLE_I_B_PREAMBLE in page.extract_text(), reader.pages)

    lines = ''.join([page.extract_text() for page in table_pages]).split('\n')
    table_lines = list(
        filter(
            lambda line: __TABLE_I_B_ENTRY_REGEX.match(line),
            lines
        )
    )

    entries = []
    for line in table_lines:
        tokens = line.split(' ')

        entry = Table9_2AEntry(
            n_line=int(tokens[0]),
            country_code=int(tokens[1]),
            code=tokens[2],

            realized_year=int(tokens[3]),
            realized_month=int(tokens[4]),
            realized_day=int(tokens[5]),
            realized_value=Decimal(tokens[6]),

            acquisition_year=int(tokens[7]),
            acquisition_month=int(tokens[8]),
            acquisition_day=int(tokens[9]),
            acquisition_value=Decimal(tokens[10]),

            expenses=Decimal(tokens[11]),
            tax_paid_abroad=Decimal(tokens[12]),

            counterpart_country_code=int(tokens[13].replace('XTB', '')) # hack due to 'XTB' coming on same line sometimes
        )

        entries.append(entry)

    return entries
