from enum import Enum

""" 公钥类型处理异常定义 Start """

class PubkeyProcessCode(Enum):
    """ 错误码枚举类型 """
    Success: int = 0 # 成功
    StringTypeError: int = 20001 # 字符串编码类型报错
    PubkeyTypeError: int = 30001 # 公钥类型报错
    ErrorCode: int = 10001 # 通用报错

class PubkeyErrorTypeMatch:

    @classmethod
    def pubkey_process_msg_match(cls, type: Enum) -> str:
        # -1标识无输入, 0为Base64编码, 1为Hex编码
        match type:
            case PubkeyProcessCode.Success:
                return "处理成功: Process Success"
            case PubkeyProcessCode.StringTypeError:
                return "输入公钥编码类型错误: String Type Error"
            case PubkeyProcessCode.PubkeyTypeError:
                return "输入公钥格式错误: Pubkey Type Error"
            case _:
                return "处理异常: Process Failed"

class PubkeyProcessError(Exception):

    def __init__(self, error_type: Enum) -> None:
        super().__init__(self)
        self.error_info = PubkeyErrorTypeMatch.pubkey_process_msg_match(error_type)

    def __str__(self) -> str:
        return self.error_info
    
""" 公钥类型处理异常定义 End """


""" ASN1.Der编码类型处理异常定义 Start """

class ASN1DerProcessCode(Enum):
    """ 错误码枚举类型 """
    Success: int = 0 # 成功
    StringTypeError: int = 20001 # 字符串编码类型报错
    ValueTypeError: int = 30001 # 类型报错
    ErrorCode: int = 10001 # 通用报错

class ASN1DerErrorTypeMatch:

    @classmethod
    def asn1der_process_msg_match(cls, type: Enum) -> str:
        match type:
            case ASN1DerProcessCode.Success:
                return "处理成功: Process Success"
            case ASN1DerProcessCode.StringTypeError:
                return "输入编码类型错误: String Type Error"
            case ASN1DerProcessCode.ValueTypeError:
                return "输入类型错误: Value Type Error"
            case _:
                return "处理异常: Process Failed"

class ASN1DerProcessError(Exception):

    def __init__(self, error_type: Enum) -> None:
        super().__init__(self)
        self.error_info = ASN1DerErrorTypeMatch.asn1der_process_msg_match(error_type)

    def __str__(self) -> str:
        return self.error_info
    
""" ASN1.Der编码类型处理异常定义 End """