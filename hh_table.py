import json
from typing import List


class HHTable:
    def __init__(self, name: str) -> None:
        with open(f"tables/{name}.json") as f:
            input_json = json.load(f)

            self.conversion_table = {}
            for symbol_data in input_json["ConversionTable"]:
                # WHYYYYYYYY
                hex_string = symbol_data.get("hexstring")
                if not hex_string:
                    hex_string = symbol_data["hexString"]

                # hedgeturd why hex string... why not integer
                # you can easily convert it to hex in c# :skull:
                id = int.from_bytes(bytes.fromhex(hex_string), "big")
                symbol = symbol_data["letter"]

                if symbol == "newline": symbol = "\n"
                elif symbol == "quote": symbol = '"'

                self.conversion_table[id] = symbol
    
    def get_symbol_by_id(self, id: int) -> str:
        if id not in self.conversion_table.keys():
            return "?"
        
        return self.conversion_table[id]
    
    def convert_symbols_to_string(self, symbols: List[int]) -> str:
        result = ""

        for id in symbols:
            result += self.get_symbol_by_id(id)
        
        return result
