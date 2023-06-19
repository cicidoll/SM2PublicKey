import base64, re

class StringConvert:
    """ 字符串格式转换方法 """

    @staticmethod
    def base64_convert_hex(input_base64: str) -> str:
        """ 将base64转换为hex字符串-输出小写 """
        return str(base64.b64decode(input_base64).hex())
    
    @staticmethod
    def hex_convert_base64(input_hex: str) -> str:
        """ 将hex转换为base64字符串 """
        return str(base64.b64encode(bytes.fromhex(input_hex)))[2:-1]
    
    @staticmethod
    def is_base64(input_str: str) -> bool:
        """ 检测字符串是否为Base64编码 """
        base64_code = "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$"
        return not StringConvert.is_hex(input_str) and bool(re.match(base64_code, input_str))
    
    @staticmethod
    def is_hex(input_str: str) -> bool:
        """ 检测字符串是否为Hex编码 """
        hex_code = "\A[0-9a-fA-F]+\Z"
        return bool(re.match(hex_code, input_str))