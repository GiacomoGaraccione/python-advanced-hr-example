import csv

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
    def __init__(self, addresses_file="addresses.csv"):
        self._employee_addresses = self._load_addresses(addresses_file)

    def _load_addresses(self, addresses_file):
        addresses = {}
        with open(addresses_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                addresses[int(row["id"])] = Address(
                    row["street"], row["city"], row["state"], row["zip_code"], row.get("street2", "")
                )
        return addresses

    def get_employee_address(self, employee_id):
        address = self._employee_addresses.get(employee_id)
        if not address:
            return ValueError(employee_id)
        return address
    
    def add_address(self, employee_id, street, city, state, zip_code, street2=""):
        new_address = {
            "id": employee_id,
            "street": street,
            "street2": street2,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }
        with open('addresses.csv', mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "street", "street2", "city", "state", "zip_code"])
            writer.writerow(new_address)
        print(f"Address for Employee {employee_id} added successfully.")

    def update_address(self, employee_id, street=None, city=None, state=None, zip_code=None, street2=None):
        updated = False
        addresses = []

        with open('addresses.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["id"]) == employee_id:
                    if street:
                        row["street"] = street
                    if city:
                        row["city"] = city
                    if state:
                        row["state"] = state
                    if zip_code:
                        row["zip_code"] = zip_code
                    if street2:
                        row["street2"] = street2
                    updated = True
                addresses.append(row)

        if updated:
            with open('addresses.csv', mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["id", "street", "street2", "city", "state", "zip_code"])
                writer.writeheader()
                writer.writerows(addresses)
            print(f"Address for Employee {employee_id} updated successfully.")
        else:
            print(f"Address for Employee {employee_id} not found.")

    def delete_address(self, employee_id):
        deleted = False
        addresses = []

        with open('addresses.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["id"]) != employee_id:
                    addresses.append(row)
                else:
                    deleted = True

        if deleted:
            with open('addresses.csv', mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["id", "street", "street2", "city", "state", "zip_code"])
                writer.writeheader()
                writer.writerows(addresses)
            print(f"Address for Employee {employee_id} deleted successfully.")
        else:
            print(f"Address for Employee {employee_id} not found.")