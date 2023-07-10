from enum import Enum
from abc import abstractclassmethod
from typing import List, Tuple
from MyError import ASN1DerProcessCode, ASN1DerProcessError
from StringConvert import StringConvert


class DerIBase:
    """ 遵循TLV格式的ASN1.Der编码规则 """

    def __init__(self, value: str) -> None:
        """ 初始化的value值需为十六进制 """
        # 定义实例属性
        self.tag: str # Tag字段，代表类型
        self.length: str # Length字段，代表长度，十六进制
        self.value: str # Value字段，代表实际值，十六进制
        # 启动主线程
        self.main(value)

    def main(self, value: str) -> None:
        """ 主线程 """
        # 输入值编码检测及赋值
        self._process_string_type(value)
        self._value: str = value
        # 处理Tag字段
        self.tag = self._value[:2]
        # 处理Length字段及Value字段长度检测
        value_len: int = self._calculation_length() # Value字段占用的字节数
        self._process_value(value_len)

    def _calculation_length(self) -> int:
        """ 计算长度 """
        #TODO 这个方法要拆出来，或者重新做一个给到DerObjects的split_sequence
        first: str = self._value[2:4] # Length字段的第一个字节
        flag: bool = True if StringConvert.hex_convert_bin(first)[0] == "0" else False # 判断第一个字段的位7是否为0
        if flag:
            value_len: int = StringConvert.hex_convert_int(first)
            self.length = first # 赋值Length字段
        else:
            num_len: int = StringConvert.bin_convert_int("0" + StringConvert.hex_convert_bin(first)[1:]) # 计算得到Length字段占用字节长度
            value_len: int = StringConvert.hex_convert_int(self._value[4: 4+num_len*2])
            self.length = self._value[2: 4+num_len*2] # 赋值Length字段
        # 返回Value字段实际长度
        return value_len
    
    def _process_value(self, value_len: int) -> None:
        """ 处理Value字段 """
        if len(self._value[2+len(self.length):]) != 2*value_len:
            raise ASN1DerProcessError(ASN1DerProcessCode.ValueTypeError) # 抛出类型异常
        # 处理Value字段
        self.value = self._value[2+len(self.length):]

    def _process_string_type(self, value: str):
        """ 输入值编码检测 """
        if StringConvert.is_base64(value) or not StringConvert.is_hex(value):
            raise ASN1DerProcessError(ASN1DerProcessCode.StringTypeError) # 抛出编码异常

    def _is_tag(self, tag: str) -> None:
        """ Tag字段检测 """
        if self.tag != tag:
            raise ASN1DerProcessError(ASN1DerProcessCode.ValueTypeError) # 抛出类型异常

class Sequence(DerIBase):
    """ Sequence-序列类型 """

    def __init__(self, value: str) -> None:
        super().__init__(value)
        # Sequence类型Tag为30
        self._is_tag(ASN1DerObjectTagsEnum.Sequence.value)

class Oid(DerIBase):
    """ OID-对象标识符类型 """

    def __init__(self, value: str) -> None:
        super().__init__(value)
        # OID类型Tag为06
        self._is_tag(ASN1DerObjectTagsEnum.Oid.value)

class BitString(DerIBase):
    """ BIT STRING类型 """

    def __init__(self, value: str) -> None:
        super().__init__(value)
        # BIT STRING类型Tag为03
        self._is_tag(ASN1DerObjectTagsEnum.BitString.value)
        # 处理Value字段的前导字节
        self._process_bitstring_value()

    def _process_bitstring_value(self) -> None:
        """ 处理Value字段的前导字节 """
        unused_num: int = StringConvert.hex_convert_int(self.value[:2])
        bin_value: str = StringConvert.hex_convert_bin(self.value[2:])
        self.value =  StringConvert.bin_convert_hex(bin_value[:len(bin_value)-unused_num] + unused_num * "0")


class ASN1DerObjectsEnum(Enum):
    """ ASN1Der对象类型枚举 """
    Sequence: Sequence = Sequence # Sequence-序列类型
    Oid: Oid = Oid # OID-对象标识符类型
    BitString: BitString = BitString # BIT STRING类型

class ASN1DerObjectTagsEnum(Enum):
    """ ASN1Der对象类型-Tag枚举 """
    Sequence: str = "30" # Sequence-序列类型
    Oid: str = "06" # OID-对象标识符类型
    BitString: str = "03" # BIT STRING类型

class ASN1DerObjectFactory:
    """ 创建ASN1.Der对象-工厂 """

    @staticmethod
    def create_der_object(value: str) -> DerIBase:
        """ 创建对应的对象类型 """
        tag: str = value[:2]
        object_name: str = ASN1DerObjectTagsEnum(tag).name
        return ASN1DerObjectsEnum[object_name].value(value)

class DerObjects:
    """ 拆分整值内的多个Der对象 """

    def __init__(self, value: str) -> None:
        # 声明类属性
        self.der_objects_list: List[DerIBase] = []
        # 赋值类属性
        self.der_objects_list = self._process_values(value)

    def _process_values(self, value: str) -> List[DerIBase]:
        data_list: List[str] = [value]
        result_list: List[DerIBase] = []
        # 开始处理
        while len(data_list) > 0:
            sub = data_list.pop()
            sub_object: DerIBase = ASN1DerObjectFactory.create_der_object(sub)
            if sub_object.tag == ASN1DerObjectTagsEnum.Sequence.value:
                data_list += self._split_sequence(sub_object.value)
            else:
                result_list.append(sub)
        return [ASN1DerObjectFactory.create_der_object(i) for i in result_list]

    def _split_sequence(self, value: str) -> List[str]:
        """ 拆分ASN1.Der.Sequence序列类型 """
        result_list: List[str] = []
        index: int = 0
        while True:
            sub_length_len, sub_value_len = self._calculation_length(value[index:])
            sub_len: int = sub_length_len*2+sub_value_len*2+2 # 整个子序列类型占的位数（字节数*2）
            result_list.append(
                value[index:index+sub_len]
            )
            index += sub_len
            if index >= len(value): break
        return result_list
    
    def _calculation_length(self, value: str) -> Tuple[int, int]:
        """ 计算长度-返回字节数 """
        length_len: int # 计算结果
        first: str = value[2:4] # Length字段的第一个字节
        flag: bool = True if StringConvert.hex_convert_bin(first)[0] == "0" else False # 判断第一个字段的位7是否为0
        if flag:
            value_len: int = StringConvert.hex_convert_int(first)
            length_len = 1
        else:
            num_len: int = StringConvert.bin_convert_int("0" + StringConvert.hex_convert_bin(first)[1:]) # 计算得到Length字段占用字节长度
            value_len: int = StringConvert.hex_convert_int(value[4: 4+num_len*2])
            length_len = 1 + num_len
        # 返回Value字段实际长度
        return length_len, value_len