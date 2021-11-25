DELIMITER = "\r\n"

class RespParser:

    def encode(self, *args):
        "Pack a series of arguments into a value Redis command"
        result = []
        result.append("*")
        result.append(str(len(args)))
        result.append(DELIMITER)
        for arg in args:
            result.append("$")
            result.append(str(len(arg)))
            result.append(DELIMITER)
            result.append(arg)
            result.append(DELIMITER)
        return "".join(result)


    def decode(self, data):
        processed, index = 0, data.find(DELIMITER)
        if index == -1:
            index = len(data)
        term = data[processed]
        try:
            if term == "*":
                return self._parse_multi_chunked(data)
            elif term == "$":
                return self._parse_chunked(data)
            elif term == "+":
                return self._parse_status(data)
            elif term == "-":
                return self._parse_error(data)
            elif term == ":":
                return self._parse_integer(data)
        except:
            return 'Invalid'


    def _parse_stream(self, data):
        cursor = 0
        data_len = len(data)
        result = []
        while cursor < data_len:
            pdata = data[cursor:]
            index = pdata.find(DELIMITER)
            count = int(pdata[1:index])

            cmd = ''
            start = index + len(DELIMITER)
            for i in range(count):
                chunk, length = self._parse_chunked(pdata, start)
                start = length + len(DELIMITER)
                cmd += " " + chunk
            cursor += start
            result.append(cmd.strip())
        return result


    def _parse_multi_chunked(self, data):
        index = data.find(DELIMITER)
        count = int(data[1:index])
        result = []
        start = index + len(DELIMITER)
        for i in range(count):
            chunk, length = self._parse_chunked(data, start)
            start = length + len(DELIMITER)
            result.append(chunk)
        return result


    def _parse_chunked(self, data, start=0):
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


    def _parse_status(self, data):
        return [True, data[1:]]


    def _parse_error(self, data):
        return [False, data[1:]]


    def _parse_integer(self, data):
        return [int(data[1:])]