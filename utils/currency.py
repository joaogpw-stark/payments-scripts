import locale


def format_to_brazilian_currency(amount_in_cents):
    if not isinstance(amount_in_cents, int):
        raise TypeError("Amount must be an integer (representing cents).")

    amount_in_reais = float(amount_in_cents) / 100.0

    formatted_value = "R${:,.2f}".format(amount_in_reais)

    formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")

    return formatted_value