from typing import Union


DELIMITER = "\r\n"

class RespParser:

    def encodeString(self, data: str) -> str:
        """Encode 'data' into a Redis RESP string"""
        result = ['+', data, DELIMITER]
        return "".join(result)
    
    def encodeError(self, data: str) -> str:
        """Encode 'data' into a Redis RESP error"""
        result = ['-', data, DELIMITER]
        return "".join(result)

    def decode(self, data: str) -> str:
        """Returns a decoded RESP command or 'Invalid' if command is invalid"""
        processed, index = 0, data.find(DELIMITER)
        if index == -1:
            index = len(data)
        term = data[processed]
        try:
            if term == "*":
                return self._parse_resp_arrays(data)
            elif term == "$":
                return self._parse_bulk_strings(data)
            elif term == "+":
                return self._parse_simple_string(data)
            elif term == "-":
                return self._parse_error(data)
            elif term == ":":
                return self._parse_integer(data)
        except:
            return 'Invalid'


    def _parse_stream(self, data: str) -> list:
        cursor = 0
        data_len = len(data)
        result = []
        while cursor < data_len:
            pdata = data[cursor:]
            index = pdata.find(DELIMITER)
            count = int(pdata[1:index])

            cmd = ''
            start = index + len(DELIMITER)
            for _ in range(count):
                chunk, length = self._parse_bulk_strings(pdata, start)
                start = length + len(DELIMITER)
                cmd += " " + chunk
            cursor += start
            result.append(cmd.strip())
        return result


    def _parse_resp_arrays(self, data: str) -> list:
        """Returns a RESP parsed array"""
        index = data.find(DELIMITER)
        count = int(data[1:index])
        result = []
        start = index + len(DELIMITER)
        for _ in range(count):
            chunk, length = self._parse_bulk_strings(data, start)
            start = length + len(DELIMITER)
            result.append(chunk)
        return result


    def _parse_bulk_strings(self, data: str, start: int = 0) -> Union[list, None]:
        """Returns a RESP parsed bulk string"""
        index = data.find(DELIMITER, start)
        if index == -1:
            index = start
        length = int(data[start + 1:index])
        if length == -1:
            if index + len(DELIMITER) == len(data):
                return None
            else:
                return None, index
        else:
            result = data[index + len(DELIMITER):index + len(DELIMITER) + length]
            return result if start == 0 else [result, index + len(DELIMITER) + length]


    def _parse_simple_string(self, data: str) -> list:
        """Returns a RESP parsed simple string"""
        return [True, data[1:]]


    def _parse_error(self, data: str) -> list:
        """Returns a RESP parsed error"""
        return [False, data[1:]]


    def _parse_integer(self, data: str) -> list[int]:
        """Returns a RESP parsed integer"""
        return [int(data[1:])]