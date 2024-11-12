class Address():
    def __init__(self, street, city, state, zip_code, street2=""):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __str__(self):
        lines = [self.street]
        if self.street2:
            lines.append(self.street2)
        lines.append(f"{self.city}, {self.state} {self.zip_code}")
        return "-".join(lines)
    
class AddressBook():
    def __init__(self):
        self._employee_addresses = {
            1: Address("Corso Duca Degli Abruzzi", "Turin", "Italy", "10100", "101"),
            2: Address("Via Roma", "Turin", "Italy", "10100"),
            3: Address("Via Po", "Turin", "Italy", "10100"),
            4: Address("Via Garibaldi", "Turin", "Italy", "10100"),
            5: Address("Via Nizza", "Turin", "Italy", "10100")
        }

    def get_employee_address(self, employee_id):
        address = self._employee_addresses.get(employee_id)
        if not address:
            return ValueError(employee_id)
        return address