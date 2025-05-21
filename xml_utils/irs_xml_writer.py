import re
import xml.etree.ElementTree as XML
from decimal import Decimal

from data.Tables import Table9_2A

__NAMESPACE_REGEX = re.compile(' xmlns=\\".*>')


def add_table_9_2A_to_file(irs_xml_file_path: str, irs_xml_file_output_path: str, accumulator: Table9_2A):
    with open(irs_xml_file_path, 'r') as f:
        text = f.read()

    # hack: remove garbage characters on beginning of file(they appear sometimes from files obtained from the portal)
    start = text.index('<')
    text = text[start:]

    # hack: remove namespace for easier parsing and portability between years
    text = re.sub(__NAMESPACE_REGEX, '>', text)

    xml = XML.fromstring(text)

    anex_j_element = xml.find(".//AnexoJq092AT01")

    if anex_j_element is None:
        raise Exception("Must have annex J created")

    # in case some entries were already present in the report
    line_number = 1 + len(anex_j_element)

    realized_value = Decimal(0.0)
    acquisition_value = Decimal(0.0)
    expenses = Decimal(0.0)
    tax_paid_abroad = Decimal(0.0)

    for entry in accumulator.entries:
        new_element = XML.fromstring(f"""
            <AnexoJq092AT01-Linha numero="{line_number}">
			    <NLinha>{950 + line_number}</NLinha>
				<CodPais>{entry.country_code}</CodPais>
				<Codigo>{entry.code}</Codigo>
				<AnoRealizacao>{entry.realized_year}</AnoRealizacao>
				<MesRealizacao>{entry.realized_month}</MesRealizacao>
				<DiaRealizacao>{entry.realized_day}</DiaRealizacao>
                <ValorRealizacao>{entry.realized_value}</ValorRealizacao>
                <AnoAquisicao>{entry.acquisition_year}</AnoAquisicao>
                <MesAquisicao>{entry.acquisition_month}</MesAquisicao>
                <DiaAquisicao>{entry.acquisition_day}</DiaAquisicao>
                <ValorAquisicao>{entry.acquisition_value}</ValorAquisicao>
                <CodPaisContraparte>{entry.counterpart_country_code}</CodPaisContraparte>
                <DespesasEncargos>{entry.expenses}</DespesasEncargos>
                <ImpostoPagoNoEstrangeiro>{entry.tax_paid_abroad}</ImpostoPagoNoEstrangeiro>
			</AnexoJq092AT01-Linha>
        """)

        anex_j_element.append(new_element)

        line_number += 1
        realized_value += entry.realized_value
        acquisition_value += entry.acquisition_value
        expenses += entry.expenses
        tax_paid_abroad += entry.tax_paid_abroad

    realized_value_element = xml.find(".//AnexoJq092AT01SomaC01")
    realized_value_element.text = str(Decimal(realized_value_element.text) + realized_value)

    acquisition_value_element = xml.find(".//AnexoJq092AT01SomaC02")
    acquisition_value_element.text = str(Decimal(acquisition_value_element.text) + acquisition_value)

    expenses_element = xml.find(".//AnexoJq092AT01SomaC03")
    expenses_element.text = str(Decimal(expenses_element.text) + expenses)

    tax_paid_abroad_element = xml.find(".//AnexoJq092AT01SomaC04")
    tax_paid_abroad_element.text = str(Decimal(tax_paid_abroad_element.text) + tax_paid_abroad)

    with open(irs_xml_file_output_path, 'w') as f:
        f.write(XML.tostring(xml, encoding='unicode'))
